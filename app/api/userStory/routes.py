from app.api.sprint.service.create_sprint import create_sprint_
from app.api.userStory.schema import CreateUserStoryRequest, CreateUserStoryResponse
from app.api.userStory.service.create_user_story import create_user_story_
from app.api.userStory.service.get_backlog_list import get_backlog_list_
from app.api.userStory.service.get_current_user_story import get_current_user_story_
from app.api.userStory.service.get_user_story import get_user_story_
from fastapi import APIRouter, Depends

from app.api.auth.schema import  UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/user_story"
tags=['user_story']

@router.post('/')
def create_user_story(body: CreateUserStoryRequest, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session):
    return create_user_story_( body=body, session=session, current_user=current_user)


# TODO MAYBE NEED IT LATER.
@router.get('/')
def get_user_story( session:Session = db_session)-> list[CreateUserStoryResponse]:
    return get_user_story_(session=session)



@router.get('xxx/{room_id}')
def get_backlog_list(room_id: str, current_user: UserResponse = Depends(get_current_active_user), session: Session = db_session):
    return get_backlog_list_(room_id = room_id, current_user= current_user, session=session)
    

@router.get('/current_user_story')
def get_current_user_story(session: Session = db_session, ):
    return get_current_user_story_(session=session,)
    
