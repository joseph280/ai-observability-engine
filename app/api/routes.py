from uuid import UUID
from fastapi import APIRouter, HTTPException

from app.core import task_store
from app.schemas.task import TaskCreate, TaskRead

router = APIRouter()
task_store = task_store.InMemoryTaskStore()


@router.get("/health")
def health_check():
    return {"status":"ok"}

@router.post("/tasks", response_model=TaskRead)
def create_task(task: TaskCreate):
    return task_store.create(task)

@router.get("/tasks/{task_id}", response_model=TaskRead)
def get_task(task_id: UUID):
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

