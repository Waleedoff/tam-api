from app.api.brd.models import Brd
from sqlalchemy.orm import Session
from sqlalchemy import select

def get_brd_ids_(session: Session):

    stmt = select(Brd)
    brds = session.execute(stmt).scalars().all()

    return brds