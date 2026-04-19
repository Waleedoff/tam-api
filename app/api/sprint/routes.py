from app.api.sprint.schema import CreateSprintRequest, SprintOverviewResponse, SprintPreviewResponse
from app.api.sprint.service.create_sprint import create_sprint_
from app.api.sprint.service.get_current_sprints import get_current_sprints_and_their_user_stories_
from app.api.sprint.service.get_sprints_exception_active import get_sprints_exception_active_
from fastapi import APIRouter, Depends

from app.api.auth.schema import GetMemeberInfoResponse, UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/sprint"
tags=['sprint']

@router.post('/')
def create_sprint( body: CreateSprintRequest, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session):
    return create_sprint_(body=body, session=session, current_user=current_user)

@router.get('/overview', response_model=SprintOverviewResponse)
def get_sprints_exception_active(session: Session = db_session):
    return get_sprints_exception_active_(session=session)


# TODO return it in the schema response 
@router.get('/active')
def get_current_sprints_and_their_user_stories( session:Session = db_session)-> list[SprintPreviewResponse]:
    return get_current_sprints_and_their_user_stories_( session=session)



