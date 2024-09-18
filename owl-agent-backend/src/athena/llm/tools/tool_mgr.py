from typing import Any
from functools import lru_cache
from athena.app_settings import get_config
import yaml, uuid
from athena.llm.tools.tool_factory import ToolInstanceFactoryInterface, OwlToolEntity
from langchain_community.tools.tavily_search import TavilySearchResults

class ToolManager():
    
    def __init__(self):
        self.TOOLS: dict = dict()


    def get_tools(self):
        return self.TOOLS
    
    def load_tools(self, path:str):
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
def get_tool_entity_manager() -> ToolManager:
    """ Factory to get access to unique instance of Tools manager"""
    global _instance
    if _instance is None:
        path = get_config().owl_tools_path
        if path is None:
            path="./athena/config/tools.yaml"
        _instance = ToolManager()
        _instance.load_tools(path)
    return _instance


class BaseToolInstanceFactory(ToolInstanceFactoryInterface):
    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]) -> list[Any]:
        tool_list=[]
        for tool_entity in tool_entities:
            # TO DO rethink about this approach
            if tool_entity.tool_id == "tavily":
                tool_list.append(TavilySearchResults(max_results=2))
            else:
                raise Exception("Not yet implemented")
        return tool_list