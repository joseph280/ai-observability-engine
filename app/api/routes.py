from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.core import task_store
from app.core.engine import LLMEngine
from app.db.models import TaskDB
from app.db.session import get_db
from app.schemas.task import TaskCreate, TaskRead
from sqlalchemy.orm import Session

router = APIRouter()
engine = LLMEngine()


@router.get("/health")
def health_check():
    return {"status":"ok"}

@router.post("/tasks", response_model=TaskRead)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    task = TaskDB(
        input_text=payload.input_text,
        status="processing"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
     
    output = engine.run_task(payload.input_text)

    task.output_text = output
    task.status = "completed"
    db.commit()
    db.refresh(task)

    return task

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

