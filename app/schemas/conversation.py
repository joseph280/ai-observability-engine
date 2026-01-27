from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    # We store token usage, latency, or evaluation scores here.
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class Conversation(BaseModel):
    id: str
    messages: List[Message] = []
    created_at: float = None
    updated_at: float = None