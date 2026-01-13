from fastapi import APIRouter, HTTPException
from starlette import status
from pydantic import BaseModel

from passlib.context import CryptContext
import bcrypt

from util.util import db_dependency, user_dependency
from models import Users

router = APIRouter(prefix="/user", tags=["user"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class ChangePasswordRequest(BaseModel):
    password: str
    new_password: str


@router.get("/")
async def get_user_details(db: db_dependency, user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed!")

    data = db.query(Users).filter(Users.id == user.get("id")).first()

    if not data:
        raise HTTPException(status_code=404, detail="User not found!")

    mod_data = {
        k: v
        for k, v in data.__dict__.items()
        if k not in ["crypt_password", "_sa_instance_state"]
    }

    if mod_data:
        return {"message": "User Details", "length": len(mod_data), "data": mod_data}


@router.put("/change-password", status_code=status.HTTP_200_OK)
async def change_password(
    new_pass: ChangePasswordRequest, db: db_dependency, user: user_dependency
):
    if not user:
        raise HTTPException(status_code=401, detail="Authentication failed!")

    req_user = db.query(Users).filter(Users.id == user.get("id")).first()

    if req_user is None:
        raise HTTPException(status_code=404, detail="Data not found!")

    if new_pass.password == new_pass.new_password:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="New password can't match the old password",
        )

    if not bcrypt_context.verify(new_pass.password, req_user.crypt_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Old password does not match, please re verify",
        )

    req_user.crypt_password = bcrypt_context.hash(new_pass.new_password)
    db.add(req_user)
    db.commit()

    return {"message": "Password changed"}
