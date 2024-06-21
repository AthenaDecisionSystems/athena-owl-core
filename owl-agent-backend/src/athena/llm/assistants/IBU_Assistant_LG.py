"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from typing_extensions import TypedDict
from athena.app_settings import get_config
from athena.llm.assistants.assistant_mgr import OwlAssistant
from athena.routers.dto_models import ConversationControl, ResponseControl
from typing import Annotated, Literal, Any
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, HumanMessage, ToolMessage
from langchain_core.runnables.config import RunnableConfig
from langgraph.pregel.types import StateSnapshot
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
import json,logging
import langchain

LOGGER = logging.getLogger(__name__)

if get_config().logging_level == "DEBUG":
    langchain.debug=True
"""
An assistance to support CSM from IBU insurance for the claim processing process
"""

"""
A two node graph to integrate with tools and LLM
"""    
class BaseToolGraphAssistant(OwlAssistant):
    
    def __init__(self,agent):
        self.memory = SqliteSaver.from_conn_string(":memory:")
        self.model = agent.get_model()
        self.prompt = agent.get_prompt()
        self.graph = create_react_agent(self.model,tools=agent.get_tools(), messages_modifier=self.modify_messages)
        self.config: dict[str, dict[str, str | None]] = dict()
        
    def get_state(self) -> StateSnapshot:
        return self.graph.get_state(RunnableConfig(configurable=self.config))
    
    def modify_messages(self, messages: list):
        return self.prompt.invoke({"messages": messages})

    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        self.config = {"configurable": {"thread_id": controller.thread_id}}
        m=HumanMessage(content=controller.query)
        graph_rep= self.graph.invoke({"messages": [m]},  self.config)
        resp = ResponseControl()
        resp.message=graph_rep["messages"][-1].content
        resp.chat_history=[ m.json() for m in graph_rep["messages"]]
        resp.assistant_id=controller.assistant_id
        resp.thread_id=controller.thread_id
        resp.user_id = controller.user_id
        return resp
    