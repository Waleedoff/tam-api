
from sqlalchemy.orm import Session
from app.api.announcement.models import Announcement, AnnouncementComment
from app.api.announcement.schemas import CreateAnnouncementComment
from app.api.auth.schema import UserResponse
from sqlalchemy import select

def create_announcement_comment_(announcement_id: str, body: CreateAnnouncementComment, session: Session, current_user: UserResponse):
    stmt_announcement = select(Announcement).where(Announcement.id == announcement_id)
    annoucement: Announcement | None = session.execute(stmt_announcement).scalar_one_or_none()
    if annoucement is None:
        raise Exception('this annoucement not available.')
    
    comment = AnnouncementComment(**body.model_dump(), announcement_id=annoucement.id, user_id = current_user.id, created_by=current_user.id )
    session.add(comment)