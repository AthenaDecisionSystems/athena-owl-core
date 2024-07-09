from pydantic import BaseModel
import uuid
from typing import Optional, Any
from langchain.tools import StructuredTool


class OwlToolEntity(BaseModel):
    tool_id: str = str(uuid.uuid4())
    toll_name: Optional[str] = ""
    tool_description: Optional[str] = ""
    tool_class_name: Optional[str] = ""
    tool_fct_name: Optional[str] = ""
    tool_arg_schema_class: Optional[str] = None
    
class ToolInstanceFactoryInterface(object):
    methods = {}
    arg_schemas = {}
    
    def define_tool(self, description: str, funct_name: str, args: Optional[str]):
        if args:
            return StructuredTool.from_function(
                func=self.methods[funct_name],
                name=funct_name,
                description=description,
                args_schema= self.arg_schemas[args], # type: ignore
                return_direct=False,
            )
        else:
            return StructuredTool.from_function(
                func=self.methods[funct_name],
                name=funct_name,
                description=description,
                return_direct=False,
            )
        
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
        pass