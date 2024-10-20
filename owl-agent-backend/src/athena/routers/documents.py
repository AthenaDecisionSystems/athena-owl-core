"""
Copyright 2024 Athena Decision Systems
@author Jerome Boyer
"""
from fastapi import File, UploadFile, Depends, APIRouter, Body
from athena.itg.store.content_mgr import FileDescription, get_content_mgr
from athena.app_settings import get_config
import logging
LOGGER = logging.getLogger(__name__)

router = APIRouter( prefix=get_config().api_route + "/a")



@router.post("/documents/", tags=["Manage documents"])
async def post_document_for_rag( file_description: FileDescription = Depends(), myFile: UploadFile = File(...)):
    """
    given the file description and the uploaded file content, process it by the content manager.
    The content in myFile may be omitted, in this case the file description has a URL path to access the file
    """
    LOGGER.info(f"REST received doc {file_description}")
    try:
        if myFile is not None:
            contents = await myFile.read()
            file_description.file_name=myFile.filename
        msg=get_content_mgr().process_doc(file_description, contents)
        return {"status": 201, "message": msg}
    except Exception as e:
         return {"status": 500, "message": "Backend exception", "error" : str(e)}

@router.get("/documents/{collection}/{query}/{top_k}", tags=["Manage documents"])
def get_documents_from_query(collection : str, query: str, top_k: int =3):
    return get_content_mgr().search(collection, query,top_k)


@router.get("/documents/", tags=["Manage documents"])
def get_all_documents() ->list[FileDescription]:
    return get_content_mgr().get_documents_with_metadata()