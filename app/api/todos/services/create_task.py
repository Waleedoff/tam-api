from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo
from app.common.enums import EmailTemplate
from app.dependencies import db_session
from sqlalchemy.orm import Session
from app.api.todos.schema import TodoCreateRequest
# from app.celery_worker.tasks import send_email_task


def create_task_(body: TodoCreateRequest, session: Session, current_user: UserResponse):
    task = Todo(**body.model_dump(), created_by=current_user.email) # TODO we'll add actual user over here.
    session.add(task)
    
    # # send_email_task.apply_async(
    # #     kwargs=dict(
    # #         source_id=f"reset_{task.id}", # TODO WE SHOULD CHANGE TO BE RANDOM 
    # #         source_type=Todo.__name__,
    # #         user_email="user.email",
    # #         subject="Accepted",
    # #         data_to_be_filled={
    # #             "recipient_name": "",
    # #             "email": f"ere@example.com",
    # #             "password": f"demoPass",
    # #         },
    # #         email_template=EmailTemplate.COMPLETED_TASK.value,
    # #     )
    # )
    