# app/api/message/service/save_message.py

from app.api.message.models import Message
from app.api.auth.schema import UserResponse
from app.api.message.schema import SaveMessageRequest
from sqlalchemy.orm import Session

def save_message_(body: SaveMessageRequest, session: Session, current_user: UserResponse):
    message = Message(
        **body.model_dump(),
        user_id=current_user.id,
        created_by=current_user.id
        
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message
