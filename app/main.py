from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from app.api.routes import router as api_router

from app.db.database import Base, engine 
from app.db.models import TaskDB, EvaluationDB  # Import models so Base knows about them

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Observability Engine",
    description="Backend service for orchestrating and observing AI task execution",
    version="0.1.0",
)

app.include_router(api_router)