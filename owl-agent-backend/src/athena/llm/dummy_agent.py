"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from .owl_agent import AgentInterface
from ..routers.dto_models import ConversationControl, ResponseControl
from ..itg.ds.insurance_claim_repo_mock import InsuranceClaimInMem
import logging
from langchain.agents import AgentExecutor, tool
from langchain_community.llms.fake import FakeListLLM
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

#@tool
def get_claim_by_id(id: int) -> str:
    """get insurance claim information given its unique claim identifier id"""
    claim_data_source = InsuranceClaimInMem()
    return claim_data_source.get_claim_json(id)

class DummyAgent(AgentInterface):
    """
    The Dummy Agent permits to test without LLM. 
    """
    def __init__(self):
        self.LOGGER = logging.getLogger("DummyAgent - ")
        self.claim_data_source = InsuranceClaimInMem()

        pass

    def build_agent_executor(self):
        prompt = ChatPromptTemplate.from_messages([
                ("system", "You are a helpful assistant for an insurance company, if you do not the answer try to use the related tools"),
                ("user", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ])
        tools = [get_claim_by_id]
        llm = FakeListLLM(responses=["call the tool get_claim_by_id with id 1"])
        agent = prompt | llm | JsonOutputParser()
        return AgentExecutor(agent=agent, verbose=True)

    def send_query(self,controller: ConversationControl) -> ResponseControl:
        self.LOGGER.info(controller)
        #agent_executor =  self.build_agent_executor()
        #rep= agent_executor.invoke({"input": conversationControl.query})
        rep = ResponseControl(message="As a dummy LLM I have no clue what you are talking about")
        return rep
        


    def send_conversation(self, controller: ConversationControl) -> ResponseControl:
        rep = ResponseControl(message="As a dummy LLM I have no clue what you are talking about")
        return rep
    
    """
    resp = ResponseControl()
        agentResponse=agent_executor.invoke({"input": conversationControl.query})
        resp.message=agentResponse["output"]
    """