from langchain_community.llms.fake import FakeListLLM
from athena.llm.agents.agent_mgr import OwlAgentDefaultRunner, OwlAgent
from athena.llm.tools.tool_mgr import OwlToolEntity
from typing import Optional, Any
from langchain_core.prompts import BasePromptTemplate

class FakeAgent(OwlAgentDefaultRunner):
    
    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        self.model=FakeListLLM(responses= ["one","two","free"], sleep = 0.4)
    
    def get_runnable(self):
        return  self.model
    
    def invoke(self, query : str) -> str:
        return self.model(query)