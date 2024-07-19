from typing import Optional, Any

from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity

from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import BasePromptTemplate

class MistralAgent(OwlAgentInterface):
    """
    Agent using Mistral LLM with supports tool calling
    """
    
    
    def __init__(self,agentEntity: OwlAgentEntity, prompt: BasePromptTemplate, tool_instances: Optional[list[Any]]):
        self.prompt = prompt
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
        #self.llm = {"input": lambda x: x["input"], "chat_history" : lambda x: x["chat_history"]}  | self.prompt | self.model | StrOutputParser()
        self.llm = self.prompt | self.model | StrOutputParser()
    
    def get_runnable(self):
        return  self.llm
    
