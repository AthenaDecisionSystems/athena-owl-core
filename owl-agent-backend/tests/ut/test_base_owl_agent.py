import unittest, sys, os
sys.path.append('./src')
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("../../.env")
from athena.llm.base_owl_agent  import BaseOwlAgent
from athena.routers.dto_models import ConversationControl, ChatRecord

class TestBaseOwlAgent(unittest.TestCase):

    def test_empty_chat_history(self):
        agent = BaseOwlAgent()
        cc = ConversationControl()
        ch = agent.build_chat_history_for_llm(cc)
        assert ch == []

    def test_chat_history(self):
        agent = BaseOwlAgent()
        cc = ConversationControl()
        cc.chat_history=[ChatRecord(role="human",content= "Hi I am bob lazard, I am born on June 27 1902"), 
                          ChatRecord(role="assistant", content="Hi how can I help you?")]
        ch = agent.build_chat_history_for_llm(cc)
        print(ch)
        assert len(ch) == 2