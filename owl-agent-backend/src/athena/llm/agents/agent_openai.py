"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_openai import ChatOpenAI
from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity
from athena.llm.tools.tool_mgr import OwlToolEntity

"""
The most basic agent
"""
class OpenAIAgent(OwlAgentInterface):

    def __init__(self,agentEntity: OwlAgentEntity, system_prompt: str, tool_entities: list[OwlToolEntity]):
        self.model=ChatOpenAI(model=agentEntity.modelName, temperature= agentEntity.temperature / 50)
    
    def get_runnable(self):
        return  self.model
        
    



    

    