from util.util import get_db, get_current_user
from tests.util.util import *
from models import Todos

from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all_authenticated(test_todo):
    response = client.get("/todo/")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "message": "All Records",
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


def test_get_by_id(test_todo):
    res = client.get("/todo/1")

    assert res.status_code == status.HTTP_200_OK
    assert res.json() == {
        "message": "All Records",
        "length": 1,
        "data": {
            "title": "test title",
            "description": "test description",
            "priority": 3,
            "complete": False,
            "user_id": 1,
            "id": 1,
        },
    }


def test_get_by_id_not_found(test_todo):
    res = client.get("todo/2")

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": "Data not found!"}


def test_create_new_todo(test_todo):
    body = {
        "title": "new test todo title",
        "description": "new test todo description",
        "priority": 5,
        "complete": False,
    }

    res = client.post("/todo", json=body)
    assert res.status_code == status.HTTP_201_CREATED
    assert "message" in res.json()
    assert res.json()["data"]["priority"] == 5

    db = TestingSessionLocal()

    data = db.query(Todos).filter(Todos.id == 2).first()

    assert data is not None
    assert data.title == body.get("title")
    assert data.description == body.get("description")
    assert data.priority == body.get("priority")
    assert data.complete == body.get("complete")


def test_update_todo(test_todo):
    body = {
        "title": "updated test title",
        "description": "updated test description",
        "priority": 5,
        "complete": False,
    }

    res = client.put("/todo/1", json=body)

    assert res.status_code == status.HTTP_200_OK
    assert "message" in res.json()

    db = TestingSessionLocal()

    data = db.query(Todos).filter(Todos.id == 1).first()

    assert data is not None
    assert data.title == body.get("title")
    assert data.description == body.get("description")
    assert data.priority == body.get("priority")
    assert data.complete == body.get("complete")


def test_update_todo_not_found(test_todo):
    body = {
        "title": "updated test title",
        "description": "updated test description",
        "priority": 5,
        "complete": False,
    }

    res = client.put("/todo/2", json=body)

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": "No data found!"}


def test_delete_todo(test_todo):
    res = client.delete("/todo/1")

    assert res.status_code == status.HTTP_200_OK
    assert "message" in res.json()

    db = TestingSessionLocal()

    data = db.query(Todos).filter(Todos.id == 1).first()

    assert data is None


def test_delete_todo_not_found(test_todo):
    res = client.delete("/todo/404")

    assert res.status_code == status.HTTP_404_NOT_FOUND
    assert res.json() == {"detail": "No record found!"}
