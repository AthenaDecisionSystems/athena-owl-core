"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from typing import Annotated, Any, Optional
import json
from typing_extensions import TypedDict
import logging
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.pregel.types import StateSnapshot
from langchain_core.messages import HumanMessage
from langchain_core.runnables.config import RunnableConfig
from athena.llm.assistants.assistant_mgr import OwlAssistant
from athena.routers.dto_models import ConversationControl, ResponseControl
    
"""
The simples assistant use one LLM
"""

LOGGER = logging.getLogger(__name__)

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # appends messages to the list of messages
    input: str

class BaseGraphAssistant(OwlAssistant):
    
    def __init__(self, agent):
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.llm = agent.get_runnable()
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", self.call_chatbot)
        graph_builder.set_entry_point("chatbot")
        graph_builder.set_finish_point("chatbot")
        self.graph = graph_builder.compile(checkpointer=self.memory)
        
        
        
    def call_chatbot(self, state: State):
        return {"input": [self.llm.invoke(state["input"])]}
    
    
    def invoke(self, request, thread_id: Optional[str]) -> dict[str, Any] | Any:
        self.config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        resp= self.graph.invoke(request, self.config)
        return resp
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)
    
    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        LOGGER.debug(f"\n@@@> query assistant {controller.query}")
        request = { "input": controller.query, "chat_history" : controller.chat_history }
        graph_rep= self.invoke(request, controller.thread_id)
        resp = ResponseControl()

        resp.message=graph_rep["messages"][-1].content
        resp.chat_history=[ m.json() for m in graph_rep["messages"]]
        resp.assistant_id=controller.assistant_id
        resp.thread_id=controller.thread_id
        resp.user_id = controller.user_id
        return resp