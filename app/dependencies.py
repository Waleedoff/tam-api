from threading import Lock

from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from app.api.auth.models import User
from app.api.auth.schema import UserResponse
from app.common.verify_token import verify_token

from app.common.enums import Department, Role
from fastapi import Depends, WebSocket
from sqlalchemy import column, table
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select
from fastapi import HTTPException
from app.common.redis_client import get_redis_client
from app.config import BaseConfig, config
from app.db.db import BaseDb


from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer


db = BaseDb(config)

def get_current_user() -> User:
    # هنا تستخرج المستخدم من التوكن
    return User(department=Department.BUSINESS, role=Role.SPECIALIST)

def get_current_user_department(user: User = Depends(get_current_user)) -> Department:
    return user.department

def get_current_user_role(user: User = Depends(get_current_user)) -> Role:
    return user.role


async def get_current_user_ws(websocket: WebSocket):
    token = websocket.query_params.get("token")
    user = verify_token(token)  # ارجع مستخدم حقيقي
    if not user:
        await websocket.close()
        raise Exception("Unauthorized")
    return user



# --- DB Session Dependencies ---
def get_db_session_dependency(SessionLocal):
    def get_db_session():
        session: Session = SessionLocal()
        try:
            with session.begin():
                yield session
        finally:
            session.close()

    return get_db_session



# src/dependencies/permissions.py

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # مجرد placeholder

def role_required(*allowed_roles: str):
    def dependency(token: str = Depends(oauth2_scheme)):
        payload = verify_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid token")

        user_role = payload.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="You don't have access")

        return payload  # يمكنك إعادة الـ payload لاستخدامها في الـ endpoint نفسه

    return Depends(dependency)




# --- Redis Client Dependency ---


def get_redis_dependency(config: BaseConfig):
    def _get_redis_client():
        return get_redis_client(config)

    return _get_redis_client


# --- Feature Flags Dependency ---
def get_feature_flags_dependency(config: BaseConfig, db: BaseDb):
    local_cache: TTLCache = TTLCache(
        maxsize=config.FEATURE_FLAG_LOCAL_CASH_SIZE_LIMIT,
        ttl=config.FEATURE_FLAG_LOCAL_CACHING_TTL,
    )
    lock = Lock()

    def _get_feature_flags():
        session: Session = db.SessionLocal()
        results = session.execute(
            select(
                table(
                    "feature_flags",
                    column("key"),
                    column("value"),
                )
            )
        )
        feature_flags = results.all()
        session.close()
        return {key: value for key, value in feature_flags}

    @cached(cache=local_cache, key=hashkey, lock=lock)
    def get_cached_feature_flags():
        return _get_feature_flags()

    return get_cached_feature_flags


# --- Pre-initialized Dependencies ---
get_db_session = get_db_session_dependency(db.SessionLocal)
db_session = Depends(get_db_session)

get_db_read_session = get_db_session_dependency(db.ReadSessionLocal)
db_read_session = Depends(get_db_read_session)

redis_client = Depends(get_redis_dependency(config=config))
feature_flags = Depends(get_feature_flags_dependency(config, db))
