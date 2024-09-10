"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer

The agent manager supports CRUD operations for the OwlAgent and 
a factory method to create the agent.
It is deployed as a Singleton
"""
from pydantic import BaseModel
import uuid
import yaml
import logging
from typing import Optional, Any
from functools import lru_cache
from athena.app_settings import get_config
from importlib import import_module
from athena.routers.dto_models import ConversationControl, ResponseControl, ChatMessage, StyledMessage
from athena.llm.prompts.prompt_mgr import get_prompt_manager
from athena.llm.tools.tool_mgr import get_tool_entity_manager
from athena.llm.tools.tool_mgr import OwlToolEntity
from langchain_core.prompts import BasePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor, create_json_chat_agent, create_structured_chat_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import AIMessage, HumanMessage

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')
LOGGER = logging.getLogger(__name__)


class OwlAgent(BaseModel):
    """
    Entity definition to persist data about a OwlAgent
    """
    agent_id: str = str(uuid.uuid4())
    name: str = ""
    description: Optional[str] = None
    modelName: str = ""
    modelClassName: Optional[str] = None
    runner_class_name: Optional[str] = "athena.llm.agents.agent_mgr.OwlAgentAbstractRunner"
    prompt_ref:  Optional[str] = None
    temperature: int = 0  # between 0 to 100 and will be converted depending of te LLM
    top_k: int = 1
    top_p: int = 1
    tools: list[str] = []



class OwlAgentDefaultRunner(object):
    agent_id: str  # keep the reference to the owl agent id, in case user change of model

    """
    Base class to represent an instance of an agent. So it defines a contract to support 
    conversations and the integration inside an assistant.
    """
    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        self.instantiate_llm(agentEntity,prompt,tool_instances)
        self.agent_id = agentEntity.agent_id
    
    def instantiate_llm(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        LOGGER.debug("Initialing base chain OwlAgent")
        if prompt:
            self.prompt = prompt
        else:
            self.prompt = ChatPromptTemplate.from_messages([
                        ("system", "You are a helpful assistant"),
            ])
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
        if tool_instances:
            self.tools = tool_instances
            agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
            #agent = create_json_chat_agent(self.model, self.tools, self.prompt)
            #agent = create_structured_chat_agent(self.model, self.tools, self.prompt)
            self.llm = AgentExecutor(agent= agent, tools=self.tools, verbose=True)
            
        else:
            if "input" in self.prompt.input_types:
                if "chat_history" in self.prompt.input_types:
                    self.llm = {"input": lambda x: x["input"], "chat_history" : lambda x: x["chat_history"]}  | self.prompt | self.model | StrOutputParser()
                else:
                    self.llm = {"input": lambda x: x["input"]}  | self.prompt | self.model | StrOutputParser()
            else:
                self.llm = self.prompt | self.model | StrOutputParser()
            self.tools = []
        return self.llm
        
    def _transform_chat_history(self, chat_history: list[ChatMessage]):
        l=[]
        for m in chat_history:
            if m.role == "human":
                l.append(HumanMessage(content=m.content))
            else:
                l.append(AIMessage(content=m.content))
        return l
    
    def process_close_answer(self, controller: ConversationControl):
        pass

    def build_response(self, controller: ConversationControl, agent_resp):
        resp = ResponseControl()
        resp.chat_history = controller.chat_history
        resp.agent_id = controller.agent_id
        resp.thread_id = controller.thread_id
        resp.user_id = controller.user_id
        if isinstance(agent_resp,dict):
            if agent_resp.get("output"):
                    resp.messages= [StyledMessage(content=agent_resp.get("output"))]
                    resp.chat_history.extend([
                            ChatMessage(role="human", content= controller.query),
                            ChatMessage(role="AI", content=str(agent_resp.get("output"))),
                            ])
        else: # str
            resp.messages=[StyledMessage(content=agent_resp)]
            resp.chat_history.extend([
                        ChatMessage(role="human", content= controller.query),
                        ChatMessage(role="AI", content=agent_resp)
                        ])
        return resp
    
    def send_conversation(self, controller: ConversationControl) -> ResponseControl | Any:
        LOGGER.debug(f"\n@@@> query assistant {controller.query}")
        lg_chat_history = self._transform_chat_history(controller.chat_history)
        if controller.query is None or len(controller.query) == 0:
            resp=self.process_close_answer(controller)
        else:
            request = { "input": [controller.query], "chat_history" : lg_chat_history }
            agent_resp= self.invoke(request, controller.thread_id)   # AIMessage
            resp= self.build_response(controller, agent_resp)
            
        return resp
    
    def get_runnable(self):
        return  self.llm
    
    def get_tools(self):
        return self.tools
    
    def get_model(self):
        return self.model
    
    def get_prompt(self):
        return self.prompt
    
    def invoke(self, request, thread_id: Optional[str], **kwargs) -> dict[str, Any] | Any:
        return self.get_runnable().invoke(request)  # by default a chain agent does not use thread_id
    
    def _instantiate_model(self,modelName, modelClass, temperature):
        module_path, class_name = modelClass.rsplit('.',1)
        mod = import_module(module_path)
        llm_model_class = getattr(mod, class_name)
        return llm_model_class(model=modelName, temperature= temperature/100)
 
    
class AgentManager(object):
    """
    The agent manager manages OwlAgent Entities.
    """
    
    def __init__(self):
        self.AGENTS: dict = dict()

    def save_agent(self, agentEntity: OwlAgent) -> str:
        self.AGENTS[agentEntity.agent_id] = agentEntity
        return agentEntity.agent_id
    
    def load_agents(self, path: str):
        with open(path, "r", encoding="utf-8") as f:
            a_dict = yaml.load(f, Loader=yaml.FullLoader)  # a dict with assistant entities
            for oa in a_dict:
                oae=OwlAgent.model_validate(a_dict[oa])
                self.AGENTS[oae.agent_id]=oae
    
    def get_agents(self) -> dict[str,OwlAgent]:
        return self.AGENTS
    
    
    def get_agent_by_id(self, id : str) -> OwlAgent:
        return self.AGENTS[id]
    
    def get_agent_by_name(self, name: str) -> OwlAgent | None:
        for e in self.AGENTS:
            if self.AGENTS[e].name == name:
                return self.AGENTS[e]
        return None
    
    def delete_agent(self,key: str) -> str:
        entry = self.AGENTS.get(key, None)
        if entry != None:
            del self.AGENTS[key]
        return "Done"
    
    def build_agent_runner(self, agent_id : str, locale: str) -> OwlAgentDefaultRunner | None:
        """
        Factory to create agent from its definition. Agent has a class to support the implementation.
        Prompt is the string, tools is a list of unique tool_id to get the definition within the agent class.
        Args:
            agent_id (str): _description_

        Returns:
            OwlAgentInterface
        """
        agent_entity = self.get_agent_by_id(agent_id)
        return self.build_agent_runner_from_entity(agent_entity,locale)

    def build_agent_runner_from_entity(self, agent_entity: OwlAgent, locale: str = "en") -> OwlAgentDefaultRunner | None:
        if agent_entity:
            module_path, class_name = agent_entity.runner_class_name.rsplit('.',1)
            mod = import_module(module_path)
            runner_class = getattr(mod, class_name)
            prompt = None
            tool_instances = None
            if agent_entity.prompt_ref:
                prompt = get_prompt_manager().build_prompt(agent_entity.prompt_ref, locale)
            if agent_entity.tools:
                tool_entities = []
                for tid in agent_entity.tools:
                    tool_entities.append(get_tool_entity_manager().get_tool_by_id(tid))
                tool_instances=get_config().get_tool_factory().build_tool_instances(tool_entities)
            return runner_class(agent_entity, prompt, tool_instances)
        return None

_instance = None

@lru_cache
def get_agent_manager() -> AgentManager:
    """ Factory to get access to unique instance of Agent manager"""
    global _instance
    if _instance is None:
        path = get_config().owl_agents_path
        if path is None:
            path="./athena/config/agents.yaml"
        _instance = AgentManager()
        _instance.load_agents(path)
    return _instance
