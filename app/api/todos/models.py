
from typing import TYPE_CHECKING
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship

from app.api.todos.enums import Priority, TaskStatus
from app.db.db import Base, Defaults

# TODO change todo to task.
class Todo(Base, Defaults):

    title: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    desription: Mapped[str] = sa.Column(sa.String, nullable=False) # type: ignore
    priority: Mapped[str] = sa.Column(sa.String, nullable=False, default=Priority.LOW) # type: ignore
    status: Mapped[str] = sa.Column(sa.String, nullable=False, default=TaskStatus.TODO)  # type: ignore
    user_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey('auth_user.id'), nullable=True)  # type: ignore
    user = relationship("User", back_populates="tasks")
    estimate: Mapped[int] = sa.Column(sa.Integer, nullable=False)
    
    user_story_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("user_stories.id"), nullable=True)
    user_story = relationship("UserStory", back_populates="tasks")
    
    key_result_id: Mapped[str] = sa.Column(sa.String, sa.ForeignKey("key_results.id"), nullable=True)
    key_results = relationship("KeyResult", back_populates="tasks")