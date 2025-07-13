from fastapi import HTTPException
from sqlalchemy import Sequence, desc, func, or_, select
from sqlalchemy.orm import Session

from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo


def get_tasks_(q: str | None,current_user: UserResponse, session: Session):
    '''Get all tasks belong to current user'''
    stmt = select(Todo).where(Todo.is_deleted != True, Todo.created_by == current_user.email).order_by(
            desc(Todo.created)
        )

    if q is not None:
        stmt = stmt.where(
            or_(

                func.lower(Todo.title).contains(q.lower()),
                func.lower(Todo.desription).contains(q.lower())

        ))

    task: Sequence[Todo]  = session.execute(stmt).scalars().all()

    if task is None:
        raise HTTPException(detail="task not found", status_code=200)

    return task
