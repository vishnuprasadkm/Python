from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from main import app
from database import Base
from models import Todos, Users

import pytest
from fastapi.testclient import TestClient
from passlib.context import CryptContext

SQLITE_TEST_DB = "sqlite:///./testdb.db"

engine = create_engine(
    SQLITE_TEST_DB, connect_args={"check_same_thread": False}, poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

argon2_context = CryptContext(schemes=["argon2"], deprecated="auto")

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "test user", "id": 1, "role": "admin"}


client = TestClient(app)


# If autouse is not set or false then need to pass it as an arg in the test case def after the db fixture
@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="test title",
        description="test description",
        priority=3,
        complete=False,
        user_id=1,
    )

    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        user_name="user",
        email="mail@mail.com",
        first_name="user",
        last_name="",
        crypt_password=argon2_context.hash("user"),
        is_active=True,
        role="admin",
        phone_number="9876543209",
    )

    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
