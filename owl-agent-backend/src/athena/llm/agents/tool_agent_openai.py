"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from athena.llm.agents.agent_mgr import OwlAgentInterface
from athena.llm.tools.tool_mgr import OwlToolEntity
from langchain import hub

"""
An open AI using tools
"""
class OpenAIToolAgent(OwlAgentInterface):

    def __init__(self,modelName, system_prompt, temperature, top_k, top_p, tool_entities: list[OwlToolEntity]):
        if "/" in system_prompt:
            self.prompt = hub.pull(system_prompt)
        else:
            self.prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history", optional=True),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
        ])
        self.model=ChatOpenAI(model=modelName, temperature= temperature / 50)
    
    def get_runnable(self):
        return   create_tool_calling_agent(self.model, self.tools, self.prompt)
        
    



    

    