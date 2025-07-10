from threading import Lock
from collections.abc import Callable

from cachetools import TTLCache, cached
from cachetools.keys import hashkey
from fastapi import Depends
from sqlalchemy import column, table
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import select

from app.db.db import BaseDb
from app.config import BaseConfig, config

db = BaseDb(config)


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


# --- Redis Client Dependency ---
from app.common.redis_client import get_redis_client


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
