

from app.api.announcement.schemas import GetAllAnnouncementComment
from app.api.auth.schema import UserResponse
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from app.api.announcement.models import Announcement, AnnouncementComment
def get_announcement_comments_(announcement_id: str, session: Session, current_user: UserResponse):
    stmt_announcement = select(AnnouncementComment).where(AnnouncementComment.announcement_id == announcement_id).options(joinedload(AnnouncementComment.user)).order_by(AnnouncementComment.created.desc())
    
    
    
    comments = session.execute(stmt_announcement).scalars().all()
    
    return [
        GetAllAnnouncementComment(
            content=c.content,
            username = c.user.username,
            created=c.created
        )
        for c in comments
    ]
    