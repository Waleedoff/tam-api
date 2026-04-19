

from app.api.auth.schema import UserResponse
from app.api.brd.models import Brd
from app.api.goal.models import Goal, KeyResult
from sqlalchemy.orm import Session
from sqlalchemy import select
def get_key_results_by_goal_id_(goal_id: str, session: Session):
    stmt = select(KeyResult).where(KeyResult.goal_id ==  goal_id)
    krs = session.execute(stmt).scalars().all()
    
    return krs