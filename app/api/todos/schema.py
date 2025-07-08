from datetime import datetime

from pydantic import BaseModel


class TodoResponse(BaseModel):
    id: str
    title: str
    desription: str | None
    priority: str

    class Config:
        form_attribute = True


class TodoCreateRequest(BaseModel):
    title: str
    desription: str


class TodoUpdateRequest(BaseModel):
    title: str
