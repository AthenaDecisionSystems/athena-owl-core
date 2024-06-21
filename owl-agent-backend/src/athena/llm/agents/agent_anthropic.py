"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_anthropic  import ChatAnthropic
from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity
from athena.llm.tools.tool_mgr import OwlToolEntity
from langchain_community.tools.tavily_search import TavilySearchResults

#tool = TavilySearchResults(max_results=2)
#tools = [tool]
"""
Agent with tools and Anthropic model
"""
class AnthropicAgent(OwlAgentInterface):

    def __init__(self,agentEntity: OwlAgentEntity, system_prompt: str, tool_entities: list[OwlToolEntity]):
        self.system = system_prompt
        self.model=ChatAnthropic(model_name=agentEntity.modelName)
        self.tools = self.build_tool_instances(tool_entities)
        
    
    def get_runnable(self):
        llm_with_tools =self.model.bind_tools(self.tools)
        return  llm_with_tools 
    
    def get_tools(self):
        return self.tools
    
    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]):
        tool_list=[]
        for tool_entity in tool_entities:
            # TO DO rethink about this approach
            if tool_entity.tool_id == "tavily":
                tool_list.append(TavilySearchResults(max_results=2))
            else:
                raise Exception("Not yet implemented")
        return tool_list