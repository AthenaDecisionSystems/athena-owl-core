"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
from athena.app_settings import get_config
from fastapi import APIRouter
from athena.llm.prompts.prompt_mgr import get_prompt_manager, OwlPromptEntity
from typing import Any, List

class PromptRequest(BaseModel):
    prompt_key: str
    prompt_locale: str
    prompt_content: str

router = APIRouter( prefix= get_config().api_route +"/a")


@router.get( "/prompts", tags=["Manage prompts"])
def get_all_prompt_entities() -> List[OwlPromptEntity]:
    all = get_prompt_manager().get_prompts()
    l = []
    for e in all.values():
        l.append(OwlPromptEntity.model_validate(e))
    return l


@router.get( "/prompts/{locale}", tags=["Manage prompts"])
def get_prompt_for_ui(locale: str) -> str:
    return get_prompt_manager().get_prompt(get_config().owl_prompts_key_name,locale)

@router.get( "/prompts/{prompt_key}/{locale}", tags=["Manage prompts"])
def get_prompt_using_key_and_locale(prompt_key: str, locale: str) -> str:
    return get_prompt_manager().get_prompt(prompt_key,locale)

@router.get( "/prompts/{prompt_key}", tags=["Manage prompts"])
def get_prompt_using_key(prompt_key: str) -> dict[str,str]:
    return get_prompt_manager().get_prompt_locales(prompt_key)

@router.post("/prompts", tags=["Manage prompts"])
def add_prompt_using_key_locale(promptRequest: PromptRequest):
    get_prompt_manager().add_prompt(promptRequest.prompt_key,promptRequest.prompt_locale, promptRequest.prompt_content)


@router.put("/prompts", tags=["Manage prompts"])
def update_prompt_using_key_locale(promptRequest: PromptRequest):
    get_prompt_manager().update_prompt(promptRequest.prompt_key,promptRequest.prompt_locale, promptRequest.prompt_content)
    
    
@router.delete( "/prompts/{prompt_key}", tags=["Manage prompts"])
def delete_prompt_using_key(prompt_key: str) -> str:
    return get_prompt_manager().delete_prompt(prompt_key)


@router.post("/prompts/reset", tags=["Manage prompts"])
def reset_assistant_definitions():
    get_prompt_manager().load_prompts(get_config().owl_prompts_path)
    return "Done"