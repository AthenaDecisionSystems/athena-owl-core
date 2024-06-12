"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_openai import ChatOpenAI
from langchain.agents import create_openai_tools_agent
from athena.llm.base_owl_agent import BaseOwlAgent
from athena.app_settings import get_config
from athena.routers.dto_models import ModelParameters

class OpenAIClient(BaseOwlAgent):



    def get_model(self, stream, parameters: ModelParameters, callbacks):
        if parameters:
            model = ChatOpenAI(model=parameters.modelName, temperature= parameters.temperature / 50, stream=stream, callbacks = callbacks)
        else:
            model = ChatOpenAI(model=get_config().owl_agent_llm_model, temperature=0, stream=stream, callbacks = callbacks)  
        return model
    
    def get_agent(self, model, prompt, tools ):
        return create_openai_tools_agent(model, tools, prompt)
    



    

    