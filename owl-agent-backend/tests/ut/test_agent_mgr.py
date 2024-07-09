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
        oae = OwlAgentEntity()
        assert oae.agent_id
        oae_json = oae.model_dump()
        print(oae_json)
        more_oas= {}
        more_oas[oae.agent_id]=oae_json
        print(yaml.dump(json.dumps(more_oas)))
        print(yaml.dump(more_oas))
        
    def test_create_get_by_id_delete_agent_entity(self):
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
        mgr = get_agent_manager()
        l = mgr.get_agents()
        assert l
        assert len(l) >= 2
    
    def test_get_assistant_by_name(self):
        # Should get the default assistant definition
        mgr=get_agent_manager()
        assert mgr
        p=mgr.get_agent_by_name("open_ai_gpt35")
        assert p
        assert "openai" in p.description
        
    def test_read_tool_list(self):
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