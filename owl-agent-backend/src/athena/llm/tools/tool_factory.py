from pydantic import BaseModel
import uuid
from typing import Optional

class OwlToolEntity(BaseModel):
    tool_id: str = str(uuid.uuid4())
    tool_description: Optional[str] = ""
    tool_class_name: Optional[str] = ""
    tool_fct_name: Optional[str] = ""
    tool_arg_schema_class: Optional[str] = None
    
class ToolInstanceFactoryInterface(object):
    
    def build_tool_instances(self, tool_entities: list[OwlToolEntity]):
        pass