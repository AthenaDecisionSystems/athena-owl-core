"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

"""
Conversation manager manages a conversation for a user to an agent.
It persists state of the conversation (not yet implemented)
"""
from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.llm.assistants.assistant_mgr import OwlAssistant, AssistantManager, get_assistant_manager
import logging
import uuid

LOGGER = logging.getLogger(__name__)

_ACTIVE_CONV: dict[str, OwlAssistant] = dict()

def get_or_start_conversation(cc: ConversationControl) -> ResponseControl | None:
    """
    Start a conversation or continue an existing one. 
    """
    assistant: OwlAssistant
    if cc.thread_id is None or cc.thread_id == "":
        cc.thread_id = str(uuid.uuid4())
    if not _ACTIVE_CONV or cc.thread_id not in _ACTIVE_CONV or  _ACTIVE_CONV[cc.thread_id] is None:
        assistant_mgr = get_assistant_manager()
        assistant = assistant_mgr.build_assistant(cc.assistant_id, cc.locale)
        _ACTIVE_CONV[cc.thread_id] = assistant
    else:
        assistant = _ACTIVE_CONV[cc.thread_id]
    LOGGER.debug(f"\n@@@> get_or_start_conversation() {assistant}")
    if assistant:
        resp = assistant.send_conversation(cc)
        return resp
    else:
        raise Exception(f"no assistant found with id {cc.assistant_id}")