from sqlalchemy.orm import Session
from sqlalchemy import select
from app.api.todos.enums import Status
from app.api.todos.models import Todo
def get_all_tasks_( session: Session):
    
    stmt = select(Todo)
    
    tasks = session.execute(stmt).scalars().all()
    return tasks
    