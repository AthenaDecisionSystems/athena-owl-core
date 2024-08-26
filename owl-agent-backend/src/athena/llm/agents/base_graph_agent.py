from athena.llm.agents.agent_mgr import OwlAgentAbstractRunner, OwlAgent
from langchain_core.prompts import BasePromptTemplate
from athena.llm.tools.tool_mgr import OwlToolEntity
from typing import Optional, Any

class BaseGraphAgent(OwlAgentAbstractRunner):

    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
