from util.util import get_db, get_current_user
from tests.util.util import *
from models import Users

from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all_todos(test_todo):
    res = client.get("/admin/todos")

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "message": "Retrieved all todo's",
        "length": 1,
        "data": [
            {
                "title": "test title",
                "description": "test description",
                "priority": 3,
                "complete": False,
                "user_id": 1,
                "id": 1,
            }
        ],
    }


def test_get_all_admin_users(test_user):
    res = client.get("/admin/admin-users")

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "message": "Data Successfully fetched",
        "length": 1,
        "data": [
            {
                "user_name": "user",
                "email": "mail@mail.com",
                "first_name": "user",
                "last_name": "",
                "is_active": True,
                "role": "admin",
                "phone_number": "9876543209",
                "id": 1,
            }
        ],
    }


def test_get_all_users(test_user):
    res = client.get("/admin/all-users")

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "message": "Data Successfully fetched",
        "length": 1,
        "data": [
            {
                "user_name": "user",
                "email": "mail@mail.com",
                "first_name": "user",
                "last_name": "",
                "is_active": True,
                "role": "admin",
                "phone_number": "9876543209",
                "id": 1,
            }
        ],
    }


def test_delete_user(test_user):
    res = client.delete("/admin/user/1")

    assert res.status_code == status.HTTP_204_NO_CONTENT

    db = TestingSessionLocal()

    data = db.query(Users).filter(Users.id == 1).first()
    assert data is None


def test_delete_user_not_found(test_user):
    res = client.delete("/admin/user/404")

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": "User not found"}
