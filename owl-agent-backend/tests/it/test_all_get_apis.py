import requests
import unittest
import json

IBU_BASE_URL="http://localhost:8002/api/v1"
class TestAPIs(unittest.TestCase):


    def test_get_all_agents(self):
        print("\n--> Get All agents\n")
        rep = requests.get(IBU_BASE_URL + "/a/agents")
        list_of_dict = json.loads(rep.content.decode())
        assert type(list_of_dict)== list
        assert "openai_chain_agent" == list_of_dict[0]["agent_id"]
        print(list_of_dict[0])


    def test_get_all_prompts(self):
        print("\n--> Get All prompts\n")
        rep = requests.get(IBU_BASE_URL + "/a/prompts")
        list_of_dict = json.loads(rep.content.decode())
        print(list_of_dict)
        assert "default_prompt" == list_of_dict[0]["prompt_id"]

    def test_get_all_tools(self):
        print("\n--> Get All tools\n")
        rep = requests.get(IBU_BASE_URL + "/a/tools")
        list_of_dict = json.loads(rep.content.decode())
        print(list_of_dict)
        assert "tavily" == list_of_dict[0]["tool_id"]


if __name__ == '__main__':
    unittest.main()