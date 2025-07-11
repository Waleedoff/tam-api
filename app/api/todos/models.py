
import sqlalchemy as sa
from sqlalchemy.orm import Mapped

from app.api.todos.enums import Priority, Status
from app.db.db import Base, Defaults


class Todo(Base, Defaults):

    title: Mapped[str] = sa.Column(sa.String, nullable=False)  # type: ignore
    desription: Mapped[str] = sa.Column(sa.String, nullable=False) # type: ignore
    priority: Mapped[str] = sa.Column(sa.String, nullable=False, default=Priority.LOW) # type: ignore
    status: Mapped[str] = sa.Column(sa.String, nullable=False, default=Status.PENDING)  # type: ignore
    is_deleted: Mapped[bool] = sa.Column(sa.Boolean, nullable=False, default=False)  # type: ignore
