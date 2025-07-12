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

    send_email_task.apply_async(
    kwargs=dict(
        source_id=f"task_completed_{task.id}_{generate_random_uuid()}",
        source_type=Todo.__name__,
        user_email=current_user.email,  # Replace "user.email" with actual user instance
        subject="Task Completed",
        data_to_be_filled={
            "recipient_name": current_user.username ,
            "email": current_user.email,
            "task_title": task.title,
            "task_priority": task.priority,
            "task_status": task.status
        },
        email_template=EmailTemplate.COMPLETED_TASK.value,
    )
)
