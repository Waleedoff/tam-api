from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.todos.models import Todo


def delete_task_(task_id: str, session: Session):
    '''Delete a task by passing thier task_id'''
    stmt = select(Todo).where(Todo.id == task_id, Todo.is_deleted != True) # type: ignore

    task: Todo | None = session.execute(stmt).scalar_one_or_none()

    if task is None:
        raise HTTPException(detail="task not found", status_code=400)

    task.is_deleted = True
