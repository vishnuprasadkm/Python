from typing import Annotated
from fastapi import FastAPI, Depends, Path, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette import status
from pydantic import BaseModel, Field

from sqlalchemy.orm import Session
import models
from models import Todos
from database import sql_engine, Sessionlocal

app = FastAPI()

# Only runs when the DB is not present
models.Base.metadata.create_all(bind=sql_engine)


def get_db():
    db = Sessionlocal()

    try:
        yield db
    finally:
        db.close()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=50)
    priority: int = Field(lt=6, gt=0, description="1 being the least till 5")
    complete: bool


# Dependency injection (declares that get_db is needed for the function to work)
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/", status_code=status.HTTP_200_OK)
async def get_all_records(db: db_dependency):
    data = db.query(Todos).all()
    return {"message": "All Records", "length": len(data), "data": data}


@app.get("/todo/{id}", status_code=status.HTTP_200_OK)
# async def get_by_id(db: db_dependency, id: int = Path(gt=0, description="Enter the record ID")):
async def get_by_id(
    id: Annotated[int, (Path(gt=0, description="Enter the record ID"))],
    db: db_dependency,
):
    data = db.query(Todos).filter(Todos.id == id).first()

    if data is not None:
        return {"message": "All Records", "length": 1, "data": data}

    raise HTTPException(status_code=404, detail="Data not found!")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_new_todo(db: db_dependency, todo: TodoRequest):
    todo_model = Todos(**todo.model_dump())

    db.add(todo_model)
    db.commit()


@app.put("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(
    db: db_dependency,
    todo: TodoRequest,
    id: int = Path(gt=0, description="Enter the ID of the record to modify"),
):
    data = db.query(Todos).filter(Todos.id == id).first()

    if data is None:
        raise HTTPException(status_code=401, detail="No data found!")

    data.title = todo.title
    data.description = todo.description
    data.priority = todo.priority
    data.complete = todo.complete

    db.add(data)
    db.commit()


@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    db: db_dependency, id: int = Path(gt=0, description="Enter the todo ID to delete")
):
    data = db.query(Todos).filter(Todos.id == id).first()

    if data is None:
        raise HTTPException(status_code=404, detail="No record found!")

    db.query(Todos).filter(Todos.id == id).delete()
    db.commit()
