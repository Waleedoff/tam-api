
from app.api.auth.models import User
from app.api.room.model import Room
from sqlalchemy.orm import Session
from app.api.auth.schema import UserResponse
from sqlalchemy import select

def get_my_product_owner_rooms_(session: Session, current_user: UserResponse):
    stmt = select(Room).where(Room.product_owner_id == current_user.id)
    rooms = session.execute(stmt).scalars().all()
    return rooms
    