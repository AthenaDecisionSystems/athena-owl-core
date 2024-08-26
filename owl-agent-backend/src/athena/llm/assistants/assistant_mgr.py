"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer

The assistant manager supports CRUD operations for the OwlAssistantEntity and a factory
to create instance of an assistant top support conversation.
There is only one manager per deployed Owl Framework backend.
"""
from pydantic import BaseModel
import uuid, yaml, logging
from functools import lru_cache
from athena.app_settings import get_config
from importlib import import_module
from athena.llm.agents.agent_mgr import get_agent_manager
from athena.routers.dto_models import ConversationControl, ResponseControl, ChatMessage
from langchain_core.messages import AIMessage, HumanMessage
from typing import Any, Optional

LOGGER = logging.getLogger(__name__)

    

class OwlAssistant(object):
    """
    Base class to represent an instance of an assistant. So it defines a contract to support conversations.
    """
    agents: []
    assistant_id: str
    
    def __init__(self, assistantID, loaded_agents):
        self.assistant_id = assistantID
        self.agents = loaded_agents
        
    def stream(self, query: str, thread_id: str):
        # TO BE DONE
        pass
    
    def transform_chat_history(self, chat_history: list[ChatMessage]):
        l=[]
        for m in chat_history:
            if m.role == "human":
                l.append(HumanMessage(content=m.content))
            else:
                l.append(AIMessage(content=m.content))
        return l
    
    def _build_response(self, controller: ConversationControl):
        resp = ResponseControl()
        resp.chat_history = controller.chat_history
        resp.assistant_id = controller.assistant_id
        resp.thread_id = controller.thread_id
        resp.user_id = controller.user_id
        return resp
    
    def invoke(self, request, thread_id: Optional[str], **kwargs) -> dict[str, Any] | Any:
        return {}
        
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        LOGGER.debug(f"\n@@@> query assistant {controller.query}")
        lg_chat_history = self.transform_chat_history(controller.chat_history)
        request = { "input": controller.query, "chat_history" : lg_chat_history }
        agent_resp= self.invoke(request, controller.thread_id)   # AIMessage
        resp = self._build_response(controller)
        if isinstance(agent_resp,dict):
            if agent_resp.get("output"):
                resp.message= agent_resp.get("output")
                resp.chat_history.extend([
                        ChatMessage(role="human", content= controller.query),
                        ChatMessage(role="AI", content=str(agent_resp.get("output"))),
                        ])
        else: # str
            resp.message=agent_resp
            resp.chat_history.extend([
                        ChatMessage(role="human", content= controller.query),
                        ChatMessage(role="AI", content=agent_resp)
                        ])
        return resp
            
    
    



