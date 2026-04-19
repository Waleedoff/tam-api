from app.api.backlog.enum import BacklogType
from app.api.todos.enums import Priority
from pydantic import BaseModel


class CreateBacklogRequest(BaseModel):
    title: str
    description: str
    type: BacklogType
    priority: Priority
    brd_id: str
    # key_result_id: str
    

class BacklogIdsResponse(BaseModel):
    id: str
    title: str





class BacklogResponse(BaseModel):
    id: str
    title: str
    description: str
    type: BacklogType
    priority: Priority
    brd_id: str