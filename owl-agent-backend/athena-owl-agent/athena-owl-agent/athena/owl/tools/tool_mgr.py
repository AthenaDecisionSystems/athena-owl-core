from typing import Any
from functools import lru_cache
import yaml, uuid
from pydantic import BaseModel
from typing import Optional, Any
from langchain.tools import StructuredTool
from langchain_community.tools.tavily_search import TavilySearchResults


class OwlToolEntity(BaseModel):
    """
    Delaration of a tool entity, read from yaml definition"""
    tool_id: str = ""
    tool_name: Optional[str] = ""
    tool_description: Optional[str] = ""
    tool_class_name: Optional[str] = ""
    tool_fct_name: Optional[str] = ""
    tool_arg_schema_class: Optional[str] = None
    tags: list[str] = []

class ToolManager():
    """
    Manage tools loaded from yaml or DB 
    """
    def __init__(self):
        self.TOOLS: dict = dict()


    def get_tools(self):
        return self.TOOLS
    
    def load_tool_definitions(self, path:str):
        with open(path, "r", encoding="utf-8") as f:
            a_dict = yaml.load(f, Loader=yaml.FullLoader)  # a dict with assistant entities
            for oa in a_dict:
                oae=OwlToolEntity.model_validate(a_dict[oa])
                self.TOOLS[oae.tool_id]=oae
    
    def save_tool(self, toolEntity: OwlToolEntity) -> str:
        if toolEntity.tool_id is None or toolEntity.tool_id == "":
            toolEntity.tool_id=str(uuid.uuid4())
        self.TOOLS[toolEntity.tool_id] = toolEntity
        return toolEntity.tool_id
    
    def get_tool_by_id(self, id: str) -> OwlToolEntity:
        return self.TOOLS[id]
    
    def get_tool_by_name(self, name: str) -> OwlToolEntity | None:
        for e in self.TOOLS:
            if self.TOOLS[e].tool_fct_name == name:
                return self.TOOLS[e]
        return None
    
    def delete_tool(self,key: str) -> str:
        entry = self.TOOLS.get(key, None)
        if entry != None:
            del self.TOOLS[key]
        return "Done"
    
    

_instance = None

@lru_cache
def get_tool_entity_manager(path) -> ToolManager:
    """ Factory to get access to unique instance of Tools manager"""
    global _instance
    if _instance is None:
        if path is None:
            path="./athena/config/tools.yaml"
        _instance = ToolManager()
        _instance.load_tool_definitions(path)
    return _instance

    
class DefaultToolInstanceFactory(object):
    """
    The extension of this factory needs to implement how to create tool instance,
    defines the method dictionary with method_name and method reference with the method aruments:
    arg_schemas is also a dict with the arguments, mostly has instance of a BaseModel
   
    Example:
    methods = { "query_crm_backend": query_crm_backend}
    arg_schemas = {"CrmArgument": CrmArgument}
    
    A OwlToolEntity should specify the key of the function and the key of the args when the function uses complex type.coroutine=
    
    OwlToolEntity(tool_id= "query_crm",
                tool_class_name= "athena.llm.tools.demo_tools",
                tool_description= "Call the customer relationship management (CRM) to get customer data.",
                tool_fct_name= "query_crm_backend",
                tool_arg_schema_class="CrmArgument")
    """
    methods = {}
    arg_schemas = {}
    
    def define_tool(self, description: str, funct_name: str, args: Optional[str]):
        if args:
            a = StructuredTool.from_function(
                func=self.methods[funct_name],
                name=funct_name,
                description=description,
                args_schema= self.arg_schemas[args], # type: ignore
                return_direct=False,
            )
            return a
        else:
            # the function signature will be used to build the argument list
            return StructuredTool.from_function(
                func=self.methods[funct_name],
                name=funct_name,
                description=description,
                return_direct=False,
            )
        
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
        """ From the list of tools to use build the function reference for LLM """
        tool_list=[]
        for tool_entity in tool_entities:
            if tool_entity.tool_id == "tavily":
                tool_list.append(TavilySearchResults(max_results=2))
            else:
                tool_list.append(self.define_tool( tool_entity.tool_description, tool_entity.tool_fct_name, tool_entity.tool_arg_schema_class))  # type: ignore
        return tool_list