
from app.api.auth.schema import UserResponse
from app.api.todos.models import Todo
from app.api.todos.schema import TodoUsersResponse
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

def get_room_tasks_(room_id: str, session: Session, current_user: UserResponse):
    stmt = (
        select(Todo)
        .options(joinedload(Todo.user))  # حمل معلومات المستخدم المرتبط بكل مهمة
        .where(Todo.room_id == room_id)
    )
    tasks = session.execute(stmt).scalars().all()
   
   
    result: list[TodoUsersResponse] = []
    for task in tasks:
        task_response = TodoUsersResponse(
            id=task.id,
            title=task.title,
            desription=task.desription,
            priority=task.priority,
            status=task.status,
            created=task.created,
            user_info=
                UserResponse(
                    id=task.user.id,
                    username=task.user.username,
                    full_name=task.user.full_name,
                    department=task.user.department,
        role=task.user.role
                )
          
        )
        result.append(task_response)

    return result