from pydantic import BaseModel, constr
from uuid import UUID
from datetime import date, datetime
from typing import Literal

TitleStr = constr(min_length=1, max_length=200)

TaskStatus = Literal["TODO", "DOING", "DONE"]
TaskPriority = Literal["LOW", "MEDIUM", "HIGH"]


class TaskCreate(BaseModel):
    title: TitleStr
    description: str | None = None
    due_date: date | None = None
    priority: TaskPriority = "MEDIUM"


class TaskPublic(BaseModel):
    id: UUID
    project_id: UUID
    title: str
    description: str | None
    due_date: date | None
    status: str
    priority: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TaskUpdateStatus(BaseModel):
    status: TaskStatus


class TaskUpdatePriority(BaseModel):
    priority: TaskPriority