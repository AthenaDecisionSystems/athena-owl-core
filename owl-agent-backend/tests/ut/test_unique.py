import unittest
import sys, os
from typing import Optional

module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
from athena.itg.store.content_mgr import get_content_mgr, FileDescription
from athena.llm.assistants.assistant_mgr import get_assistant_manager, OwlAssistantEntity
from athena.routers.dto_models import ConversationControl
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

    def test_calling_mistral_ollama_agent(self):
        mgr = get_assistant_manager()
        oae: Optional[OwlAssistantEntity] = mgr.get_assistant_by_id("mistral_tool_assistant")
        if oae is None:
            raise ValueError("mistral_tool_assistant not found")
        assistant = mgr.build_assistant(oae.assistant_id,"en")
        assert assistant
        # Default assistant has one LLM and one tool to search the web
        cc = ConversationControl(query="what is langgraph?", thread_id="thread_test")
        rep = assistant.send_conversation(cc)
        print(rep)
