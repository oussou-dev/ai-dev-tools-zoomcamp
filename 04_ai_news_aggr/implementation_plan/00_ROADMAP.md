# 🚀 Implementation Roadmap: AI News Aggregator

This document defines the strict execution order of prompts to build the project without dependency errors.

## 🛠️ Phase 1: Foundations & Infrastructure
*Objective: Set up the environment.*

- [ ] **1. Project Configuration** (`pyproject.toml`)
    - *Prompt ID: 01*
    - *Action:* Run `uv sync` or `pip install .`
- [ ] **2. Docker Infrastructure** (`docker/docker-compose.yml`)
    - *Prompt ID: 02*
    - *Action:* Run `docker-compose up -d`
- [ ] **3. Env Variables** (`app/example.env`)
    - *Prompt ID: 03*
    - *Action:* Copy to `.env` and fill in API keys.

## 🗄️ Phase 2: Database
*Objective: Define the data schema (Models).*

- [ ] **4. Connection** (`app/database/connection.py`)
    - *Prompt ID: 04*
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
    - *Prompt ID: 8*
    - *Content:* `YOUTUBE_CHANNELS` list.
- [ ] **9. YouTube Scraper** (`app/scrapers/youtube.py`)
    - *Prompt ID: 9*
- [ ] **10. OpenAI Scraper** (`app/scrapers/openai.py`)
    - *Prompt ID: 10*
- [ ] **11. Anthropic Scraper** (`app/scrapers/anthropic.py`)
    - *Prompt ID: 11*

## 🧠 Phase 4: Intelligence (Agents)
*Objective: Analyze and summarize data.*

- [ ] **12. User Profile** (`app/profiles/user_profile.py`)
    - *Prompt ID: 12*
- [ ] **13. Digest Agent** (`app/agents/digest_agent.py`)
    - *Prompt ID: 13*
- [ ] **14. Curator Agent** (`app/agents/curator_agent.py`)
    - *Prompt ID: 14*
- [ ] **15. Email Agent** (`app/agents/email_agent.py`)
    - *Prompt ID: 15*

## 🔗 Phase 5: Orchestration (Services)
*Objective: Link DB and Agents.*

- [ ] **16. Emailing Service** (`app/services/email.py`)
    - *Prompt ID: 16*
    
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

- [ ] **18. Scraper Runner** (`app/runner.py`)
    - *Prompt ID: 22*
- [ ] **19. Daily Pipeline** (`app/daily_runner.py`)
    - *Prompt ID: 23*
- [ ] **20. Entry Point** (`main.py`)
    - *Prompt ID: 24*

## 🧹 Phase 7: Finalization
*Objective: Cleanup and Documentation.*

- [ ] **21. Package Initialization** (`init_packages.py`)
    - *Prompt ID: 25*
    - *Action:* Run `python init_packages.py` (Creates missing `__init__.py` files).
- [ ] **22. Documentation** (`README.md`)
    - *Prompt ID: 26*

## 🧪 Phase 8: Quality Assurance (Tests)
*Objective: Verify stability without spending API credits.*

- [ ] **23. Setup Tests** (`tests/conftest.py`)
    - *Prompt ID: 27*
    - *Action:* `uv add --dev pytest` (or `pip install pytest`)
- [ ] **24. Database Tests** (`tests/test_database.py`)
    - *Prompt ID: 28*
    - *Action:* `pytest tests/test_database.py`
- [ ] **25. Pipeline Mock Tests** (`tests/test_pipeline.py`)
    - *Prompt ID: 29*
    - *Action:* `pytest`