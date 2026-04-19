from app.api.auth.schema import UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.api.brd.schema import BrdResponse, CreateBrdRequest, getBrdIdResponse
from app.api.brd.service.create_brd import create_brd_
from app.api.brd.service.get_brd import get_brd_
from app.api.brd.service.get_brd_ids import get_brd_ids_
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import db_session
from app.common.schemas import ValidationErrorLoggingRoute

router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/brd"
tags=['brd']

@router.post('/')
def create_brd(body: CreateBrdRequest, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session):
    return create_brd_(body=body, session=session, current_user = current_user)

@router.get('/')
def get_brd(current_user: UserResponse = Depends(get_current_active_user), session: Session = db_session)-> list[BrdResponse]:
    return get_brd_(current_user=current_user, session=session)

@router.get('/ids')
def get_brd_ids(session: Session = db_session)-> list[getBrdIdResponse]:
    return get_brd_ids_( session=session)