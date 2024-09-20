"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

"""
Conversation manager manages a conversation between users and agent.
When the conversation start, one of the attribute is the unique agent id.
This manager may instantiate an agent if not already created.
It persists state of the conversation (not yet implemented)
"""
from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgentDefaultRunner
import logging
import uuid

LOGGER = logging.getLogger(__name__)

# manage a list of active conversations
_ACTIVE_CONV: dict[str, OwlAgentDefaultRunner] = dict()

def _get_new_owl_agent(agent_id, locale):
    agent_mgr = get_agent_manager()
    return agent_mgr.build_agent_runner(agent_id, locale)

    
def get_or_start_conversation(cc: ConversationControl) -> ResponseControl | None:
    """
    Start a conversation or continue an existing one based on the thread id.  
    """
    owl_agent: OwlAgentDefaultRunner = None
    if cc.thread_id is None or cc.thread_id == "":
        cc.thread_id = str(uuid.uuid4())
    if not _ACTIVE_CONV or cc.thread_id not in _ACTIVE_CONV or  _ACTIVE_CONV[cc.thread_id] is None:
        # new conversation so let create an agent
        owl_agent = _get_new_owl_agent(cc.agent_id, cc.locale)
        _ACTIVE_CONV[cc.thread_id]= owl_agent
    else:
        owl_agent = _ACTIVE_CONV[cc.thread_id]
        if owl_agent.agent_id != cc.agent_id:
            # user may have changed the configuration; so create a new agent
            owl_agent = _get_new_owl_agent(cc.agent_id, cc.locale)
            _ACTIVE_CONV[cc.thread_id]=owl_agent
        
    LOGGER.debug(f"\n@@@> get_or_start_conversation() {owl_agent}")
    if owl_agent:
        resp = owl_agent.send_conversation(cc)
        # TO DO add persistence to document oriented DB, key= thread_id and payload is cc + resp
        return resp
    else:
        raise Exception(f"no agent found with id {cc.agent_id}")