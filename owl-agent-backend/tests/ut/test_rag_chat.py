import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
from athena.itg.store.content_mgr import get_content_mgr, FileDescription

from athena.routers.dto_models import ConversationControl
from athena.llm.conversations.conversation_mgr import get_or_start_conversation
class TestRagConversation(unittest.TestCase):
    
    
    def test_getting_athena_content_and_query_it(self):
        print("Test crawling a web site to vector store and do a query to path data to openAI")
        fd=FileDescription()
        fd.name="athena-decision-web"
        fd.file_name= fd.name
        fd.type="html"
        fd.file_base_uri="https://athenadecisions.com/"
        service = get_content_mgr()
        rep=service.process_doc(fd,None)
        print(repr)
        
        cc = ConversationControl()
        cc.locale="en"
        cc.assistant_id="base_graph_assistant"
        cc.thread_id="1"
        cc.query="what is athena decision systems?"
        rep = get_or_start_conversation(cc)
        assert rep
        assert rep.message
        print(rep)
        
if __name__ == '__main__':
    unittest.main()