

from app.api.auth.schema import UserResponse
from app.api.brd.models import Brd
from app.api.brd.schema import CreateBrdRequest
from sqlalchemy.orm import Session

def create_brd_(body: CreateBrdRequest, session: Session, current_user: UserResponse):
    brd = Brd(**body.model_dump(),created_by = current_user.id)
    session.add(brd)

    