import asyncio
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

    async def run_task(self, input_text: str) -> tuple [str, float]:
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
        #Use LLM to judge
        return
    



    
    def _run_dummy(self, input_text: str) -> tuple [str, float]:
        # Temporary fake model
        return f"[DUMMY MODEL OUTPUT] You said: {input_text}", 0.999