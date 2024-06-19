"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from pydantic import BaseModel
import uuid, yaml
from functools import lru_cache
from athena.app_settings import get_config
from importlib import import_module
from athena.routers.dto_models import ConversationControl, ResponseControl, ModelParameters
from athena.llm.prompts.prompt_mgr import get_prompt_manager
from athena.llm.tools.tool_mgr import get_tool_manager

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
    name: str = ""
    description: str = ""
    modelName: str = ""
    class_name: str = "athena.llm.agents.agent_openai.OpenAIClient"
    prompt_ref:  str = "default_prompt"
    temperature: int = 0  # between 0 to 100 and will be converted depending of te LLM
    top_k: int = 1
    top_p: int = 1
    tools: list[str] = []
    
    
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
    
    def get_or_build_agent(self, agent_id : str, locale: str) -> OwlAgentInterface | None:
        """_summary_
        Factory to create agent from its definition. Agent has a class to support the implementation.
        Prompt is the string, tools is a list of unique tool_id to get the definition within the agent class.
        Args:
            agent_id (str): _description_

        Returns:
            OwlAgentInterface | None: _description_
        """
        agent_entity = self.get_agent_by_id(agent_id)
        if agent_entity is not None:
            module_path, class_name = agent_entity.class_name.rsplit('.',1)
            mod = import_module(module_path)
            klass = getattr(mod, class_name)
            sys_prompt = get_prompt_manager().get_prompt(agent_entity.prompt_ref, locale)
            tools = []
            for tid in agent_entity.tools:
                tools.append(get_tool_manager().get_tool_by_id(tid))
            return klass(agent_entity.modelName, sys_prompt, agent_entity.temperature, agent_entity.top_p, tools)
        return None
            
_instance = None

@lru_cache
def get_agent_manager() -> AgentManager:
    """ Factory to get access to unique instance of Agent manager"""
    global _instance
    if _instance is None:
        path = get_config().owl_agents_path
        if path is None:
            path="./athena/config/agents.json"
        _instance = AgentManager()
        _instance.load_agents(path)
    return _instance
