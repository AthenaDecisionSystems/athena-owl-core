from langchain_community.llms.fake import FakeListLLM
from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity
from athena.llm.tools.tool_mgr import OwlToolEntity

class FakeAgent(OwlAgentInterface):
    
    def __init__(self, agentEntity: OwlAgentEntity, system_prompt: str, tool_entities: list[OwlToolEntity]):
        self.model=FakeListLLM(responses= ["one","two","free"], sleep = 0.4)
    
    def get_runnable(self):
        return  self.model
    
    def invoke(self, query : str) -> str:
        return self.model(query)