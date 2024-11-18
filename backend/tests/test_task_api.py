from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_task_retrieve_list():
    # Test task list retrieval
    response = client.get("/tasks")
    assert response.status_code == 200

    # Test task creation
    response = client.post(
        "/tasks",
        json={
            "name": "Test Task",
            "content": "This is a test task content",
            "url": "https://webwatch.live/test",
            "discord_url": "string",
            "enabled_notification_options": ["EMAIL"],
            "enabled": True,
        },
    )
    assert response.status_code == 201