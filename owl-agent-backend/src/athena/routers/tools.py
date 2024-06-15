"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

from athena.app_settings import get_config
from fastapi import APIRouter
from typing import List
from athena.llm.tools.tool_mgr import get_tool_manager, OwlToolEntity

    
router = APIRouter( prefix= get_config().api_route +"/a")


@router.get( "/tools/")
def get_all_tools() -> List[OwlToolEntity]:
    all = get_tool_manager().get_tools()
    l = []
    for e in all.values():
            l.append(OwlToolEntity.model_validate(e))
    return l

@router.get("/tools/{id}")
def get_tool_by_id(id: str) -> OwlToolEntity:
    return get_tool_manager().get_tool_by_id(id)

@router.get("/tools/name/{name}")
def get_tool_by_name(name: str) -> OwlToolEntity | None:
    return get_tool_manager().get_tool_by_name(name)

@router.post("/tools/")
def new_tool_entity(e: OwlToolEntity) -> str:
    return get_tool_manager().save_tool(e)

@router.put("/tools/{id}")
def update_tool_entity(id: str, e: OwlToolEntity) -> str:
    return get_tool_manager().save_tool(e)


@router.delete("/tools/{id}")
def delete_tool_entity(id: str) -> str:
    return get_tool_manager().delete_tool(id)