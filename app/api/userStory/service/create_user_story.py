

from app.api.room.enums import WorkItemType
from app.api.room.model import Room, RoomMember, Sprint, UserStory
from app.api.userStory.enums import PipelineStage
from app.api.userStory.schema import CreateWorkItemRequest
from sqlalchemy.orm import Session
from app.api.auth.schema import UserResponse
from sqlalchemy import select
from decimal import Decimal
from sqlalchemy import select, func, exists
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

def _next_order_rank(session: Session, room_id: str, stage: PipelineStage) -> Decimal:
    stmt = (
        select(func.max(UserStory.order_rank))
        .where(UserStory.room_id == room_id, UserStory.pipeline_stage == stage)
    )
    max_rank = session.execute(stmt).scalar_one_or_none()
    return (max_rank or Decimal("1000")) + Decimal("1000")

def _is_member(session: Session, room_id: str, user_id: str) -> bool:
    q = select(exists().where(RoomMember.room_id == room_id, RoomMember.user_id == user_id))
    return bool(session.execute(q).scalar())

def create_work_item_(
    room_id: str,
    body: CreateWorkItemRequest,
    current_user: UserResponse,
    session: Session
):
    # 1) الغرفة + الصلاحيات
    room = session.execute(select(Room).where(Room.id == room_id)).scalar_one_or_none()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")

    is_po = (room.product_owner_id == current_user.id)
    is_member = _is_member(session, room_id, current_user.id)

    if not (is_po or is_member):
        raise HTTPException(status_code=403, detail="Not a project member")

    # سياسة صلاحيات بسيطة (تقدر تغيّرها):
    if body.work_item_type != WorkItemType.BUG and not is_po:
        raise HTTPException(status_code=403, detail="Only PO can create non-bug items")

    # 2) تحقق sprint_id (اختياري)
    sprint_id = body.sprint_id
    sprint = None
    if sprint_id:
        sprint = session.execute(
            select(Sprint).where(Sprint.id == sprint_id, Sprint.room_id == room_id)
        ).scalar_one_or_none()
        if sprint is None:
            raise HTTPException(status_code=400, detail="Sprint does not belong to this room")

    # 3) احسب order_rank إذا ما أُرسل
    order_rank = Decimal(str(body.order_rank)) if body.order_rank is not None else _next_order_rank(session, room_id, body.pipeline_stage)

    # 4) أنشئ العنصر
    us = UserStory(
        title=body.title,
        description=body.description,
        actor=body.actor.value if body.actor else None,
        actor_custom=body.actor_custom,

        acceptance_criteria=body.acceptance_criteria,
        story_points=body.story_points,

        priority=body.priority,                 # Enum في الموديل
        pipeline_stage=body.pipeline_stage,     # Enum في الموديل
        order_rank=order_rank,

        work_item_type=body.work_item_type,     # عمودك اسمه work_item_type (ليس type)
        extras=body.extras or {},

        room_id=room_id,
        sprint_id=sprint_id,                    # None إذا مو مُجدول

        created_by=current_user.id,
        # status نتركه default = "not_started" من الموديل
    )
    session.add(us)
    session.flush()  # لو تحتاج ترجع id

    return us
