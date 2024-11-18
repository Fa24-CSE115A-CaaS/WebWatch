from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def register_user():
    response = client.post("/users/register", json={"email": "test@webwatch.live", "password": "Password1233!"})
    assert response.status_code == 201
    return response.json()["access_token"]

access_token = register_user()

def test_task_retrieve_list():
    # Test task list retrieval
    response = client.get("/tasks", headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200

def test_task_create():
    # Test task creation
    response = client.post(
        "/tasks",
        headers={"Authorization": "Bearer " + access_token},
        json={
            "name": "Test Task",
            "content": "",
            "url": "https://webwatch.live/test",
            "discord_url": "string",
            "enabled_notification_options": ["EMAIL"],
            "enabled": True,
        },
    )
    assert response.status_code == 201