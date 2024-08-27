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
    def test_base_agent_with_openai_tool_chain(self):
        """
        Validate conversation with history. Baseagent uses openai agent with a prompt with chat history
        """
        cc = ConversationControl()
        cc.agent_id="base_openai_tool_agent"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        
        print(f"agent --> {rep.message}") 
        
        cc.chat_history=rep.chat_history
        cc.query="What is my last name?"
        print(f"Continue the conversation with  --> {cc}") 
        rep = get_or_start_conversation(cc)
        print(f"agent --> {rep}")
        assert rep
        assert rep.chat_history
        assert rep.message
        assert "last name is TheBuilder" in rep.message
        
    def test_conversation_with_base_tool_agent(self):
        cc = ConversationControl()
        cc.agent_id="base_openai_tool_agent"
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