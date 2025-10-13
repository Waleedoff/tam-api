from app.api.todos.schema import TodoResponse
from app.common.redis_client import RedisClient
from fastapi import HTTPException
from sqlalchemy import Sequence, desc, func, or_, select
from sqlalchemy.orm import Session

from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo
def get_tasks_(user_story_id: str, q: str | None, redis_client: RedisClient, current_user: UserResponse, session: Session):
    '''Get all tasks belong to current user'''
    

    stmt = select(Todo).where(
        Todo.is_deleted != True,
        Todo.user_story_id == user_story_id
    ).order_by(desc(Todo.created))

    if q is not None:
        stmt = stmt.where(
            or_(
                func.lower(Todo.title).contains(q.lower()),
                func.lower(Todo.desription).contains(q.lower())
            )
        )

    task: Sequence[Todo] = session.execute(stmt).scalars().all()
    # if not task:
    #     raise HTTPException(detail="task not found", status_code=400)

    return task
