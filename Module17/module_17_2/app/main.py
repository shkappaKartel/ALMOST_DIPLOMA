from fastapi import FastAPI
from Module17.module_17_1.app.routers import task, user
import Module17.module_17_2.app.models.user as user_model
import Module17.module_17_2.app.models.task as task_model

app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)


@app.get('/')
async def welcome():
    return {"message": "Welcome to Taskmanager"}
