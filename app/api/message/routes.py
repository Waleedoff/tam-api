# app/api/chat/routes.py

from app.api.auth.schema import UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.api.message.schema import MessageResponse
from app.api.message.service.get_messages import get_messages_
from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.common.websocket_admin import ConnectionManager
from app.common.verify_token import verify_token
from app.api.auth.models import User
from app.api.message.models import Message
from app.dependencies import db_session
from app.common.schemas import ValidationErrorLoggingRoute
from datetime import datetime
import json

router = APIRouter(route_class=ValidationErrorLoggingRoute)
manager = ConnectionManager()

prefix = "/chat"
tags = ['chat']

@router.websocket("/ws/rooms/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: str,
    token: str = Query(...),
    session: Session = db_session,
):
    
    # ✅ تحقق من التوكن
    current_user_payload = verify_token(token)
    
    if not current_user_payload:
        await websocket.close(code=1008)
        return

    # ✅ تحقق من وجود المستخدم في قاعدة البيانات
    user_id = current_user_payload.id
    current_user = session.query(User).filter(User.id == user_id).first()
    if not current_user:
        await websocket.close(code=1008)
        return
    
    current_user.is_online = True
    session.commit()

    await manager.connect(websocket, room_id)
    try:
        while True:
            # استقبل الرسالة كـ JSON
            data = await websocket.receive_text()
            try:
                payload = json.loads(data)
                content = payload.get("content")
            except json.JSONDecodeError:
                continue  # تجاهل رسائل غير صالحة

            if not content:
                continue  # تجاهل الرسائل الفارغة

            # ⛳️ حفظ الرسالة
            message = Message(
                content=content,
                room_id=room_id,
                user_id=current_user.id,
                created_by=current_user.id,
                created=datetime.utcnow(),
                updated=datetime.utcnow(),
            )
            session.add(message)
            session.commit()

            # 📡 إرسال الرسالة لجميع المستخدمين
            await manager.broadcast(room_id, {
                "username": current_user.username,
                "message": content
            })

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
        current_user.is_online = False
        session.commit()




@router.get("/{room_id}")
def get_messages(room_id: str, session: Session = db_session, 
                 current_user: UserResponse = Depends(get_current_active_user)) -> list[MessageResponse]:
    return get_messages_(room_id=room_id, current_user=current_user,  session=session)