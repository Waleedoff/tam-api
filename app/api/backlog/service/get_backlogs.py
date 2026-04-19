

from app.api.auth.schema import UserResponse
from app.api.backlog.model import Backlog
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_backlogs_(session: Session, current_user: UserResponse):
    stmt = select(Backlog)
    bgs = session.execute(stmt).scalars().all()
    return bgs