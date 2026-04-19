

from app.api.auth.schema import UserResponse
from app.api.goal.models import Goal
from sqlalchemy.orm import Session
from sqlalchemy import select



def get_goals_ids_(session: Session):
    stmt = select(Goal)
    ids = session.execute(stmt).scalars().all()
    return ids