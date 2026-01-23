class Evaluator:
    """
    Simple rule-based evaluation. 
    In the future, this could use another LLM to grade the response.
    """
    def evaluate(self, user_input: str, ai_response: str) -> dict:
        score = 1.0
        flags = []

        #Rule 1: Latency/Empty Check 
        if not ai_response:
            return {"score":0, "flags": ["empty_response"]}
        
        #Rule 2: "I don't know" detection (Basic Hallucination Guard)
        refusal_patterns = ["i don't know", "cannot assist", "language model"]
        if any(p in ai_response.lower() for p in refusal_patterns):
            score = 0.5
            flags.append("refusal_detected")

        #Rule 3: Conciseness (Sample rule)
        if len(ai_response) > 2000:
            flags.append("verbose_output")

        return {
            "score": score,
            "flags": flags,
            "passed": score >0.7
        }