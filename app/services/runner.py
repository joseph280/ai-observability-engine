import uuid
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.engine import LLMEngine
from app.core.evaluator import Evaluator
from app.core.logger import get_logger
from app.db.models import EvaluationDB, TaskDB
from app.db.session import get_db
from app.schemas.task import TaskCreate

logger = get_logger(__name__)

class TaskRunner:
    def __init__(self):
        self.engine = LLMEngine()
        self.evaluator = Evaluator()

    async def run(self, input_text: str, db: Session) -> TaskDB:     
        # 1. Log Start. Create Task (Status: Processing)
        logger.info("task_processing_start", extra={"input_snippet": input_text[:50]})

        task = TaskDB(
            input_text=input_text,
            status="processing"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # 2. Run LLM
        try: 
            output, math_score = await self.engine.run_task(input_text)
            task.output_text = output
            task.status = "completed"
        except Exception as e:
            task.output_text = str(e)
            task.status = "failed"
            db.commit()
            # Log the business failure
            logger.error("task_processing_failed", extra={"task_id": task.id, "error": str(e)})
            raise e
        
        # 3. Run Evaluation (The Observability Layer)
        eval_result = await self.evaluator.evaluate(input_text, output)

        # Log the evaluation outcome
        logger.info(
            "task_evaluated", 
            extra={
                "task_id": task.id, 
                "judge_score": eval_result["judge_score"], 
                "passed": eval_result["passed"],
                "reasoning": eval_result["reasoning"],
                "confidence_score": math_score
            }
        )
        # 4. Save Evaluation
        evaluation = EvaluationDB(
            id =str(uuid.uuid4()),
            task_id = task.id,
            passed = eval_result["passed"],
            judge_score = eval_result["judge_score"],
            reasoning = eval_result["reasoning"],
            confidence_score = math_score
        )
        db.add(evaluation)

        #Final commit
        db.commit()
        db.refresh(task)

        logger.info("task_completed_successfully", extra={"task_id": task.id})
        return task

