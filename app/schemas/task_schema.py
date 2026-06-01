from pydantic import BaseModel
from typing import Optional

class TaskResponse(BaseModel):
    id: str
    title: str
    user_id: str
    description: Optional[str] = None
    completed: bool
    isUpdated: bool = False
    self_task: bool

class TaskSchema(BaseModel):
    title: str
    description: str

class TaskUpdateSchema(BaseModel):
    description: str
    completed: bool