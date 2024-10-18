import unittest
import sys, os, json
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()

from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

"""
Test at the conversation manager service level, different agents with or without tools

This is the bigger non-regression test.
"""
class TestConversation(unittest.TestCase):
     
    def define_conversation_control(self,agent_id:str, query: str, thread_id: str) -> str:
        cc = ConversationControl()
        cc.agent_id=agent_id
        cc.user_id="remote_test"
        cc.thread_id=thread_id
        cc.chat_history=[]
        cc.query=query
        return cc
        
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
        cc = self.define_conversation_control("openai_chain_agent","Hi, I'm Bob and my last name is TheBuilder.", "T1")
        self._validate_history(cc) 
 
    def test_conv_anthropic_base_agent(self):
        print("\n------- test_conv_anthropic_base_agent")
        cc = self.define_conversation_control("anthropic_claude_3_base","Hi, I'm Bob and my last name is TheBuilder.", "T12")
        self._validate_history(cc)
        
    def test_conv_openai_chain_base_graph_agent(self):
        print("\n------- test_conv_openai_base_graph_agent")
        cc = self.define_conversation_control("openai_graph_agent","Hi, I'm Bob and my last name is TheBuilder.", "T3")
        self._validate_history(cc)
    
    def test_thread_id_is_set_by_backend(self):
        print("\n------- test_thread_id_is_set_by_backend")
        cc = self.define_conversation_control("openai_graph_agent","Hi, I'm Bob and my last name is TheBuilder.", None)
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.messages
        assert rep.thread_id
        print(f"\n\nagent --> {rep}") 

    def test_conversation_with_chain_tool_agent(self):
        cc = self.define_conversation_control("openai_tool_chain","What is Athena Decision Systems?",None)
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.chat_history
        assert rep.messages
        print(f"agent --> {rep}")
        assert "Athena Decision Systems is a company" in rep.messages[0].content

    def test_conversation_with_tool_graph_agent(self):
        cc = self.define_conversation_control("base_tool_graph_agent","What is Athena Decision Systems?",None)
        rep = get_or_start_conversation(cc)
        print(f"agent --> {rep}")
        assert "Athena Decision Systems is a company" in rep.messages[0].content

    def test_watson_base_graph_agent(self):
        cc = self.define_conversation_control("watson_graph_agent","What is Athena Decision Systems?",None)
        cc.agent_id="watson_graph_agent"
        cc.user_id="unit_test"
        cc.thread_id="1"
        cc.chat_history=[]
        cc.query="What is Athena Decision Systems?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.chat_history
        assert rep.messages
        print(f"agent --> {rep.chat_history}")
        assert "Athena Decision Systems" in rep.messages[0].content


if __name__ == '__main__':
    unittest.main()