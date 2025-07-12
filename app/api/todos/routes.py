
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.auth.schema import UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.api.todos.enums import Status
from app.api.todos.schema import TaskStatistics, TodoCreateRequest, TodoResponse
from app.api.todos.services.create_task import create_task_
from app.api.todos.services.delete_task import delete_task_
from app.api.todos.services.edit_task import edit_task_
from app.api.todos.services.edit_task_attribute import edit_task_attribute_
from app.api.todos.services.get_task_by_id import get_task_by_id_
from app.api.todos.services.get_task_statistics import get_tasks_statistics_
from app.api.todos.services.get_tasks import get_tasks_
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/task"
tags=['task']


@router.get('/statistics')
def get_tasks_statistics(session: Session = db_session,
                         current_user: UserResponse = Depends(get_current_active_user)
                         )-> TaskStatistics:
    return get_tasks_statistics_(session=session, current_user=current_user)


@router.get('')
def get_taks(q: str | None = None,  session: Session = db_session,
             current_user: UserResponse = Depends(get_current_active_user)
             )-> list[TodoResponse]:
    return get_tasks_(q=q, session=session, current_user=current_user)

@router.post('')
def create_task(body: TodoCreateRequest, session: Session = db_session,
                current_user: UserResponse = Depends(get_current_active_user)):

    return create_task_(current_user=current_user, body= body, session=session)


@router.put('/{task_id}')
def delete_task(task_id: str, session: Session = db_session):

    return delete_task_(task_id= task_id, session=session)



@router.put('/{task_id}/status')
def edit_task(task_id: str,status: Status,  current_user: UserResponse = Depends(get_current_active_user),  session: Session = db_session):

    return edit_task_(current_user=current_user, status = status, task_id = task_id, session=session)



@router.get('/{task_id}')
def get_task_by_id(task_id: str, session: Session = db_session):

    return get_task_by_id_(task_id= task_id, session=session)


@router.put('/{task_id}/edit')
def edit_task_attribute(body: TodoCreateRequest, task_id: str, session: Session = db_session):

    return edit_task_attribute_(body = body, task_id = task_id, session=session)



