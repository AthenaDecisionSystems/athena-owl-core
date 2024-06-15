"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from langchain_openai import ChatOpenAI


"""
The most basic agent
"""
class OpenAIAgent():

    def __init__(self,modelName, system_prompt, temperature, top_k, top_p):
        self.model=ChatOpenAI(model=modelName, temperature= temperature / 50)
    
    def get_runnable(self):
        return  self.model
        
    



    

    