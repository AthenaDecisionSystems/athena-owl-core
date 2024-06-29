"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
from typing import List, Optional
    
class ChatMessage(BaseModel):
    content: str
    role: str

    
class ConversationControl(BaseModel):
    locale: Optional[str] = "en"
    query: str = ""
    reset: bool = False  # to reset everything back to default config.
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


