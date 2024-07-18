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
        self.model=ChatMistralAI(model=agentEntity.modelName, temperature=agentEntity.temperature)
        if tool_instances:
            self.tools = tool_instances
            agent = create_tool_calling_agent(self.model, self.tools, self.prompt)
            self.llm = AgentExecutor(agent= agent, tools=self.tools, verbose=True)
        else:
            self.llm = {"input": lambda x: x["input"], "chat_history" : lambda x: x["chat_history"]}  | self.prompt | self.model | StrOutputParser()
  
    
    def get_runnable(self):
        llm_with_tools =self.model.bind_tools(self.tools)
        return  llm_with_tools 
    
    def get_tools(self):
        return self.tools