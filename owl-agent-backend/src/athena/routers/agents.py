"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

from athena.app_settings import get_config
from fastapi import APIRouter
from typing import List
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgentEntity

    
router = APIRouter( prefix= get_config().api_route +"/a")


@router.get( "/agents/")
def get_all_agent_entities() -> List[OwlAgentEntity]:
    all = get_agent_manager().get_agents()
    l = []
    for e in all.values():
            l.append(OwlAgentEntity.model_validate(e))
    return l

@router.get("/agents/{id}")
def get_agent_entity_by_id(id: str) -> OwlAgentEntity:
    return get_agent_manager().get_agent_by_id(id)

@router.get("/agents/name/{name}")
def get_agent_entity_by_name(name: str) -> OwlAgentEntity | None:
    return get_agent_manager().get_agent_by_name(name)

@router.post("/agents/")
def new_agent_entity(e: OwlAgentEntity) -> str:
    return get_agent_manager().save_agent(e)

@router.put("/agents/{id}")
def update_agent_entity(id: str, e: OwlAgentEntity) -> str:
    return get_agent_manager().save_agent(e)


@router.delete("/agents/{id}")
def delete_agent_entity(id: str) -> str:
    return get_agent_manager().delete_agent(id)

@router.post("/agents/reset")
def reset_from_files():
    return get_agent_manager().load_agents(get_config().owl_agents_path)