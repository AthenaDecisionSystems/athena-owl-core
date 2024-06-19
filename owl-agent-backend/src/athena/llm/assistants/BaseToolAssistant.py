"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from typing_extensions import TypedDict
from athena.llm.assistants.assistant_mgr import OwlAssistant
from typing import Annotated, Any, Literal
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langgraph.pregel.types import StateSnapshot
from langgraph.checkpoint.sqlite import SqliteSaver
from  athena.routers.dto_models import ConversationControl, ResponseControl
import json
import langchain

langchain.debug=True

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""
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
        return {"messages": outputs}
    
    
class BaseToolAssistant(OwlAssistant):
    """
    An assistant using an agent with tools and tool node to execute the tool call
    """
    
    def __init__(self, agent):
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.llm = agent.get_runnable()
        tool_node=BasicToolNode(agent.get_tools())
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
        self.graph = graph_builder.compile(checkpointer=self.memory)
        
    
    def call_llm(self, state: AgentState):
        messages = state['messages']
        print(messages)
        message = self.llm.invoke(messages)
        return {'messages': [message]}
    

    def invoke(self, query: str, thread_id: str) -> dict[str, Any] | Any:
        self.config = {"configurable": {"thread_id": thread_id}}
        m=HumanMessage(content=query)
        resp= self.graph.invoke({"messages":[m]}, self.config)
        return resp
    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        graph_rep= self.invoke(controller.query, controller.thread_id)
        resp = ResponseControl()
        resp.message=graph_rep["messages"][-1].content
        resp.chat_history=[ m.json() for m in graph_rep["messages"]]
        resp.assistant_id=controller.assistant_id
        resp.thread_id=controller.thread_id
        resp.user_id = controller.user_id
        return resp
         
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(self.config)
    
    
    def route_tools(self,
        state: AgentState,
    ) -> Literal["tools", END]:
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
    
    