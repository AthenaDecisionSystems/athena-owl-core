import logging
from athena.llm.agents.agent_mgr import OwlAgentAbstractRunner, OwlAgent
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


class BaseToolGraphAgent(OwlAgentAbstractRunner):