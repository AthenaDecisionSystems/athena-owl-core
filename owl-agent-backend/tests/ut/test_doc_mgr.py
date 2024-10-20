import unittest
import sys, os
module_path = "./src"
sys.path.append(os.path.abspath(module_path))
os.environ["CONFIG_FILE"] = "./tests/ut/config/config.yaml"
from dotenv import load_dotenv
load_dotenv()
from athena.itg.store.content_mgr import get_content_mgr, FileDescription



def build_file_descriptor(name: str, type: str,fname: str):
    """
    define a file descriptor to be reused by test cases
    """
    fd=FileDescription()
    fd.name=name
    fd.file_name=fname
    fd.file_base_uri="./tests/ut/documents"
    fd.type=type
    fd.collection_name="test"
    return fd
    

class TestDocumentManager(unittest.TestCase):
    """
    Test all operations of the content manager with vector store, local
    """
    @classmethod
    def setUpClass(cls):
        cls.service = get_content_mgr()

    def test_1_no_file_doc_post_operation(self):
        """
        Validate we cannot post without any file uploaded
        """
        assert self.service
        with self.assertRaises(Exception) as context:
            rep=self.service.process_doc(None,None)
        self.assertTrue('description content is mandatory' in str(context.exception))

    def test_process_txt_from_folder(self):
        """ 
        Validate reading, chunking, then searching stuff from a text file
        """
        print("\n--> test_process_ text\n")
        fd = build_file_descriptor("Claims-complaint-rules", "text","ibu-claims-complaint-rules.txt")
        rep=self.service.process_doc(fd,None)
        print(rep)
        assert rep
        assert "chunks" in rep
        rep = self.service.search("test","which rule take into account  payment score and their claims score?",1)
        assert len(rep) != 0 
        print(rep[0].page_content)
        assert "Rule 38" in rep[0].page_content

    def test_process_md_from_folder(self):
        """ 
        Validate reading, chunking, then searching stuff from a markdown file
        """
        print("\n--> test_process_md_from_folder test\n")
        fd = build_file_descriptor("Claims-complaint-rules-md","md","ibu-claims-complaint-rules.md")
        rep=self.service.process_doc(fd,None)
        print(rep)
        assert rep
        assert "chunks" in rep
        rep = self.service.search("test","what is Rule 38?",1)
        print(rep)
        assert len(rep) != 0 
        print(rep[0].page_content)
        
    def test_process_html_from_folder(self):
        print("\n--> test_process HTML file test\n")
        fd = build_file_descriptor("Claims-complaint-rules-html","html","ibu-claims-complaint-rules.html")
        rep=self.service.process_doc(fd,None)
        assert rep
        rep = self.service.search("test","what is the content of rule 41?",1 )
        print(rep)

    def test_process_pdf_from_folder(self):
        print("\n--> test_process_pdf_from_folder\n")
        fd = build_file_descriptor("Claims-complaint-rules-pdf","pdf", "ibu-claims-complaint-rules.pdf")
        rep=self.service.process_doc(fd,None)
        assert rep
        rep = self.service.search("test","what is claim handling",2)
        print(rep[0].page_content.encode())

    def test_process_html_from_URL(self):
        print("\n--> test_process load HTML pagefrom public web site and search\n")
        fd=FileDescription()
        fd.name="athena-decision-web"
        fd.file_name= fd.name
        fd.type="html"
        fd.file_base_uri="https://athenadecisionsystems.github.io/athena-docs/"
        rep=self.service.process_doc(fd,None)
        assert rep
        rep = self.service.search("test","do you know Owl framework from Athena?",2)
        print(rep)

    def test_list_of_documents(self):
        """
        get the list of files with their metada
        """
        documents: list[FileDescription] = self.service.get_documents_with_metadata()
        assert documents
        assert len(documents) > 2
        assert documents[0].file_name

    def test_build_content(self):
        print("\n--> test_build_content\n")
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
                                                            collection_name="test",
                                                            description = "The history of a Dave_Grahan.")
        self.service.process_doc(file_description, content)
        rep=self.service.search("test","what kind of problem Dave Gahan has?",2)
        print(rep)

   
        
if __name__ == '__main__':
    unittest.main()