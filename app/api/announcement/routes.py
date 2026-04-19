
from fastapi import APIRouter, Depends
from fastapi.params import Depends

from app.api.announcement.service.announceComment import create_announcement_comment_
from app.api.announcement.enums import VoteType
from app.api.announcement.schemas import CreateAnnoucementRequest, CreateAnnoucementResponse, CreateAnnouncementComment, GetAllAnnouncementComment
from app.api.announcement.service.create_announcement import create_announcement_
from app.api.announcement.service.get_announcement_comments import get_announcement_comments_
from app.api.announcement.service.get_announcements import get_announcements_
from app.api.announcement.service.vote_on_announcement import vote_on_announcement_
from app.api.auth.schema import UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session


router =  APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/announcement"
tags = ["announcement"]



@router.post('/')
def create_announcement(body: CreateAnnoucementRequest, session: Session = db_session, current_user: UserResponse = Depends(get_current_active_user)):
    return create_announcement_(body=body, session=session, current_user=current_user)


@router.get('/')
def get_announcements(session: Session = db_session, current_user: UserResponse = Depends(get_current_active_user)) -> list[CreateAnnoucementResponse]:
    return get_announcements_(session=session, current_user=current_user)



@router.post("/{announcement_id}/vote", response_model=None)
def vote_on_announcement(announcement_id: str, vote: VoteType, session: Session = db_session, current_user: UserResponse = Depends(get_current_active_user)):
    return vote_on_announcement_(announcement_id=announcement_id, vote=vote,  session=session, current_user=current_user )

@router.post('/{announcement_id}/comment')
def create_announcement_comment(announcement_id: str, body: CreateAnnouncementComment, session: Session = db_session, current_user: UserResponse = Depends(get_current_active_user)):
    return create_announcement_comment_(announcement_id= announcement_id, body=body, session=session, current_user=current_user)



@router.get('/{announcement_id}/comments')
def get_announcement_comments(announcement_id: str, session: Session = db_session, current_user: UserResponse = Depends(get_current_active_user))-> list[GetAllAnnouncementComment]:
    return get_announcement_comments_(announcement_id= announcement_id, session=session, current_user=current_user)

