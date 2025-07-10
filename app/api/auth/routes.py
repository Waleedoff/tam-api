from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.auth.schema import CreateUserRequest, Token, UserLoginRequest, UserResponse
from app.api.auth.services.authSetup import (
    get_current_active_user,
)
from app.api.auth.services.user_login import user_login_
from app.api.auth.services.user_register import user_register_
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import db_session

router =  APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/auth"
tags = ["auth"]


@router.post("/register",)
async def user_register(body: CreateUserRequest, session: Session = db_session):
    return user_register_(body=body, session=session)


@router.post("/login",)
def user_login(body: UserLoginRequest, session:Session = db_session)->Token:
    form_data = OAuth2PasswordRequestForm(
        username=body.username,
        password=body.password,
        scope="",           # إذا كنت لا تستخدم scopes
        client_id=None,
        client_secret=None,
    )

    return user_login_(form_data = form_data, session=session)





# @router.get("/user/me/items")
# async def read_own_items(current_user: UserResponse = Depends(get_current_active_user)):
#     return [{"item_id": 1, "owner": current_user}]
