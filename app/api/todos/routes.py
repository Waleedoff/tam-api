
from fastapi import APIRouter
from app.api.todos.enums import Priority, Status
from app.api.todos.schema import TodoCreateRequest, TodoResponse
from app.api.todos.services.create_task import create_task_
from app.api.todos.services.delete_task import delete_task_
from app.api.todos.services.edit_task import edit_task_
from app.api.todos.services.get_tasks import get_tasks_
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session



router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/task"
tags=['task']  

@router.get("")
def get_taks(status: Status, priority: Priority ,q: str | None = None,  session: Session = db_session)-> TodoResponse:
    return get_tasks_(q=q, status=status, priority=priority, session=session)

@router.post('')
def create_task(body: TodoCreateRequest, session: Session = db_session):
    
    return create_task_(body= body, session=session)


@router.put('/{task_id}')
def delete_task(task_id: str, session: Session = db_session):
    
    return delete_task_(task_id= task_id, session=session)


@router.put('/{task_id}/edit')
def edit_task(body: TodoCreateRequest, task_id: str, session: Session = db_session):
    
    return edit_task_(body = body, task_id = task_id, session=session)

