"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import os,sys
from typing import Any, Generator

from  athena.routers.dto_models import ConversationControl, ResponseControl, ModelParameters


class AgentInterface:


    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        """
        Send the current chat conversation with history and query to a backend LLM, as the conversation control may have settings for RAG and decision services
        then the others functions of this class may be called. This method needs to be overridden for each different LLM
        """
        pass

    async def conversation_stream(self,conversationControl:ConversationControl) -> Generator[str, Any, Any] | Any:
        pass
    

    
