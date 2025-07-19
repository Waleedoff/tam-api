
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.api.todos.enums import Priority, Status
from app.db.db import Base, Defaults
from app.api.room.enums import PublishingStatus




room_users = sa.Table(
    "room_users",
    Base.metadata,
    sa.Column("room_id", sa.ForeignKey("rooms.id"), primary_key=True),
    sa.Column("user_id", sa.ForeignKey("auth_user.id"), primary_key=True),
)

class Room(Base, Defaults):

    name: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    desription: Mapped[str] = sa.Column(sa.String, nullable=False) # type: ignore
    priority: Mapped[str] = sa.Column(sa.String, nullable=False, default=Priority.LOW) # type: ignore
    status: Mapped[str] = sa.Column(sa.String, nullable=False, default=PublishingStatus.DRAFT)  # type: ignore
    publishing_statu: Mapped[bool] = sa.Column(sa.Boolean, nullable=False, default=False)  # type: ignore
    user_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey('auth_user.id'), nullable=False)  # type: ignore
    user = relationship("User", back_populates="rooms")

    # 👥 جميع المستخدمين (بما فيهم المالك)
    members = relationship("User", secondary=room_users, back_populates="joined_rooms")
    
    
    tasks = relationship("Todo", back_populates="room")  # ← داخل Room

    
    
    


