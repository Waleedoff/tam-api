from fastapi import APIRouter, Depends

from app.api.auth.schema import GetMemeberInfoResponse, UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.api.room.schema import CreateRoomReques, RoomPreviewResponse
from app.api.room.service.create_room import create_room_
from app.api.room.service.get_my_rooms import get_my_rooms_
from app.api.room.service.get_room_members import get_room_members_
from app.api.room.service.get_room_tasks import get_room_tasks_
from app.api.room.service.publish_room import publish_room_
from app.api.room.service.unpublish import unpublish_room_
from app.api.todos.schema import  TodoCreateRequest, TodoUsersResponse
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/room"
tags=['room']



@router.post('/')
def create_room(body: CreateRoomReques, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session):
    return create_room_(body=body, session=session, current_user=current_user)




@router.post('/publish/{room_id}')
def publish_room( session: Session= db_session, current_user: UserResponse = Depends(get_current_active_user)):
    return publish_room_(session=session, current_user=current_user)



@router.post('/unpublish/{room_id}')
def unpublish_room( session: Session= db_session, current_user: UserResponse = Depends(get_current_active_user)):
    return unpublish_room_(session=session, current_user=current_user)

 

@router.post('/{room_id}')
def unpublish_room( session: Session= db_session, current_user: UserResponse = Depends(get_current_active_user)):
    return unpublish_room_(session=session, current_user=current_user)


@router.get("/me")
def get_my_rooms(session: Session= db_session, current_user: UserResponse = Depends(get_current_active_user)) -> list[RoomPreviewResponse]:
    return get_my_rooms_(session=session, current_user=current_user)

@router.get("/members/{room_id}")
def get_room_members(room_id: str, session: Session = db_session, current_user: UserResponse = Depends(get_current_active_user))-> list[GetMemeberInfoResponse]:
    return get_room_members_(room_id=room_id, session=session, current_user=current_user)




@router.get("/tasks/{room_id}")
def get_room_tasks(room_id: str, session: Session = db_session, current_user: UserResponse = Depends(get_current_active_user))-> list[TodoUsersResponse]:
    return get_room_tasks_(room_id=room_id, session=session, current_user=current_user)




@router.get("/me/product-owner")
def get_my_product_owner_rooms(session: Session= db_session, current_user: UserResponse = Depends(get_current_active_user)) -> list[RoomPreviewResponse]:
    return get_my_product_owner_rooms_(session=session, current_user=current_user)
