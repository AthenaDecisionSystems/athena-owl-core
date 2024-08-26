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
