from datetime import datetime

from app.api.todos.enums import Priority
from pydantic import BaseModel


class TodoResponse(BaseModel):
    id: str
    title: str
    desription: str | None
    priority: str
    status: str

    class Config:
        form_attribute = True


class TodoCreateRequest(BaseModel):
    title: str
    desription: str
    priority: Priority


class TodoUpdateRequest(BaseModel):
    title: str
