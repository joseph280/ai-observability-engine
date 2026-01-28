from datetime import datetime, timezone
import uuid
from sqlalchemy import Boolean, Column, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import relationship

from app.db.database import Base


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    input_text = Column(Text, nullable=False)
    output_text = Column(Text)
    evaluation = relationship("EvaluationDB", back_populates="task", uselist=False, cascade="all, delete-orphan")
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

class EvaluationDB(Base):
    __tablename__ = "evaluations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    task_id = Column(String, ForeignKey("tasks.id"))
    score = Column(Float, default=0.0) #AI Judge score
    confidence_score = Column(Float, default = 0.0) #Statistical log-probability average
    passed = Column(Boolean)
    reasoning = Column(Text) # We will join the 'flags' list into a string here

    task = relationship("TaskDB", back_populates="evaluation")