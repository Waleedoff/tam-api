from fastapi import HTTPException
from app.api.todos.enums import Priority, Status
from app.api.todos.models import Todo
from sqlalchemy.orm import Session
from sqlalchemy import select, or_, func

def get_tasks_(q: str | None, status: Status, priority: Priority, session: Session):
    
    stmt = select(Todo).where(Todo.is_deleted != True)
    
    if status is not None:
        stmt = stmt.where(Todo.status == status)
        
    
    if priority is not None:
        stmt = stmt.where(Todo.priority == priority)
        
        
    if q is not None:
        stmt = stmt.where(
            or_(
         
                func.lower(Todo.title).contains(q.lower()),
                func.lower(Todo.desription).contains(q.lower())

        ))
        
    task: Todo | None = session.execute(stmt).scalar_one_or_none()
    
    if task is None:
        raise HTTPException(detail="task not found", status_code=400)
    
    return task
    