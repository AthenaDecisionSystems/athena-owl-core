"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import logging
from athena.llm.agents.agent_mgr import OwlAgentDefaultRunner, OwlAgent
from athena.llm.tools.tool_mgr import OwlToolEntity
from typing import Annotated, Any, Optional
from typing_extensions import TypedDict

from langchain_core.prompts import BasePromptTemplate
from langchain_core.runnables.config import RunnableConfig
from langchain_core.messages import AnyMessage

from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.pregel.types import StateSnapshot
from langgraph.graph import StateGraph

LOGGER = logging.getLogger(__name__)

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # appends messages to the list of messages
    input: str
    chat_history:  Annotated[list[AnyMessage], add_messages]

class BaseGraphAgent(OwlAgentDefaultRunner):

    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        #self.memory = SqliteSaver.from_conn_string(":memory:")
        self.agent_id = agentEntity.agent_id
        self.llm=super().instantiate_llm(agentEntity, prompt,tool_instances)
        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", self.call_chatbot)
        graph_builder.set_entry_point("chatbot")
        graph_builder.set_finish_point("chatbot")
        self.graph = graph_builder.compile()

        #self.graph = graph_builder.compile(checkpointer=self.memory)

    def call_chatbot(self, state: State):
        """return the new state for the graph"""
        messages = state['chat_history']
        msg = state["input"]
        LOGGER.debug(f"@@@ > call_chatbot in Base Graph Assistant: {messages}")
        message = self.llm.invoke({"input": msg, "chat_history" : messages})
        return {'chat_history': [message]}
    
    
    def invoke(self, request, thread_id: Optional[str]) -> dict[str, Any] | Any:
        self.config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        resp= self.graph.invoke(request, self.config)
        msg=resp["chat_history"][-1].content
        return msg
    
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)