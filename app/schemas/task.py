from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, ConfigDict


class EvaluationBase(BaseModel):
    score: float
    passed: bool
    reasoning: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

class TaskCreate(BaseModel):
    input_text: str 


class TaskRead(BaseModel):
    id: UUID
    input_text: str
    output_text: Optional[str]
    status:str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes = True)