"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
from athena.app_settings import get_config
from fastapi import APIRouter
from athena.llm.prompts.prompt_mgr import get_prompt_manager


class PromptRequest(BaseModel):
    prompt_key: str
    prompt_locale: str
    prompt_content: str

router = APIRouter( prefix= get_config().api_route +"/a")


@router.get( "/prompts/")
def get_all_prompt_entities(locale: str) -> str:
    return get_prompt_manager().get_prompts()

@router.get( "/prompts/{locale}")
def get_prompt_for_ui(locale: str) -> str:
    return get_prompt_manager().get_prompt(get_config().owl_prompts_key_name,locale)

@router.get( "/prompts/{prompt_key}/{locale}")
def get_prompt_using_key_and_locale(prompt_key: str, locale: str) -> str:
    return get_prompt_manager().get_prompt(prompt_key,locale)

@router.get( "/prompts/{prompt_key}")
def get_prompt_using_key(prompt_key: str) -> dict[str,str]:
    return get_prompt_manager().get_prompt_locales(prompt_key)

@router.post("/prompts/")
def add_prompt_using_key_locale(promptRequest: PromptRequest):
    get_prompt_manager().add_prompt(promptRequest.prompt_key,promptRequest.prompt_locale, promptRequest.prompt_content)


@router.put("/prompts/")
def update_prompt_using_key_locale(promptRequest: PromptRequest):
    get_prompt_manager().update_prompt(promptRequest.prompt_key,promptRequest.prompt_locale, promptRequest.prompt_content)