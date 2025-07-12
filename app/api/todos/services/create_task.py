from app.api.auth.models import User
from sqlalchemy.orm import Session

from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo
from app.api.todos.schema import TodoCreateRequest
from app.celery_worker.tasks import send_email_task
from app.common.enums import EmailTemplate
from app.common.generate_random_id_uuid import generate_random_uuid
from sqlalchemy import select

def create_task_(body: TodoCreateRequest, session: Session, current_user: UserResponse):
    user_stmt = select(User).where(User.email == current_user.email)
    user: User | None = session.execute(user_stmt).scalar_one_or_none()
    if user is None:
        raise Exception(detail='user not found', status=401)
    task = Todo(**body.model_dump(),user_id=user.id, created_by=current_user.email) # TODO we'll add actual user over here.
    session.add(task)

   