import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
from athena.itg.store.content_mgr import get_content_mgr, FileDescription


class TestDocumentManager(unittest.TestCase):
    """
    Test all operations of the content manager with vector store, remote or local
    """

    def test_1_no_file_doc_post_operation(self):
        """
        Validate we cannot post without any file uploaded
        """
        service = get_content_mgr()
        assert service
        with self.assertRaises(Exception) as context:
            rep=service.process_doc(None,None)
        self.assertTrue('description content is mandatory' in str(context.exception))

    def build_file_descriptor(self, type: str,fname: str):
        fd=FileDescription()
        fd.name="Claims-complaint-rules"
        fd.file_name=fname
        fd.file_base_uri="./tests/ut/documents"
        fd.type=type
        fd.collection_name="test"
        return fd
    
    def test_process_txt_from_folder(self):
        print("\n--> test_process_ text\n")
        fd = self.build_file_descriptor("text","ibu-claims-complaint-rules.txt")
        service = get_content_mgr()
        rep=service.process_doc(fd,None)
        print(rep)
        assert rep
        assert "chunks" in rep
        rep = service.search("test","what is rule 53?",1)
        assert len(rep) == 0 
        rep = service.search("test","what is Rule 38?",1)
        print(rep)

    def test_process_md_from_folder(self):
        print("\n--> test_process_md_from_folder test\n")
        fd = self.build_file_descriptor("md","ibu-claims-complaint-rules.md")
        service = get_content_mgr()
        rep=service.process_doc(fd,None)
        print(rep)
        assert rep
        assert "chunks" in rep
        rep = service.search("test","what is Rule 38?",1)
        print(rep)
        rep = service.search("test","what is rule 53?",1)
        assert len(rep) == 0 
        
    def test_process_html_from_folder(self):
        print("\n--> test_process HTML file test\n")
        fd = self.build_file_descriptor("html","ibu-claims-complaint-rules.html")
        service = get_content_mgr()
        rep=service.process_doc(fd,None)
        assert rep
        rep = service.search("test","what is the content of rule 41?",1 )
        print(rep)

    def _test_process_pdf_from_folder(self):
        print("\n--> test_process_pdf_from_folder\n")
        fd = self.build_file_descriptor("pdf")
        fd.file_name="ibu-claims-complaint-rules.pdf"
        service = get_content_mgr()
        rep=service.process_doc(fd,None)
        assert rep
        rep = service.search("what is claim handling")
        print(rep[0].page_content.encode())

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
        rep = service.search("do you know OwlAthena")
        print(rep)

    def _test_build_content(self):
        """
        Should create  a file descriptor and a file for processing
        """
        
        content=b"""
# Dave Gahan, has experienced a life of both fame and hardship:
## Fame and Success
Dave Gahan has been the lead singer of Depeche Mode since the band's inception in 1980. With the band, he has sold over 100 million albums worldwide and has become known for his powerful voice and stage presence.

## Drug Addiction
Dave Gahan struggled with drug addiction, particularly heroin, for many years. He overdosed in 1996 and was clinically dead for six minutes before being revived.
Gahan has faced several health issues, including a heart attack during a concert in 1993, bladder cancer in 2009, and vocal cord injuries.

## Personal Life: 
Dave Gahan has been married twice and has three children. His first marriage ended due to his drug addiction, and his second marriage has been ongoing since 1997.
Gahan is widely regarded as one of the greatest rock vocalists of all time, and Depeche Mode has been inducted into the Rock and Roll Hall of Fame. Despite his personal struggles, Gahan continues to perform and record music with Depeche Mode.
"""
        file_description: FileDescription = FileDescription(name = "Dave_Grahan",
                                                            file_name= "Dave_Grahan.md", 
                                                            type = "md", 
                                                            description = "The history of a Dave_Grahan.")
        service = get_content_mgr()
        service.process_doc(file_description, content)
        print(service.search("what kind of problem Dave Gahan has?"))
        
if __name__ == '__main__':
    unittest.main()