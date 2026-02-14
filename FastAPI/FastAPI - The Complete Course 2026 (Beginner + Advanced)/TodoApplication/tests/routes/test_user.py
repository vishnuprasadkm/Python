from util.util import get_current_user, get_db
from tests.util.util import *
from models import Todos, Users

from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_user_details(test_user):
    res = client.get("/user/")

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "message": "User Details",
        "length": 1,
        "data": {
            "user_name": "user",
            "email": "mail@mail.com",
            "first_name": "user",
            "last_name": "",
            "is_active": True,
            "role": "admin",
            "phone_number": "9876543209",
            "id": 1,
        },
    }


def test_change_password(test_user):
    res = client.put(
        "user/change-password", json={"password": "user", "new_password": "user1"}
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"message": "Password changed"}


def test_change_password_same_password(test_user):
    res = client.put(
        "user/change-password", json={"password": "user", "new_password": "user"}
    )

    assert res.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert res.json() == {
        "detail": "New password can't match the old password",
    }


def test_change_password_wrong_password(test_user):
    res = client.put(
        "user/change-password", json={"password": "user1", "new_password": "user"}
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
    assert res.json() == {
        "detail": "Old password does not match, please re verify",
    }


def test_change_phone_number(test_user):
    res = client.put("user/change-phone-number", json={"phone_number": "1234567890"})

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {"message": "Phone number updated successfully!"}


def test_change_phone_number_invalid(test_user):
    res = client.put("user/change-phone-number", json={"phone_number": "1234567890897981"})

    assert res.status_code == status.HTTP_406_NOT_ACCEPTABLE
    assert res.json() == {"detail": "Phone number must be between 10 and 13 digits (including optional country code)."}
