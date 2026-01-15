Prompt_01
```
# Task_1
Generate the file `pyproject.toml` at the root of the project.
This file defines the project metadata and dependencies.

# Format
Use the standard PEP 621 `[project]` table format.

# Content Requirements

1.  **Project Metadata**:
    - Name: "ai_news_aggr"
    - Version: "0.1.0"
    - Description: "AI news aggregator"
    - Readme: "README.md"
    - Python Requirement: ">=3.12"

2.  **Dependencies**:
    Include the following libraries with these specific version constraints:
    - `beautifulsoup4>=4.14.2`
    - `docling>=2.61.2`
    - `feedparser>=6.0.12`
    - `markdown>=3.7.0`
    - `markdownify>=0.11.6`
    - `openai>=2.7.2`
    - `psycopg2-binary>=2.9.11`
    - `pydantic>=2.0.0`
    - `python-dotenv>=1.2.1`
    - `requests>=2.32.5`
    - `sqlalchemy>=2.0.44`
    - `youtube-transcript-api>=1.2.3`

3.  **Dev Dependencies** (under `[dependency-groups]` -> `dev`):
    - `ipykernel>=7.1.0`
    - `pytest>=8.0.0`
```

---

Prompt_02
```
# Task_2
Generate the file `docker/docker-compose.yml`.
This file defines the database service required for the application.

# Content Requirements

1.  **Service Definition**:
    - Service Name: `postgres`
    - Image: `postgres:17`
    - Container Name: `ai-news-aggregator-db`

2.  **Environment Configuration**:
    - Use Shell Parameter Expansion syntax (`${VARIABLE:-default}`) for flexibility.
    - `POSTGRES_USER` (default: postgres)
    - `POSTGRES_PASSWORD` (default: postgres)
    - `POSTGRES_DB` (default: ai_news_aggregator)

3.  **Networking & Storage**:
    - **Ports**: Map `${POSTGRES_PORT:-5432}` on host to `5432` on container.
    - **Volumes**: Mount a named volume `postgres_data` to `/var/lib/postgresql/data` for persistence.

4.  **Healthcheck**:
    - Command: `pg_isready -U ${POSTGRES_USER:-postgres}`
    - Interval: 10s
    - Timeout: 5s
    - Retries: 5

5.  **Top-Level Volumes**:
    - Define the `postgres_data` volume at the bottom of the file.

```
---

Prompt_03

```
# Task_3
Generate the file `app/example.env`.
This file serves as a template for the environment variables required by the application.

# Content
Include the following variables with empty values for secrets and default values for configuration:

1.  **API Keys**:
    - `OPENAI_API_KEY=`
    - `ANTHROPIC_API_KEY=`

2.  **Email Configuration**:
    - `MY_EMAIL=`
    - `APP_PASSWORD=`

3.  **Database Configuration**:
    - `POSTGRES_USER=postgres`
    - `POSTGRES_PASSWORD=postgres`
    - `POSTGRES_DB=ai_news_aggregator`
    - `POSTGRES_HOST=localhost`
    - `POSTGRES_PORT=5432`

# Proxy Configuration (Optional but recommended based on your scrapers)
    - `PROXY_USERNAME=`
    - `PROXY_PASSWORD=`

# Instructions
Add a comment at the top explaining that users should copy this file to `.env` and fill in their secrets.
```

