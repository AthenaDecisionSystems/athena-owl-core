import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
import yaml,json
from yaml import BaseLoader
from athena.llm.assistants.assistant_mgr import get_assistant_manager, OwlAssistantEntity
from athena.routers.dto_models import ConversationControl
from typing import Optional 

class TestAssistantsManager(unittest.TestCase):
    """
    Validate the assistant manager manages assistant entity and can create assistant runtime to support a conversation.
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

    
    def test_define_new_assistant(self):
        mgr=get_assistant_manager()
        oa = OwlAssistantEntity()
        oa.name= "test_assistant"
        oa.description="a test base assistant for demo"
        oa.class_name="athena.llm.assistants.BaseGraphAssistant.BaseGraphAssistant"
        oad_id=mgr.save_assistant(oa)
        assert oad_id
        oa2 = mgr.get_assistant_by_id(oad_id)
        assert oa2
        assert "test base assistant" in oa2.description
        mgr.delete_assistant(oad_id)
    
    def test_validate_loading_from_yaml_file(self):
        mgr=get_assistant_manager()
        all = mgr.get_assistants()
        assert all
        print(f"--> {all}")
        l = []
        for e in all.values():
            l.append(OwlAssistantEntity.model_validate(e))
       
        print(str(l))
        
    def test_get_assistant_by_name(self):
        # Should get the default assistant definition
        mgr=get_assistant_manager()
        assert mgr
        p=mgr.get_assistant_by_name("Base assistant")
        assert p
        assert "base assistant" in p.description
        
    def test_calling_base_agent(self):
        mgr = get_assistant_manager()
        oae: Optional[OwlAssistantEntity] = mgr.get_assistant_by_name("Base assistant")
        if oae is None:
            raise ValueError("Base assistant not found")
        base_assistant = mgr.build_assistant(oae.assistant_id,"en")
        assert base_assistant
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = base_assistant.send_conversation(cc)
        print(rep)
        
    def _calling_mistral_ollama_agent(self):
        mgr = get_assistant_manager()
        oae: Optional[OwlAssistantEntity] = mgr.get_assistant_by_id("mistral_tool_assistant")
        if oae is None:
            raise ValueError("mistral_tool_assistant not found")
        base_assistant = mgr.build_assistant(oae.assistant_id,"en")
        assert base_assistant
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = base_assistant.send_conversation(cc)
        print(rep)

if __name__ == '__main__':
    unittest.main()
