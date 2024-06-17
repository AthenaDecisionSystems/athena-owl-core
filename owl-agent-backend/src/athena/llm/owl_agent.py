"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import os,sys
from typing import Any, Generator

from  athena.routers.dto_models import ConversationControl, ResponseControl, ModelParameters
from langgraph.pregel.types import StateSnapshot

class AgentInterface:
    def send_query(self,controller: ConversationControl) -> ResponseControl | Any:
        """
        Send the given query to a backend LLM, as the conversation control may have settings for RAG and decision services
        then the others functions of this class may be called. This method needs to be overridden for each different LLM
        """
        pass

    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        """
        Send the current chat conversation with history and query to a backend LLM, as the conversation control may have settings for RAG and decision services
        then the others functions of this class may be called. This method needs to be overridden for each different LLM
        """
        pass

    async def conversation_stream(self,conversationControl:ConversationControl) -> Generator[str, Any, Any] | Any:
        pass
    
    def get_model(self, stream, parameters: ModelParameters, callbacks):
        return None  
    
    def get_agent(self, model, prompt, tools ) -> StateSnapshot:
        pass
