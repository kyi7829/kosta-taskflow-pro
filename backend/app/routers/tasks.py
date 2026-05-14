import logging
from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Task
from app.schemas import TaskCreate, TaskDetail, TaskSummary, TaskUpdate

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("", response_model=TaskDetail, status_code=201)
def create_task(body: TaskCreate, db: Session = Depends(get_db)):
    task = Task(
        title=body.title,
        description=body.description,
        status=body.status,
        due_at=body.due_at,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    logger.info("Task 생성 완료: id=%s", task.id)
    return task


@router.get("", response_model=List[TaskSummary])
def list_tasks(db: Session = Depends(get_db)):
    return db.query(Task).order_by(Task.created_at.desc(), Task.id.desc()).all()


@router.get("/{task_id}", response_model=TaskDetail)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="해당 Task를 찾을 수 없습니다.")
    return task


@router.put("/{task_id}", response_model=TaskDetail)
def update_task(task_id: int, body: TaskUpdate, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="해당 Task를 찾을 수 없습니다.")

    # 전달된 필드만 업데이트 (부분 수정)
    update_data = body.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    task.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(task)
    logger.info("Task 수정 완료: id=%s", task.id)
    return task


@router.delete("/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="해당 Task를 찾을 수 없습니다.")
    db.delete(task)
    db.commit()
    logger.info("Task 삭제 완료: id=%s", task_id)
