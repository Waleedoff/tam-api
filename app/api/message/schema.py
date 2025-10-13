# app/api/chat/schema.py
from pydantic import BaseModel
from datetime import datetime

class SaveMessageRequest(BaseModel):
    content: str
    room_id: str

# class MessageResponse(BaseModel):
#     id: str
#     content: str
#     room_id: str
#     user_id: str




class MessageResponse(BaseModel):
    id: str
    content: str
    username: str  # لازم ترجعه من backend
    created: datetime
    gender: str
