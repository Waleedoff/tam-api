import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import column, select, table, insert
from sqlalchemy.orm import Session, scoped_session
from sqlalchemy_utils import create_database, drop_database

from app.celery_worker.tasks import celery
from app.config import config
from app.db.db import BaseDb
from app.main import app

base_db = BaseDb(config)
ScopedSession = scoped_session(base_db.SessionLocal, scopefunc=lambda: "")


def get_celery_test_task():
    class TestCustomTask(celery.Task):
        _session = None

        def before_start(self, *args, **kwargs):
            ScopedSession().flush()
            self._session = None

        def after_return(self, *args, **kwargs):
            if self._session is not None:
                self._session.flush()

        @property
        def app_config(self):
            return config

        @property
        def session(self):
            if self._session is None:
                self._session = ScopedSession()
            return self._session

    return TestCustomTask


def get_db_session_overwrite():
    test_session = ScopedSession()
    test_session.expire_all()
    nested = test_session.begin_nested()

    try:
        yield test_session
        if nested.is_active:
            nested.commit()
    except Exception:
        if nested.is_active:
            nested.rollback()
        raise


@pytest.fixture(autouse=True)
def transaction_flag():
    db_connection = base_db.engine.connect()
    db_connection.begin()
    ScopedSession(bind=db_connection)
    yield
    ScopedSession.remove()
    db_connection.close()


@pytest.fixture()
def session():
    return ScopedSession()


@pytest.fixture(scope="session")
def client() -> TestClient:  # type: ignore
    from app.dependencies import get_db_session, get_db_read_session
    
    app.dependency_overrides[get_db_session] = get_db_session_overwrite
    app.dependency_overrides[get_db_read_session] = get_db_session_overwrite

    try:
        create_database(base_db.engine.url)
    except Exception as e:
        print("⚠️ Could not create database:", e)

    os.system("alembic upgrade head")
    celery.Task = get_celery_test_task()

    yield TestClient(app=app)

    base_db.engine.dispose()
    drop_database(base_db.engine.url)
