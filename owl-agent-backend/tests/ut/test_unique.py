import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv("../../.env")
from athena.itg.store.content_mgr import get_content_mgr, FileDescription


class TestUniqueStuff(unittest.TestCase):

    

        
    def test_process_html_from_URL(self):
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
