from app.api.room.model import Room
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth.models import User
from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo
from app.api.todos.schema import TodoCreateRequest


def create_task_(body: TodoCreateRequest, room_id: str, sprint_id: str, user_story_id: str,   session: Session, current_user: UserResponse):
    '''Create a new task and related to current user'''
    stmt = select(Room).where(Room.id == room_id)
    room = session.execute(stmt).scalar_one_or_none()
    if room is None:
        raise Exception('room not found')
    user_stmt = select(User).where(User.email == current_user.email)
    
    # TODO check on the sprint_id and user_story_id and make it inside it if any. otherwise make it backlog
    user: User | None = session.execute(user_stmt).scalar_one_or_none()
    if user is None:
        raise Exception(detail='user not found', status=401)
    task = Todo(**body.model_dump(),user_id=user.id, created_by=current_user.email,room_id=room_id, sprint_id=sprint_id, user_story_id=user_story_id )
    session.add(task)
