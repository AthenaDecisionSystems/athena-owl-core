"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity
from athena.llm.tools.tool_mgr import OwlToolEntity
from langchain import hub
from langchain_community.tools.tavily_search import TavilySearchResults
"""
An open AI using tools
"""
class OpenAIToolAgent(OwlAgentInterface):

    def __init__(self, agentEntity: OwlAgentEntity, system_prompt: str, tool_entities: list[OwlToolEntity]):
        if "/" in system_prompt:
            self.prompt = hub.pull(system_prompt)
        else:
            self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ])
        self.model=ChatOpenAI(model=agentEntity.modelName, temperature= agentEntity.temperature / 50)
        self.tools = self.build_tool_instances(tool_entities)
        
    def get_runnable(self):
        return   create_tool_calling_agent(self.model, self.tools, self.prompt)
        
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

    

    