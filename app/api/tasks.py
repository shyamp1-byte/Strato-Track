from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.db import get_db
from app.services.auth_dependency import get_current_user
from app.schemas.task import TaskCreate, TaskPublic
from app.services import task as task_service
from app.schemas.task import TaskUpdateStatus


router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["tasks"])


@router.post("", response_model=TaskPublic, status_code=status.HTTP_201_CREATED)
def create_task(
    project_id: UUID,
    payload: TaskCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return task_service.create_task(
            db=db,
            owner_id=user.id,
            project_id=project_id,
            title=payload.title,
            description=payload.description,
            due_date=payload.due_date,
            priority=payload.priority,
        )
    except ValueError as e:
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise


@router.get("", response_model=list[TaskPublic])
def list_tasks(
    project_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return task_service.list_tasks(db=db, owner_id=user.id, project_id=project_id)
    except ValueError as e:
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise

@router.patch("/{task_id}", response_model=TaskPublic)
def patch_task_status(
    project_id: UUID,
    task_id: UUID,
    payload: TaskUpdateStatus,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return task_service.update_task_status(
            db=db,
            owner_id=user.id,
            project_id=project_id,
            task_id=task_id,
            status=payload.status,
        )
    except ValueError as e:
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "TASK_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Task not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    project_id: UUID,
    task_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        task_service.delete_task(db=db, owner_id=user.id, project_id=project_id, task_id=task_id)
    except ValueError as e:
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "TASK_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Task not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise