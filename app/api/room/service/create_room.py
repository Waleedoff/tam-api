from app.api.auth.models import User
from app.api.auth.schema import UserResponse
from app.api.room.model import Room
from app.api.room.schema import CreateRoomReques
from sqlalchemy.orm import Session  

def create_room_(body: CreateRoomReques,current_user: UserResponse, session: Session):
    users = session.query(User).filter(User.id.in_(body.members)).all()
    room = Room(**body.model_dump(exclude={"members"}), created_by=current_user.id, user_id=current_user.id, members=users)
    session.add(room)
    
    