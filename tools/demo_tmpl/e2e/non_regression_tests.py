"""
a bunch of calls to the backend servers to validate the major functions
"""
from pydantic import BaseModel

import requests

IBU_BASE_URL="http://localhost:8000/api/v1"
PROMPT_REFERENCE="ibu_loan_prompt"
ASSISTANT_REF="ibu_assistant"

class OwlAssistantEntity(BaseModel):
    """
    Entity to persist data about a OwlAssistant
    """
    assistant_id: str = ""
    name: str = ""
    description: str = "A default assistant to do simple LLM calls"
    class_name : str = "athena.llm.assistants.BaseAssistant.BaseAssistant"
    agent_id: str = ""
    
def verify_health(base_url):
  print("\n--> Validate the Web App is Alive\n")

  rep = requests.get(base_url + "/health").content.decode()
  print(f"\n@@@> {rep}")
  assert "Alive" in rep
  

def validate_access_to_ibu_prompt(base_url):
  print("\n--> Get IBU default prompt\n")
  rep = requests.get(base_url + f"/a/prompts/{PROMPT_REFERENCE}/en").content.decode()
  print(f"\n@@@> {rep}")
  assert "bank" in rep
  
  
def validate_ibu_assistant(base_url):
  print("\n--> Get IBU Loan assistant entity\n")
  resp = requests.get(base_url + f"/a/assistants/{ASSISTANT_REF}")
  a_str= resp.content.decode()
  print(f"\n@@@> {a_str}")
  ae = OwlAssistantEntity.model_validate_json(json_data=a_str)
  print(f"\n@@@> {ae}")
  #print(obj["agent_id"])
  return ae
  

def validate_ibu_agent(base_url,agent_id):
  print("\n--> Get IBU loan agent entity\n")
  rep = requests.get(base_url + "/a/agents/"+agent_id).content.decode()
  print(f"\n@@@> {rep}")
  return rep

def validate_ibu_tools(base_url, tool_id):
  print("\n--> Get IBU loan tool entity\n")
  rep = requests.get(base_url + "/a/tools/"+tool_id).content.decode()
  print(f"\n@@@> {rep}")
  return rep

def validate_get_credit_score(base_url, fn: str, ln: str):
  print("\n--> Get information about one of the client\n")
  data='{ "locale": "en",\
    "query": "What is the credit score of Robert Smith using IBU loan database?",\
    "assistant_id": "ibu_assistant", \
    "thread_id" : "1", \
    "user_id" : "a_test_user"\
  }'
  rep = requests.post(base_url + "/c/generic_chat", data=data, headers = {"Content-Type": "application/json"}).content.decode()
  print(f"\n@@@> {rep}")
  return rep


  
if __name__ == "__main__":
  print("################ Non Regression Tests ##############")
  verify_health(IBU_BASE_URL)
  validate_access_to_ibu_prompt(IBU_BASE_URL)
  ae=validate_ibu_assistant(IBU_BASE_URL)
  validate_ibu_agent(IBU_BASE_URL,ae.agent_id)
  validate_ibu_tools(IBU_BASE_URL,"ibu_client_by_name")
  validate_get_credit_score(IBU_BASE_URL,"Robert", "Smith")
  






