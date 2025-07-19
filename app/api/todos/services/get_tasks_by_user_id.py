from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.todos.models import Todo
def get_tasks_by_user_id_(user_id: str, session: Session):
    stmt = select(Todo).where(Todo.user_id == user_id)
    tasks = session.execute(stmt).scalars().all()
    
    return tasks
    