from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.api.todos.models import Todo


def get_tasks_by_user_story_id_(user_story_id: str, session: Session):
    stmt = select(Todo).where(Todo.user_story_id == user_story_id)
    tasks = session.execute(stmt).scalars().all()
    
    return tasks
    