from app.api.sprint.schema import CreateSprintRequest, SprintPreviewResponse
from app.api.sprint.service.create_sprint import create_sprint_
from app.api.sprint.service.get_sprints import get_sprints_
from app.api.userStory.schema import CreateWorkItemRequest, CreateUserStoryResponse
from app.api.userStory.service.create_user_story import create_work_item_
from app.api.userStory.service.get_backlog_list import get_backlog_list_
from app.api.userStory.service.get_user_story import get_user_story_
from fastapi import APIRouter, Depends

from app.api.auth.schema import  UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/work_item"
tags=['work_item']

@router.post('/{room_id}')
def create_work_item(room_id: str,  body: CreateWorkItemRequest, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session):
    return create_work_item_(room_id=room_id, body=body, session=session, current_user=current_user)



@router.get('xxx/{room_id}')
def get_backlog_list(room_id: str, current_user: UserResponse = Depends(get_current_active_user), session: Session = db_session):
    return get_backlog_list_(room_id = room_id, current_user= current_user, session=session)
    
    

# TODO MAYBE NEED IT LATER.
@router.get('/{room_id}/{sprint_id}')
def get_user_story(room_id: str, sprint_id: str, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session)-> list[CreateUserStoryResponse]:
    return get_user_story_(room_id=room_id, sprint_id=sprint_id, session=session, current_user=current_user)
