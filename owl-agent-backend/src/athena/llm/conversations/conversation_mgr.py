"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

"""
Conversation manager manages a conversation for a user to an agent_
"""
from athena.routers.dto_models import ConversationControl, ResponseControl
from athena.llm.assistants.assistant_mgr import AssistantManager, get_assistant_manager
import uuid
_ACTIVE_CONV: dict = dict()

def get_or_start_conversation(cc: ConversationControl) -> ResponseControl | None:
    """
    Start a conversation or continue an existing one. 
    """
    if not _ACTIVE_CONV or _ACTIVE_CONV[cc.thread_id] is None:
        assistant_mgr = get_assistant_manager()
        assistant = assistant_mgr.get_or_build_assistant(cc.assistant_id)
        _ACTIVE_CONV[cc.thread_id]= assistant
    else:
        assistant=_ACTIVE_CONV[cc.thread_id]
    if assistant:
        resp = ResponseControl()
        rep = assistant.invoke(cc.query,cc.thread_id)
        resp.message=rep["messages"][-1].content
        resp.chat_history=rep["messages"]
        resp.assistant_id=cc.assistant_id
        resp.thread_id=cc.thread_id
        resp.user_id = cc.user_id
        return resp
    else:
        raise Exception(f"no assistant found with id {cc.assistant_id}")