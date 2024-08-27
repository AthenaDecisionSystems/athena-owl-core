import unittest
import sys,os
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
sys.path.append('./src')
from athena.main import app
from athena.app_settings import  get_config
from athena.routers.dto_models import ConversationControl,ResponseControl
from fastapi.testclient import TestClient

"""
Test the app at the api level using FastAPI test client, and the configuration for integration tests.
Run from folder above tests.

pytest -s tests/it/test_app_api.py

Goals: 
* validate health and version paths
* address a general query to using the default prompt so it can validate reaching the selected LLM
"""
class TestAssistantsAPIs(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.client = TestClient(app)
        print("init test done")
       

    def build_ConversationControl(self):
        ctl = ConversationControl()
        ctl.agent_id="openai_chain_agent"
        ctl.user_id="test_user"
        ctl.thread_id="1"
        return ctl
    
    def test_basic_assistant(self):
        print(">>> test_basic_assistant \n ")
        ctl = self.build_ConversationControl()
        ctl.query="You are an expert in AI, can you answer this question: What is the value proposition of LangChain?"
        response=self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"\n--it--> {response.content}")
        assert response
        assert response.status_code == 200
        print(type(response.content))        
        assert "sorry" in response.content.decode() # type: ignore
    
    def _test_fake_assistant(self):
        print(">>> test_fake_assistant \n ")
        ctl = self.build_ConversationControl()
        ctl.agent_id="fake_assistant"
        ctl.thread_id="2"
        ctl.query="You are an expert in AI, can you answer this question: What is the value proposition of LangChain?"
        response=self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"\n--it--> {response.content}")
        assert response
        assert response.status_code == 200
        
    def test_basic_tool_assistant(self):
        print(">>> test_basic_tool_assistant \n ")
        ctl = self.build_ConversationControl()
        ctl.agent_id="openai_tool_chains"
        ctl.thread_id="3"
        ctl.query="You are an expert in AI, can you answer this question: What is Athena Decision Systems?"
        response=self.client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"\n--it--> {response.content}")
        assert response
        assert response.status_code == 200
        
    def test_mistral_agent(self):
        print("\n\n >>> test_mistral_agent at the API level\n")
        client = TestClient(app)
        ctl = ConversationControl()
        ctl.agent_id="mistral_large_agent"
        ctl.user_id="test_user"
        ctl.thread_id="1"
        ctl.query="What is Athena Owl Agent?"
        response=client.post(get_config().api_route + "/c/generic_chat", json= ctl.model_dump())
        print(f"\n---> {response.content}")
        if "500" in response.content.decode():
            self.fail("Error in backend")
      

if __name__ == '__main__':
    unittest.main()