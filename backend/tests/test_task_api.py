from fastapi.testclient import TestClient
from constants.task import MIN_INTERVAL_SECONDS, MAX_INTERVAL_SECONDS
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

TASK_DATA = {
    "name": "Test Task",
    "url": "https://webwatch.live/test",
    "enabled_notification_options": ["EMAIL"],
    "interval": MIN_INTERVAL_SECONDS,
    "enabled": True,
}


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
        json=TASK_DATA,
    )
    assert response.status_code == 201
    assert response.json()["id"] == 1


def test_task_create_interval_too_small():
    # Test task creation
    task_data = TASK_DATA.copy()
    task_data["interval"] = MIN_INTERVAL_SECONDS - 1
    response = client.post(
        "/tasks",
        headers={"Authorization": "Bearer " + access_token},
        json=task_data,
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "interval"


def test_task_create_interval_too_large():
    # Test task creation
    task_data = TASK_DATA.copy()
    task_data["interval"] = MAX_INTERVAL_SECONDS + 1
    response = client.post(
        "/tasks",
        headers={"Authorization": "Bearer " + access_token},
        json=task_data,
    )
    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"][1] == "interval"


def test_task_create_no_auth():
    # Test task creation without authorization
    response = client.post(
        "/tasks",
        json=TASK_DATA,
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


def test_user_delete_success():
    # Test user deletion
    response = client.delete(
        "/users/delete",
        headers={"Authorization": "Bearer " + access_token},
    )
    assert response.status_code == 200

    # Verify user is deleted
    response = client.post(
        "/users/login",
        data={
            "grant_type": "password",
            "username": "test@webwatch.live",
            "password": "Password1233!",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
