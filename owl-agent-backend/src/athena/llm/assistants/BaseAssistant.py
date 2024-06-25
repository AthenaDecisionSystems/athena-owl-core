from langchain_core.messages import AIMessage, HumanMessage
from athena.llm.assistants.assistant_mgr import OwlAssistant, OwlAssistantEntity
from athena.routers.dto_models import ConversationControl, ResponseControl
from typing import Any
import logging

LOGGER = logging.getLogger(__name__)

class BaseAssistant(OwlAssistant):
    """
    Assistant based on chaining with prompt, llm and potentially retriever.
    Assistants are created via the assistant manager factory method
    Agent may use tools or not.
    """
    
    def __init__(self, agent):
        self.llm = agent.get_runnable()
        
    def invoke(self, request):
        return self.llm.invoke(request) 
        
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        LOGGER.debug(f"\n@@@> query assistant {controller.query}")
        request = { "input": controller.query, "chat_history" : controller.chat_history }
        chain_rep= self.invoke(request)   # AIMessage
        resp = ResponseControl()
        resp.chat_history = controller.chat_history
        if isinstance(chain_rep,dict):
            if chain_rep.get("output"):
                resp.message= chain_rep.get("output")
                resp.chat_history.extend([
                        HumanMessage(content= controller.query),
                        AIMessage(content=chain_rep.get("output")),
                        ])
        else: # str
            resp.message=chain_rep
            resp.chat_history.extend([
                        HumanMessage(content= controller.query),
                        AIMessage(content=chain_rep),
                        ])
        resp.assistant_id=controller.assistant_id
        resp.thread_id=controller.thread_id
        resp.user_id = controller.user_id
        return resp