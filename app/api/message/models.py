
from app.db.db import Base, Defaults
from sqlalchemy.orm import Mapped, relationship
import sqlalchemy as sa


class Message(Base, Defaults): 
    content: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    room_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("rooms.id"), nullable=False) # type: ignore
    user_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("auth_user.id"), nullable=False) # type: ignore
    # ORM Relations
    room = relationship("Room", back_populates="messages")
    user = relationship("User", back_populates="messages")
