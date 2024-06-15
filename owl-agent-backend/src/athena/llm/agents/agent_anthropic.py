"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_anthropic  import ChatAnthropic

#from langchain_community.tools.tavily_search import TavilySearchResults
#tool = TavilySearchResults(max_results=2)
#tools = [tool]
"""
Agent with tools and Anthropic model
"""
class AnthropicAgent():

    def __init__(self,modelName, system_prompt_txt, temperature, top_p, tools):
        self.system = system_prompt_txt
        self.model=ChatAnthropic(model_name=modelName, temperature= temperature, top_p = top_p)
        self.tools = tools
        
    
    def get_runnable(self):
        llm_with_tools =self.model.bind_tools(self.tools)
        return  llm_with_tools 
    
    def get_tools(self):
        return self.tools