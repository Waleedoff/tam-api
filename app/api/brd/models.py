
from app.db.db import Base, Defaults
from sqlalchemy.orm import Mapped, relationship
import sqlalchemy as sa
from datetime import datetime
from app.api.todos.schema import Priority



# TODO should add code in the future. like -> BRD_001 think about their business.
class Brd(Base, Defaults): 
    title: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    business_objective:  Mapped[str] = sa.Column(sa.String, nullable=False)
    scopeIn: Mapped[str] = sa.Column(sa.String, nullable=False)
    scopeOut: Mapped[str] = sa.Column(sa.String, nullable=False)
    priority: Mapped[str] = sa.Column(sa.String, nullable=False, default=Priority.LOW) # type: ignore
    goal_id: Mapped[str] = sa.Column(sa.ForeignKey("goals.id"),
        nullable=False) 
    goal = relationship("Goal", back_populates='brd')
    backlog = relationship("Backlog", back_populates='brd')