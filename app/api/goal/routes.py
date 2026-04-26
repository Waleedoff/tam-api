from app.api.goal.schema import CreateGoalReques, CreateGoalResponse, GoalResponse
from app.api.goal.services.create_goal import create_goal_
from app.api.goal.services.get_goals_ids import get_goals_ids_
from app.api.goal.services.get_key_results_by_id import get_key_results_by_goal_id_
from app.api.goal.services.get_my_goals import get_my_goals_
from fastapi import APIRouter, Depends

from app.api.auth.schema import UserResponse
from app.api.auth.services.authSetup import get_current_active_user


from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session
from sqlalchemy.orm import Session

router = APIRouter(route_class=ValidationErrorLoggingRoute)
prefix = "/goal"
tags=['goal']

@router.post('')
def create_goal(body: CreateGoalReques, current_user: UserResponse = Depends(get_current_active_user), session:Session = db_session):
    return create_goal_(body=body, session=session, current_user=current_user)




@router.get('')
def get_my_goals(current_user:UserResponse = Depends(get_current_active_user), session: Session=db_session)-> list[CreateGoalResponse]:
    return get_my_goals_(current_user=current_user, session= session)


@router.get('/ids')
def get_goals_ids( session: Session=db_session) -> list[GoalResponse]:
    return get_goals_ids_( session=session)




@router.get('/{goal_id}')
def get_key_results_by_goal_id(goal_id: str, session: Session = db_session,):
    return get_key_results_by_goal_id_(goal_id=goal_id, session = session)