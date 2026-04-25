from fastapi.testclient import TestClient


def test_register_user_(client: TestClient):
    body ={
  "full_name": "waleedp",
  "username": "waleedp",
  "password": "product",
  "email": "waleedp@example.com",
  "gender": "MALE",
  "department": "DEVOLOPER",
  "role": "product"
}
    response = client.post("/auth/register", json=body)
    assert response.status_code == 200
