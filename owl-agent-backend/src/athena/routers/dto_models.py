"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
from typing import List, Optional
    
class ChatMessage(BaseModel):
    content: str
    role: str



# a closed answer is received from the client-side UI app that interacts with the server-side assistant
class ClosedAnswer(BaseModel):
    """
    Definition of an answer to a closed question
    Answers to closed questions are used to enrich the objects kept as named parameters in the LangGraph AgentState
    """
    key_name: str = ""
    input: str = ""

"""
# this is a sample yaml describing an answer to a closed question

power_of_the_vehicle_engine:
  - key_name: "the vehicle.engine.power"      # used to reinject a value in the agent state
  - input: "120.0"                            # the value to be reinjected


[
  {
    "key_name": "the vehicle.engine.power",
    "input": "120.0"
  },
  {
    "key_name": "the vehicle.registration_date",
    "input": "2021-10-26"
  }
]  
"""

class ClosedQuestionControl(BaseModel):
    locale: Optional[str] = "en"
    closed_answers: List[ClosedAnswer]
    reset: bool = False  # to reset everything back to default config.
    callWithVectorStore: Optional[bool] = False
    user_id: Optional[str] = ""
    agent_id: Optional[str] = ""
    thread_id: Optional[str] = ""
    chat_history:   List[ChatMessage] = []

    
class ConversationControl(BaseModel):
    locale: Optional[str] = "en"
    query: str = ""
    reset: bool = False  # to reset everything back to default config.
    callWithVectorStore: Optional[bool] = False
    user_id: Optional[str] = ""
    agent_id: Optional[str] = ""
    thread_id: Optional[str] = ""
    chat_history:   List[ChatMessage] = []


class ResponseChoice(BaseModel):
    choice: str = ""

class ResponseControl(BaseModel):
    message: Optional[str] = ''
    status: int = 200
    type: str = "OpenQuestion"
    question: Optional[str] = ''
    question_type: Optional[str] = ''
    possibleResponse: Optional[List[ResponseChoice]] = None
    error: Optional[str] = ''
    chat_history: List[ChatMessage] = []
    user_id: Optional[str] = ""
    agent_id: Optional[str] = ""
    thread_id: Optional[str] = ""


