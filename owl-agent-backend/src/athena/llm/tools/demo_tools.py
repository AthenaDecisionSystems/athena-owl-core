"""
This class demonstrate tool / function implementation for demo and testing.

Any solution needs to implement this kind of class.
It has to implement the factory method to create the tools
"""
from typing import Any
from langchain_core.tools import tool
from athena.llm.tools.tool_factory import ToolInstanceFactoryInterface
from athena.llm.tools.tool_mgr import OwlToolEntity

def query_crm_backend(query: str):
    """Call the customer relationship management (CRM) to get customer data."""
    return ["The customer records from DEMO CRM"]


class DemoToolInstanceFactory(ToolInstanceFactoryInterface):
    # use to map to function
    methods = { "query_crm_backend": query_crm_backend}
    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
        """ From the list of tools to use build the function reference for LLM """
        tool_list=[]
        for tool_entity in tool_entities:
            tool_list.append(self.define_tool( tool_entity.tool_description, tool_entity.tool_fct_name, tool_entity.tool_arg_schema_class))
        return tool_list
