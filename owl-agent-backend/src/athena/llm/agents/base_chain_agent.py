

from langchain_core.output_parsers import StrOutputParser

from langchain_core.messages import AIMessage, HumanMessage
from langchain.agents import create_tool_calling_agent, AgentExecutor


from langchain.agents.format_scratchpad.openai_tools import format_to_openai_tool_messages
from langchain.agents.output_parsers.tools import ToolsAgentOutputParser
from langchain_core.prompts import BasePromptTemplate
from athena.llm.agents.agent_mgr import OwlAgentInterface, OwlAgentEntity

# TODO assess if there is not a better approach
from athena.app_settings import get_config, AppSettings
from typing import Optional, Any
from importlib import import_module


class OwlAgent(OwlAgentInterface):
    tools = None
    
    def __init__(self, agentEntity: OwlAgentEntity, prompt: BasePromptTemplate, tool_instances: Optional[list[Any]]):
        self.prompt = prompt
        self.model=self._instantiate_model(agentEntity.modelName, agentEntity.modelClassName, agentEntity.temperature)
        if tool_instances:
            self.tools = tool_instances
            llm_with_tools = self.model.bind_tools(self.tools)
            agent = (
                                {
                                    "input": lambda x: x["input"],
                                    "agent_scratchpad": lambda x: format_to_openai_tool_messages(
                                        x["intermediate_steps"]
                                    ),
                                    "chat_history": lambda x: x["chat_history"],
                                }
                                | self.prompt
                                | llm_with_tools
                                | ToolsAgentOutputParser()
                            )
            #create_tool_calling_agent(self.model, self.tools, self.prompt)
            self.llm = AgentExecutor(agent= agent, tools=self.tools, verbose=True)
            
        else:
            self.llm = {"input": lambda x: x["input"], "chat_history" : lambda x: x["chat_history"]}  | self.prompt | self.model | StrOutputParser()
            
    def _instantiate_model(self,modelName, modelClass, temperature):
        module_path, class_name = modelClass.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        return klass(model=modelName, temperature= temperature/100)
       
    def get_runnable(self):
        #return   self.prompt |  self.model.bind(self.tools) | StrOutputParser()
        return  self.llm
    

    