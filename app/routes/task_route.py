from fastapi import APIRouter, HTTPException
from typing import List
from bson import ObjectId

from database.db import db
from schemas.task_schema import (
    TaskSchema,
    TaskResponse,
    TaskUpdateSchema
)

taskRouter = APIRouter()


@taskRouter.get("/", response_model=List[TaskResponse])
async def get_tasks(user_id: str):

    own_tasks = await db.tasks.find(
        {
            "user_id": user_id
        }
    ).to_list(None)

    juniors = await db.users.find(
        {
            "manager_id": user_id
        }
    ).to_list(None)

    junior_ids = [
        str(user["_id"])
        for user in juniors
    ]

    admin_tasks = []

    if junior_ids:
        admin_tasks = await db.tasks.find(
            {
                "user_id": {
                    "$in": junior_ids
                },
                "self_task": False
            }
        ).to_list(None)

    tasks = own_tasks + admin_tasks

    return [
        TaskResponse(
            id=str(task["_id"]),
            title=task["title"],
            user_id=task["user_id"],
            description=task.get("description"),
            completed=task["completed"],
            isUpdated=task.get("isUpdated", False),
            self_task=task["self_task"]
        )
        for task in tasks
    ]


@taskRouter.post("/", response_model=TaskResponse)
async def post_task(
    task: TaskSchema,
    user_id: str,
    target_user: str
):

    target_user_doc = await db.users.find_one(
        {
            "_id": ObjectId(target_user)
        }
    )

    if not target_user_doc:
        raise HTTPException(
            status_code=404,
            detail="Target user not found"
        )

    if (
        user_id != target_user
        and str(target_user_doc.get("manager_id")) != user_id
    ):
        raise HTTPException(
            status_code=403,
            detail="Don't have permission"
        )

    new_task = {
        "title": task.title,
        "description": task.description,
        "completed": False,
        "isUpdated": False,
        "user_id": target_user,
        "self_task": user_id == target_user
    }

    result = await db.tasks.insert_one(
        new_task
    )

    created_task = await db.tasks.find_one(
        {
            "_id": result.inserted_id
        }
    )

    return TaskResponse(
        id=str(created_task["_id"]),
        title=created_task["title"],
        user_id=created_task["user_id"],
        description=created_task.get("description"),
        completed=created_task["completed"],
        isUpdated=created_task["isUpdated"],
        self_task=created_task["self_task"]
    )


@taskRouter.put(
    "/{task_id}",
    response_model=TaskResponse
)
async def update_task(
    task_id: str,
    updated_task: TaskUpdateSchema,
    user_id: str
):

    task = await db.tasks.find_one(
        {
            "_id": ObjectId(task_id)
        }
    )

    if not task:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )

    if task["self_task"]:

        if task["user_id"] != user_id:
            raise HTTPException(
                status_code=403,
                detail="You can only update your own task"
            )

    else:

        owner = await db.users.find_one(
            {
                "_id": ObjectId(task["user_id"])
            }
        )

        if not owner:
            raise HTTPException(
                status_code=404,
                detail="Task owner not found"
            )

        if str(owner.get("manager_id")) != user_id:
            raise HTTPException(
                status_code=403,
                detail="Only manager can update this task"
            )

    await db.tasks.update_one(
        {
            "_id": ObjectId(task_id)
        },
        {
            "$set": {
                "description": updated_task.description,
                "completed": updated_task.completed,
                "isUpdated": True
            }
        }
    )

    updated = await db.tasks.find_one(
        {
            "_id": ObjectId(task_id)
        }
    )

    return TaskResponse(
        id=str(updated["_id"]),
        title=updated["title"],
        user_id=updated["user_id"],
        description=updated.get("description"),
        completed=updated["completed"],
        isUpdated=updated["isUpdated"],
        self_task=updated["self_task"]
    )