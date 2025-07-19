from sqlalchemy.orm import Session

from app.api.announcement.models import Announcement
from app.api.announcement.schemas import CreateAnnoucementRequest
from app.api.auth.schema import UserResponse


def create_announcement_(body: CreateAnnoucementRequest, session: Session, current_user: UserResponse):
    new_announcement = Announcement(**body.model_dump(), created_by = current_user.id, organization_id='xyz')
    session.add(new_announcement)