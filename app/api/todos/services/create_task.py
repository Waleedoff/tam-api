from app.api.todos.models import Todo
from app.dependencies import db_session
from sqlalchemy.orm import Session
from app.api.todos.schema import TodoCreateRequest


def create_task_(body: TodoCreateRequest, session: Session):
    task = Todo(**body.model_dump(), created_by='tam-user') # TODO we'll add actual user over here.
    session.add(task)
    