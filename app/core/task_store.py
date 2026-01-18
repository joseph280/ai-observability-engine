from datetime import datetime, timezone
from typing import Dict
from uuid import UUID, uuid4

from app.schemas.task import TaskCreate, TaskRead


class InMemoryTaskStore:
    def __init__(self):
        self._tasks: Dict[UUID, TaskRead] = {}

    def create(self, task: TaskCreate) -> TaskRead:
        task_read = TaskRead(
            id = uuid4(),
            input_text=task.input_text,
            output_text=None,
            status="pending",
            created_at=datetime.now(timezone.utc)
        )
        self._tasks[task_read.id] = task_read
        return task_read

    def get(self, task_id:UUID) -> TaskRead | None:
        return self._tasks.get(task_id)