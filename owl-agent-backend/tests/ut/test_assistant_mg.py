import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
import yaml
from yaml import BaseLoader
from athena.llm.assistants.assistant_mgr import get_assistant_manager, OwlAssistant
from importlib import import_module

class TestAssistantsManager(unittest.TestCase):
    
    
    def test_owl_assistant(self):
        oa = OwlAssistant()
        assert oa.assistant_id
        oa_json = oa.model_dump()
        print(oa_json)
        print(yaml.dump(oa_json))
    
    def test_yaml_def(self):
        definition = """
        owl_assistant:
            name: default_assistant
            assistant_id: 8970e5f2-2542-40c7-b2e5-2d578e11168c
            class_name: athena.llm.assistants.BaseAssistant.BaseAssistant
            description: A default assistant to do simple LLM call
        """
        obj = yaml.load(definition, BaseLoader)  # return a dict
        oad = obj["owl_assistant"] 
        oa = OwlAssistant.model_validate(oad)  # now it is a OwlAssistant
        print(oa.description)
        module_path, class_name = oa.class_name.rsplit('.',1)
        mod = import_module(module_path)
        klass = getattr(mod, class_name)
        owl_assistant= klass()
        print(owl_assistant.invoke("a test"))
        
    def _get_default_assistant(self):
        # Should get the default assistant definition
        mgr=get_assistant_manager()
        assert mgr
        p=mgr.get_assistant_by_name("default_assistant")
        assert p
        


if __name__ == '__main__':
    unittest.main()
