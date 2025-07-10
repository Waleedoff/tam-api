import pytest
from fastapi.testclient import TestClient


def test_create_task_(client: TestClient):
    body = {
        "title": "tam task",
        "description": "anything you want",
    }
    response = client.post("/task", json=body)
    assert response.status_code == 200
