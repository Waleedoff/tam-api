from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth.schema import UserResponse
from app.api.todos.enums import Status
from app.api.todos.models import Todo
from app.celery_worker.tasks import send_email_task
from app.common.enums import EmailTemplate
from app.common.generate_random_id_uuid import generate_random_uuid


def edit_task_(current_user: UserResponse, status: Status,  task_id: str, session: Session):
    '''
    Edit task status, but keep in mind if status
    changed to be completed will recieve and email
    '''
    stmt = select(Todo).where(Todo.id == task_id,Todo.is_deleted != True)

    task: Todo | None = session.execute(stmt).scalar_one_or_none()

    if task is None:
        raise HTTPException(detail="task not found", status_code=400)

    if status == Status.COMPLETED.value:
        send_email_task.apply_async(
        kwargs=dict(
            source_id=f"task_completed_{task.id}_{generate_random_uuid()}",
            source_type=Todo.__name__,
            user_email=current_user.email,
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

    task.status = status.value
