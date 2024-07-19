from pydantic import BaseModel
import uuid
from typing import Optional, Any
from langchain.tools import StructuredTool


class OwlToolEntity(BaseModel):
    tool_id: str = str(uuid.uuid4())
    tool_name: Optional[str] = ""
    tool_description: Optional[str] = ""
    tool_class_name: Optional[str] = ""
    tool_fct_name: Optional[str] = ""
    tool_arg_schema_class: Optional[str] = None
    
class ToolInstanceFactoryInterface(object):
    """
    The extension of this factory needs to implement how to create tool instance.
    The methods is a dict with method_name and method. Example:
    methods = { "query_crm_backend": query_crm_backend}
    arg_schemas is also a dict with the arguments, mostly has instance of a BaseModel
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
        pass