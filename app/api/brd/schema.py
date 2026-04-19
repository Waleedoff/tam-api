from app.api.todos.enums import Priority
from pydantic import BaseModel


class CreateBrdRequest(BaseModel):
    title: str
    business_objective: str | None = ""
    priority: Priority
    scopeIn: str
    scopeOut: str
    goal_id: str 



class BrdResponse(BaseModel):
    id: str
    title: str
    priority: str
    business_objective: str
    scopeIn: str
    scopeOut: str


class getBrdIdResponse(BaseModel):
    id: str
    title: str