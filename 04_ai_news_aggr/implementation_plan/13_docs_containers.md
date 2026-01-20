Prompt_33
```
# Task_1
Finalize the containerization by creating the missing Dockerfile and updating the composition.

# Sub-Task 1: Generate `Dockerfile`
Create a file named `Dockerfile` at the root of the project.

**Content Requirements:**
- **Base Image**: `python:3.12-slim`
- **Setup**:
    - Set `WORKDIR /app`
    - Install `curl` (for healthchecks).
    - Install `uv` (since we use it in commands): `pip install uv`
    - Copy `pyproject.toml` .
    - Install dependencies: `uv sync` (or `pip install .` if preferred, but ensure consistency).
    - Copy the rest of the code: `COPY . .`
    - **Env**: Add `ENV PATH="/root/.local/bin:$PATH"` if needed for uv, or ensure uv is in path.

# Sub-Task 2: Update `docker/docker-compose.yml`
Update the file to orchestrate the full stack.

**Content Requirements:**

1.  **Service 1: `postgres`** (Existing):
    - Ensure it has a `healthcheck` (`test: ["CMD-SHELL", "pg_isready -U postgres"]`).

2.  **Service 2: `backend`**:
    - **Build**:
        - Context: `..` (Project Root, assuming docker-compose is in /docker folder)
        - Dockerfile: `Dockerfile`
    - **Command**: `uv run uvicorn app.api.main:app --host 0.0.0.0 --port 8000`
    - **Ports**: `"8000:8000"`
    - **Depends On**:
        - `postgres`:
            - `condition`: `service_healthy`
    - **Environment**:
        - `DATABASE_URL=postgresql+psycopg2://${POSTGRES_USER:-postgres}:${POSTGRES_PASSWORD:-postgres}@postgres:5432/${POSTGRES_DB:-ai_news_aggregator}`
        - `OPENAI_API_KEY=${OPENAI_API_KEY}`

3.  **Service 3: `frontend`**:
    - **Build**:
        - Context: `..`
        - Dockerfile: `Dockerfile`
    - **Command**: `uv run streamlit run app/frontend/main.py --server.port 8501 --server.address 0.0.0.0`
    - **Ports**: `"8501:8501"`
    - **Depends On**: `backend`
    - **Environment**:
        - `API_URL=http://backend:8000`

# Goal
Ensure `docker-compose up --build` works by creating the Dockerfile first, then referencing it.
```