from app.api.room.enums import SprintStatus
from app.api.room.model import Sprint, UserStory
from sqlalchemy.orm import Session
from sqlalchemy import select


def fill_sprint_by_their_user_stories_(user_stories_ids: list[str], sprint_id: str, session: Session):
    stmt = select(Sprint).where(Sprint.id == sprint_id, Sprint.status == SprintStatus.PLANNED)
    sprint: Sprint | None = session.execute(stmt).scalar_one_or_none()

    if sprint is None:
        raise Exception('not found any sprint')

    user_stories = session.execute(
        select(UserStory).where(UserStory.id.in_(user_stories_ids))
    ).scalars().all()

    for user_story in user_stories:
        user_story.sprint_id = sprint_id

    session.commit()
