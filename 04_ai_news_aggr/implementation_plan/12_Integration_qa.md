# Phase 12: Integration QA

Testing the API endpoints ensures the contract is valid and the frontend won't crash.

---

Prompt_32

```
# Task_1
Generate `tests/test_api.py`.

# Goal
Verify the API endpoints return the expected status codes and data structures.

# Tech
- `fastapi.testclient.TestClient`
- `pytest`

# Logic
1.  **Setup**:
    - Import `TestClient`.
    - Import `app` from `app.api.main`.
    - Import `get_db` from `app.api.main`.
    - **Crucial**: Use `app.dependency_overrides[get_db] = override_get_db` to ensure tests use the test database fixture (from `conftest.py`) instead of the production DB.

2.  **Test 1: Health Check (`GET /health`)**:
    - Call `client.get("/health")`.
    - Assert status code is 200.
    - Assert response is `{"status": "ok"}`.

3.  **Test 2: Trigger Pipeline (`POST /pipeline/run`)**:
    - Call `client.post("/pipeline/run")`.
    - Assert status code is 202 (Accepted) or 200.
    - Assert the JSON response contains `"message": "Pipeline started in background"`.
    - *Note:* Since it runs in the background, we don't need to wait for it to finish in this specific test.

4.  **Test 3: Fetch Digests (`GET /digests`)**:
    - **Pre-requisite**: Insert a dummy digest into the test database first (using the `test_db` fixture).
    - Call `client.get("/digests")`.
    - Assert status code is 200.
    - Assert the returned list is not empty.
    - Assert the first item has fields `title`, `summary`, `article_type`.

# Goal
Validate the full HTTP request-response cycle.
```
