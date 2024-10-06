import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
import yaml,json
from yaml import BaseLoader
from langchain.tools import StructuredTool
from athena.llm.tools.tool_mgr import get_tool_entity_manager, OwlToolEntity
from athena.llm.tools.demo_tools import DemoToolInstanceFactory
from importlib import import_module

class TestToolManager(unittest.TestCase):
    
    def test_1_owl_tool_entity_definition(self):
        " Test to understand model dumps ..."
        oae = OwlToolEntity()
        oae.tool_id="hello_fct"
        oae.tool_fct_name="hello"
        oae_as_dict = oae.model_dump()
        assert type(oae_as_dict) == dict
        more_oas= {}
        more_oas[oae.tool_id]=oae
        assert type(more_oas) == dict
        try:
            alist = json.dumps(more_oas)
        except Exception as e:
            print("this is expected as  OwlToolEntity is not JSON serializable")
        more_oas= {}
        more_oas[oae.tool_id]=oae_as_dict
        alist = json.dumps(more_oas)
        print(yaml.dump(alist))
        print(yaml.dump(more_oas))
    
    def test_2_get_all_predefined_tools(self):
        mgr = get_tool_entity_manager()
        l = mgr.get_tools()
        assert l
        assert len(l) >= 2
        for te in l:
            assert l[te].tool_id

    
    def test_crd_operations(self):
        mgr = get_tool_entity_manager()
        entity = OwlToolEntity()
        entity.tool_fct_name = "tool_test"
        tid=mgr.save_tool(entity)
        assert tid
        e2 = mgr.get_tool_by_id(tid)
        assert e2
        rep = mgr.delete_tool(tid)
        assert "Done" in rep
        try:
            e3 = mgr.get_tool_by_id(tid)
        except Exception as e:
            print(e)
    
    def test_get_tool_by_function_name(self):
        mgr = get_tool_entity_manager()
        ote= mgr.get_tool_by_function_name("query_crm_backend")
        assert ote
        assert ote.tool_id
        assert ote.tool_fct_name == "query_crm_backend"

    def test_build_tool_intance_given_its_id(self):
        mgr = get_tool_entity_manager()
        ote= mgr.get_tool_by_id("query_crm")
        otes=[ote]
        factory = DemoToolInstanceFactory()
        tool_instances=factory.build_tool_instances(otes)
        print(tool_instances)
        assert isinstance(tool_instances[0],StructuredTool)
        st : StructuredTool = tool_instances[0]
        assert st.name == "query_crm_backend"
    
if __name__ == '__main__':
    unittest.main()