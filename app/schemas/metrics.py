from pydantic import BaseModel


class SystemMetrics(BaseModel):
    total_requests:int
    successful_requests: int
    failed_requests: int
    pending_requests: int
    average_quality_score: float
    pass_rate: float 