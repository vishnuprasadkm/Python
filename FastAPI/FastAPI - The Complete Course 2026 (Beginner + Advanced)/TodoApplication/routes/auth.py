from typing import Annotated, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from starlette import status

from datetime import timedelta, timezone, datetime

from jose import jwt
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordRequestForm
import hashlib
from passlib.context import CryptContext

from models import Users
from util.util import db_dependency, user_dependency
from config import SECRET_KEY, ALGORITHM

router = APIRouter(prefix="/auth", tags=["auth"])
# email_pattern = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

argon2_context = CryptContext(schemes=["argon2"], deprecated="auto")


class CreateUserRequest(BaseModel):
    user_name: str = Field(min_length=5)
    email: str = Field(default="test@mail.com")
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=1)
    password: str
    phone_number: str = Field(min_length=10, max_length=10, default="xxxxxxxxxx")
    
    # role: str = Field(default="user")  # role can be given as a additional parameter

    class ConfigDict:   # Config deprecated
        # allow to allow extra fields, ignore to ignore, forbid to reject extra fields in the request body
        extra = "allow"


class Token(BaseModel):
    access_token: str
    token_type: str


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.user_name == username).first()

    if not user:
        return False

    if not argon2_context.verify(password, user.crypt_password):
        return False
    return user


def create_access_token(username: str, user_id: int, role: str, expiry_time: timedelta):

    encodes = {"sub": username, "id": user_id, "role": role}
    expiries = datetime.now(timezone.utc) + expiry_time
    encodes.update({"exp": expiries})

    return jwt.encode(encodes, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, new_user: CreateUserRequest):

    try:
        user_model = new_user.model_dump()
        user_pass = user_model.pop("password")
        user_model["crypt_password"] = argon2_context.hash(user_pass)

        if user_model.get("role") == "":
            user_model["role"] = "user"

        print(user_model)
        user_model = Users(**user_model)
        db.add(user_model)
        db.commit()
        db.refresh(user_model)

        return {
            "message": "User created!",
            "length": 1,
            "data": {
                k: v
                for k, v in user_model.__dict__.items()
                if k not in ["crypt_password", "_sa_instance_state"]
            },
        }
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists"
        )


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    valid_user = authenticate_user(form_data.username, form_data.password, db)

    if not valid_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please reverify your credentials",
        )

    token = create_access_token(
        valid_user.user_name, valid_user.id, valid_user.role, timedelta(minutes=30)
    )
    return {"access_token": token, "token_type": "bearer"}
