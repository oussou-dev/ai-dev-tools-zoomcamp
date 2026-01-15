## 🏗️ Developer Guide: Recreating with AI

This project was built using "Vibe Coding" (AI-assisted development). If you want to recreate it from scratch or understand how it was built, follow the **Implementation Plan**.

Inside the `implementation_plan/` folder, you will find markdown files containing the exact prompts used to generate every single file in this repository.

### Execution Order (Strict)

To rebuild the project without dependency errors, feed the prompts to your LLM (Claude Sonnet 3.5 or GPT-4o) in this specific order:

#### 🟢 Phase 1: Infrastructure
*Context: `@01_infra.md`* 
1.  **Prompt 01**: Generate `pyproject.toml`. -> *Run `uv sync`*
2.  **Prompt 02**: Generate `docker-compose.yml`. -> *Run `docker-compose up -d`*
3.  **Prompt 03**: Generate `example.env`. -> *Configure your `.env`*

#### 🔵 Phase 2: Database
*Context: `@02_database.md`*
4.  **Prompt 04**: `connection.py`
5.  **Prompt 05**: `models.py`
6.  **Prompt 06**: `repository.py`
7.  **Prompt 07**: `create_tables.py` -> *Run `python -m app.database.create_tables`*

#### 🟠 Phase 3: Ingestion
*Context: `@03_scrapers.md`*
8.  **Prompt 08**: `config.py`
9.  **Prompt 09**: `youtube.py`
10. **Prompt 10**: `openai.py`
11. **Prompt 11**: `anthropic.py`

#### 🟣 Phase 4: Intelligence
*Context: `@04_agents.md`*
12. **Prompt 12**: `user_profile.py`
13. **Prompt 13**: `digest_agent.py`
14. **Prompt 14**: `curator_agent.py`
15. **Prompt 15**: `email_agent.py`

#### 🔴 Phase 5: Services
*Context: `@05_services.md`*
16. **Prompt 16**: `email.py`
17. **Prompt 17**: `process_youtube.py`
18. **Prompt 18**: `process_anthropic.py`
19. **Prompt 19**: `process_digest.py`
20. **Prompt 20**: `process_curator.py`
21. **Prompt 21**: `process_email.py`

#### 🟤 Phase 6: Runners
*Context: `@06_runners.md`*
22. **Prompt 22**: `runner.py`
23. **Prompt 23**: `daily_runner.py`
24. **Prompt 24**: `main.py`

#### ⚫ Phase 7: Finalization
*Context: `@07_finalization.md`*
25. **Prompt 25**: `init_packages.py` -> *Run `python init_packages.py`*

#### ⚫ Phase 8: Tests
*Context: `@08_tests.md`*
26. **Prompt 26**: `conftest.py` -> *Run `uv add --dev pytest`*
27. **Prompt 27**: `test_database.py`
28. **Prompt 28**: `test_pipeline.py` -> *Run `pytest`*
