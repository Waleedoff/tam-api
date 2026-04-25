from fastapi.testclient import TestClient


def test_create_task_requires_auth(client: TestClient):
    body = {
        "title": "tam task",
        "desription": "anything you want",
        "status": "TODO",
        "estimate": 1,
        "priority": "HIGH",
        "user_story_id": "non-existent-id",
    }
    response = client.post("/task/", json=body)
    assert response.status_code == 401


def test_create_task_invalid_user_story(client: TestClient, auth_token: str):
    body = {
        "title": "tam task",
        "desription": "anything you want",
        "status": "TODO",
        "estimate": 1,
        "priority": "HIGH",
        "user_story_id": "non-existent-id",
    }
    response = client.post("/task/", json=body, headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 404
