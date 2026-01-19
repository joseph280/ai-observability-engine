from fastapi import FastAPI
from app.api.routes import router as api_router
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(
    title="AI Observability Engine",
    description="Backend service for orchestrating and observing AI task execution",
    version="0.1.0",
)

app.include_router(api_router)