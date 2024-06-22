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
        assert rep.message
        
        print(f"\n\nAssistant --> {rep}") 
        
        cc.chat_history=rep.chat_history
        cc.query="What is my last name?"
        print(f"Continue the conversation with  --> {cc}") 
        rep = get_or_start_conversation(cc)
        print(f"\n\nAssistant --> {rep}") 
        assert "last name is TheBuilder" in rep.message
        
        
    def test_base_assistant_with_chat_history(self):
        """
        Validate conversation with history. BaseAssistant uses openai agent with a prompt with chat history
        """
        print("\n------- test_base_assistant_with_chat_history")
        cc = ConversationControl()
        cc.assistant_id="base_openai_assistant"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        self._validate_history(cc)
       

    
    def test_start_conversation_with_base_openai_assistant(self):
        print("\n------- test_start_conversation_with_base_openai_assistant")
        cc = ConversationControl()
        cc.assistant_id="base_openai_assistant"
        cc.user_id="unit_test"
        cc.thread_id="2"
        cc.chat_history=[]
        cc.query="What is Athena Decision Systems?"
        rep = get_or_start_conversation(cc)
        assert rep
        print(f"Assistant --> {rep}")   
        # the response should be generic, see with tool to get a real better answer     
 
    def test_conv_anthropic_base_assistant(self):
        print("\n------- test_conv_anthropic_base_assistant")
        cc = ConversationControl()
        cc.assistant_id="claude3_assistant"
        cc.user_id="unit_test"
        cc.thread_id="2"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        self._validate_history(cc)
        
    def _conv_openai_base_graph_assistant(self):
        print("\n------- test_conv_openai_base_graph_assistant")
        cc = ConversationControl()
        cc.assistant_id="base_graph_assistant"
        cc.user_id="unit_test"
        cc.thread_id="3"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        self._validate_history(cc)
        
if __name__ == '__main__':
    unittest.main()