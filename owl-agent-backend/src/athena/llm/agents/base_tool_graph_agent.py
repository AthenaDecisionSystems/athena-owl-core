"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import logging


from typing import Annotated, Any, Optional, Literal
from typing_extensions import TypedDict

from langchain_core.prompts import BasePromptTemplate
from langchain_core.messages import AnyMessage, ToolMessage, HumanMessage

from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.pregel.types import StateSnapshot
from langgraph.prebuilt import ToolNode, tools_condition

from athena.llm.agents.agent_mgr import OwlAgentDefaultRunner, OwlAgent
from athena.llm.tools.tool_mgr import OwlToolEntity

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(2)

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    input: str


class BaseToolGraphAgent(OwlAgentDefaultRunner):

    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        self.agent_id = agentEntity.agent_id
        #self.llm=super().instantiate_llm(agentEntity, prompt, tool_instances)
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
        model_with_tools = self.model.bind_tools(tool_instances)
        self.llm = prompt | model_with_tools
        tool_node=ToolNode(tool_instances)
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node("llm", self.call_llm)
        graph_builder.add_node("tools", tool_node)
        graph_builder.add_conditional_edges(
            "llm",
            tools_condition
        )
        graph_builder.add_edge("tools", "llm")
        graph_builder.set_entry_point("llm")
        self.graph = graph_builder.compile(checkpointer=MemorySaver())

    def call_llm(self, state: AgentState):
        """return the new state for the graph"""
        messages = state['messages']
        question = state.get("input")
        LOGGER.debug(f"@@@ > call_chatbot in Base Graph Assistant: {messages}")
        response = self.llm.invoke(messages)
        return {'messages': [response]}
    

    def invoke(self, request, thread_id: str) -> dict[str, Any] | Any:
        self.config = {"configurable": {"thread_id": thread_id}}
        user_input=request["input"][0]
        msg=request["chat_history"]
        msg.append(user_input)
        print(f"messages: {msg}, input: {user_input}")
        resp= self.graph.invoke({"messages": [("user", user_input)]}, self.config)
        return  resp["messages"][-1].content
         
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)
    
    
    def route_tools(self,
        state: AgentState,
    ) -> Literal["tools", "__END__"]:
        """Use in the conditional_edge to route to the ToolNode if the last message

        has tool calls. Otherwise, route to the end."""
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state to tool_edge: {state}")
        if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
            return "tools"
        return END