from fastapi.testclient import TestClient
from server import app
import argon2

client = TestClient(app)

"""
# Removed until user delete is implemented?
def test_user_register_success():
    # Test user registration
    response = client.post("/users/register", json={"email": "test@webwatch.live", "password": "Password1233!"})
    assert response.status_code == 201
"""


def test_user_register_fail_duplicate():
    # Test user registration with duplicate username
    response = client.post(
        "/users/register",
        json={"email": "test@webwatch.live", "password": "Password1233!!!"},
    )
    assert response.status_code == 409


def test_user_login_fail():
    # Test user login with wrong password
    try:
        response = client.post(
            "/users/login",
            data={
                "grant_type": "password",
                "username": "test@webwatch.live",
                "password": "WrongPassword1233!!",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        assert response.status_code == 400
    except argon2.exceptions.VerifyMismatchError:
        pass  # This is expected
    else:
        assert False, "Expected VerifyMismatchError was not raised"


def test_user_login_success():
    # Test user login with correct password
    response = client.post(
        "/users/login",
        data={
            "grant_type": "password",
            "username": "test@webwatch.live",
            "password": "Password1233!",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200


def test_user_verify():
    # Test user verification
    response = client.post(
        "/users/login",
        data={
            "grant_type": "password",
            "username": "test@webwatch.live",
            "password": "Password1233!",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    response = client.get(f"/users/verify?token={access_token}")
    assert response.status_code == 200
    assert response.json() == {"email": "test@webwatch.live"}


def test_user_me():
    # Test user me
    response = client.post(
        "/users/login",
        data={
            "grant_type": "password",
            "username": "test@webwatch.live",
            "password": "Password1233!",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    response = client.get(
        "/users/me", headers={"Authorization": "Bearer " + access_token}
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@webwatch.live"


def test_user_me_no_auth():
    # Test user me without auth
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_user_reset_password_success():
    # Test password reset
    response = client.post(
        "/users/login",
        data={
            "username": "test@webwatch.live",
            "password": "Password1233!",
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    access_token = response.json()["access_token"]
    response = client.post(
        "/users/reset_password",
        json={
            "new_password": "NewPassword1233!!",
            "confirm_password": "NewPassword1233!!",
        },
        headers={"Authorization": "Bearer " + access_token},
    )

    assert response.status_code == 200


def test_user_reset_password_mismatch():
    # Test password reset with mismatched passwords
    response = client.post(
        "/users/login",
        data={
            "username": "test@webwatch.live",
            "password": "NewPassword1233!!",
        },
    )
    headers = ({"Content-Type": "application/x-www-form-urlencoded"},)
    assert response.status_code == 200
    access_token = response.json()["access_token"]

    response = client.post(
        "/users/reset_password",
        json={
            "new_password": "NewPassword1233!!",
            "confirm_password": "MismatchedPassword1233!!",
        },
        headers={"Authorization": "Bearer " + access_token},
    )

    assert response.status_code == 422
