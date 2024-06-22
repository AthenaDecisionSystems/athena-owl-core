
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.chat_models import ChatOllama
from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.tools import ToolsAgentOutputParser

from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity
from athena.llm.tools.tool_mgr import OwlToolEntity


from typing import Optional
from importlib import import_module


class OwlAgent(OwlAgentInterface):
    tools = None
    
    def __init__(self, agentEntity: OwlAgentEntity, system_prompt: str, tool_entities: Optional[list[OwlToolEntity]]):
        if "/" in system_prompt:
            self.prompt = hub.pull(system_prompt)
        else:
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
            ])
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
        if tool_entities:
            self.tools = self.build_tool_instances(tool_entities)
            llm_with_tools = self.model.bind_tools(self.tools)
            agent = (
                                {
                                    "input": lambda x: x["input"],
                                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                                        x["intermediate_steps"]
                                    ),
                                    "chat_history": lambda x: x["chat_history"],
                                }
                                | self.prompt
                                | llm_with_tools
                                | ToolsAgentOutputParser()
                            )
            #create_tool_calling_agent(self.model, self.tools, self.prompt)
            self.llm = AgentExecutor(agent= agent, tools=self.tools, verbose=True)
            
        else:
            self.llm = {"input": lambda x: x["input"], "chat_history" : lambda x: x["chat_history"]}  | self.prompt | self.model | StrOutputParser()
            
    def _instantiate_model(self,modelName, modelClass, temperature):
        module_path, class_name = modelClass.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        return klass(model=modelName, temperature= temperature/100)
       
    def get_runnable(self):
        #return   self.prompt |  self.model.bind(self.tools) | StrOutputParser()
        return  self.llm
    

    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]):
        tool_list=[]
        for tool_entity in tool_entities:
            # TO DO rethink about this approach
            if tool_entity.tool_id == "tavily":
                tool_list.append(TavilySearchResults(max_results=2))
            else:
                raise Exception("Not yet implemented")
        return tool_list