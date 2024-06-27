"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
from typing import List, Optional, Union
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
    
class ChatMessage(BaseModel):
    content: str
    role: str
    
class ModelParameters(BaseModel):
    modelName: str = "gpt-3.5-turbo-0125"
    modelClass: str = "agent_openai"
    prompt_ref:  str = "default_prompt"
    temperature: int = 0  # between 0 to 100 and will be converted depending of te LLM
    top_k: int = 1
    top_p: int = 1
    
    
class ConversationControl(BaseModel):
    #callWithVectorStore: bool = False
    #callWithDecisionService: bool = False
    locale: Optional[str] = "en"
    query: str = ""
    #type: str = "chat"
    reset: bool = False  # to reset everything back to default config.
    #modelParameters: Optional[ModelParameters] = None
    user_id: Optional[str] = ""
    assistant_id: Optional[str] = ""
    thread_id: Optional[str] = ""
    chat_history:   List[ChatMessage] = []


class ResponseChoice(BaseModel):
    choice: str = ""

class ResponseControl(BaseModel):
    message: Optional[str] = ''
    status: int = 200
    type: str ="OpenQuestion"
    question: Optional[str] = ''
    question_type: Optional[str] = ''
    possibleResponse: Optional[List[ResponseChoice]] = None
    error: Optional[str] = ''
    chat_history: List[ChatMessage] = []
    user_id: Optional[str] = ""
    assistant_id: Optional[str] = ""
    thread_id: Optional[str] = ""


