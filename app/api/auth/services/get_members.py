
from typing import Sequence
from app.api.auth.models import User
from sqlalchemy.orm import Session
from sqlalchemy import select, func
def get_memebers_(q: str,  session: Session):
    
    stmt = select(User)
    if q is not None:
        stmt = stmt.where(
            func.lower(User.username).contains(q.lower()),
        )
    
    member: Sequence[User] = session.execute(stmt).scalars().all()
    return member