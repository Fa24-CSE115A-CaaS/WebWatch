from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


def register_user():
    response = client.post(
        "/users/register",
        json={"email": "test@webwatch.live", "password": "Password1233!"},
    )
    assert response.status_code == 201
    return response.json()["access_token"]


access_token = register_user()


def test_task_retrieve_list():
    # Test task list retrieval
    response = client.get("/tasks", headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200


def test_task_retrieve_no_auth():
    # Test task list retrieval without authorization
    response = client.get("/tasks")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_task_create():
    # Test task creation
    response = client.post(
        "/tasks",
        headers={"Authorization": "Bearer " + access_token},
        json={
            "name": "Test Task",
            "url": "https://webwatch.live/test",
            "enabled_notification_options": ["EMAIL"],
            "enabled": True,
        },
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_task_create_no_auth():
    # Test task creation without authorization
    response = client.post(
        "/tasks",
        json={
            "name": "Test Task",
            "url": "https://webwatch.live/test",
            "enabled_notification_options": ["EMAIL"],
            "enabled": True,
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_task_edit():
    # Test task editing
    response = client.put(
        "/tasks/1",
        headers={"Authorization": "Bearer " + access_token},
        json={
            "name": "Test Task edited",
            "url": "https://webwatch.live/test",
            "enabled_notification_options": ["EMAIL"],
            "enabled": True,
        },
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Task edited"


def test_task_edit_no_auth():
    # Test task editing without authorization
    response = client.put(
        "/tasks/1",
        json={
            "name": "Test Task edited",
            "url": "https://webwatch.live/test",
            "enabled_notification_options": ["EMAIL"],
            "enabled": True,
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_task_retrieve_not_empty():
    # Test task list retrieval with tasks
    response = client.get("/tasks", headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert response.json() != []


def test_task_delete_no_auth():
    # Test task deletion without authorization
    response = client.delete("/tasks/1")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_task_delete_success():
    # Test task deletion
    response = client.delete(
        "/tasks/1", headers={"Authorization": "Bearer " + access_token}
    )
    assert response.status_code == 204


def test_task_delete_fail():
    # Test task deletion failure
    response = client.delete(
        "/tasks/1", headers={"Authorization": "Bearer " + access_token}
    )
    assert response.status_code == 404


def test_task_retrieve_empty():
    # Test task list retrieval with no tasks
    response = client.get("/tasks", headers={"Authorization": "Bearer " + access_token})
    assert response.status_code == 200
    assert response.json() == []
