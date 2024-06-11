"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_anthropic.chat_models import ChatAnthropic

from athena.llm.base_owl_agent import BaseOwlAgent
from athena.app_settings import get_config
from athena.routers.dto_models import ModelParameters
from langchain.agents import create_tool_calling_agent

class AnthropicClient(BaseOwlAgent):
   
    def get_model(self, stream, parameters: ModelParameters, callbacks):
        if parameters:
            model = ChatAnthropic(model=get_config().owl_agent_llm_model, temperature= parameters.temperature / 100, stream=stream, callbacks = callbacks)
        else:
            model = ChatAnthropic(model=get_config().owl_agent_llm_model, temperature=0, stream=stream, callbacks = callbacks)  
        return model
    
    def get_agent(self, model, prompt, tools ):
        return create_tool_calling_agent(model,tools,prompt)