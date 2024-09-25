import unittest, sys, os
import yaml,json
from yaml import BaseLoader
from langchain.tools import StructuredTool
from athena.owl.tools.tool_mgr import get_tool_entity_manager, OwlToolEntity
from importlib import import_module

class TestToolManager(unittest.TestCase):
    
    def test_owl_tool_entity_definition(self):
        oae = OwlToolEntity()
        oae.tool_fct_name="hello"
        oae_json = oae.model_dump()
        more_oas= {}
        more_oas[oae.tool_id]=oae_json
        print(yaml.dump(json.dumps(more_oas)))
        print(yaml.dump(more_oas))
    
    def test_get_all_predefined_tools(self):
        mgr = get_tool_entity_manager("tests/config/tools.yaml")
        l = mgr.get_tools()
        assert l
        assert len(l) >= 1
        print(l)
    
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
    
if __name__ == '__main__':
    unittest.main()