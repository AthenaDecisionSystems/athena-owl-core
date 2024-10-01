from typing import Annotated, Any, Optional, Literal
import os
from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.metanames import GenTextParamsMetaNames
from langchain_ibm import WatsonxLLM

from langchain_core.prompts import BasePromptTemplate
from athena.llm.agents.agent_mgr import OwlAgentDefaultRunner, OwlAgent
from athena.llm.tools.tool_mgr import OwlToolEntity

class SequenceOfActionAgent(OwlAgentDefaultRunner):

    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        self.agent_id = agentEntity.agent_id
        self.prompt = prompt
        self.checkpointer = None
        project_id=os.environ.get("IBM_WATSON_PROJECT_ID")
        watson_api_key=os.environ.get("IBM_WATSONX_APIKEY")
        watsonx_url=os.environ.get("IBM_WATSONX_URL")
        credentials = Credentials(url=watsonx_url,
                                  api_key=watson_api_key)
        parameters = {
            GenTextParamsMetaNames.DECODING_METHOD: "sample",
            GenTextParamsMetaNames.MAX_NEW_TOKENS: 200,
            GenTextParamsMetaNames.MIN_NEW_TOKENS: 10,
            GenTextParamsMetaNames.TEMPERATURE: agentEntity.temperature,
            GenTextParamsMetaNames.TOP_K: agentEntity.top_k,
        }
        self.llm =  prompt | WatsonxLLM(url=credentials.get('url'),
                      apikey=credentials.get('apikey'),
                      project_id=project_id,
                      model_id=agentEntity.modelName,
                      params=parameters
                    )


class AdaptiveRagWithToolGraphAgent(OwlAgentDefaultRunner):


    def __init__(self, agentEntity: OwlAgent, prompt: Optional[BasePromptTemplate], tool_instances: Optional[list[OwlToolEntity]]):
        self.agent_id = agentEntity.agent_id
        project_id=os.environ.get("IBM_WATSON_PROJECT_ID")
        watson_api_key=os.environ.get("IBM_WATSONX_APIKEY")
        watsonx_url=os.environ.get("IBM_WATSONX_URL")
        