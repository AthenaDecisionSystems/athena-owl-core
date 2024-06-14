
from typing_extensions import TypedDict
from athena.llm.assistants.assistant_mgr import OwlAssistant
from typing import Annotated
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, SystemMessage, HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

class AgentState(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]
    
class BaseAssistant(OwlAssistant):
    
    def __init__(self):
        self.system= "a prompt"
        self.model = ChatOpenAI(model="gpt-3.5-turbo")
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.call_llm)
        graph.add_node("action", self.take_action)
        graph.add_conditional_edges(
            "llm",
            self.exists_action,
            {True: "action", False: END}
        )
        graph.add_edge("action", "llm")
        graph.set_entry_point("llm")
        self.graph = graph.compile()
    
    def call_llm(self, state: AgentState):
        messages = state['messages']
        print(messages)
        if self.system:
            messages = [SystemMessage(content=self.system)] + messages
        message = self.model.invoke(messages)
        return {'messages': [message]}
    
    def take_action(self, state: AgentState):
         pass
    
    def exists_action(self, state: AgentState):
        result = state['messages'][-1]
        return len(result.tool_calls) > 0
    
     
    def stream(self,query: str) -> str:
        return "response to query"
    
    def invoke(self, query: str) -> str:
        m=HumanMessage(content=query)
        result = self.graph.invoke({"messages": [m]})
        return result['messages'][-1].content
    