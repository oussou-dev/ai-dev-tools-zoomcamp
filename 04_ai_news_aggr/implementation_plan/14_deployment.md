# Phase 14: Deployment Preparation

This phase prepares the application for Railway deployment by creating production-ready Dockerfiles.

---

Prompt_34

```
# Task_1
Update `app/frontend/main.py` (and any other frontend pages) to handle dynamic API URLs.

# Context
In development, the API is at `http://localhost:8000`.
In production (Railway), the API will be at a public URL (e.g., `https://api-news-production.up.railway.app`).

# Logic
1.  Import `os` and `dotenv`.
2.  Load `.env` (using `load_dotenv()`).
3.  Define a constant `API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")`.
4.  **Crucial**: Remove any trailing slash from the URL to ensure consistency.
5.  Replace all hardcoded string references to `http://localhost:8000` with the `API_BASE_URL` variable.

# Goal
Ensure the frontend can talk to the backend regardless of where it is hosted.

```

---

Prompt_35
```
# Task_2
Generate two specific Dockerfiles in the `docker/` folder for production deployment.

# 1. `docker/Dockerfile.api`
Create a Dockerfile optimized for the FastAPI Backend.
- **Base**: `python:3.12-slim`
- **Workdir**: `/app`
- **Setup**:
    - Copy `pyproject.toml` .
    - Install dependencies: `pip install .` (Ensure `uvicorn` and `fastapi` are installed).
- **Copy Code**: `COPY . .` (Copy the entire project root to maintain package structure).
- **Command**: `CMD ["uvicorn", "app.api.main:app", "--host", "0.0.0.0", "--port", "8000"]`

# 2. `docker/Dockerfile.frontend`
Create a Dockerfile optimized for the Streamlit Frontend.
- **Base**: `python:3.12-slim`
- **Workdir**: `/app`
- **Setup**:
    - Copy `pyproject.toml` .
    - Install dependencies: `pip install .` (Ensure `streamlit` is installed).
- **Copy Code**: `COPY . .`
- **Expose**: 8501
- **Command**: `CMD ["streamlit", "run", "app/frontend/main.py", "--server.port=8501", "--server.address=0.0.0.0"]`

# Goal
Allow Railway to build two different services from the same repository by pointing to different Dockerfiles.
```
