

from app.api.auth.schema import UserResponse
from app.api.goal.models import Goal, KeyResult
from app.api.goal.schema import CreateGoalReques

from sqlalchemy.orm import Session

def create_goal_(body: CreateGoalReques, current_user: UserResponse, session: Session):
    
    goal = Goal(**body.model_dump(exclude="key_results"), created_by = current_user.id)
    session.add(goal)
    session.flush()

    key_results = [
            KeyResult(**kr.model_dump(), goal_id=goal.id, created_by=current_user.id)
            for kr in body.key_results
        ]
    
    '''
    تخيل مطعم:
```
👨‍🍳 الطباخ (SQLAlchemy) = يستقبل الطلبات
🍕 الطلب الواحد (Object) = KeyResult
📦 صندوق طلبات (List) = [KeyResult, KeyResult]
الطباخ يقول:

"أعطني طلب واحد في كل مرة!"

أنت أعطيته:

صندوق كامل فيه 5 طلبات دفعة وحدة!

الطباخ يصرخ:

"ما أقدر أطبخ صندوق! أعطني الطلبات واحد واحد!"
    
    '''
    
    # TODO check what does that diffrent between session.add_all vs session.add cause i guess one for sqlalchemy object and some for another
    session.add_all(key_results)
    session.refresh(goal)
        # 3. حفظ كل شيء
    session.commit()
        
    # TODO remember that issue when return data inside data CHECK ON THAT PROBLEM
    return goal