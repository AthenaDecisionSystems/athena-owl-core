import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()

from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation, get_conversation_trace_given_thread_id

"""
Validate conversation with tool with one or two tests to better debug code
"""    
class TestConversationWithTool(unittest.TestCase):
  
    
    def test_conversation_with_tool_graph_agent(self):
        cc = ConversationControl()
        cc.agent_id="base_tool_graph_agent"
        cc.user_id="unit_test"t
        cc.thread_id="T1"
        cc.chat_history=[]
        cc.query="What is Athena Decision Systems?"
        rep = get_or_start_conversation(cc)  # rep is a responscontrol object
        assert rep
        print(f"rep --> {rep}")
        assert rep.chat_history
        assert rep.messages
        print(f"history --> {rep.chat_history}")
        assert "Athena Decision Systems" in rep.messages[0].content
        trace = get_conversation_trace_given_thread_id("T1")
        print(f"agent's trace --> {trace}")

if __name__ == '__main__':
    unittest.main()