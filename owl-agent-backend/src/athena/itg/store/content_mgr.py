"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter, MarkdownHeaderTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyMuPDFLoader, BSHTMLLoader, WebBaseLoader
from langchain_core.documents import Document

import os, logging
from typing import List, Optional, Dict, Tuple, Any
from pydantic import BaseModel
import chromadb
import os
from athena.app_settings import get_config

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(get_config().logging_level_int)
DEFAULT_K = 4 
DEFAULT_COLLECTION_NAME="owl_default"
"""
Service to manage documents for semantic search in vector data base and to support
Retrieval Augmented Generation. 
"""

class FileDescription(BaseModel):
    """
    Metadata about a file, with potential URI to access to the file content, and collection name so we can
    isolate content in the vector store
    """
    name: Optional[str] = ''
    description: Optional[str] = ''
    type: str= "md"
    file_name: Optional[str] = ''
    file_base_uri: Optional[str] = ''
    collection_name: Optional[str] = DEFAULT_COLLECTION_NAME


# 09/26/24 Added to support chromadb changes in its call api. so this is a wrapper class for openai embedding only
class CustomOpenAIEmbeddings(OpenAIEmbeddings):

    def __init__(self, openai_api_key, *args, **kwargs):
        super().__init__(openai_api_key=openai_api_key, *args, **kwargs)
        
    def _embed_documents(self, texts):
        return super().embed_documents(texts)  # <--- use OpenAIEmbedding's embedding function

    def __call__(self, input):
        return self._embed_documents(input)
    

    
# supported embedding
embeddings={"OpenAIEmbeddings": CustomOpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"),
                                                       model = get_config().owl_agent_vs_embedding_fct_model)}



class ContentManager:
    """
    Content manager exposes APIs to process unstructured pdf, html, markdown, or text file and
    offers a retriever for LLM chains or agents. It is a singleton.
    External configuration comes from app_settings
    """
    _instance = None

    def __new__(cls, **kwargs):
        _instance = super().__new__(cls)
        cls.content_repo_path=get_config().owl_agent_content_file_path
        if not os.path.exists(cls.content_repo_path):
            os.makedirs(cls.content_repo_path)
        return _instance
        

    def process_doc(self, file_description: FileDescription, content)-> str:
        """
        Persist  metadata file and potentially the file content in the storage location as specified in config
        """
        if file_description:
            if content:
                file_description.file_base_uri=self.persist_content(file_description.file_name, content)
            
            if file_description.file_name:
                # persist metadata file - if already exists replace it
                file_name_base=file_description.file_name[:file_description.file_name.rfind('.')]
                f = open(self.content_repo_path + "/" + file_name_base + ".json","w")
                f.write(file_description.model_dump_json())
                f.close()
                LOGGER.debug("Saved metadata " + file_name_base)
   
            chunks=self.process_file_content(file_description)
            rep =  f"document {file_description.name} processed with {chunks} chunks embedded"
            LOGGER.debug(f"@@@> {rep}")
            return rep
        else:
            raise Exception("The file description content is mandatory")
        
      
            
    def process_file_content(self,file_description: FileDescription) -> int:
        """
        From the document type, perform the different chunking and embedding
        """
        if file_description.type == "pdf":
            documents= self.split_pdf_docs(file_description)
        elif file_description.type == "text":
            documents= self.split_txt_docs(file_description)
        elif file_description.type == "md":
            documents= self.split_md_docs(file_description)
        elif file_description.type == "html":
            documents= self.split_html_docs(file_description)
        else:
            documents = []
        self.process_documents(documents,file_description.collection_name)
        return len(documents)
            
    def split_txt_docs(self,file_description: FileDescription)-> List[Document]:
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
                chunk_size=300,
                chunk_overlap=20,
                length_function=len,
                is_separator_regex=False
            )
        texts=[]
        with open(file_description.file_base_uri + "/" + file_description.file_name) as f: # type: ignore
            doc = f.read()
            texts = text_splitter.create_documents([doc],[{"source": file_description.file_name}])
        return texts
    
    def split_md_docs(self, file_description: FileDescription) -> List[Document]:
        docs=[]
        with open(file_description.file_base_uri + "/" + file_description.file_name, 'r') as file:
            markdown_document = file.read()
            headers_to_split_on =[ ("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
            markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
            docs = markdown_splitter.split_text(markdown_document)
            # docs include metadatas with headers reference
        return docs
        
    def split_html_docs(self, file_description: FileDescription) -> List[Document]:
        """
         Load HTML doc or URL.
        """
        docs=[]
        if "http" not in file_description.file_base_uri:
            loader=BSHTMLLoader(file_description.file_base_uri + "/" + file_description.file_name) 
        else:
            loader = WebBaseLoader(
                web_paths=(file_description.file_base_uri,)
            )
        docs = loader.load()
        return docs


    def split_pdf_docs(self, file_description: FileDescription) -> List[Document]:
        loader = PyMuPDFLoader(file_description.file_base_uri + "/" + file_description.file_name)
        documents = loader.load_and_split()
        return documents


    def process_documents(self, docs, collection_name: str = DEFAULT_COLLECTION_NAME):
        """
        For each documents build a vector representation and persist both in a collection
        """
        vs = self.get_vector_store(collection_name)
        vs.from_documents(documents=docs, 
                          client=vs._client,
                          persist_directory=vs._persist_directory,
                          embedding= embeddings[get_config().owl_agent_vs_embedding_fct],
                          collection_name=collection_name)

        LOGGER.debug(f"Vector store updated with {len(docs)} docs")
        LOGGER.debug(f" within {vs._client.count_collections()} collection")



    def persist_content(self,filename, content) -> str:
        """persist the uploaded file
        """
        file_path = self.content_repo_path + "/" + filename
        if type(content) == "str":
            f = open(file_path, "w")
        else:
            f = open(file_path, "wb")
        f.write(content)
        f.close()
        return self.content_repo_path


    def get_retriever(self, collection_name:str=DEFAULT_COLLECTION_NAME):
        vs = self.get_vector_store()
        return vs.as_retriever()



    def get_vector_store(self, collection_name:str =DEFAULT_COLLECTION_NAME):
        """
        When there is a Vector Store URL, access the collection via the http client
        if not use local persistence
        """
        url = get_config().owl_agent_vs_url
        path=get_config().owl_agent_vs_path
        if path and len(url) == 0:
            client = chromadb.PersistentClient(path)
            vdb=Chroma(client=client, 
                       collection_name=collection_name,
                       persist_directory=path,
                       embedding_function=embeddings[get_config().owl_agent_vs_embedding_fct],)
        else:
            host,port = url.split(':')
            client = chromadb.HttpClient(host= host, port=port)
            vdb=Chroma(client=client, collection_name=collection_name,embedding_function=embeddings[get_config().owl_agent_vs_embedding_fct],)
        client.get_or_create_collection(name=collection_name, 
                                    embedding_function=embeddings[get_config().owl_agent_vs_embedding_fct],
                                    metadata={"hnsw:space": "cosine"})
        
        return vdb


    def search(self, collection_name: str=DEFAULT_COLLECTION_NAME, query: str = "", top_k: int = 1) -> List[Tuple[str, float]]:
        vs = self.get_vector_store(collection_name)
        # query_embedding = embeddings[get_config().owl_agent_vs_embedding_fct](query)
        docs = vs.similarity_search(
               query,  # type: ignore
                k=top_k
            )
        # vector_store.similarity_search_by_vector
        return docs

    def clear_collection(self, collection_name: str= DEFAULT_COLLECTION_NAME):
        vs = self.get_vector_store(collection_name)
        vs._client.delete_collection(collection_name)


def get_content_mgr() -> ContentManager:
    """ Factory to get access to unique instance of content manager"""
    if ContentManager._instance is None:
        ContentManager._instance = ContentManager()
    return ContentManager._instance