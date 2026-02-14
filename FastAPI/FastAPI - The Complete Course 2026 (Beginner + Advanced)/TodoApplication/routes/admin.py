from fastapi import APIRouter, HTTPException
from starlette import status

from models import Todos, Users
from util.util import db_dependency, user_dependency

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/todos", status_code=status.HTTP_200_OK)
async def get_all_todos(db: db_dependency, user: user_dependency):
    if user.get("role") == "admin":
        data = db.query(Todos).all()

        if data:
            return {
                "message": "Retrieved all todo's",
                "length": len(data),
                "data": data,
            }
        raise HTTPException(status_code=404, detail="Data not found!")
    raise HTTPException(status_code=404, detail="Access Denied!")


@router.get("/admin-users", status_code=status.HTTP_200_OK)
async def get_all_admin_users(db: db_dependency, user: user_dependency):
    if user and user.get("role") == "admin":
        data = db.query(Users).filter(Users.role == "admin").all()

        if data:
            mod_data = [
                {
                    k: v
                    for k, v in u.__dict__.items()
                    if k not in ["crypt_password", "_sa_instance_state"]
                }
                for u in data
            ]
            return {
                "message": "Data Successfully fetched",
                "length": len(data),
                "data": mod_data,
            }
        raise HTTPException(status_code=404, detail="Data not found!")
    raise HTTPException(status_code=404, detail="Access Denied!")


@router.get("/all-users", status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency, user: user_dependency):
    if user.get("role") == "admin":
        data = db.query(Users).all()

        if data:
            mod_data = [
                {
                    k: v
                    for k, v in u.__dict__.items()
                    if k not in ["crypt_password", "_sa_instance_state"]
                }
                for u in data
            ]
            return {
                "message": "Data Successfully fetched",
                "length": len(data),
                "data": mod_data,
            }
        raise HTTPException(status_code=404, detail="Data not found!")
    raise HTTPException(status_code=404, detail="Access Denied!")


@router.delete("/user/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_users(db: db_dependency, user: user_dependency, id: int):
    valid_user = db.query(Users).filter(Users.id == id).first()

    if user.get("role") != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not Authorized"
        )

    if valid_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    db.query(Users).filter(Users.id == id).delete()
    db.commit()
