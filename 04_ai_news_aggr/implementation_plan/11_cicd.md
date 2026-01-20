# Phase 11: CI/CD (GitHub Actions)

Automation of testing to ensure stability before merging.

---

Prompt_31

```
# Task_1
Generate `.github/workflows/ci.yml`.

# Goal
Automate testing on every push using GitHub Actions.

# Content Requirements
1.  **Triggers**: `push` to `main`, `pull_request`.
2.  **Job**: `test` (runs on `ubuntu-latest`).
3.  **Service Container (Crucial)**:
    - Define a `postgres` service using image `postgres:17`.
    - Env: `POSTGRES_USER=postgres`, `POSTGRES_PASSWORD=postgres`, `POSTGRES_DB=ai_news_aggregator`.
    - Ports: Map `5432:5432`.
    - Options: Use healthcheck `--health-cmd pg_isready ...`.
4.  **Steps**:
    1.  **Checkout Code**: Use `actions/checkout@v4`.
    2.  **Setup Python**: Use `actions/setup-python@v5` with version `3.12`.
    3.  **Install uv**: Use an explicit install command or action.
    4.  **Install Dependencies**: `uv sync`.
    5.  **Run Tests**:
        - Command: `uv run pytest`
        - **Env Vars**: You MUST inject dummy environment variables for the tests to run:
            - `OPENAI_API_KEY=dummy`
            - `POSTGRES_HOST=localhost` (Because service ports are mapped to localhost in GHA).
            - `POSTGRES_PORT=5432`

# Goal
Ensure tests pass with a real database instance before merging code.
```