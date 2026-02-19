from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.services.auth_dependency import get_current_user
from app.schemas.task import TaskPublic, TaskUpdateStatus, TaskUpdatePriority
from app.services import task as task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/{task_id}/status", response_model=TaskPublic)
def set_status(
    task_id: UUID,
    payload: TaskUpdateStatus,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return task_service.set_task_status(db=db, owner_id=user.id, task_id=task_id, status=payload.status)
    except ValueError as e:
        if str(e) == "TASK_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Task not found")
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise

@router.post("/{task_id}/priority", response_model=TaskPublic)
def set_priority(
    task_id: UUID,
    payload: TaskUpdatePriority,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return task_service.set_task_priority(db=db, owner_id=user.id, task_id=task_id, priority=payload.priority)
    except ValueError as e:
        if str(e) == "TASK_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Task not found")
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise