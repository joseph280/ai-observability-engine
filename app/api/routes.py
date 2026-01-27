from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException

from app.core import task_store
from app.core.engine import LLMEngine
from app.db.models import TaskDB
from app.db.session import get_db
from app.schemas.metrics import SystemMetrics
from app.schemas.task import TaskCreate, TaskRead
from sqlalchemy.orm import Session

from app.services.analytics import AnalyticsService
from app.services.runner import TaskRunner

router = APIRouter()
runner = TaskRunner()
analytics = AnalyticsService()


@router.get("/health")
def health_check():
    return {"status":"ok"}

@router.post("/tasks", response_model=TaskRead)
async def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    return await runner.run(payload.input_text, db)

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: str, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.get("/metrics", response_model=SystemMetrics)
def get_system_stats(db: Session = Depends(get_db)):
    return analytics.get_metrics(db)