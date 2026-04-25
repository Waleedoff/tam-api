
from app.api.room.model import Room
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.common.generate_random_id_uuid import generate_random_id
from app.db.db import Base, Defaults

class User(Base, Defaults):
    __override_tablename__ = "auth_user"
    url_id: Mapped[str] = sa.Column(sa.String, nullable=False, index=True, unique=True, default=generate_random_id)
    username: Mapped[str] = sa.Column(sa.String, nullable=False)
    full_name: Mapped[str] = sa.Column(sa.String, nullable=False)
    email: Mapped[str] = sa.Column(sa.String, nullable=False)
    hashed_password: Mapped[str] = sa.Column(sa.String, nullable=False)
    disabled: Mapped[bool] = sa.Column(sa.Boolean, default=False)
    gender:  Mapped[str] = sa.Column(sa.String, nullable=False)
    department: Mapped[str] = sa.Column(sa.String, nullable=False)
    role: Mapped[str] = sa.Column(sa.String, nullable=False)
    is_online: Mapped[bool] = sa.Column(sa.Boolean, default=False)
    test_rollback:  Mapped[str] = sa.Column(sa.String, nullable=False)
    tasks = relationship("Todo", back_populates="user", cascade="all, delete-orphan")
    organization = relationship("Organization", back_populates="users")
    organization_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey('organizations.id'), nullable=False)
    announcement_vote = relationship("AnnouncementVote", back_populates="user", cascade="all, delete-orphan")
    announcement_comments = relationship("AnnouncementComment", back_populates="user", cascade="all, delete-orphan")
    
    
    # rooms to check who is own this room, I GUESS WE DON'T NEEDED 
    rooms = relationship("Room", foreign_keys=[Room.user_id], back_populates="user", cascade="all, delete-orphan")
    
    memberships = relationship("RoomMember", back_populates="user", cascade="all, delete-orphan")
    joined_rooms = relationship(
        "Room",
        secondary="room_members",
        primaryjoin="User.id==RoomMember.user_id",
        secondaryjoin="Room.id==RoomMember.room_id",
        viewonly=True
    )
    messages = relationship("Message", back_populates="user", cascade="all, delete-orphan")




