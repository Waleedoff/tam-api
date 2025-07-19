
from datetime import datetime

from pydantic import BaseModel


class CreateRoomReques(BaseModel):
  
    name: str
    desription: str | None
    priority: str
    status: str
    created: datetime
    members: list[str] # list of ids

    class Config:
        form_attribute = True


class RoomPreviewResponse(BaseModel):
    id: str
    name: str
    status: str
    priority: str
    created: datetime
    