from langchain_community.llms.fake import FakeListLLM
from athena.llm.agents.agent_mgr import OwlAgentInterface

class FakeAgent(OwlAgentInterface):
    
    def __init__(self,modelName, system_prompt, temperature, top_k, top_p):
        self.model=FakeListLLM(responses= ["one","two","free"], sleep = 0.4)
    
    def get_runnable(self):
        return  self.model
    
    def invoke(self, query : str) -> str:
        return self.model(query)