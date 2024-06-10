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

"""
Routes for the conversations. There is one instance created per request
"""
LOGGER = logging.getLogger(__name__)

def init():
    global owl_agent
    build_get_glossary(get_config().owl_glossary_path)
    module_path, class_name = get_config().owl_agent_llm_client_class.rsplit('.',1)
    mod = import_module(module_path)
    klass = getattr(mod, class_name)
    owl_agent= klass()
    init_logger()
    LOGGER.debug(f"OWL Agent used is {klass}")

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
        f"Logging level: {LOGGER.getEffectiveLevel()}, should be " + str(get_config().logging_level_int)
    )


router = APIRouter( prefix=get_config().api_route + "/c",
                   dependencies=[Depends(get_config),Depends(init)])

@router.post("/generic_qa")
def generic_qa(conversationControl: ConversationControl) -> ResponseControl:
    """
    supports Q&A interactions with the configured LLM. The conversation controller includes the
    query and flags to control a demonstration: using RAG and using decision service for best action
    """
    global owl_agent
    LOGGER.debug(f"Input= {conversationControl}")
    resp = ResponseControl()
    try:
        resp = owl_agent.send_query(conversationControl)
    except Exception as e:
        LOGGER.debug(str(e))
        resp.status = 500
        resp.message = f"ERROR: backend exception {str(e)}"

    LOGGER.debug(resp)
    return resp

@router.post("/generic_chat")
def generic_chat(conversationControl: ConversationControl) -> ResponseControl:
    global owl_agent
    LOGGER.debug(f"Input from chat UI= {conversationControl}")
    resp = ResponseControl()
    try:
        resp = owl_agent.send_conversation(conversationControl)
    except Exception as e:
        LOGGER.debug(str(e))
        resp.status = 500
        resp.error = f"ERROR: backend exception {str(e)}"
    LOGGER.debug(resp)
    return resp


@router.post("/chat")
async def chat_with_owl(conversationControl: ConversationControl) -> Response:
    global owl_agent
    LOGGER.debug(f"Stream input from chat UI= {conversationControl}")
    async def event_stream() -> AsyncGenerator[str, None]:
        async for chunk in owl_agent.conversation_stream(conversationControl):
            yield chunk
    return StreamingResponse(event_stream(), media_type="text/event-stream")


