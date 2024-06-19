"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from athena.llm.owl_agent import AgentInterface
from athena.routers.dto_models import ConversationControl, ResponseControl
from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from athena.llm.prompts.prompt_mgr import get_prompt_manager
from athena.itg.tool_manager import get_tools_to_use
from athena.app_settings import get_config
import logging
import asyncio

LOGGER = logging.getLogger(__name__)
q = asyncio.Queue()
stop_item = "###finish###"


class BaseOwlAgent(AgentInterface):
    """
    Base Owl Agent to support chat bot conversation with history or Q&A and some basic tools or tool placeholders
    """
    max_history=5
    
    def __init__(self):
        self.max_history -= get_config().owl_agent_llm_history_length
        


    def build_agent_executor(self,controller:ConversationControl,stream = False, callbacks = None):
        prompt= self.assess_what_prompt_to_use(controller)
        tools = get_tools_to_use(controller)
        model = self.get_model(stream,controller.modelParameters, callbacks)
        model.bind_tools(tools)
        agent = self.get_agent(model, prompt, tools)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)

    def send_conversation(self,controller:ConversationControl) -> ResponseControl:
        LOGGER.debug(f"In send_conversation legacy {controller}")
        agent_executor =  self.build_agent_executor(controller,False)
        chat_history = controller.chat_history
        resp = ResponseControl()
        agentResponse=agent_executor.invoke({"input": controller.query, "chat_history":chat_history})
        LOGGER.debug(f"---> {agentResponse}")
        resp.chat_history=agentResponse["chat_history"]
        # should we build the history here?
        resp.message=agentResponse["output"]
        LOGGER.debug(resp)
        return resp
    

    async def conversation_stream(self,controller:ConversationControl):
        agent_executor =  self.build_agent_executor(controller,stream=True, callbacks=[StreamingStdOutCallbackHandlerYield()])
        await agent_executor.agenerate([{"input": controller.query, "chat_history": conversationControl.chat_history}])
        while True:
                item = await q.get()
                if item == stop_item:
                    break
                yield item
        pass
    
    def assess_what_prompt_to_use(self,controller:ConversationControl):
        """
        Looking at the query and the fact to use decision service or not and vector store, select the matching prompt
        """
        system_prompt = get_prompt_manager().get_prompt(controller.modelParameters.prompt_ref,controller.locale)
        # conversationControl.type does not seem necessary
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="context", optional=True),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ])

        return  prompt
    
    def build_chat_history_for_llm(self,controller:ConversationControl):
        ch = []
        for cr in controller.chat_history[self.max_history:]:
            if cr.role == "human" or cr.role == "user":
                ch.append(HumanMessage(content=cr.content))
            else:
                ch.append(AIMessage(content=cr.content))
        return ch