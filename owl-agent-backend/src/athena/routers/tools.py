"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

from athena.app_settings import get_config
from fastapi import APIRouter
from typing import List
from athena.llm.tools.tool_mgr import get_tool_entity_manager, OwlToolEntity

    
router = APIRouter( prefix= get_config().api_route +"/a")


@router.get( "/tools/", tags=["Manage tools"])
def get_all_tools() -> List[OwlToolEntity]:
    all = get_tool_entity_manager().get_tools()
    l = []
    for e in all.values():
            l.append(OwlToolEntity.model_validate(e))
    return l

@router.get("/tools/{id}", tags=["Manage tools"])
def get_tool_by_id(id: str) -> OwlToolEntity:
    return get_tool_entity_manager().get_tool_by_id(id)

@router.get("/tools/functionname/{name}", tags=["Manage tools"])
def get_tool_by_function_name(name: str) -> OwlToolEntity | None:
    return get_tool_entity_manager().get_tool_by_function_name(name)

@router.post("/tools/", tags=["Manage tools"])
def new_tool_entity(e: OwlToolEntity) -> str:
    return get_tool_entity_manager().save_tool(e)

@router.put("/tools/{id}", tags=["Manage tools"])
def update_tool_entity(id: str, e: OwlToolEntity) -> str:
    return get_tool_entity_manager().save_tool(e)


@router.delete("/tools/{id}", tags=["Manage tools"])
def delete_tool_entity(id: str) -> str:
    return get_tool_entity_manager().delete_tool(id)


@router.post("/tools/reset", tags=["Manage tools"])
def reset_from_files():
    return get_tool_entity_manager().load_tool_definitions(get_config().owl_tools_path)