from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.auth.schema import UserResponse
from app.api.todos.enums import Status
from app.api.todos.models import Todo
from app.api.todos.schema import RecentTasks, TaskStatistics


def get_tasks_statistics_(current_user: UserResponse, session: Session) -> TaskStatistics:
    ''' Count tasks per status & return last five tasks'''
    pending_count = session.scalar(
        select(func.count()).select_from(Todo).where(
            Todo.status == Status.PENDING.value,
            Todo.is_deleted != True,
            Todo.created_by == current_user.email
        )
    )

    in_progress_count = session.scalar(
        select(func.count()).select_from(Todo).where(
            Todo.status == Status.IN_PROGRESS.value,
            Todo.is_deleted != True,
            Todo.created_by == current_user.email
        )
    )

    completed_count = session.scalar(
        select(func.count()).select_from(Todo).where(
            Todo.status == Status.COMPLETED.value,
            Todo.is_deleted != True,
            Todo.created_by == current_user.email
        )
    )

    recent_stmt = select(Todo).where(
        Todo.is_deleted != True,
        Todo.created_by == current_user.email
    ).order_by(Todo.created.desc()).limit(5)

    recent_tasks_raw = session.execute(recent_stmt).scalars().all()

    recent_tasks = [
        RecentTasks(task=todo.title, status=todo.status)
        for todo in recent_tasks_raw
    ]

    return TaskStatistics(
        pending_count=pending_count or 0,
        in_progress=in_progress_count or 0,
        completed=completed_count or 0,
        recent_tasks=recent_tasks
    )
