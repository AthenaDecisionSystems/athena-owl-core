"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from typing import Annotated, Any

from typing_extensions import TypedDict

from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.pregel.types import StateSnapshot

from athena.llm.assistants.assistant_mgr import OwlAssistant

    
"""
The simples assistant use one LLM
"""


class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # appends messages to the list of messages
    messages: Annotated[list, add_messages]





class BaseAssistant(OwlAssistant):
    
    def __init__(self, agent):
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.llm = agent.get_runnable()
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", self.call_chatbot)
        graph_builder.set_entry_point("chatbot")
        graph_builder.set_finish_point("chatbot")
        self.graph = graph_builder.compile(checkpointer=self.memory)
        
        
        
    def call_chatbot(self, state: State):
        return {"messages": [self.llm.invoke(state["messages"])]}
    
    
    def invoke(self, query: str, thread_id: str) -> dict[str, Any] | Any:
        self.config = {"configurable": {"thread_id": thread_id}}
        resp= self.graph.invoke({"messages": ("user", query)}, self.config)
        return resp
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)