"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain.agents import create_tool_calling_agent, AgentExecutor, tool, create_openai_tools_agent
from langchain.tools.retriever import create_retriever_tool
from importlib import import_module
from typing import Sequence
import logging
from athena.app_settings import get_config
from athena.routers.dto_models import ConversationControl
from athena.itg.store.content_mgr import get_content_mgr
from athena.itg.decisions.nba_ds_dummy import callDecisionService

"""
Tool manager manages the different tools to be used by the different Agents of the solution.
It has dependencies and knowledge on the domain of the solution.
Use decision service, content manager and different repositories
"""

# For each tool definition, the function signature is important as it will be what LLM will try
# to build for
LOGGER = logging.getLogger(__name__)


@tool
def get_client_by_id(id: int) -> dict:
    """get insurance client information given its unique client identifier id"""
    client = {"id" : id, "name": "Smith", "firstName": "Robert"}
    return client

@tool
def get_client_by_name(name: str) -> dict:
    """get client information given his or her name"""
    client = {"id" : 2, "name": name, "firstName": "Robert"}
    return client

@tool
def define_next_best_action_with_decision(client_id : int, intentionToLeave: bool ):
    """perform the next best action given the current state of the insurance claim knowing 
    its unique claim_id and the current client motivation.
    extract the  client motive and if he has the intention to leave
    """
    return callDecisionService( client_id, intentionToLeave, "en")




_tools = [get_client_by_id, get_client_by_name]

def get_tools_to_use(conversationControl:ConversationControl) -> Sequence[tool] :
    """
    Define the Tools to be used by the Agent. It is controlled by the input controller object to give
    more context
    """
    _tools = [get_client_by_id, get_client_by_name]
    if conversationControl.callWithDecisionService:
        _tools.append(define_next_best_action_with_decision)
    if conversationControl.callWithVectorStore:
        retriever = get_content_mgr().get_retriever()
        retriever_tool = create_retriever_tool(retriever, "insurance_specific",
                            "Search for information about insurance policy. For any questions about insurance, you must use this tool!")
        _tools.append(retriever_tool)
    LOGGER.debug(_tools)
    return _tools

def get_current_tools():
    return _tools