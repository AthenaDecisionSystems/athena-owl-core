from langchain_core.messages import AIMessage, HumanMessage
from athena.llm.assistants.assistant_mgr import OwlAssistant, OwlAssistantEntity
from athena.routers.dto_models import ConversationControl, ResponseControl, ChatMessage
from typing import Any, Optional
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
        
    def invoke(self, request, thread_id: Optional[str]) -> dict[str, Any] | Any:
        return self.llm.invoke(request) 
        