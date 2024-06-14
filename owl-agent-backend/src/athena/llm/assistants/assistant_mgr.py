from pydantic import BaseModel
import uuid
from functools import lru_cache
from athena.app_settings import get_config

class OwlAssistant(BaseModel):
    """
    
    """
    assistant_id: str = str(uuid.uuid4())
    name: str = "default_assistant"
    description: str = "A default assistant to do simple LLM calls"
    class_name : str = "athena.llm.assistants.BaseAssistant.py"
    
    
class AssistantManager():
    """
    A repository to manage OwlAssistant Entity
    """
    
    def __init__(self):
        self.ASSISTANTS: dict

    def add_assistant(self, assistant: OwlAssistant):
        """Adds a new assistant, using a key to the assistants inventory.

        Args:
            assistant (str): The Owl Assistant definition.

        """
        self.ASSISTANTS[assistant.assistant_id] = assistant
    
    def load_assistants(self, path: str):
        pass

_instance = None

@lru_cache
def get_assistant_manager() -> AssistantManager:
    """ Factory to get access to unique instance of Prompts manager"""
    global _instance
    if _instance is None:
        path = get_config().owl_assistants_path
        if path is None:
            path="./athena/config/prompts.json"
        _instance = AssistantManager()
        _instance.load_assistants(path)
    return _instance
