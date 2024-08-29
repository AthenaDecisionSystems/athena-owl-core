import unittest
import sys, os
from typing import Optional

module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
from athena.itg.store.content_mgr import get_content_mgr, FileDescription
from athena.llm.agents.agent_mgr import get_agent_manager, OwlAgent
from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation

class TestUniqueStuff(unittest.TestCase):

    

        
    def _test_process_html_from_URL(self):
        print("\n--> test_process HTML page test\n")
        fd=FileDescription()
        fd.name="athena-decision-web"
        fd.file_name= fd.name
        fd.type="html"
        fd.file_base_uri="https://athenadecisions.com/"
        service = get_content_mgr()
        rep=service.process_doc(fd,None)
        assert rep
        print(rep)
        rep = service.search("do you know OwlAthena")
        print(rep)

    def _calling_mistral_ollama_agent(self):
        mgr = get_agent_manager()
        oae: Optional[OwlAgent] = mgr.get_agent_by_id("mistral_large")
        if oae is None:
            raise ValueError("mistral_large not found")
        agent = mgr.build_agent_runner(oae.agent_id,"en")
        assert agent
        # Default agent has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = agent.send_conversation(cc)
        print(rep)
        


 

if __name__ == '__main__':
    unittest.main()