
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.common.generate_random_id_uuid import generate_random_id
from app.db.db import Base, Defaults
from app.api.room.model import room_users

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
    tasks = relationship("Todo", back_populates="user", cascade="all, delete-orphan")
    organization = relationship("Organization", back_populates="users")
    organization_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey('organizations.id'), nullable=False)
    announcement_vote = relationship("AnnouncementVote", back_populates="user", cascade="all, delete-orphan")
    announcement_comments = relationship("AnnouncementComment", back_populates="user", cascade="all, delete-orphan")
    
    
    # rooms to check who is own this room, I GUESS WE DON'T NEEDED 
    rooms = relationship("Room", back_populates="user", cascade="all, delete-orphan")
    joined_rooms = relationship("Room", secondary=room_users, back_populates="members")


