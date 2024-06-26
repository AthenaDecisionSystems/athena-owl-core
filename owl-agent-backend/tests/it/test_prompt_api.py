
import unittest
from dotenv import load_dotenv
import sys,os
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("./.env")
sys.path.append('./src')
from athena.main import app
from athena.app_settings import  get_config
from athena.routers.prompts import PromptRequest
from fastapi.testclient import TestClient

"""
Test the app at the api level using FastAPI test client, and configuration for tests.
Run from folder above tests.

pytest -s tests/it/test_app_api.py
"""
class TestPromptApi(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        self.client = TestClient(app)
        print("init test done")
       

    def test_get_default_prompt(self):
        response = self.client.get(get_config().api_route +"/a/prompts/default_prompt/en")
        print(f"\n--it--> {response.json()}")
        assert response is not None
        assert response.status_code == 200
        assert "conversation" in response.json()

    def test_post_new_instruction(self):
        pr= PromptRequest(prompt_key="test_prompt", prompt_locale="en", prompt_content="You are an helpful assistant")
        response = self.client.post(get_config().api_route + "/a/prompts/",json = pr.model_dump())
        assert response is not None
        assert response.status_code == 200
        response = self.client.get(get_config().api_route + "/a/prompts/test_prompt/en")
        print(f"\n--it--> {response.json()}")
        assert "helpful assistant" in response.json()



    def test_prompt_for_ui(self):
        response = self.client.get( get_config().api_route + "/a/prompts/en").content.decode()
        assert response is not None
        print(f"\n--it--> {response}")
        assert response.find("question based") > 0
        response =  self.client.get( get_config().api_route + "/a/prompts/fr").content.decode()
        assert response is not None
        print(f"\n--it--> {response}")
        assert response.find("utilisateur") > 0
        response = self.client.get( get_config().api_route + "/a/prompts/es").content.decode()
        assert response is not None
        print(f"\n--it--> {response}")
        assert response.find("siguiente") > 0
        
if __name__ == '__main__':
    unittest.main()