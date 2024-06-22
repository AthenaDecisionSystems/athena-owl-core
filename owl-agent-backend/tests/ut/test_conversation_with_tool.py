import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
from athena.llm.agent_openai import OpenAIClient
from athena.routers.dto_models import ConversationControl, ModelParameters
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestConversationWithTool(unittest.TestCase):
    """
    Validate conversation with tool to get news from search
    """
    def test_base_assistant_with_chat_history(self):
        """
        Validate conversation with history. BaseAssistant uses openai agent with a prompt with chat history
        """
        cc = ConversationControl()
        cc.assistant_id="base_openai_tool_assistant"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="Hi, I'm Bob and my last name is TheBuilder."
        
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        
        print(f"Assistant --> {rep.message}") 
        
        cc.chat_history=rep.chat_history
        cc.query="What is my last name?"
        print(f"Continue the conversation with  --> {cc}") 
        rep = get_or_start_conversation(cc)
        print(f"Assistant --> {rep}")
        assert rep
        assert rep.chat_history
        assert rep.message
        assert "last name is TheBuilder" in rep.message
        
    def test_conversation_with_base_tool_assistant(self):
        cc = ConversationControl()
        cc.assistant_id="base_openai_tool_assistant"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="What is Athena Decision Systems?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.chat_history
        assert rep.message
        print(f"Assistant --> {rep}")        
        
if __name__ == '__main__':
    unittest.main()