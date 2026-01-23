from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.engine import LLMEngine
from app.core.evaluator import Evaluator
from app.db.models import TaskDB
from app.db.session import get_db
from app.schemas.task import TaskCreate

class TaskRunner:
    def __init__(self):
        self.engine = LLMEngine()
        self.evaluator = Evaluator()

def run(self, input_text: str, db: Session) -> TaskDB:        
        # 1. Create Task (Status: Processing)
        task = TaskDB(
            input_text=input_text,
            status="processing"
        )
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # 2. Run LLM
        try: 
            output = self.engine.run_task(input_text)
            task.output_text = output
            task.status = "completed"
        except Exception as e:
            #Log failure to DB so we can debug it later
            task.output_text = str(e)
            task.status = "failed"
            db.commit()
            raise e
        
        # 3. Run Evaluation (The Observability Layer)
        eval_result = self.evaluator.evaluate(input_text, output)

        # 4. Save Evaluation     
        evaluation = EvaluationDB(
            task_id = task.id,
            success = eval_result["success"],
            score = eval_result["score"],
            reasoning = eval_result["reasoning"]
        )
        db.add(evaluation)

        #Final commit
        db.commit()
        db.refresh(task)

        return task

