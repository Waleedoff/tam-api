import pytest
from fastapi.testclient import TestClient

# from tests.data import SeedData


# @pytest.fixture
# def create_a_todo_for_2_users(client: TestClient, seed_data: SeedData):

#     res = client.post(
#         url="/todo",
#         json={"title": "user1 todo"},
#         headers={"Authorization": f"Bearer {seed_data.users_tokens[0]}"},
#     )
#     assert res.status_code == 200

#     res = client.post(
#         url="/todo",
#         json={"title": "user2 todo"},
#         headers={"Authorization": f"Bearer {seed_data.users_tokens[1]}"},
#     )
#     assert res.status_code == 200

#     print("two todos has been created one for user1 another for user2")


# def test_list_todos_by_user(client: TestClient, seed_data: SeedData, create_a_todo_for_2_users):

#     res = client.get(
#         url="/todo",
#         headers={"Authorization": f"Bearer {seed_data.users_tokens[0]}"},
#     )
#     assert res.status_code == 200
#     assert len(res.json()) == 1
#     assert res.json()[0]["title"] == "user1 todo"

#     res = client.get(
#         url="/todo",
#         headers={"Authorization": f"Bearer {seed_data.users_tokens[1]}"},
#     )
#     assert res.status_code == 200
#     assert len(res.json()) == 1
#     assert res.json()[0]["title"] == "user2 todo"


# import pytest
# from sqlalchemy.orm import Session

# from app.schemas import TodoCreateRequest
# from app.models import Todo
# from app.crud.todo import create_task_  # غيّر المسار حسب مكانك الفعلي


# @pytest.fixture
# def todo_data():
#     return TodoCreateRequest(
#         title="Test Task",
#         desription="This is a test task",
#     )


from fastapi.testclient import TestClient


def test_create_task_(client: TestClient):
    # assert False,
    body = {
        "title": "tam task",
        "description": "anything you want",
    }
    response = client.post("/task", json=body)
    assert response.status_code == 200
