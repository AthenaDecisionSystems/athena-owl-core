"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

from athena.app_settings import get_config
from fastapi import APIRouter
from typing import List
from athena.llm.assistants.assistant_mgr import get_assistant_manager, OwlAssistantEntity

    
router = APIRouter( prefix= get_config().api_route +"/a")


@router.get( "/assistants/")
def get_all_assistant_entities() -> List[OwlAssistantEntity]:
    all = get_assistant_manager().get_assistants()
    l = []
    for e in all.values():
            l.append(OwlAssistantEntity.model_validate(e))
    return l

@router.get("/assistants/{id}")
def get_assistant_entity_by_id(id: str) -> OwlAssistantEntity:
    return get_assistant_manager().get_assistant_by_id(id)

@router.get("/assistants/name/{name}")
def get_assistant_entity_by_name(name: str) -> OwlAssistantEntity | None:
    return get_assistant_manager().get_assistant_by_name(name)

@router.post("/assistants/")
def new_assistant_entity(e: OwlAssistantEntity) -> str:
    return get_assistant_manager().save_assistant(e)

@router.put("/assistants/{id}")
def update_assistant_entity(id: str, e: OwlAssistantEntity) -> str:
    return get_assistant_manager().save_assistant(e)


@router.delete("/assistants/{id}")
def delete_assistant_entity(id: str) -> str:
    return get_assistant_manager().delete_assistant(id)

@router.post("/assistants/reset")
def reset_assistant_definitions():
    get_assistant_manager().load_assistants(get_config().owl_assistants_path)
    return "Done"