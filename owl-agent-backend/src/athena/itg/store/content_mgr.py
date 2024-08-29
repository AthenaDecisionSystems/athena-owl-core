"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_text_splitters.markdown import MarkdownTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader, BSHTMLLoader, WebBaseLoader
import os, logging
from typing import List, Optional 
from athena.app_settings import get_config
from pydantic import BaseModel

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(get_config().logging_level_int)

"""
Service to manage documents for semantic search and RAG context source
"""
embeddings={"OpenAIEmbeddings": OpenAIEmbeddings}

class FileDescription(BaseModel):
    """
    Metadata about a file, with potential URI to access to the file content
    """
    name: Optional[str] = ''
    description: Optional[str] = ''
    type: str= "md"
    file_name: Optional[str] = ''
    file_base_uri: Optional[str] = ''


class ContentManager:
    """
    Content manager exposes APIs to process unstructured pdf, html, markdown, txt file and
    offers a retriever for LLM chains or agents. It is a singleton.
    External configuration come from app_settings
    """
    _instance = None

    def __new__(cls, **kwargs):
        _instance = super().__new__(cls)

        config= get_config()
        cls.path=config.owl_agent_content_file_path
        if not os.path.exists(cls.path):
            os.makedirs(cls.path)
        return _instance
        

    def process_doc(self, file_description: FileDescription, content)-> str:
        """
        Persist  metadata file and potentially the file content in storage uri as specified in config
        """
        if file_description:
            if content:
                file_description.file_base_uri=self.persist_content(file_description.file_name, content)
            
            if file_description.file_name:
                # persist metadata file
                file_name_base=file_description.file_name[:file_description.file_name.rfind('.')]
                f = open(self.path + "/" + file_name_base + ".json","w")
                f.write(file_description.model_dump_json())
                f.close()
                LOGGER.debug("Saved metadata " + file_name_base)
   
            chunks=self.build_vector_content(file_description)
            rep =  f"document {file_description.name} processed with {chunks} chunks embedded"
            LOGGER.debug(f"@@@> {rep}")
            return rep
        else:
            raise Exception("The file description content is mandatory")
        
      
       

            
    def build_vector_content(self,file_description: FileDescription) -> int:
        # From the document type, perform the different chunking and embedding
        if file_description.type == "pdf":
            return self.embed_pdf_docs(file_description)
        elif file_description.type == "text":
            return self.embed_txt_docs(file_description)
        elif file_description.type == "md":
            return self.embed_md_docs(file_description)
        elif file_description.type == "html":
            return self.embed_html_docs(file_description)
        else:
            return 0

            
    def embed_txt_docs(self,file_description: FileDescription)-> int:
        text_splitter = RecursiveCharacterTextSplitter(
                separators=[
                    "\n\n",
                    "\n",
                    " ",
                    ".",
                    ",",
                    "\u200b",  # Zero-width space
                    "\uff0c",  # Fullwidth comma
                    "\u3001",  # Ideographic comma
                    "\uff0e",  # Fullwidth full stop
                    "\u3002",  # Ideographic full stop
                    "",
                ],
                chunk_size=100,
                chunk_overlap=20,
                length_function=len,
                is_separator_regex=False
            )
        with open(file_description.file_base_uri + "/" + file_description.file_name) as f: # type: ignore
            doc = f.read()
            texts = text_splitter.create_documents([doc])
            self.build_embeddings(texts)
            return len(texts)
    
    def embed_md_docs(self, file_description: FileDescription) -> int:
        """
         split a markdown file by a specified set of headers.
        """
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
            ]
        with open(file_description.file_base_uri + "/" + file_description.file_name, 'r') as file:
            markdown_document = file.read()
            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on, strip_headers=False)
            md_header_splits = markdown_splitter.split_text(markdown_document)
            self.build_embeddings(md_header_splits)       
            LOGGER.debug(f"Added {str(len(md_header_splits))} chunks to vector DB ")
            return len(md_header_splits)
        
    def embed_html_docs(self, file_description: FileDescription) -> int:
        """
         Load HTML doc or URL.
        """
        if "http" not in file_description.file_base_uri:
            loader=BSHTMLLoader(file_description.file_base_uri + "/" + file_description.file_name) 
        else:
            loader = WebBaseLoader(
                web_paths=(file_description.file_base_uri,)
            )
        docs = loader.load()
        self.build_embeddings(docs)       
        LOGGER.info(f"Added {str(len(docs))} chunks to vector DB ")
        return len(docs)


    def embed_pdf_docs(self, file_description: FileDescription) -> int:
        loader = PyMuPDFLoader(file_description.file_base_uri + "/" + file_description.file_name)
        documents = loader.load_and_split()
        self.build_embeddings(documents)   
        return len(documents)

    def build_embeddings(self,docs):
        vs = self.get_vector_store()
        vs.from_documents(documents=docs, embedding= embeddings[get_config().owl_agent_vs_embedding_fct](),  persist_directory=get_config().owl_agent_vs_path)
        print(f"Vector store updated with docs... {docs[0]}")
        
    def persist_content(self,filename, content) -> str:
        file_path = self.path + "/" + filename
        if type(content) == "str":
            f = open(file_path, "w")
        else:
            f = open(file_path, "wb")
        f.write(content)
        f.close()
        return self.path

    def get_retriever(self):
        return self.get_vector_store().as_retriever()

    def get_vector_store(self):
        if len(get_config().owl_agent_vs_url) == 0:
            self.vdb=Chroma(persist_directory=get_config().owl_agent_vs_path, embedding_function=embeddings[get_config().owl_agent_vs_embedding_fct]())
        else:
            LOGGER.info("Not implemented")
        return self.vdb


    def search(self, query: str):
        return self.get_vector_store().similarity_search(query, k=10)


def get_content_mgr() -> ContentManager:
    """ Factory to get access to unique instance of content manager"""
    if ContentManager._instance is None:
        ContentManager._instance = ContentManager()
    return ContentManager._instance