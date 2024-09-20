"""
This class demonstrate tool / function implementation for demo and testing.

Any solution needs to implement this kind of class.
It has to implement the factory method to create the tools
"""
from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel, Field

from athena.llm.tools.tool_mgr import DefaultToolInstanceFactory


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



class DemoToolInstanceFactory(DefaultToolInstanceFactory):
    # use to map to function
    methods = { "query_crm_backend": query_crm_backend}
    arg_schemas = {"CrmArgument": CrmArgument}
    

