from app.core.engine import LLMEngine


class Evaluator:
    def __init__(self):
        self.engine = LLMEngine()
        
        
    async def evaluate(self, user_input: str, ai_response: str) -> dict:
        """
        Hybrid Evaluation:
        1. Fast/Free Static Checks (Guardrails)
        2. Deep AI Analysis (The Judge)
        """

        if not ai_response:
            return {
                "judge_score": 0.0, 
                "passed": False, 
                "reasoning": "Critical Failure: AI response was empty."
            }
        else:
            # If it passes basic sanity checks, ask the Judge.
            return await self.engine.evaluate_text(user_input, ai_response)