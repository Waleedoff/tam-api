# services/auto_tasks_simple.py
from typing import List, Optional

from app.api.auth.models import User

# ثبّت الماب حسب أقسامك (DEVOLOPER/BUSINESS/HR/FINAINC)
CATEGORY_TO_DEPT = {
    "BE": "DEVOLOPER",
    "FE": "DEVOLOPER",
    "API": "DEVOLOPER",
    "DB": "DEVOLOPER",
    "QA": "DEVOLOPER",
    "DEVOPS": "DEVOLOPER",
    "PM": "BUSINESS",
    "DOCS": "BUSINESS",
    "HR": "HR",
    "PAYROLL": "FINAINC",
    "BILLING": "FINAINC",
}

def _norm(s: str) -> str:
    return (s or "").strip().upper()

def _resolve_dept(category: str) -> str:
    return CATEGORY_TO_DEPT.get(_norm(category), "DEVOLOPER")

def pick_assignee_simple(members: List[User], dept: str) -> Optional[str]:
    dept = _norm(dept)
    for m in members:
        if _norm(m.department) == dept:
            return m.id
    return None  # ما لقينا أحد
