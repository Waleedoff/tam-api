from fastapi import HTTPException
from app.api.todos.enums import Status
from app.api.todos.models import Todo
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.todos.schema import TodoCreateRequest

def edit_task_attribute_(body: TodoCreateRequest,  task_id: str, session: Session):
    
    stmt = select(Todo).where(Todo.id == task_id, Todo.is_deleted != True)
    
    task: Todo | None = session.execute(stmt).scalar_one_or_none()
    
    task.update_attributes(body.model_dump())
    