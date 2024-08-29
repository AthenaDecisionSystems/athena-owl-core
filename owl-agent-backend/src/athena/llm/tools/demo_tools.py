"""
This class demonstrate tool / function implementation for demo and testing.

Any solution needs to implement this kind of class.
It has to implement the factory method to create the tools
"""
from typing import Any, Optional
from enum import Enum
from pydantic.v1 import BaseModel, Field

from athena.llm.tools.tool_factory import ToolInstanceFactoryInterface
from athena.llm.tools.tool_mgr import OwlToolEntity


# Demonstrate complex argument with enumerated value
class CustomerClassEnum(str, Enum):
    retail = 'retail'
    isv = 'isv'
    media = "media"
    telecom = "telecom"


class CrmArgument(BaseModel):
    """
    The argument to the CRM call is a json with the attribute user_id, customer_id, query and customer_class
    """
    user_id: Optional[str] = Field(None, description="user id of the connected user")
    customer_id: Optional[str] = Field(None, description="the customer id to search in the CRM")
    customer_class: Optional[str] = Field(None, description="The class of customer to search in")
    query: Optional[str] = Field(None, description="the user search query")


def query_crm_backend(crmArgument: CrmArgument):
    """Call the customer relationship management (CRM) to get customer data."""
    # normally process the  argument. This is for demonstration of passing a BaseModel as arg
    return [{"customer_id": "C001", "description": "The customer records from DEMO CRM"}]



class DemoToolInstanceFactory(ToolInstanceFactoryInterface):
    # use to map to function
    methods = { "query_crm_backend": query_crm_backend}
    arg_schemas = {"CrmArgument": CrmArgument}
    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
        """ From the list of tools to use build the function reference for LLM """
        tool_list=[]
        for tool_entity in tool_entities:
            tool_list.append(self.define_tool( tool_entity.tool_description, tool_entity.tool_fct_name, tool_entity.tool_arg_schema_class))  # type: ignore
        return tool_list
