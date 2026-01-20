from datetime import datetime

from pydantic import BaseModel


class DigestResponse(BaseModel):
    """Response model for a digest entry."""

    id: str
    title: str
    url: str
    summary: str
    article_type: str
    published_at: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class RunPipelineResponse(BaseModel):
    """Response model for pipeline execution."""

    status: str
    message: str
