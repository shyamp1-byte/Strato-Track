from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from uuid import UUID
from fastapi import HTTPException

from app.core.db import get_db
from app.services.auth_dependency import get_current_user
from app.schemas.project import ProjectCreate, ProjectPublic
from app.services import project as project_service
from app.schemas.project import ProjectUpdateStatus, ProjectUpdate

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectPublic, status_code=status.HTTP_201_CREATED)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return project_service.create_project(
    db=db,
    owner_id=user.id,
    title=payload.title,
    target_due_date=payload.target_due_date,
)

@router.get("", response_model=list[ProjectPublic])
def list_projects(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return project_service.list_projects(db=db, owner_id=user.id)

@router.patch("/{project_id}", response_model=ProjectPublic)
def patch_project(
    project_id: UUID,
    payload: ProjectUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return project_service.update_project(
            db=db,
            owner_id=user.id,
            project_id=project_id,
            title=payload.title,
            target_due_date=payload.target_due_date,
        )
    except ValueError as e:
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise

@router.post("/{project_id}/status", response_model=ProjectPublic)
def set_project_status(
    project_id: UUID,
    payload: ProjectUpdateStatus,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        return project_service.update_project_status(
            db=db,
            owner_id=user.id,
            project_id=project_id,
            status=payload.status,
        )
    except ValueError as e:
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise

@router.post("/{project_id}/delete", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    try:
        project_service.delete_project(db=db, owner_id=user.id, project_id=project_id)
    except ValueError as e:
        if str(e) == "PROJECT_NOT_FOUND":
            raise HTTPException(status_code=404, detail="Project not found")
        if str(e) == "FORBIDDEN":
            raise HTTPException(status_code=403, detail="Forbidden")
        raise