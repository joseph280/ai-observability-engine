import asyncio
import json
import math
import os

from openai import AsyncOpenAI

from app.core.logger import get_logger

#Initialize the logger for this module
logger = get_logger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # Log critical error before crashing
    logger.critical("missing_openai_api_key")
    raise RuntimeError("OPENAI_API_KEY is not set")

client = AsyncOpenAI(api_key=api_key)

class LLMEngine:
    def __init__(self, provider: str ="openai"):
        self.provider = provider

    async def run_task(self, input_text: str) -> tuple [str, float, float]:
        """
        Send input_text to an LLM and return output_text.
        """
        retries = 2
        last_error = None

        for attempt in range(retries + 1):
            try:
                start_time = asyncio.get_event_loop().time()

                # Log attempt start
                logger.info("llm_request_start", extra={"attempt": attempt + 1})

                if self.provider == "openai":
                    output, confidence = await self._run_openai(input_text)
                else:
                    output, confidence = self._run_dummy(input_text)
                    
                latency = asyncio.get_event_loop().time() - start_time
                
                # STRUCTRED LOG: We pass metrics as data, not string text
                logger.info(
                    "llm_request_success", 
                    extra={
                        "latency": round(latency, 4), 
                        "attempt": attempt + 1,
                        "token_count": len(output.split()) 
                    }
                )

                return output, confidence
            
            except Exception as e:
                last_error = e
                # Log failure with the error message
                logger.error(
                    "llm_request_failed", 
                    extra={"attempt": attempt + 1, "error": str(e)}
                )
                await asyncio.sleep(1)

        logger.critical("llm_max_retries_exceeded")
        raise RuntimeError(f"LLM failed after {retries} retries") from last_error
    
    async def _run_openai(self, input_text: str) -> tuple[str, float]:
        response = await client.responses.create(
            model="gpt-3.5-turbo",
            instructions="You are a helpful assistant.",
            top_logprobs=1,
            input= input_text,
            timeout=15,
            include=["message.output_text.logprobs"]
        )

        #Parse Output Text
        content_item = response.output[0].content[0]
        text_content = content_item.text

        #Parse Logprobs
        raw_logprobs = getattr(content_item, "logprobs", [])

        if not raw_logprobs:
            return text_content, 0.0

        #Calculate average Confidence
        linear_probs = []
        for token_data in raw_logprobs:
            lp = getattr(token_data, "logprob", -100)
            linear_probs.append(math.exp(lp))

        avg_confidence = sum(linear_probs) / len(linear_probs) if linear_probs else 0.0

        return text_content, avg_confidence
    

    async def evaluate_text(self, input_text: str, output_text: str) -> dict:
        #Use LLM as a Semantic AI Judge
        #1. Define the rules:
        judge_instructions = """
        You are a High-Precision AI Quality Auditor. 
        Instead of rounding to the nearest 0.5, you must provide a granular score 
        based on a 100-point scale converted to a float (e.g., 0.64, 0.82, 0.17).

        SCORING CONTINUUM:
        - 1.0: Flawless. Factual, insightful, and perfectly logical.
        - 0.70 - 0.99: High quality with minor optimizations possible.
        - 0.40 - 0.69: Mediocre. Technically safe but generic, circular, or "filler" text.
        - 0.00 - 0.39: Failure. Nonsense, hallucinations, or validating logically broken prompts.

        CRITICAL EVALUATION:
        If the input is nonsensical (e.g., "Why is true not true"), penalize generic 
        supportive answers heavily. A "canned" empathetic response to gibberish 
        should result in a score between 0.10 and 0.25.

        OUTPUT FORMAT:
        Return ONLY valid JSON:
        {
            "judge_score": float,
            "passed": boolean,
            "reasoning": string (max 15 words)
        }
        """

        # 2. Present the Evidence
        evidence = f"User Input: {input_text}\nAI Response: {output_text}"

        try:
            #3. Call the Judge
            response = await client.responses.create(
                model="gpt-3.5-turbo",
                instructions=judge_instructions,
                input= evidence,
                timeout=15,
                temperature=0.1 #Low temp = strict judge
            )

            #4. Extract and clean JSON
            raw_text = response.output[0].content[0].text

            #5. Remove Markdown fences if found
            clean_json = raw_text.replace("```json", "").replace("```", "").strip()

            return json.loads(clean_json)
        except Exception as e:
            #If the Judge fails, we don't fail the while req.
            logger.error("judge_failed", extra={"error":str(e)})
            return {
                "judge_score":0.0,
                "passed": False,
                "reasoning": "Judge execution failed"
            }
    



    
    def _run_dummy(self, input_text: str) -> tuple [str, float]:
        # Temporary fake model
        return f"[DUMMY MODEL OUTPUT] You said: {input_text}", 0.999