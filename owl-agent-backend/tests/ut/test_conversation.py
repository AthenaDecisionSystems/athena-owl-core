import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("../../.env")
from athena.llm.agent_openai import OpenAIClient
from athena.routers.dto_models import ConversationControl, ModelParameters
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage

class TestConversation(unittest.TestCase):
    """
    Validate conversation with history
    """
    
    def test_with_chat_history(self):
        
        cc = ConversationControl()
        cc.modelParameters = ModelParameters()
        cc.modelParameters.prompt_ref = "default_prompt"
        cc.chat_history = [
            AIMessage(content="Hello! How can I assist you today?"),
            HumanMessage(content="Hi, I'm Bob and my last name is TheBuilder.")
        ]
        cc.query="What is my last name?"
        agent = OpenAIClient()
        rep = agent.send_conversation(cc)
        assert rep
        assert rep.message
        assert "last name is TheBuilder" in rep.message
        cc.reset=True
        cc.query="Can you give me my last name?"
        rep = agent.send_conversation(cc)
        print(rep)
    
