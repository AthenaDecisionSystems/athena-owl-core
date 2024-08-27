"""
code to isolate a test if needed
"""
import unittest, sys, os
from dotenv import load_dotenv
load_dotenv()
# Order of the following code is important to make the tests working
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
import yaml,json
from typing import Optional 
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgent
from athena.routers.dto_models import ConversationControl


class TestAgentsManager(unittest.TestCase):
    def test_calling_base_graph_agent(self):
        print("\n\n test_calling_base_graph_agent\n")
        mgr = get_agent_manager()
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("openai_graph_agent")
        if oae is None:
            raise ValueError("Base agent not found")
        base_assistant =  mgr.build_agent_runner(oae.agent_id,"en")
        assert base_assistant
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = base_assistant.send_conversation(cc)
        assert rep
        print(rep)

if __name__ == '__main__':
    unittest.main()