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
    
    def test_conversation_with_base_tool_assistant(self):
        cc = ConversationControl()
        cc.assistant_id="base_tool_assistant"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="What is Athena Decision Systems?"
        rep = get_or_start_conversation(cc)
        assert rep
        print(f"Assistant --> {rep.message}")        
        
if __name__ == '__main__':
    unittest.main()