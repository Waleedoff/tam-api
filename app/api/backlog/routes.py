from app.api.backlog.schema import BacklogIdsResponse, BacklogResponse, CreateBacklogRequest

from app.api.backlog.service.create_backlog import create_backlog_
from app.api.backlog.service.get_backlog_ids import get_backlog_ids_
from app.api.backlog.service.get_backlogs import get_backlogs_
from fastapi import APIRouter, Depends

from app.api.auth.schema import UserResponse
from app.api.auth.services.authSetup import get_current_active_user


from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session

router = APIRouter(route_class=ValidationErrorLoggingRoute)
prefix = "/backlog"
tags=['backlog']

@router.post('/')
def create_backlog(body: CreateBacklogRequest, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session):
    return create_backlog_(body=body, session=session, current_user=current_user)



@router.get('/')
def get_backlogs(current_user: UserResponse = Depends(get_current_active_user), session: Session =db_session)-> list[BacklogResponse]:
    return get_backlogs_(current_user=current_user, session=session)


@router.get('/ids')
def get_backlog_ids(current_user: UserResponse = Depends(get_current_active_user), session: Session = db_session) -> list[BacklogIdsResponse]:
    return get_backlog_ids_(current_user=current_user, session=session)
 
