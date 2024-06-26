"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse

import logging
from typing import AsyncGenerator
from importlib import import_module
from athena.routers.dto_models import ResponseControl, ConversationControl
from athena.app_settings import get_config
from athena.glossary.glossary_mgr import build_get_glossary
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

"""
Routes for the conversations. There is one instance created per request
"""
LOGGER = logging.getLogger(__name__)

# DEPRECATED
def init():
    global owl_agent
    build_get_glossary(get_config().owl_glossary_path)
    init_logger()


def init_logger():
    LOGGER.setLevel(get_config().logging_level_int)
    # Create handlers (e.g., console and file handlers)
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(f"{__name__}.log")
    # Set the logging level for handlers if different from the logger's level
    console_handler.setLevel(get_config().logging_level_int)
    file_handler.setLevel(get_config().logging_level_int)
    LOGGER.addHandler(console_handler)
    LOGGER.addHandler(file_handler)
    LOGGER.debug(
        f"\n@@@> Logging level: {LOGGER.getEffectiveLevel()}, should be " + str(get_config().logging_level_int)
    )


router = APIRouter( prefix=get_config().api_route + "/c",
                   dependencies=[Depends(get_config),Depends(init)])


@router.post("/generic_chat")
def synchronous_chat_with_owl(conversationControl: ConversationControl) -> ResponseControl:
    global owl_agent
    LOGGER.debug(f"\n@@@> Input from chat UI= {conversationControl}")
    resp = ResponseControl()
    try:
        if not conversationControl.assistant_id or conversationControl.assistant_id == "":
            conversationControl.assistant_id=get_config().owl_agent_default_assistant
        resp = get_or_start_conversation(conversationControl)
        
    except Exception as e:
        LOGGER.debug(f"\n@@@> Exception in chat conversation with error: {str(e)}")
        resp.status = 500
        resp.error = f"ERROR: backend exception {str(e)}"
        resp.assistant_id = conversationControl.assistant_id
        resp.user_id = conversationControl.user_id
        resp.thread_id = conversationControl.thread_id
        resp.chat_history = conversationControl.chat_history
    LOGGER.debug(f"\n@@@> {resp}")
    return resp


@router.post("/chat")
async def async_chat_with_owl(conversationControl: ConversationControl) -> Response:
    global owl_agent
    LOGGER.debug(f"\n@@@> Stream input from chat UI= {conversationControl}")
    async def event_stream() -> AsyncGenerator[str, None]:
        async for chunk in owl_agent.conversation_stream(conversationControl):
            yield chunk
    return StreamingResponse(event_stream(), media_type="text/event-stream")


