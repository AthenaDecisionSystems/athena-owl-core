"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_anthropic import ChatAnthropic

from .base_owl_agent import BaseOwlAgent
from ..app_settings import get_config



class AnthropicClient(BaseOwlAgent):

    def get_model(self, stream, callbacks):
        return ChatAnthropic(model=get_config().owl_agent_llm_model, temperature=0, stream=stream, callbacks = callbacks)