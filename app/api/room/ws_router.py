# from fastapi import WebSocket, WebSocketDisconnect, APIRouter, Depends
# from typing import Dict, List
# from app.dependencies import get_current_user  # المصادقة إذا تحتاج

# router = APIRouter()

# # تخزين الاتصالات لكل غرفة
# active_connections: Dict[str, List[WebSocket]] = {}

# def get_room_connections(room_id: str):
#     if room_id not in active_connections:
#         active_connections[room_id] = []
#     return active_connections[room_id]

# @router.websocket("/ws/rooms/{room_id}")
# async def websocket_endpoint(websocket: WebSocket, room_id: str):
#     await websocket.accept()
#     connections = get_room_connections(room_id)
#     connections.append(websocket)

#     try:
#         while True:
#             data = await websocket.receive_text()
#             # إرسال الرسالة لكل المستخدمين في الغرفة
#             for conn in connections:
#                 if conn != websocket:
#                     await conn.send_text(data)
#     except WebSocketDisconnect:
#         connections.remove(websocket)
