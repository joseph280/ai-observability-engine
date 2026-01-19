from app.core.engine import LLMEngine


engine = LLMEngine(provider="openai")

output = engine.run_task("Explain why observability matters.")
print("OUTPUT:")
print(output)