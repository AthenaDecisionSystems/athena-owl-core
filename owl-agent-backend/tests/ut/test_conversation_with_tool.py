import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()

from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestConversationWithTool(unittest.TestCase):
    """
    Validate conversation with tool to get news from search
    """    
    def test_conversation_with_chain_tool_agent(self):
        cc = ConversationControl()
        cc.agent_id="openai_tool_chain"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="What is Athena Decision Systems?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.chat_history
        assert rep.message
        print(f"agent --> {rep}")        
    
    def test_conversation_with_tool_graph_agent(self):
        cc = ConversationControl()
        cc.agent_id="base_tool_graph_agent"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="What is Athena Decision Systems?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.chat_history
        assert rep.message
        print(f"agent --> {rep}")
        
if __name__ == '__main__':
    unittest.main()