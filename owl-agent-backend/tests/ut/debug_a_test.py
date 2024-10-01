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
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("watson_llama_3_70_agent")
        if oae is None:
            raise ValueError("agent not found")
        owl_agent_runner =  mgr.build_agent_runner(oae.agent_id,"en")
        assert owl_agent_runner
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = owl_agent_runner.send_conversation(cc)
        assert rep.messages
        print(rep.messages[0].content)
        trace = owl_agent_runner.get_conversation_trace(cc.thread_id)
        print("-"*40)
        print(f"Trace = {trace}")
        print("-"*40)


if __name__ == '__main__':
    unittest.main()