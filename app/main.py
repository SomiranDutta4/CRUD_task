from fastapi import FastAPI
from routes.task_route import taskRouter
from routes.user_route import userRouter
from routes.admin import adminRoute

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Task Manager API"}

app.include_router(taskRouter,prefix='/task')
app.include_router(userRouter,prefix='/user')
app.include_router(adminRoute,prefix='/admin')