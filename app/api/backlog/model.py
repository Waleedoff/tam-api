from app.api.backlog.enum import BacklogType
from app.db.db import Base, Defaults
from sqlalchemy.orm import Mapped, relationship
import sqlalchemy as sa
from datetime import datetime
from app.api.todos.schema import Priority


class Backlog(Base, Defaults): 

    title: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    description:  Mapped[str] = sa.Column(sa.String, nullable=False)
    type: Mapped[str] = sa.Column(sa.String, nullable=False, default=BacklogType.BUG)
    priority: Mapped[str] = sa.Column(sa.String, nullable=False, default=Priority.LOW) # type: ignore
    
    brd_id: Mapped[str] = sa.Column(sa.ForeignKey("brds.id"), nullable=False)
    brd = relationship("Brd", back_populates='backlog')
    
    key_result_id: Mapped[str] = sa.Column(sa.ForeignKey("key_results.id"), nullable=False)
    key_results = relationship("KeyResult", back_populates='backlog')
    
    user_story = relationship("UserStory", back_populates='backlog')