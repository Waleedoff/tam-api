


from app.api.auth.models import User
from app.api.auth.schema import UserResponse
from app.api.brd.models import Brd
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_brd_(current_user: UserResponse, session: Session):
    stmt = select(Brd)
    brds = session.execute(stmt).scalars().all()

    return brds