
from datetime import datetime

from pydantic import BaseModel


class CreateRoomReques(BaseModel):
    name: str
    description: str | None
    priority: str
    status: str
    product_owner_id: str
    members: list[str] # list of ids
    sprint_length_days: int

    class Config:
        form_attribute = True


class RoomPreviewResponse(BaseModel):
    id: str
    name: str
    status: str
    priority: str
    created: datetime
    