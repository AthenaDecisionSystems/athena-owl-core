import os, sys
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgent
import yaml, json

oae = OwlAgent()
oae.tools=["tool_1","tool_2"]
oae_json = oae.model_dump()
print(oae_json)
more_oas= {}
more_oas[oae.agent_id]=oae_json
print(yaml.dump(json.dumps(more_oas)))
print(yaml.dump(more_oas))

yaml_definition="""
default_agent:
  agent_id: 9b4d211e-4822-42d0-b4ff-d5fa9941476c
  class_name: athena.llm.agents.agent_openai.OpenAIClient
  description: ''
  modelName: 'gpt-4o'
  name: 'openai_gpt4'
  prompt_ref: default_prompt
  temperature: 0
  tools:
  - tool_1
  - tool_2
  top_k: 1
  top_p: 1
"""

obj = yaml.load(yaml_definition, yaml.BaseLoader)  # return a dict
oad = obj["default_agent"] 
oa = OwlAgent.model_validate(oad)
print(oa)


