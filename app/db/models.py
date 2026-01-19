from datetime import datetime, timezone
import uuid
from sqlalchemy import Column, DateTime, Integer, String, Text

from app.db.database import Base


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    input_text = Column(Text, nullable=False)
    output_text = Column(Text)
    status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))