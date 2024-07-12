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
from athena.routers.dto_models import ConversationControl, ResponseControl, ChatMessage
from langchain_core.messages import AIMessage, HumanMessage
from typing import Any, Optional

LOGGER = logging.getLogger(__name__)

class OwlAssistant(object):
    agents: []
    assistant_id: str
    
    def __init__(self, assistantID, loaded_agents):
        self.assistant_id = assistantID
        self.agents = loaded_agents
        
    def stream(self, query: str, thread_id: str):
        # TO BE DONE
        pass
    
    def transform_chat_history(self, chat_history: list[ChatMessage]):
        l=[]
        for m in chat_history:
            if m.role == "human":
                l.append(HumanMessage(content=m.content))
            else:
                l.append(AIMessage(content=m.content))
        return l
    
    def _build_response(self, controller: ConversationControl):
        resp = ResponseControl()
        resp.chat_history = controller.chat_history
        resp.assistant_id = controller.assistant_id
        resp.thread_id = controller.thread_id
        resp.user_id = controller.user_id
        return resp
    
    def invoke(self, request, thread_id: Optional[str], **kwargs) -> dict[str, Any] | Any:
        return {}
        
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        LOGGER.debug(f"\n@@@> query assistant {controller.query}")
        lg_chat_history = self.transform_chat_history(controller.chat_history)
        request = { "input": controller.query, "chat_history" : lg_chat_history }
        agent_resp= self.invoke(request, controller.thread_id)   # AIMessage
        resp = self._build_response(controller)
        if isinstance(agent_resp,dict):
            if agent_resp.get("output"):
                resp.message= agent_resp.get("output")
                resp.chat_history.extend([
                        ChatMessage(role="human", content= controller.query),
                        ChatMessage(role="AI", content=str(agent_resp.get("output"))),
                        ])
        else: # str
            resp.message=agent_resp
            resp.chat_history.extend([
                        ChatMessage(role="human", content= controller.query),
                        ChatMessage(role="AI", content=agent_resp)
                        ])
        return resp
            
    
    
class OwlAssistantEntity(BaseModel):
    """
    Entity to persist data about a OwlAssistant
    """
    assistant_id: str = str(uuid.uuid4())
    name: str = "default_assistant"
    description: str = "A default assistant to do simple LLM calls"
    class_name : str = "athena.llm.assistants.BaseAssistant.BaseAssistant"
    agents: list[str] = []
    
class AssistantManager(object):
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
    
    def get_assistant_by_id(self, id: str) -> OwlAssistantEntity:
        """
        Get Assistant entity description given its unique identifier
        Args:
            id (str): unique identifier persisted as assistant_id

        Returns:
            OwlAssistantEntity: The assistant entity with information to create instance of the assistant with one to many agents
        """
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
        return "Done!"
    
    def save_assistants(self, path: str = "assistants.yaml"):
        """Save the entire prompts in external file."""
        with open(path, "w", encoding="utf-8") as of:
            yaml.dump(self.ASSISTANTS, of)
        return path

        
    def build_assistant(self, assistant_id : str, locale: str) -> OwlAssistant:
        """
        A factory method to create an assistant executor using the AssistantEntity information
        Args:
            assistant_id (str): _description_
            locale (str): _description_

        Returns:
            OwlAssistant: _description_
        """
        oa = self.get_assistant_by_id(assistant_id)
        LOGGER.debug(f"--> in get_or_build_assistant {oa}")
        if oa is not None:
            module_path, class_name = oa.class_name.rsplit('.',1)
            mod = import_module(module_path)
            klass = getattr(mod, class_name)
            LOGGER.debug(f"--> {class_name} created")
            
            if len(oa.agents) == 0:
                return klass(assistant_id)
            agents=[]
            for aid in oa.agents:
                agent=get_agent_manager().build_agent(aid, locale)
                agents.append(agent)
            return klass(assistant_id,agents)
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
