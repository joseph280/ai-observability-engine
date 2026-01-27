from sqlalchemy import func
from sqlalchemy.orm import Session

from app.db.models import EvaluationDB, TaskDB

class AnalyticsService:
    def get_metrics(self, db:Session) -> dict:
        #1. Volume Metrics
        total_tasks = db.query(func.count(TaskDB.id)).scalar() or 0

        #Count by status
        completed = db.query(func.count(TaskDB.id)).filter(TaskDB.status == "completed").scalar() or 0
        failed = db.query(func.count(TaskDB.id)).filter(TaskDB.status == "failed").scalar() or 0
        pending = db.query(func.count(TaskDB.id)).filter(TaskDB.status == "processing").scalar() or 0

        #Quality Metrics (Aggregations)
        avg_score = db.query(func.avg(EvaluationDB.score)).scalar() or 0.0

        #Pass rate
        total_evals = db.query(func.count(EvaluationDB.id)).scalar() or 0
        passed_evals = db.query(func.count(EvaluationDB.id)).filter(EvaluationDB.passed == True).scalar() or 0

        pass_rate = (passed_evals/(total_evals+failed)) if total_evals>0 else 0.0

        return {
            "total_requests": total_tasks,
            "successful_requests": completed,
            "failed_requests": failed,
            "pending_requests": pending,
            "average_quality_score":  round(avg_score, 2),
            "pass_rate": round(pass_rate, 2)
        }