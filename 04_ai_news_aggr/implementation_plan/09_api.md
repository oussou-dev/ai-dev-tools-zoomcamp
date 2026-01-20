# Phase 9: API Layer (FastAPI)

This phase wraps the internal logic into a REST API to satisfy the Architecture and API Contract requirements.

---


Prompt_29

```
# Task_1
Generate `app/api/main.py` and `app/schemas.py`.

# Goal
Create a FastAPI backend to serve the aggregated news and trigger the pipeline.

# Tech
- FastAPI, Pydantic, SQLAlchemy.
- Use `BackgroundTasks` for long-running operations.

# Requirements `app/schemas.py`
Define Pydantic models (DTOs):
1.  `DigestResponse`:
    - Fields: `id` (str), `title` (str), `url` (str), `summary` (str), `article_type` (str), `published_at` (datetime), `created_at` (datetime).
    - Config: `from_attributes = True` (orm_mode).
2.  `RunPipelineResponse`:
    - Fields: `status` (str), `message` (str).

# Requirements `app/api/main.py`
1.  **Setup**:
    - Initialize `app = FastAPI(title="AI News Aggregator API")`.
    - Add `CORSMiddleware` allowing `["*"]` (to allow Streamlit/Frontend access).
2.  **Imports**:
    - Import `Repository`, `get_db_url`, `SessionLocal` from `app.database`.
    - Import `run_daily_pipeline` from `app.daily_runner`.
3.  **Dependency**:
    - Create `get_db()` that yields a database session (`SessionLocal`).
4.  **Endpoints**:
    - `GET /health`: Returns `{"status": "ok"}`.
    - `POST /pipeline/run`:
        - Accepts query params: `hours` (int=24), `top_n` (int=10).
        - **Crucial**: Use `BackgroundTasks` to call `run_daily_pipeline(hours, top_n)`.
        - Returns: `{"status": "accepted", "message": "Pipeline started in background"}` immediately.
    - `GET /digests`:
        - Accepts `limit` (int=50).
        - Uses `Repository.get_recent_digests(hours=1000)` (using a large hour window to act as "all recent").
        - logic: Instantiate Repository with the session, call `get_recent_digests`, and return the list.
        - Response Model: `List[DigestResponse]`.

# Instructions
- Ensure strict type hinting.
- Do NOT try to filter by score (as it is not stored in the DB).
- Handle Dependency Injection for the DB session correctly (`Depends(get_db)`).
```