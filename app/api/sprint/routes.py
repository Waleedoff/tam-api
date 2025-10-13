from app.api.sprint.schema import CreateSprintRequest, SprintPreviewResponse
from app.api.sprint.service.create_sprint import create_sprint_
from app.api.sprint.service.get_sprints import get_sprints_
from fastapi import APIRouter, Depends

from app.api.auth.schema import GetMemeberInfoResponse, UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/sprint"
tags=['sprint']

@router.post('/{room_id}')
def create_sprint(room_id: str, body: CreateSprintRequest, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session):
    return create_sprint_(room_id=room_id, body=body, session=session, current_user=current_user)





# TODO return it in the schema response 
@router.get('/{room_id}')
def get_sprints(room_id: str,  current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session)-> list[SprintPreviewResponse]:
    return get_sprints_(room_id=room_id, session=session, current_user=current_user)



