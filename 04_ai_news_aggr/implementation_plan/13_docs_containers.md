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

---

Prompt_34
```
# Task_2
Generate the final `README.md`.

# Content Requirements (Strict Order)

1.  **🚨 Vibe Coding / Recreation Guide (Top Priority)**:
    - **Place this section at the very top**, immediately after the project title.
    - **Content**: "This project was built using AI-assisted development ('Vibe Coding').  If you want to recreate it from scratch or understand the exact prompts used to build it, please refer to the **[Developer Guide (from_scratch.md)](./from_scratch.md)**."
    - Add a mention that the `implementation_plan/` folder contains the "DNA" of the project.

2.  **Project Title & Description**:
    - Title: **AI News Aggregator**
    - Description: A full-stack AI-powered news platform. It scrapes, summarizes, and serves AI trends via a FastAPI backend and a Streamlit dashboard.

3.  **Architecture Diagram**:
    - **Flow**: `[Scrapers] -> [Postgres] -> [FastAPI] -> [Streamlit]`.
    - **AI**: Agents (Digest/Curator) run in the background via the API.

4.  **Features**:
    - **Multi-Source Scraping**: YouTube, OpenAI, Anthropic.
    - **Smart Summarization**: GPT-4o-mini powered.
    - **Interactive UI**: Trigger pipelines, view digests.
    - **REST API**: Swagger docs available.
    - **Containerized**: Full Docker support.

5.  **Quick Start**:
    - **Prerequisites**: Docker, Python 3.12, OpenAI API Key.
    - **Step 1**: Clone repo.
    - **Step 2**: `cp app/example.env .env` and fill keys.
    - **Step 3 (The Magic Command)**:
      ```bash
      docker-compose up --build
      ```
    - **Step 4**: Open `http://localhost:8501` for the App and `http://localhost:8000/docs` for the API.

6.  **Tech Stack**:
    - Badges for Python, FastAPI, Streamlit, Docker, PostgreSQL.

# Style
Professional, clear, designed for developers who might want to fork or recreate the project.
```