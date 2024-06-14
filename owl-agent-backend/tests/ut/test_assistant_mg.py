import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
import yaml,json
from yaml import BaseLoader
from athena.llm.assistants.assistant_mgr import get_assistant_manager, OwlAssistantEntity
from importlib import import_module

class TestAssistantsManager(unittest.TestCase):
    """
    Validate the assistant manager manages assistant meta data and can create assistant runtime to support a conversation.
    """
    
    def test_owl_assistant(self):
        oa = OwlAssistantEntity()
        assert oa.assistant_id
        oa_json = oa.model_dump()
        print(oa_json)
        more_oas= {}
        more_oas[oa.assistant_id]=oa_json
        print(yaml.dump(json.dumps(more_oas)))
        print(yaml.dump(more_oas))
    
    def test_yaml_def(self):
        yaml_definition = """
        default_assistant:
            name: default_assistant
            assistant_id: 8970e5f2-2542-40c7-b2e5-2d578e11168c
            class_name: athena.llm.assistants.BaseAssistant.BaseAssistant
            description: A default assistant to do simple LLM call
        """
        obj = yaml.load(yaml_definition, BaseLoader)  # return a dict
        oad = obj["default_assistant"] 
        oa = OwlAssistantEntity.model_validate(oad)  # now it is a OwlAssistant
        print(oa.description)
        module_path, class_name = oa.class_name.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        owl_assistant= klass()
        print(owl_assistant.invoke("a test"))
    
    def test_define_new_assistant(self):
        mgr=get_assistant_manager()
        oa = OwlAssistantEntity()
        oa.name= "base_assistant"
        oa.description="a base assistant for demo"
        oa.class_name="athena.llm.assistants.BaseAssistant.BaseAssistant"
        oad_id=mgr.save_assistant(oa)
        assert oad_id
        oa2 = mgr.get_assistant_by_id(oad_id)
        assert oa2
        assert "base assistant" in oa2.description
    
    def test_validate_loading_from_yaml_file(self):
        mgr=get_assistant_manager()
        all = mgr.get_assistants()
        assert all
        print(f"--> {all}")
        l = []
        for e in all.values():
            print(e)
            l.append(OwlAssistantEntity.model_validate(e))
       
        print(str(l))
        
    def test_get_assistant_by_name(self):
        # Should get the default assistant definition
        mgr=get_assistant_manager()
        assert mgr
        p=mgr.get_assistant_by_name("default_assistant")
        assert p
        assert "default assistant" in p.description
        


if __name__ == '__main__':
    unittest.main()
