"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

from athena.app_settings import get_config
from fastapi import APIRouter
from typing import List
from athena.llm.assistants.assistant_mgr import get_assistant_manager, OwlAssistant

    
router = APIRouter( prefix= get_config().api_route +"/a")


@router.get( "/assistants/")
def get_all_prompts() -> List[OwlAssistant]:
    return get_assistant_manager().get_assistants()