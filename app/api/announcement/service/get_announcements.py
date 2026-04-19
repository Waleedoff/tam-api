from sqlalchemy.orm import Session
from sqlalchemy import select, func
from app.api.announcement.enums import AnnouncementStatus, VoteType
from app.api.announcement.models import Announcement, AnnouncementVote
from app.api.announcement.schemas import CreateAnnoucementResponse
from app.api.auth.schema import UserResponse

def get_announcements_(session: Session, current_user: UserResponse):
    stmt = (
        select(Announcement)
        .where(Announcement.publishing_status == AnnouncementStatus.PUBLISHED.value)
        .order_by(Announcement.created.desc())
    )

    announcements = session.execute(stmt).scalars().all()  # type: ignore

    response: list[CreateAnnoucementResponse] = []

    for announcement in announcements:
        # Count votes for this announcement
        helpful_count = session.scalar(
            select(func.count()).select_from(AnnouncementVote)
            .where(
                AnnouncementVote.announcement_id == announcement.id,
                AnnouncementVote.vote_type == VoteType.HELPFUL,
            )
        ) or 0

        unhelpful_count = session.scalar(
            select(func.count()).select_from(AnnouncementVote)
            .where(
                AnnouncementVote.announcement_id == announcement.id,
                AnnouncementVote.vote_type == VoteType.UNHELPFUL,
            )
        ) or 0

        response.append(
            CreateAnnoucementResponse(
                id=announcement.id,
                title=announcement.title,
                content=announcement.content,
                media_url=announcement.media_url,
                vote=CreateAnnoucementResponse.VoteResponse(
                    helpfull=helpful_count,
                    unhelpfull=unhelpful_count,
                )
            )
        )

    return response
