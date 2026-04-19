

from app.api.auth.schema import UserResponse
from app.api.room.enums import PublishingStatus
from app.api.room.model import Room
from sqlalchemy.orm import Session  
from sqlalchemy import select
def unpublish_room_(room_id: str, session: Session, currentt_user: UserResponse):
    stmt = select(Room).where(Room.id == room_id, Room.publishing_statu != PublishingStatus.DRAFT)
    room: Room | None = session.execute(stmt).scalar_one_or_none()
    if room is None:
        raise Exception('room not found')
    
    room.publishing_statu = PublishingStatus.DRAFT.value