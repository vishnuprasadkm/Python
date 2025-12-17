from typing import Annotated
from fastapi import APIRouter, Path, HTTPException

from models import Todos
from starlette import status
from pydantic import BaseModel, Field
from util.util import db_dependency, user_dependency

router = APIRouter(prefix="/todo", tags=["todos"])


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(lt=6, gt=0, description="1 being the least till 5")
    complete: bool


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_records(user: user_dependency, db: db_dependency):
    data = []
    if user.get("role") == "admin":
        data = db.query(Todos).all()
    else:
        data = db.query(Todos).filter(Todos.user_id == user.get("id")).all()

    return {"message": "All Records", "length": len(data), "data": data}


@router.get("/{id}", status_code=status.HTTP_200_OK)
# async def get_by_id(db: db_dependency, id: int = Path(gt=0, description="Enter the record ID")):
async def get_by_id(
    id: Annotated[int, (Path(gt=0, description="Enter the record ID"))],
    user: user_dependency,
    db: db_dependency,
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Authenticate"
        )

    data = []
    if user.get("role") == "admin":
        data = db.query(Todos).filter(Todos.id == id).first()
    else:
        data = (
            db.query(Todos)
            .filter(Todos.user_id == user.get("id"))
            .filter(Todos.id == id)
            .first()
        )

    if data is not None:
        return {"message": "All Records", "length": 1, "data": data}

    raise HTTPException(status_code=404, detail="Data not found!")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_new_todo(user: user_dependency, db: db_dependency, todo: TodoRequest):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please Authenticate",
        )

    todo_model = Todos(**todo.model_dump(), user_id=user.get("id"))

    db.add(todo_model)
    db.commit()
    db.refresh(todo_model)

    return {"message": "Todo Created!", "data": todo_model}


@router.put("/{id}", status_code=status.HTTP_200_OK)
async def update_todo(
    db: db_dependency,
    user: user_dependency,
    todo: TodoRequest,
    id: int = Path(gt=0, description="Enter the ID of the record to modify"),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Authenticate"
        )

    data = []
    if user.get("role") == "admin":
        data = db.query(Todos).filter(Todos.id == id).first()
    else:
        data = (
            db.query(Todos)
            .filter(Todos.user_id == user.get("id"))
            .filter(Todos.id == id)
            .first()
        )

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No data found!"
        )

    data.title = todo.title
    data.description = todo.description
    data.priority = todo.priority
    data.complete = todo.complete

    db.add(data)
    db.commit()
    return {"message": "Todo updated!", "data": data}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_todo(
    db: db_dependency,
    user: user_dependency,
    id: int = Path(gt=0, description="Enter the todo ID to delete"),
):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Please Authenticate"
        )

    data = []
    if user.get("role") == "admin":
        data = db.query(Todos).filter(Todos.id == id).first()
    else:
        data = (
            db.query(Todos)
            .filter(Todos.user_id == user.get("id"))
            .filter(Todos.id == id)
            .first()
        )

    if data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No record found!"
        )

    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()
    return {"message": f"{id} data deleted!"}
