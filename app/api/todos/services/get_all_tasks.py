from sqlalchemy.orm import Session
from sqlalchemy import func, select,or_
from app.api.todos.enums import Status
from app.api.todos.models import Todo
def get_all_tasks_(q: str, session: Session):
    stmt = select(Todo).where(Todo.is_deleted == False)
    
    if q is not None:
        stmt.where(
            or_(
                func.lower(Todo.title).contains(q.lower()),                
            )
        )
    
    tasks = session.execute(stmt).scalars().all()
    return tasks
    