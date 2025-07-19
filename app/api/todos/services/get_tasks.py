from app.api.todos.schema import TodoResponse
from app.common.redis_client import RedisClient
from fastapi import HTTPException
from sqlalchemy import Sequence, desc, func, or_, select
from sqlalchemy.orm import Session

from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo
def get_tasks_(q: str | None, redis_client: RedisClient, current_user: UserResponse, session: Session):
    '''Get all tasks belong to current user'''
    cache_key = f"user_tasks:{current_user.id}:{q or 'all'}"
    
    if cached := redis_client.get_data(cache_key):
        print('take it from cache\n')
        return cached  # Return cached tasks

    stmt = select(Todo).where(
        Todo.is_deleted != True,
        Todo.created_by == current_user.email
    ).order_by(desc(Todo.created))

    if q is not None:
        stmt = stmt.where(
            or_(
                func.lower(Todo.title).contains(q.lower()),
                func.lower(Todo.desription).contains(q.lower())
            )
        )

    task: Sequence[Todo] = session.execute(stmt).scalars().all()

    if not task:
        raise HTTPException(detail="task not found", status_code=200)
    serialized_tasks = [TodoResponse.model_validate(t, from_attributes=True).model_dump() for t in task]

    redis_client.cache_data(cache_key, serialized_tasks,)  # Cache for 5 minutes (optional)
    return task
