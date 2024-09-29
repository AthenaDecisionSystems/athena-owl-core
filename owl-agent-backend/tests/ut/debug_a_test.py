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
from langchain_core.messages import AIMessage

class TestAgentsManager(unittest.TestCase):
    def test_calling_base_graph_agent(self):
        print("\n\n debug a test \n")
        mgr = get_agent_manager()
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("base_tool_graph_agent")
        if oae is None:
            raise ValueError("agent not found")
        owl_agent =  mgr.build_agent_runner(oae.agent_id,"en")
        assert owl_agent
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = owl_agent.send_conversation(cc)
        assert rep.messages
        print(rep)
        trace = owl_agent.get_conversation_trace(cc.thread_id)
        print("-"*40)
        print( trace)
        print("-"*40)


if __name__ == '__main__':
    unittest.main()