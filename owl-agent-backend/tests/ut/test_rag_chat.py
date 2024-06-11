import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("../../.env")
from athena.itg.store.content_mgr import get_content_mgr, FileDescription
from athena.llm.base_owl_agent  import BaseOwlAgent
from athena.llm.agent_openai  import OpenAIClient
from athena.routers.dto_models import ConversationControl

class TestRagConversation(unittest.TestCase):
    
    
    def test_getting_athena_content_and_query_it(self):
        print("Test crawling a web site to vector store and do a query to openAI")
        fd=FileDescription()
        fd.name="athena-decision-web"
        fd.file_name= fd.name
        fd.type="html"
        fd.file_base_uri="https://athenadecisions.com/"
        service = get_content_mgr()
        rep=service.process_doc(fd,None)
        print(repr)
        agent = OpenAIClient()
        cc = ConversationControl()
        cc.callWithDecisionService=False
        cc.callWithVectorStore=True
        cc.locale="fr"
        cc.type="chat"
        cc.prompt_ref="default_prompt"
        cc.query="what is athena decision systems?"
        rep=agent.send_conversation(cc)
        print(rep)
        