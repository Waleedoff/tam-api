


from app.api.auth.schema import UserResponse
from app.api.backlog.model import Backlog
from sqlalchemy.orm import Session
from sqlalchemy import select
def get_backlog_ids_(current_user: UserResponse, session: Session):
    
    stmt = select(Backlog)

    
    backlogs = session.execute(stmt).scalars().all()
    return backlogs