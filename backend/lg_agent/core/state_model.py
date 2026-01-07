from typing_extensions import Annotated,TypedDict,List, Optional
from langgraph.graph.message import add_messages

class State(TypedDict):
    intent:str
    messages: Annotated[List,add_messages] 
    obj_dir: str = "D:/Shi-SF-Agent/saleforce-Agent/org_2/force-app/main/default/objects"
    xml_content:str
    obj_name:Optional[str]
    response:str
    