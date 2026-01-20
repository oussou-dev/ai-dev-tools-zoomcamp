Prompt_26
```
# Task_1
Set up the testing infrastructure for the project.

# Requirements
1.  **Dependencies**: Check if `pytest` is in `pyproject.toml`. If not, tell me to run `uv add --dev pytest` or `pip install pytest`.
2.  **Directory**: Create a `tests/` directory at the root.
3.  **Files**:
    - `tests/__init__.py` (empty).
    - `tests/conftest.py`: This file should define `pytest` fixtures.
        - Create a `test_db` fixture that creates an in-memory SQLite database (or a temporary Postgres connection) for testing purposes, creates tables, and tears them down after tests.
        - Yield a session for the tests to use.

# Goal
Ensure we can run `pytest` and it detects the configuration.

```

---

Prompt_27

```
# Task_2
Generate `tests/test_database.py`.

# Logic
Write unit tests for `app/database/repository.py`.
1.  **Test Video Insert**: Try inserting a dummy YouTube video and retrieving it.
2.  **Test Deduplication**: Try inserting the same video twice and assert it doesn't crash (idempotency).
3.  **Test Article Insert**: Do the same for OpenAI/Anthropic articles.

# Goal
Verify that the Repository pattern works and data is saved correctly.

```

---


Prompt_28

```
# Task_3
# Task
Generate `tests/test_pipeline.py`.

# Logic
Since we don't want to call real APIs (OpenAI/YouTube) during tests (to save money and time), use `unittest.mock`.
1.  **Mock Scrapers**: Create a test that simulates `run_scrapers` returning fake data, and verify `run_daily_pipeline` handles it.
2.  **Mock LLM**: Mock the `DigestAgent` to return a static summary "This is a test summary" instead of calling OpenAI.

# Goal
Ensure the pipeline logic (the plumbing) works without needing real external connections.

```


