import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()

from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestConversation(unittest.TestCase):
    
    def _validate_history(self, cc : ConversationControl):
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.messages
        
        print(f"\n\nagent --> {rep}") 
        
        cc.chat_history=rep.chat_history
        cc.query="What is my last name?"
        print(f"Continue the conversation with  --> {cc}") 
        rep = get_or_start_conversation(cc)
        print(f"\n\nagent --> {rep}") 
        assert "last name is TheBuilder" in rep.messages[0].content
        
        
    def test_base_agent_openai_chain_with_chat_history(self):
        """
        Validate conversation with history. Baseagent uses openai agent with a prompt with chat history
        """
        print("\n------- test_base_agent_with_chat_history")
        cc = ConversationControl()
        cc.agent_id="openai_chain_agent"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        self._validate_history(cc) 
 
    def _test_conv_anthropic_base_agent(self):
        print("\n------- test_conv_anthropic_base_agent")
        cc = ConversationControl()
        cc.agent_id="anthropic_claude_3_base"
        cc.user_id="unit_test"
        cc.thread_id="2"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        self._validate_history(cc)
        
    def test_conv_openai_chain_base_graph_agent(self):
        print("\n------- test_conv_openai_base_graph_agent")
        cc = ConversationControl()
        cc.agent_id="openai_graph_agent"
        cc.user_id="unit_test"
        cc.thread_id="3"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        self._validate_history(cc)
    
    def test_thread_id_is_set_by_backend(self):
        print("\n------- test_thread_id_is_set_by_backend")
        cc = ConversationControl()
        cc.agent_id="openai_chain_agent"
        cc.user_id="unit_test"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.messages
        assert rep.thread_id
        
        print(f"\n\nagent --> {rep}") 
        
if __name__ == '__main__':
    unittest.main()