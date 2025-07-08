from fastapi import HTTPException
from app.api.todos.models import Todo
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.todos.schema import TodoCreateRequest

def edit_task_(body: TodoCreateRequest, task_id: str, session: Session):
    
    stmt = select(Todo).where(Todo.id == task_id, Todo.is_deleted != True)
    
    task: Todo | None = session.execute(stmt).scalar_one_or_none()
    
    if task is None:
        raise HTTPException(detail="task not found", status_code=400)
    
    task.update_attributes(body.model_dump())
    