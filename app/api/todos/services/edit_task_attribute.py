from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.todos.models import Todo
from app.api.todos.schema import TodoCreateRequest


def edit_task_attribute_(body: TodoCreateRequest,  task_id: str, session: Session):
    '''Edit task body if any'''
    stmt = select(Todo).where(Todo.id == task_id, Todo.is_deleted != True)

    task: Todo | None = session.execute(stmt).scalar_one_or_none()

    task.update_attributes(body.model_dump())
