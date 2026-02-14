from util.util import get_db
from tests.util.util import *
from models import Users
from routes.auth import authenticate_user, create_access_token, ALGORITHM, SECRET_KEY

from fastapi import status
from jose import jwt
from datetime import timedelta

app.dependency_overrides[get_db] = override_get_db


def test_authenticate_user(test_user):
    db = TestingSessionLocal()

    user = authenticate_user(test_user.user_name, "user", db)

    assert user is not None
    assert user.user_name == test_user.user_name

    wrong_password_user = authenticate_user(test_user.user_name, "user123", db)

    assert wrong_password_user is False

    invalid_user = authenticate_user("invalidUser", "user123", db)

    assert invalid_user is False


def test_create_access_token(test_user):
    username = "user"
    user_id = 8
    role = "admin"
    expiry_time = timedelta(hours=5)

    token = create_access_token(username, user_id, role, expiry_time)

    decoded_token = jwt.decode(
        token, SECRET_KEY, ALGORITHM, options={"verify_signature": False}
    )

    assert decoded_token["sub"] == username
    assert decoded_token["id"] == user_id
    assert decoded_token["role"] == role


def test_login_for_access_token(test_user):
    res = client.post(
        "/auth/token",
        data={"username": test_user.user_name, "password": "user"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert res.status_code == status.HTTP_200_OK
    assert "access_token" in res.json()
    assert res.json()["token_type"] == "bearer"


def test_login_for_access_token_invalid_user(test_user):
    res = client.post(
        "/auth/token",
        data={"username": test_user.user_name, "password": "user123"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() == {"detail": "Please reverify your credentials"}


def test_create_user(test_user):
    body = {
        "user_name": "user123",
        "email": "test@mail.com",
        "first_name": "user",
        "last_name": "123",
        "password": "user123",
        "phone_number": "9876543207",
    }

    res = client.post("/auth/", json=body)
    assert res.status_code == status.HTTP_201_CREATED

    assert res.json() == {
        "message": "User created!",
        "length": 1,
        "data": {
            "user_name": "user123",
            "email": "test@mail.com",
            "first_name": "user",
            "last_name": "123",
            "phone_number": "9876543207",
            "id": 2,
            "is_active": True,
            "role": None,
        },
    }

    db = TestingSessionLocal()
    data = db.query(Users).filter(Users.id == 2).first()

    assert data is not None
    assert data.user_name == "user123"
