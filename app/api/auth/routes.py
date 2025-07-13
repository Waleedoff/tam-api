
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.auth.schema import CreateUserRequest, Token, UserLoginRequest
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
        scope="",
        client_id=None,
        client_secret=None,
    )

    return user_login_(form_data = form_data, session=session)
