from app.api.auth.schema import UserResponse
from app.api.message.models import Message
from app.api.message.schema import MessageResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
def get_messages_(room_id: str, session: Session, current_user: UserResponse):
  
    stmt = select(Message).options(joinedload(Message.user)).where(Message.room_id == room_id).order_by(Message.created)
    
    messages = session.execute(stmt).scalars().all()
    
    
    
    
    return [
        MessageResponse(
            content=msg.content,
            username = msg.user.username,
            id = msg.id,
            created = msg.created,
            gender=msg.user.gender
        )
        for msg in messages 
    ]