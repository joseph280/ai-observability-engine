import os
import time

from openai import OpenAI

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise RuntimeError("OPENAI_API_KEY is not set")

client = OpenAI(api_key)

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

                if self.provider == "openai":
                    output = self._run_openai(input_text)
                else:
                    output = self._run_dummy(input_text)
                    
                latency = time.time() - start_time
                print(f"[LLMEngine] latency={latency:.2f}s")

                return output
            except Exception as e:
                last_error = e
                print(f"[LLMEngine] attempt {attempt+1} failed: {e}")

            raise RuntimeError("LLM failed after retries") from last_error
    
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