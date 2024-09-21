"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
import logging
import json
from athena.llm.agents.agent_mgr import OwlAgentDefaultRunner, OwlAgent
from athena.llm.tools.tool_mgr import OwlToolEntity
from typing import Annotated, Any, Optional, Literal
from typing_extensions import TypedDict

from langchain_core.prompts import BasePromptTemplate
from langchain_core.messages import AnyMessage, ToolMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.pregel.types import StateSnapshot


LOGGER = logging.getLogger(__name__)

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    input: Optional[HumanMessage]

class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage.
    return the new state for the graph
    """
    def __init__(self, tools: list) -> None:
        # build a dict tool name: tool
        self.tools_by_name = {tool.name: tool for tool in tools}

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []
        for tool_call in message.tool_calls:
            tool_result = self.tools_by_name[tool_call["name"]].invoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        print(outputs)
        return {"messages": outputs}
    
class BaseToolGraphAgent(OwlAgentDefaultRunner):

    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        self.agent_id = agentEntity.agent_id
        self.llm=super().instantiate_llm(agentEntity, prompt,tool_instances)
        tool_node=BasicToolNode(tool_instances)
        graph_builder = StateGraph(AgentState)
        graph_builder.add_node("llm", self.call_llm)
        graph_builder.add_node("tools", tool_node)
        graph_builder.add_conditional_edges(
            "llm",
            self.route_tools,
            {"tools": "tools", END: END}
        )
        graph_builder.add_edge("tools", "llm")
        graph_builder.set_entry_point("llm")
        self.graph = graph_builder.compile(checkpointer=MemorySaver())

    def call_llm(self, state: AgentState):
        """return the new state for the graph"""
        messages = state['messages']
        msg = state["input"]
        LOGGER.debug(f"@@@ > call_chatbot in Base Graph Assistant: {messages}")
        message = self.llm.invoke({"messages": messages})
        return {'messages': [message], 'input': msg}
    

    def invoke(self, request, thread_id: str) -> dict[str, Any] | Any:
        self.config = {"configurable": {"thread_id": thread_id}}
        m=HumanMessage(content=request["input"])
        msg=request["chat_history"]
        msg.append(m)
        print(f"messages: {msg}, input: {m}")
        resp= self.graph.invoke({"messages": msg, "input": [m]}, self.config)
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