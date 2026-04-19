# routers/auto_tasks.py
from app.api.room.model import Room, UserStory
from app.api.todos.models import Todo
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from app.dependencies import db_session, get_current_user
from core.langChain.auto_tasks_simple import  _resolve_dept, _norm, pick_assignee_simple
from core.langChain.agent_task_breakdown_simple import run_breakdown_agent
from collections import defaultdict, deque
# أعلى الملف
import random


router = APIRouter(prefix="/auto_tasks", tags=["auto_tasks"])


prefix = "/agent"
tags=['agent']


def _norm_priority(p: str) -> str:
    p = _norm(p)
    return p if p in {"HIGH","MEDIUM","LOW"} else "LOW"
def _dept_key(user) -> str:
    # نفس أسلوبك في _norm: نحول القسم لحروف كبيرة ونعالج None
    return (getattr(user, "department", "") or "").strip().upper()

def _build_all_bucket(members):
    ordered = sorted(
        members,
        key=lambda m: (getattr(m, "full_name", "") or getattr(m, "username", "") or getattr(m, "email", "") or m.id)
    )
    return deque([m.id for m in ordered])


def _pick_rr(buckets, dept: str):
    """
    يأخذ أول عضو من الطابور ويعمل rotate علشان المهمة اللي بعدها تروح للي بعده.
    """
    key = (dept or "").strip().upper()
    q = buckets.get(key)
    if not q:
        return None
    uid = q[0]
    q.rotate(-1)
    return uid


@router.post("/propose")
def propose(room_id: str = Query(...), user_story_id: str = Query(...),
           session: Session = db_session,
           current_user = Depends(get_current_user)):

    # 1) جب البيانات الأساسية
    room: Room = session.query(Room).filter_by(id=room_id).one()
    us: UserStory = session.query(UserStory).filter_by(id=user_story_id).one()

    # 2) نادِ الوكيل
    context = {
        "room_name": room.name,
        "departments": list({(m.department or "").upper() for m in room.members}),
        "user_story": {
            "title": us.title,
            "description": us.description or "",
            "actor": us.actor,
            "acceptance_criteria": us.acceptance_criteria or "",
            "priority": us.priority,
        },
    }
    agent = run_breakdown_agent(context)

    # ✅ 2.1) حضّر طوابير التوزيع لكل قسم
    all_bucket = _build_all_bucket(room.members)
    def _pick_all():
        uid = all_bucket[0]
        all_bucket.rotate(-1)
        return uid

    # 3) ابنِ قائمة مقترحة بسيطة
    recommended: List[Dict] = []
    for t in agent["tasks"]:
        category = t.get("category","BE")
        dept = _resolve_dept(category)  # نفس دالتك اللي ترجع مثلاً DEVOLOPER لـ BE/FE/QA

        # ✅ توزيع Round-Robin داخل نفس القسم
        assignee_id = _pick_all() or room.product_owner_id or current_user.id

        desc = t.get("description") or "-"  # Todo.desription لازم نص غير فاضي
        recommended.append({
            "title": t["title"],
            "desription": desc,                 # مطابق لعمودك
            "priority": _norm_priority(t.get("priority")),
            "status": "PENDING",
            "user_id": assignee_id,             # المكلّف
            "room_id": room.id,
            "sprint_id": us.sprint_id,
            "user_story_id": us.id,
            "category": category,
            "dept_resolved": dept,
        })

    return {"recommended": recommended}

@router.post("/commit")
def commit(payload: Dict,
           session: Session = db_session,
           current_user = Depends(get_current_user)):
    try:
        recommended: List[Dict] = payload.get("recommended", [])
        if not recommended:
            raise ValueError("recommended is empty")

        created_ids: List[str] = []
        for p in recommended:
            # ضمان الحقول الأساسية
            if not p.get("title"):
                continue
            if not p.get("desription"):
                p["desription"] = "-"

            todo = Todo(
                title=p["title"],
                desription=p["desription"],
                priority=_norm_priority(p.get("priority")),
                status="PENDING",
                is_deleted=False,
                user_id=p["user_id"],
                room_id=p["room_id"],
                sprint_id=p.get("sprint_id"),
                user_story_id=p.get("user_story_id"),
                created_by = 'system'
            )
            session.add(todo)
            session.flush()  # يعطينا ID قبل الـ commit
            created_ids.append(todo.id)

        session.commit()
        return {"count": len(created_ids), "ids": created_ids}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=400, detail=str(e))
