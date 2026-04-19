
from app.db.db import Base, Defaults
from sqlalchemy.orm import Mapped, relationship
import sqlalchemy as sa
from datetime import datetime

class Goal(Base, Defaults): 
    title: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    description: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    deadline: Mapped[datetime] = sa.Column(sa.DateTime, nullable=False)
    

    key_results = relationship(
        "KeyResult",
        back_populates="goal",
        cascade="all, delete-orphan"
    )

    brd = relationship(
        "Brd",
        back_populates="goal",
        cascade="all, delete-orphan"
    )


class KeyResult(Base, Defaults):
    __tablename__ = "key_results"
    title: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    target_value: Mapped[float] = sa.Column(sa.Float, nullable=False)  # type: ignore
    # TODO should add current value attribute over here.

    goal_id: Mapped[str] = sa.Column(sa.String, # TODO should delete sa.string cause it's deplicated.
        sa.ForeignKey("goals.id"),
        nullable=False
    )
    # Relations orm level.
    goal = relationship("Goal", back_populates="key_results")
    
    # Relations orm level.
    tasks = relationship("Todo", back_populates="key_results", cascade="all, delete-orphan")
    backlog = relationship("Backlog", back_populates='key_results')
    
    @property
    def progress(self) -> float:
        if self.target_value == 0:
            return 0.0
        return min((self.current_value / self.target_value) * 100, 100)
