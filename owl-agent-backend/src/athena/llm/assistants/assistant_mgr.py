"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
import uuid, yaml, logging
from functools import lru_cache
from athena.app_settings import get_config
from importlib import import_module
from athena.llm.agents.agent_mgr import get_agent_manager
from  athena.routers.dto_models import ConversationControl, ResponseControl
from typing import Any

LOGGER = logging.getLogger(__name__)

class OwlAssistant():
    
    def stream(self, query: str, thread_id: str) -> str:
        pass
    
    def invoke(self, query: str, thread_id: str) -> str:
        pass
    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        pass 
    
    def get_state(self):
        pass
    
class OwlAssistantEntity(BaseModel):
    """
    Entity to persist data about a OwlAssistant
    """
    assistant_id: str = str(uuid.uuid4())
    name: str = "default_assistant"
    description: str = "A default assistant to do simple LLM calls"
    class_name : str = "athena.llm.assistants.BaseAssistant.BaseAssistant"
    agent_id: str = ""
    
class AssistantManager():
    """
    A repository to manage OwlAssistant Entity
    """
    
    def __init__(self):
        self.ASSISTANTS: dict = dict()

    def save_assistant(self, assistant: OwlAssistantEntity) -> str:
        """Adds a new assistant, using a key to the assistants inventory.
        Args:
            assistant: The Owl Assistant definition.
        """
        self.ASSISTANTS[assistant.assistant_id] = assistant
        return assistant.assistant_id
    
    def get_assistant_by_id(self, id : str) -> OwlAssistantEntity:
        return self.ASSISTANTS[id]
    
    def load_assistants(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            a_dict = yaml.load(f, Loader=yaml.FullLoader)  # a dict with assistant entities
            for oa in a_dict:
                oae=OwlAssistantEntity.model_validate(a_dict[oa])
                self.ASSISTANTS[oae.assistant_id]=oae
    
    
    def get_assistants(self) -> dict[str,OwlAssistantEntity]:
        return self.ASSISTANTS

    def get_assistant_by_name(self, name: str) -> OwlAssistantEntity | None:
        for e in self.ASSISTANTS:
            if self.ASSISTANTS[e].name == name:
                return self.ASSISTANTS[e]
        return None
    
    def delete_assistant(self,key: str) -> str:
        entry = self.ASSISTANTS.get(key, None)
        if entry != None:
            del self.ASSISTANTS[key]
    
    def save_assistants(self, path: str = "assistants.yaml"):
        """Save the entire prompts in external file."""
        with open(path, "w", encoding="utf-8") as of:
            yaml.dump(self.ASSISTANTS, of)
        return path

        
    def get_or_build_assistant(self, assistant_id : str) -> OwlAssistant:
        oa = self.get_assistant_by_id(assistant_id)
        LOGGER.debug(f"--> in get_or_build_assistant {oa}")
        if oa is not None:
            module_path, class_name = oa.class_name.rsplit('.',1)
            mod = import_module(module_path)
            klass = getattr(mod, class_name)
            LOGGER.debug(f"--> {class_name} created")
            if oa.agent_id and oa.agent_id != "":
                agent=get_agent_manager().get_or_build_agent(oa.agent_id)
                return klass(agent)
            else:
                return klass()
        return None



_instance = None

@lru_cache
def get_assistant_manager() -> AssistantManager:
    """ Factory to get access to unique instance of assistant manager"""
    global _instance
    if _instance is None:
        path = get_config().owl_assistants_path
        if path is None:
            path="./athena/config/assistants.json"
        _instance = AssistantManager()
        _instance.load_assistants(path)
    return _instance
