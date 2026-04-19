from app.api.auth.models import User
from app.api.auth.schema import UserResponse
from app.api.room.enums import RoomMemberRole, RoomMemberStatus
from app.api.room.model import Room, RoomMember
from app.api.room.schema import CreateRoomReques
from sqlalchemy.orm import Session  
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError

def create_room_(body: CreateRoomReques, current_user: UserResponse, session: Session):
    # 1) جهّز قائمة الأعضاء (أضمن إدخال المنشئ دائماً)
    member_ids = set(body.members or [])
    member_ids.add(current_user.id)

    users = session.query(User).filter(User.id.in_(member_ids)).all()
    found_ids = {u.id for u in users}
    missing = member_ids - found_ids
    if missing:
        raise HTTPException(status_code=400, detail=f"Unknown member ids: {sorted(missing)}")

    # 2) أنشئ الغرفة بدون members/created_by (استخدم user_id)
    room = Room(
        **body.model_dump(exclude={"members", "product_owner_id"}),  # باقي الحقول من الـbody
        user_id=current_user.id,  # المنشئ
        created_by=current_user.id,
    )

    # 3) عيّن الـPO (افتراضي المنشئ إن ما أُرسل)
    po_id = getattr(body, "product_owner_id", None) or current_user.id
    room.product_owner_id = po_id
    if po_id not in found_ids:
        raise HTTPException(status_code=400, detail="product_owner_id must be included in members")

    session.add(room)
    session.flush()  # عشان room.id

    # 4) أنشئ عضويات المشروع
    for u in users:
        role = RoomMemberRole.PO if u.id == po_id else RoomMemberRole.MEMBER
        room.members_assoc.append(
            RoomMember(
                room_id=room.id,
                user_id=u.id,
                role_in_room=role,
                status=RoomMemberStatus.ACTIVE,
                created_by=current_user.id,
            )
        )

    # 5) حفظ
    try:
        session.flush()
    except IntegrityError as e:
        session.rollback()
        raise HTTPException(status_code=400, detail="Room create failed (integrity): "+str(e.orig))

    session.refresh(room)
    return room