from sqlalchemy.orm import Session
from uuid import UUID
from datetime import date

from app.models.task import Task

def create_task(db: Session, project_id: UUID, title: str, description: str | None, due_date: date | None, priority: str):
    task = Task(
        project_id=project_id,
        title=title,
        description=description,
        due_date=due_date,
        priority=priority,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def list_tasks(db: Session, project_id: UUID):
    return db.query(Task).filter(Task.project_id == project_id).all()

def get_task_by_id(db: Session, task_id: UUID):
    return db.query(Task).filter(Task.id == task_id).first()

def update_task_status(db: Session, task: Task, status: str):
    task.status = status
    db.commit()
    db.refresh(task)
    return task

def update_task_priority(db: Session, task: Task, priority: str):
    task.priority = priority
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()

def delete_tasks_for_project(db: Session, project_id: UUID):
    db.query(Task).filter(Task.project_id == project_id).delete()
    db.commit()