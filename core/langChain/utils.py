from app.api.auth.schema import UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.common.enums import Role
from fastapi import Depends, HTTPException  

SENSITIVE_KEYWORDS = [
    "password", "كلمة المرور", "email", "رقم", "phone", "secret",
    "ssn", "رقم الهوية", "رقم سري", "الرقم السري", "age", "العمر"
]

def is_sensitive_question(question: str) -> bool:
    return any(word.lower() in question.lower() for word in SENSITIVE_KEYWORDS)


def can_use_ai(current_user: UserResponse = Depends(get_current_active_user)):
    if current_user.role != Role.MANAGER:
        raise HTTPException(status_code=403, detail="Not allowed to use AI assistant")
    return current_user
