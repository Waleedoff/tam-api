from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth.models import User
from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo
from app.api.todos.schema import TodoCreateRequest


def create_task_(body: TodoCreateRequest, session: Session, current_user: UserResponse):
    '''Create a new task and related to current user'''
    user_stmt = select(User).where(User.email == current_user.email)
    user: User | None = session.execute(user_stmt).scalar_one_or_none()
    if user is None:
        raise Exception(detail='user not found', status=401)
    task = Todo(**body.model_dump(),user_id=user.id, created_by=current_user.email)
    session.add(task)
