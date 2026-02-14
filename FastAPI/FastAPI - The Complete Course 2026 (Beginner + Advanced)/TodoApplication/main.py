from fastapi import FastAPI
import models
from database import sql_engine
from routes import auth, todos, admin, user

app = FastAPI()

# Only runs when the DB is not present
models.Base.metadata.create_all(bind=sql_engine)

@app.get("/active-status")
def active_status():
    return {"status": "active"}

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)
