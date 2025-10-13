
from app.common.enums import Role
from app.common.redis_client import RedisClient
from app.common.utils import make_cache_key
from core.langChain.utils import can_use_ai, is_sensitive_question
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Query
from core.langChain.agent import get_sql_agent
from app.api.auth.schema import UserResponse
from app.api.auth.services.authSetup import get_current_active_user
from app.api.todos.enums import Status
from app.api.todos.schema import TaskStatistics, TodoCreateRequest, TodoResponse
from app.api.todos.services.create_task import create_task_
from app.api.todos.services.delete_task import delete_task_
from app.api.todos.services.edit_task import edit_task_
from app.api.todos.services.edit_task_attribute import edit_task_attribute_
from app.api.todos.services.get_all_tasks import get_all_tasks_
from app.api.todos.services.get_task_by_id import get_task_by_id_
from app.api.todos.services.get_task_statistics import get_tasks_statistics_
from app.api.todos.services.get_tasks import get_tasks_
from app.api.todos.services.get_tasks_by_user_id import get_tasks_by_user_id_
from app.common.schemas import ValidationErrorLoggingRoute
from app.dependencies import  db_session, redis_client
from core.langChain.agent import get_sql_agent


router = APIRouter(route_class=ValidationErrorLoggingRoute)

prefix = "/task"
tags=['task']


@router.get("/langchain-query")
def query_database(
    q: str = Query(...),
    current_user: UserResponse = Depends(can_use_ai),
    redis_client: RedisClient = redis_client
    ):
    if is_sensitive_question(q):
        return {"response": "⚠️ عذرًا، لا يمكنني مشاركة هذه المعلومة الحساسة."}

    key = make_cache_key(q)

    cached_answer = redis_client.get_data(key)
    if cached_answer:
        print('take it form cache'*10)
        return {"response": cached_answer}

    agent = get_sql_agent()     # TODO check this is the best way to running the agent.
    result = agent.run(q)

    redis_client.cache_data(key, result, ex=3600 * 24) # keep in mind 3600 -> equal an hour and you said (3600 * 24) it means a day

    return {"response": result}


@router.get('/statistics')
def get_tasks_statistics(session: Session = db_session,
                         current_user: UserResponse = Depends(get_current_active_user)
                         )-> TaskStatistics:
    return get_tasks_statistics_(session=session, current_user=current_user)


@router.get('/{user_story_id}')
def get_taks(user_story_id: str, q: str | None = None,  session: Session = db_session, redis_client: RedisClient = redis_client,
             current_user: UserResponse = Depends(get_current_active_user)
             )-> list[TodoResponse]:
    return get_tasks_(user_story_id=user_story_id,  q=q, redis_client=redis_client, session=session, current_user=current_user)


@router.get('/workspace')
def get_all_taks(q: str | None = None,  session: Session = db_session)-> list[TodoResponse]:
    return get_all_tasks_(q=q, session=session)




@router.post('')
def create_task(room_id: str, body: TodoCreateRequest,sprint_id: str | None, user_story_id: str| None = None, session: Session = db_session,
                current_user: UserResponse = Depends(get_current_active_user)):

    return create_task_(room_id=room_id, sprint_id=sprint_id, user_story=user_story_id , current_user=current_user, body= body, session=session)


@router.put('/{task_id}')
def delete_task(task_id: str, session: Session = db_session):

    return delete_task_(task_id= task_id, session=session)


@router.put('/{task_id}/status')
def edit_task(task_id: str,status: Status, redis_client: RedisClient = redis_client,  current_user: UserResponse = Depends(get_current_active_user),
              session: Session = db_session):

    return edit_task_(redis_client=redis_client,current_user=current_user, status = status, task_id = task_id, session=session)

@router.get('/{task_id}')
def get_task_by_id(task_id: str, session: Session = db_session):
    return get_task_by_id_(task_id= task_id, session=session)

@router.put('/{task_id}/edit')
def edit_task_attribute(body: TodoCreateRequest, task_id: str, session: Session = db_session):

    return edit_task_attribute_(body = body, task_id = task_id, session=session)


@router.get('/{user_id}/tasks')
def get_tasks_by_user_id(user_id: str, session: Session = db_session) -> list[TodoResponse]:
    return get_tasks_by_user_id_(user_id=user_id, session=session)

