# from app.api.backlog.model import Backlog
# from app.api.brd.models import Brd
# from app.api.goal.models import Goal, KeyResult
# from app.api.room.model import UserStory
# from app.api.todos.models import Todo
# from app.api.todos.schema import TodoResponse
# from app.common.redis_client import RedisClient
# from fastapi import HTTPException
# from sqlalchemy import Sequence, desc, func, or_, select
# from sqlalchemy.orm import Session, joinedload

# from typing import Any, List
from app.api.auth.schema import UserResponse
from app.api.goal.models import KeyResult
from app.api.todos.models import Todo
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.orm import joinedload


def get_tasks_(current_user: UserResponse, session: Session):
    stmt = (select(Todo).where(Todo.user_id == current_user.id).options(
            joinedload(Todo.key_results)
            .joinedload(KeyResult.goal)
        ))
    
    result = session.execute(stmt).scalars().unique().all()

    return result