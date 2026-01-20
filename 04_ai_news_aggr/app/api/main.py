from typing import List

from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.connection import SessionLocal, get_database_url
from app.database.repository import Repository
from app.daily_runner import run_daily_pipeline
from app.schemas import DigestResponse, RunPipelineResponse

# Initialize FastAPI app
app = FastAPI(title="AI News Aggregator API")

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency: Get database session
def get_db() -> Session:
    """Yield a database session for dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Health check endpoint
@app.get("/health")
def health_check() -> dict:
    """Health check endpoint to verify API is running."""
    return {"status": "ok"}


# Pipeline execution endpoint
@app.post("/pipeline/run", response_model=RunPipelineResponse)
def run_pipeline(
    background_tasks: BackgroundTasks,
    hours: int = 24,
    top_n: int = 10,
) -> RunPipelineResponse:
    """Trigger the daily pipeline in the background.

    Args:
        background_tasks: FastAPI background tasks
        hours: Number of hours to look back for content (default: 24)
        top_n: Number of top articles to include in email (default: 10)

    Returns:
        RunPipelineResponse with status and message
    """
    background_tasks.add_task(run_daily_pipeline, hours=hours, top_n=top_n)
    return RunPipelineResponse(
        status="accepted",
        message="Pipeline started in background",
    )


# Get recent digests endpoint
@app.get("/digests", response_model=List[DigestResponse])
def get_digests(limit: int = 50, db: Session = Depends(get_db)) -> List[DigestResponse]:
    """Fetch recent digests.

    Args:
        limit: Maximum number of digests to return (default: 50)
        db: Database session (injected)

    Returns:
        List of DigestResponse objects
    """
    repo = Repository(session=db)

    # Use a large hour window (1000 hours ≈ 41 days) to get all recent digests
    digests = repo.get_recent_digests(hours=1000)

    # Apply limit
    return digests[:limit]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
