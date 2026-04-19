from app.api.room.enums import SprintStatus, UserStoryStatus
from app.api.room.model import Sprint, UserStory
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, func, case

def get_sprints_exception_active_(session: Session):
    stmt = (
        select(
            Sprint.id,
            Sprint.name,
            Sprint.description,
            Sprint.start_date,
            Sprint.end_date,
            Sprint.status,
            func.count(UserStory.id).label("total_stories"),
            func.sum(
                case(
                    (UserStory.status == UserStoryStatus.DONE, 1),
                    else_=0
                )
            ).label("completed_stories"),
            func.sum(UserStory.story_points).label("total_points"),
            func.sum(
                case(
                    (UserStory.status == UserStoryStatus.DONE, UserStory.story_points),
                    else_=0
                )
            ).label("completed_points")
        )
        .outerjoin(UserStory, UserStory.sprint_id == Sprint.id)
        .where(
            Sprint.status.in_([
                SprintStatus.PLANNED,
                SprintStatus.COMPLETED
            ])
        )
        .group_by(Sprint.id)
    )

    rows = session.execute(stmt).all()

    result = {
        "planned": [],
        "completed": []
    }

    for row in rows:
        progress = 0
        if row.total_points:
            progress = int((row.completed_points or 0) / row.total_points * 100)

        sprint_data = {
            "id": row.id,
            "name": row.name,
            "description": row.description,
            "start_date": row.start_date,
            "end_date": row.end_date,
            "total_stories": row.total_stories,
            "completed_stories": row.completed_stories or 0,
            "total_points": row.total_points or 0,
            "completed_points": row.completed_points or 0,
            "progress_percentage": progress
        }

        if row.status == SprintStatus.PLANNED:
            result["planned"].append(sprint_data)
        else:
            result["completed"].append(sprint_data)

    return result
