"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
from typing import List, Optional, Union
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
    

class ModelParameters(BaseModel):
    modelName: str = ""
    modelClass: str = "agent_openai"
    temperature: int = 0  # between 0 to 100 and will be converted depending of te LLM
    top_k: int = 1
    top_p: int = 1
    
    
class ConversationControl(BaseModel):
    callWithVectorStore: bool = False
    callWithDecisionService: bool = False
    locale: str = "en"
    query: str = ""
    type: str = "chat"
    reset: bool = False
    prompt_ref:  str = "openai_insurance_with_tool"
    modelParameters: Optional[ModelParameters] = None
    chat_history: List[Union[HumanMessage, AIMessage]] = []


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
    chat_history: List[Union[HumanMessage, AIMessage]] = []


