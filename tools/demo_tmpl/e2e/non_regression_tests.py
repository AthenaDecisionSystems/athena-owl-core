"""
a bunch of calls to the backend servers to validate the major functions
"""
from pydantic import BaseModel
import unittest
import requests

import requests

IBU_BASE_URL="http://localhost:8000/api/v1"
PROMPT_REF="default_prompt"
ASSISTANT_REF="base_graph_assistant"
AGENT_REF="openai_tool_chain"
TOOL_REF="tavily"

class OwlAssistantEntity(BaseModel):
    """
    Entity to persist data about a OwlAssistant
    """
    assistant_id: str = ""
    name: str = ""
    description: str = "A default assistant to do simple LLM calls"
    class_name : str = "athena.llm.assistants.BaseAssistant.BaseAssistant"
    agent_id: str = ""
 
class TestHappyPathScenario(unittest.TestCase):
  
    def test_verify_health(self):
        print("\n--> Validate the Web App is Alive\n")
        rep = requests.get(IBU_BASE_URL + "/health", timeout = 10).content.decode()
        assert "Alive" in rep
        print(f"@@@> {rep} -> good!")


    def test_perform_general_knowledge_query_legacy(self):
        print("\n--> Validate Basic Query to LLM\n")
        data='{  "locale": "en",\
          "query": "can you give me some information about Athena Decision Systems?",\
          "assistant_id": "' + ASSISTANT_REF + '",  \
          "user_id" : "remote_test", \
          "chat_history": [],\
          "thread_id" : "1" \
        }'
        print(data)
        rep = requests.post(IBU_BASE_URL + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}, timeout = 10).content.decode()
        print(f"@@@> {rep}")
        assert rep   

  

    def test_validate_access_to_prompt_entity_api(self):
      print("\n--> Get IBU default prompt\n")
      rep = requests.get(IBU_BASE_URL + f"/a/prompts/{PROMPT_REF}/en").content.decode()
      print(f"\n@@@> {rep}")
      assert "conversation" in rep
  
      
    def test_validate_base_assistant_entity_api(self):
      print("\n--> Get base assistant entity\n")
      resp = requests.get(IBU_BASE_URL + f"/a/assistants/{ASSISTANT_REF}")
      a_str= resp.content.decode()
      print(f"\n@@@> {a_str}")
      ae = OwlAssistantEntity.model_validate_json(json_data=a_str)
      print(f"\n@@@> {ae}")
      #print(obj["agent_id"])
      return ae
      

    def test_validate_agent_entity_api(self):
      print("\n--> Get base agent entity\n")
      rep = requests.get(IBU_BASE_URL + "/a/agents/"+AGENT_REF).content.decode()
      print(f"\n@@@> {rep}")
      return rep

    def test_validate_tools_entity_api(self):
      print("\n--> Get IBU loan tool entity\n")
      rep = requests.get(IBU_BASE_URL + "/a/tools/"+TOOL_REF).content.decode()
      print(f"\n@@@> {rep}")
      return rep

    # ADD HERE your own scenario test


  
if __name__ == "__main__":
    print("################ Non Regression Tests ##############")
    unittest.main()
  
  






