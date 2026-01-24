import os
import time

from openai import OpenAI

from app.core.logger import get_logger

#Initialize the logger for this module
logger = get_logger(__name__)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    # Log critical error before crashing
    logger.critical("missing_openai_api_key")
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key=api_key)

class LLMEngine:
    def __init__(self, provider: str ="openai"):
        self.provider = provider

    def run_task(self, input_text: str) -> str:
        """
        Send input_text to an LLM and return output_text.
        """
        retries = 2
        last_error = None

        for attempt in range(retries + 1):
            try:
                start_time = time.time()

                # Log attempt start
                logger.info("llm_request_start", extra={"attempt": attempt + 1})

                if self.provider == "openai":
                    output = self._run_openai(input_text)
                else:
                    output = self._run_dummy(input_text)
                    
                latency = time.time() - start_time
                
                # STRUCTRED LOG: We pass metrics as data, not string text
                logger.info(
                    "llm_request_success", 
                    extra={
                        "latency": round(latency, 4), 
                        "attempt": attempt + 1,
                        "token_count": len(output.split()) # Rough estimate
                    }
                )

                return output
            except Exception as e:
                last_error = e
                # Log failure with the error message
                logger.error(
                    "llm_request_failed", 
                    extra={"attempt": attempt + 1, "error": str(e)}
                )
                time.sleep(1)

        logger.critical("llm_max_retries_exceeded")
        raise RuntimeError(f"LLM failed after {retries} retries") from last_error
    
    def _run_openai(self, input_text: str) -> str:
        response = client.responses.create(
            model="gpt-3.5-turbo",
            instructions="You are a helpful assistant.",
            input= input_text,
            timeout=15,
        )

        return response.output_text
    
    
    def _run_dummy(self, input_text: str) -> str:
        # Temporary fake model
        return f"[DUMMY MODEL OUTPUT] You said: {input_text}"