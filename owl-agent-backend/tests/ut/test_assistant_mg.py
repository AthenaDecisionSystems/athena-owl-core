from dotenv import load_dotenv
load_dotenv()
import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"

module_path = "./src"
sys.path.append(os.path.abspath(module_path))
import yaml,json
from yaml import BaseLoader
from athena.llm.assistants.assistant_mgr import get_assistant_manager, OwlAssistantEntity
from athena.routers.dto_models import ConversationControl
from typing import Optional 

class TestAssistantsManager(unittest.TestCase):
    """
    Validate that the assistant manager manages assistant entity and can create assistant executor to support a conversation.
    """
    
    def test_owl_assistant_entity_serialization(self):
        print("\n\n test_owl_assistant_entity_serialization\n")
        # Use the default setting of the OwlAssistantEntity
        oa = OwlAssistantEntity()
        assert oa.assistant_id
        oa_dict = oa.model_dump()
        assert oa_dict["class_name"] == "athena.llm.assistants.BaseAssistant.BaseAssistant"
        oas= {}
        oas[oa.assistant_id]=oa_dict
        oas_json_str=json.dumps(oas)
        assert "BaseAssistant.BaseAssistant" in oas_json_str
        # to map to a yaml
        oas_yaml_str=yaml.dump(json.dumps(oas))
        print(oas_yaml_str)
        assert isinstance(oas_yaml_str,(str))
        yaml_str=yaml.dump(oas)
        print(f"Yaml view:\n {yaml_str}\n")
 
    
    def test_yaml_definition_to_entity(self):
        print("\n\n test_yaml_definition_to_entity\n")
        yaml_definition = """
        default_assistant:
            name: default_assistant
            assistant_id: 8970e5f2-2542-40c7-b2e5-2d578e11168c
            class_name: athena.llm.assistants.BaseAssistant.BaseAssistant
            description: A default assistant to do simple LLM call
            agents:
                - base_agent
        """
        obj = yaml.load(yaml_definition, BaseLoader)  # return a dict
        oad = obj["default_assistant"] 
        oa = OwlAssistantEntity.model_validate(oad)  # now it is a OwlAssistant
        assert len(oa.agents) == 1
        assert oa.name == "default_assistant"

    
    def test_define_new_assistant_delete_it(self):
        print("\n\n test_define_new_assistant_delete_it\n")
        mgr=get_assistant_manager()
        oa = OwlAssistantEntity()
        oa.name= "test_assistant"
        oa.description="a test base assistant for demo"
        oa.class_name="athena.llm.assistants.BaseGraphAssistant.BaseGraphAssistant"
        os.agents= ["base_agent"]
        oad_id=mgr.save_assistant(oa)
        assert oad_id
        oa2 = mgr.get_assistant_by_id(oad_id)
        assert oa2
        print(oa2)
        assert "test base assistant" in oa2.description
        mgr.delete_assistant(oad_id)
    
    def test_validate_loading_all_assistants(self):
        print("\n\n test_validate_loading_all_assistants\n")
        mgr=get_assistant_manager()
        all = mgr.get_assistants()
        assert all
        assert len(all) > 1
        l = []
        for e in all.values():
            l.append(OwlAssistantEntity.model_validate(e))
        print(str(l))
        
    def test_get_assistant_by_name(self):
        print("\n\n test_get_assistant_by_name\n")
        # Should get the default assistant definition
        mgr=get_assistant_manager()
        assert mgr
        p=mgr.get_assistant_by_name("Base openai assistant")
        assert p
        assert "default assistant" in p.description
        
    def test_calling_base_agent(self):
        print("\n\n test_calling_base_agent\n")
        mgr = get_assistant_manager()
        oae: Optional[OwlAssistantEntity] = mgr.get_assistant_by_id("base_openai_tool_assistant")
        if oae is None:
            raise ValueError("Base assistant not found")
        base_assistant = mgr.build_assistant(oae.assistant_id,"en")
        assert base_assistant
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = base_assistant.send_conversation(cc)
        assert rep
        print(rep)
        
    def _calling_mistral_ollama_agent(self):
        # THIS TEST FAILS because the langchain api does not have a bind_tools method on ollama chat. 
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
