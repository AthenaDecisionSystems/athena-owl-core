import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
import yaml,json
from typing import Optional 
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgentEntity

class TestAgentsManager(unittest.TestCase):
    """
    Validate CRUD on agent entity and factory of agent instance
    """



    def test_owl_agent_entity_to_json_to_yaml(self):
        print("\n\n >>> test_owl_agent_entity_to_json_to_yaml\n")
        # Use the default setting of the OwlAssistantEntity
        oae = OwlAgentEntity()
        assert oae.agent_id
        oae_dict = oae.model_dump()
        assert oae_dict["class_name"] == "athena.llm.agents.agent_openai.OpenAIClient"
        oaes= {}
        oaes[oae.agent_id]=oae_dict
        oaes_json_str=json.dumps(oaes)
        assert "OpenAIClient" in oaes_json_str
        # to map to a yaml
        oaes_yaml_str=yaml.dump(json.dumps(oaes))
        print(oaes_yaml_str)
        assert isinstance(oaes_yaml_str,(str))
        yaml_str=yaml.dump(oaes)
        print(f"Yaml view:\n {yaml_str}\n")
 
        
    def test_create_get_by_id_delete_agent_entity(self):
        print("\n\n >>> test_create_get_by_id_delete_agent_entity\n")
        oae = OwlAgentEntity()
        oae.name="test_agent"
        oae.description="an openai based agent"
        mgr = get_agent_manager()
        oad_id=mgr.save_agent(oae)
        assert oad_id
        oa2 = mgr.get_agent_by_id(oad_id)
        assert oa2
        assert "openai" in oa2.description
        assert "test_agent" in oa2.name
        rep = mgr.delete_agent(oad_id)
        assert "Done" == rep
    
    def get_all_predefined(self):
        print("\n\n >>> get_all_predefined\n")
        mgr = get_agent_manager()
        l = mgr.get_agents()
        assert l
        assert len(l) >= 2
    
    def test_get_agent_by_name(self):
        # Should get the default agent definition
        print("\n\n >>> test_get_agent_by_name\n")
        mgr=get_agent_manager()
        assert mgr
        p=mgr.get_agent_by_name("open_ai_gpt35")
        assert p
        assert "openai" in p.description
        
    def test_read_tool_list(self):
        print("\n\n >>> test_read_tool_list\n")
        mgr=get_agent_manager()
        p=mgr.get_agent_by_name("anthropic_claude_3")
        assert type(p) == OwlAgentEntity
        assert p.tools
        print(p)
        
    def _test_calling_fake_agent(self):
        mgr = get_agent_manager()
        oae: Optional[OwlAgentEntity] = mgr.get_agent_by_id("fake_agent")
        if oae is None:
            raise ValueError("Fake agent not found")
        fake_assistant = mgr.build_agent(oae.agent_id,"en")
        assert fake_assistant
        rep = fake_assistant.invoke("what is langgraph?")
        assert "one" == rep
        rep = fake_assistant.invoke("really?")
        assert "two" == rep
    
if __name__ == '__main__':
    unittest.main()