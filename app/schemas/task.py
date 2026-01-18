from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    input_text: str = Field(..., min_length=1, description="User-provided task input")


class TaskRead(BaseModel):
    id: UUID
    input_text: str
    output_text: Optional[str]
    status:str
    created_at: datetime