
from app.api.auth.schema import UserResponse
from app.api.backlog.model import Backlog
from app.api.backlog.schema import CreateBacklogRequest
from sqlalchemy.orm import Session

def create_backlog_(body: CreateBacklogRequest, current_user: UserResponse, session: Session):   
    backlog = Backlog(**body.model_dump(), key_result_id="69bf108d-e5f0-40be-ac30-812170001339", created_by = current_user.id)
    session.add(backlog)
    
    return