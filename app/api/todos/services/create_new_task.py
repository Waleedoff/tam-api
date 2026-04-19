from app.api.backlog.model import Backlog
from app.api.room.model import UserStory
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException, status

from app.api.auth.models import User
from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo
from app.api.todos.schema import TodoCreateRequest


def create_new_task_(
    body: TodoCreateRequest,
    session: Session,
    current_user: UserResponse
):
    """Create task with enforced relationships and consistency"""
    # -------------------------
    # 1. Get current user
    # -------------------------
    user = session.execute(
        select(User).where(User.email == current_user.email)
    ).scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # -------------------------
    # 2. Get UserStory + العلاقات
    # -------------------------
    stmt = (
        select(UserStory)
        .where(UserStory.id == body.user_story_id)
        .options(
            joinedload(UserStory.backlog)
            .joinedload(Backlog.key_results)
        )
    )

    user_story = session.execute(stmt).scalar_one_or_none()


    if not user_story:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserStory not found"
        )

    # -------------------------
    # 3. Validate relations
    # -------------------------
    if not user_story.backlog:
        raise HTTPException(
            status_code=400,
            detail="UserStory has no backlog"
        )

    if not user_story.backlog.key_results:
        raise HTTPException(
            status_code=400,
            detail="Backlog has no KeyResult"
        )

    key_result = user_story.backlog.key_results

    # -------------------------
    # 4. Create Task
    # -------------------------
    task = Todo(**body.model_dump(), 
        user_id=user.id,
        created_by=current_user.id,
        key_result_id=key_result.id,  # 🔥 enforced from backend
    )

    session.add(task)
    session.commit()

    return task