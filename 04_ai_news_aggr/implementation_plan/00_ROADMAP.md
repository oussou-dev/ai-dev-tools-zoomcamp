# 🚀 Implementation Roadmap: AI News Aggregator

This document defines the strict execution order of prompts to build the project without dependency errors.

## 🛠️ Phase 1: Foundations & Infrastructure
*Objective: Set up the environment.*

- [ ] **1. Project Configuration** (`pyproject.toml`)
    - *Prompt ID: 01* (found in `implementation_plan/01_infra.md`)
    - *Action:* Run `uv sync` or `pip install .`
- [ ] **2. Docker Infrastructure** (`docker/docker-compose.yml`)
    - *Prompt ID: 02*
    - *Action:* Run `docker-compose up -d` (Database only for dev).
- [ ] **3. Env Variables** (`app/example.env`)
    - *Prompt ID: 03*
    - *Action:* Copy to `.env` and fill in API keys.

## 🗄️ Phase 2: Database
*Objective: Define the data schema (Models).*

- [ ] **4. Connection** (`app/database/connection.py`)
    - *Prompt ID: 04* (found in `implementation_plan/02_database.md`)
- [ ] **5. SQLAlchemy Models** (`app/database/models.py`)
    - *Prompt ID: 05*
- [ ] **6. Repository Pattern** (`app/database/repository.py`)
    - *Prompt ID: 06*
- [ ] **7. Creation Script** (`app/database/create_tables.py`)
    - *Prompt ID: 07*
    - *Action:* Verify by running `python -m app.database.create_tables` (after creating `__init__.py` files or waiting for Phase 7).

## ⚙️ Phase 3: Ingestion (Scrapers)
*Objective: Fetch raw data.*

- [ ] **8. Configuration** (`app/config.py`)
    - *Prompt ID: 08* (found in `implementation_plan/03_scrapers.md`)
    - *Content:* `YOUTUBE_CHANNELS` list.
- [ ] **9. YouTube Scraper** (`app/scrapers/youtube.py`)
    - *Prompt ID: 09*
- [ ] **10. OpenAI Scraper** (`app/scrapers/openai.py`)
    - *Prompt ID: 10*
- [ ] **11. Anthropic Scraper** (`app/scrapers/anthropic.py`)
    - *Prompt ID: 11*

## 🧠 Phase 4: Intelligence (Agents)
*Objective: Analyze and summarize data.*

- [ ] **12. User Profile** (`app/profiles/user_profile.py`)
    - *Prompt ID: 12* (found in `implementation_plan/04_agents.md`)
- [ ] **13. Digest Agent** (`app/agents/digest_agent.py`)
    - *Prompt ID: 13*
- [ ] **14. Curator Agent** (`app/agents/curator_agent.py`)
    - *Prompt ID: 14*
- [ ] **15. Email Agent** (`app/agents/email_agent.py`)
    - *Prompt ID: 15*

## 🔗 Phase 5: Orchestration (Services)
*Objective: Link DB and Agents.*

- [ ] **16. Emailing Service** (`app/services/email.py`)
    - *Prompt ID: 16* (found in `implementation_plan/05_services.md`)
- [ ] **17. Youtube Service** (`app/services/process_youtube.py`)
    - *Prompt ID: 17*
- [ ] **18. Anthropic Service** (`app/services/process_anthropic.py`)
    - *Prompt ID: 18*
- [ ] **19. Digest Service** (`app/services/process_digest.py`)
    - *Prompt ID: 19*
- [ ] **20. Curator Service** (`app/services/process_curator.py`)
    - *Prompt ID: 20*
- [ ] **21. Email Service** (`app/services/process_email.py`)
    - *Prompt ID: 21*

## 🚀 Phase 6: Execution (Runners)
*Objective: The ON button.*

- [ ] **22. Scraper Runner** (`app/runner.py`)
    - *Prompt ID: 22* (Found in `implementation_plan/06_runners.md`)
- [ ] **23. Daily Pipeline** (`app/daily_runner.py`)
    - *Prompt ID: 23*
- [ ] **24. Entry Point** (`main.py`)
    - *Prompt ID: 24*

## 🧹 Phase 7: Utilities
*Objective: Prepare package structure.*

- [ ] **25. Package Initialization** (`init_packages.py`)
    - *Prompt ID: 25* (Found in `implementation_plan/07_finalization.md`)
    - *Action:* Run `python init_packages.py` (Creates missing `__init__.py` files).

## 🧪 Phase 8: Core QA (Tests)
*Objective: Verify stability of the core pipeline.*

- [ ] **26. Setup Tests** (`tests/conftest.py`)
    - *Prompt ID: 26* (Found in `implementation_plan/08_tests.md`)
    - *Action:* `uv add --dev pytest` (or `pip install pytest`)
- [ ] **27. Database Tests** (`tests/test_database.py`)
    - *Prompt ID: 27*
    - *Action:* `pytest tests/test_database.py`
- [ ] **28. Pipeline Mock Tests** (`tests/test_pipeline.py`)
    - *Prompt ID: 28*
    - *Action:* `pytest tests/test_pipeline.py`

## 🌐 Phase 9: API (FastAPI)
*Objective: Serve data via REST to satisfy API Contract.*

- [ ] **29. FastAPI Application** (`app/api/main.py`)
    - *Prompt ID: 29* (Found in `implementation_plan/09_api.md`)
    - *Content:* Exposes endpoints like `/pipeline/run` and `/digests`.
    - *Action:* `uv run uvicorn app.api.main:app --reload` (Check docs at /docs).

## 🖥️ Phase 10: Frontend (Streamlit)
*Objective: User Interaction consuming the API.*

- [ ] **30. Streamlit App** (`app/frontend/main.py`)
    - *Prompt ID: 30* (Found in `implementation_plan/10_frontend.md`)
    - *Logic:* **Must fetch data via HTTP requests to localhost:8000**.
    - *Action:* `uv run streamlit run app/frontend/main.py`.

## 🔄 Phase 11: CI/CD
*Objective: Automation.*

- [ ] **31. GitHub Actions** (`.github/workflows/ci.yml`)
    - *Prompt ID: 31* (Found in `implementation_plan/11_cicd.md`)
    - *Action:* Commit and push to verify tests run automatically.

## 🧪 Phase 12: Integration QA
*Objective: Test the API Endpoints.*

- [ ] **32. API Tests** (`tests/test_api.py`)
    - *Prompt ID: 32* (Found in `implementation_plan/12_integration_qa.md`)
    - *Action:* `pytest tests/test_api.py`.

## 📚 Phase 13: Docs & Containerization
*Objective: Documentation & Full Containerization.*

- [ ] **33. Full Stack Containers** (`Dockerfile` & `docker-compose.yml`)
    - *Prompt ID: 33* (Found in `implementation_plan/13_docs_containers.md`)
    - *Content:* Generates Dockerfile and updates compose to include `api` and `frontend`.
    - *Action:* `docker-compose up --build` (Runs the WHOLE app).
- [ ] **34. Documentation** (`README.md`)
    - *Prompt ID: 34*
    - *Action:* Document the API, Docker setup, and link to `from_scratch.md`.

## 🚀 Phase 14: Deployment (Railway)
*Objective: Go Live.*

- [ ] **35. Production Configuration** (`app/frontend/main.py` update)
    - *Prompt ID: 35* (Found in `implementation_plan/14_deployment.md`)
    - *Action:* Ensure Frontend uses dynamic `API_URL`.
- [ ] **36. Production Dockerfiles** (`docker/Dockerfile.api`, `docker/Dockerfile.frontend`)
    - *Prompt ID: 36*
    - *Action:* Create optimized builds for Railway services.