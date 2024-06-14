import unittest, sys, os
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))

from athena.llm.assistants.assistant_mgr import get_assistant_manager
from importlib import import_module

class TestBaseOwlAssistant(unittest.TestCase):
    """
    Simulate a conversation flow using the base assistant
    """
    
    def test_calling_base_agent(self):
        mgr = get_assistant_manager()
        oae = mgr.get_assistant_by_name("default_assistant")
        default_assistant = mgr.get_or_build_assistant(oae.assistant_id)
        assert default_assistant
        # Default assistant has one LLM and one tool to search the web
        rep = default_assistant.invoke("what is langgraph?")
        print(rep)
        
if __name__ == '__main__':
    unittest.main()