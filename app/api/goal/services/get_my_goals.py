


from app.api.auth.schema import UserResponse
from app.api.goal.models import Goal
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select

def get_my_goals_(current_user: UserResponse, session: Session):
    stmt = (
    select(Goal)
    .where(Goal.created_by == current_user.id)
    .options(joinedload(Goal.key_results))
)

    goals = session.execute(stmt).scalars().unique().all()
    # TODO EXPLAINATION WHY WE USED UNIQUE OVER THERE.
    '''
    instead of using unique keyword result will be:
    [
    Goal(id=1),
    Goal(id=1),
    Goal(id=2)
    ]

    but when we use it then result will be:

    [
    Goal(id=1, key_results=[A, B]),
    Goal(id=2, key_results=[C])
    ]
    '''
    return goals

