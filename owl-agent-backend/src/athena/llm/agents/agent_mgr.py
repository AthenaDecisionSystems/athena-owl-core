from pydantic import BaseModel
import uuid, yaml
from functools import lru_cache
from athena.app_settings import get_config
from importlib import import_module
from  athena.routers.dto_models import ConversationControl, ResponseControl, ModelParameters

class OwlAgentInterface:
    def send_query(self,controller: ConversationControl) -> ResponseControl:
        """
        Send the given query to a backend LLM, as the conversation control may have settings for RAG and decision services
        then the others functions of this class may be called. This method needs to be overridden for each different LLM
        """
        pass

    def send_conversation(self, controller: ConversationControl) -> ResponseControl:
        """
        Send the current chat conversation with history and query to a backend LLM, as the conversation control may have settings for RAG and decision services
        then the others functions of this class may be called. This method needs to be overridden for each different LLM
        """
        pass

    
    def get_model(self, stream, parameters: ModelParameters, callbacks):
        return None  
    
    def get_agent(self, model, prompt, tools ):
        return None 
    
    
class OwlAgentEntity(BaseModel):
    agent_id: str = str(uuid.uuid4())
    name: str = "DefaultAgent"
    description: str = "The default agent uses openai"
    model_name: str = "gpt-3.5-turbo-0125"
    class_name: str = "athena.llm.agents.agent_openai.OpenAIClient"
    prompt_ref:  str = "default_prompt"
    temperature: int = 0  # between 0 to 100 and will be converted depending of te LLM
    top_k: int = 1
    top_p: int = 1
    
    
class AgentManager():
    
    def __init__(self):
        self.AGENTS: dict = dict()

    def save_agent(self, agentEntity: OwlAgentEntity) -> str:
        self.AGENTS[agentEntity.agent_id] = agentEntity
        return agentEntity.agent_id
    
    def load_agents(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            a_dict = yaml.load(f, Loader=yaml.FullLoader)  # a dict with assistant entities
            for oa in a_dict:
                oae=OwlAgentEntity.model_validate(a_dict[oa])
                self.AGENTS[oae.agent_id]=oae
    
    def get_agents(self) -> dict[str,OwlAgentEntity]:
        return self.AGENTS
    
    
    def get_agent_by_id(self, id : str) -> OwlAgentEntity:
        return self.AGENTS[id]
    
    def get_agent_by_name(self, name: str) -> OwlAgentEntity | None:
        for e in self.AGENTS:
            if self.AGENTS[e].name == name:
                return self.AGENTS[e]
        return None
    
    def delete_agent(self,key: str) -> str:
        entry = self.AGENTS.get(key, None)
        if entry != None:
            del self.AGENTS[key]
        return "Done"
    
    def get_or_build_agent(self, agent_id : str) -> OwlAgentInterface | None:
        oa = self.get_agent_by_id(agent_id)
        if oa is not None:
            module_path, class_name = oa.class_name.rsplit('.',1)
            mod = import_module(module_path)
            klass = getattr(mod, class_name)
            return klass()
        return None
    
    
_instance = None

@lru_cache
def get_agent_manager() -> AgentManager:
    """ Factory to get access to unique instance of Prompts manager"""
    global _instance
    if _instance is None:
        path = get_config().owl_agents_path
        if path is None:
            path="./athena/config/agents.json"
        _instance = AgentManager()
        _instance.load_agents(path)
    return _instance
