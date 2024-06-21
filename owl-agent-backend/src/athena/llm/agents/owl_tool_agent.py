
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity
from athena.llm.tools.tool_mgr import OwlToolEntity
from langchain.agents import create_tool_calling_agent
from langchain import hub
from typing import Optional
from importlib import import_module
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_community.chat_models import ChatOllama

class OwlToolAgent(OwlAgentInterface):
    tools = None
    
    def __init__(self, agentEntity: OwlAgentEntity, system_prompt: str, tool_entities: Optional[list[OwlToolEntity]]):
        if "/" in system_prompt:
            self.prompt = hub.pull(system_prompt)
        else:
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history", optional=True),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad", optional=True),
            ])
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
        if tool_entities:
            self.tools = self.build_tool_instances(tool_entities)
     
    def _instantiate_model(self,modelName, modelClass, temperature):
        module_path, class_name = modelClass.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        return klass(model=modelName, temperature= temperature/100)
       
    def get_runnable(self):
        #return   self.prompt |  self.model.bind(self.tools) | StrOutputParser()
        return  create_tool_calling_agent(self.model, self.tools, self.prompt)
    

    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]):
        tool_list=[]
        for tool_entity in tool_entities:
            # TO DO rethink about this approach
            if tool_entity.tool_id == "tavily":
                tool_list.append(TavilySearchResults(max_results=2))
            else:
                raise Exception("Not yet implemented")
        return tool_list