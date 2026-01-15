Prompt_04
```
# Task_1
Generate the file `app/database/connection.py`.
This module handles the database connection string construction and session management.

# Technical Stack
- **Libs:** `sqlalchemy` (create_engine, sessionmaker), `python-dotenv` (load_dotenv), `os`.

# Code Requirements

1.  **Environment Setup**:
    - Call `load_dotenv()` at the top level to load variables from `.env`.

2.  **`get_database_url() -> str`**:
    - Retrieve the following environment variables using `os.getenv`, with these specific defaults:
        - `POSTGRES_USER` (default: "postgres")
        - `POSTGRES_PASSWORD` (default: "postgres")
        - `POSTGRES_HOST` (default: "localhost")
        - `POSTGRES_PORT` (default: "5432")
        - `POSTGRES_DB` (default: "ai_news_aggregator")
    - Return a formatted PostgreSQL connection string: `postgresql://user:password@host:port/db`.

3.  **Global Objects**:
    - `engine`: Initialize using `create_engine(get_database_url())`.
    - `SessionLocal`: Initialize using `sessionmaker` with `autocommit=False`, `autoflush=False`, and `bind=engine`.

4.  **`get_session()`**:
    - A simple helper function that returns a new instance of `SessionLocal()`.

# Style Guide
- Ensure the connection string format matches standard PostgreSQL requirements.

```

---

Prompt_05
```
# Task_2
Generate the file `app/database/models.py`.
This file defines the SQLAlchemy ORM schema for the application.

# Technical Stack
- **Library:** `sqlalchemy` (ORM).
- **Base:** Use `declarative_base`.

# Code Requirements

1.  **Setup**:
    - Import `datetime`, `Optional`.
    - Import SQLAlchemy types: `Column`, `String`, `DateTime`, `Text`.
    - Initialize `Base = declarative_base()`.

2.  **Define Tables (Classes)**:

    **A. `YouTubeVideo`** (`__tablename__ = "youtube_videos"`)
    - `video_id`: String, Primary Key.
    - `title`, `url`, `channel_id`: String, Not Null.
    - `published_at`: DateTime, Not Null.
    - `description`: Text.
    - `transcript`: Text, Nullable (default None).
    - `created_at`: DateTime, default to `datetime.utcnow`.

    **B. `OpenAIArticle`** (`__tablename__ = "openai_articles"`)
    - `guid`: String, Primary Key.
    - `title`, `url`: String, Not Null.
    - `description`: Text.
    - `published_at`: DateTime, Not Null.
    - `category`: String, Nullable.
    - `created_at`: DateTime, default to `datetime.utcnow`.

    **C. `AnthropicArticle`** (`__tablename__ = "anthropic_articles"`)
    - `guid`: String, Primary Key.
    - `title`, `url`: String, Not Null.
    - `description`: Text.
    - `published_at`: DateTime, Not Null.
    - `category`: String, Nullable.
    - `markdown`: Text, Nullable (stores the converted content).
    - `created_at`: DateTime, default to `datetime.utcnow`.

    **D. `Digest`** (`__tablename__ = "digests"`)
    - `id`: String, Primary Key.
    - `article_type`: String, Not Null (e.g., "youtube", "openai").
    - `article_id`: String, Not Null (links to video_id or guid).
    - `url`, `title`: String, Not Null.
    - `summary`: Text, Not Null (the LLM output).
    - `created_at`: DateTime, default to `datetime.utcnow`.

# Style Guide
- Ensure proper imports from `sqlalchemy.orm`.

```

---

Prompt_06

```
# Task_3
Generate the file `app/database/repository.py`.
This file implements the Repository Pattern to abstract all database interactions.

# Context
- It depends on `app.database.models` (for the Tables) and `app.database.connection` (for the Session).
- It handles data for YouTube Videos, OpenAI Articles, Anthropic Articles, and Digests.

# Code Requirements

1.  **Imports & Setup**:
    - Import `datetime`, `timedelta`, `timezone`, `List`, `Optional`, `Dict`, `Any`.
    - Import `Session` from `sqlalchemy.orm`.
    - Import all models from `.models`.
    - Import `get_session` from `.connection`.
    - Create class `Repository` with an `__init__` that accepts an optional `session`. If None, use `get_session()`.

2.  **CRUD Methods (Implement specific logic for each)**:

    **A. YouTube Methods**:
    - `create_youtube_video(...)`: Check if `video_id` exists. If not, add and commit.
    - `bulk_create_youtube_videos(videos: List[dict])`: Iterate, check existence for each, add new ones to session, commit once at the end. Return count of added items.
    - `get_youtube_videos_without_transcript(limit)`: Return videos where `transcript` is None.
    - `update_youtube_video_transcript(video_id, transcript)`: Update and commit.

    **B. OpenAI Methods**:
    - `create_openai_article(...)`: Check if `guid` exists.
    - `bulk_create_openai_articles(...)`: Same bulk logic as YouTube.

    **C. Anthropic Methods**:
    - `create_anthropic_article(...)`: Check if `guid` exists.
    - `bulk_create_anthropic_articles(...)`: Same bulk logic.
    - `get_anthropic_articles_without_markdown(limit)`: Return articles where `markdown` is None.
    - `update_anthropic_article_markdown(guid, markdown)`: Update and commit.

3.  **Complex Aggregation Logic**:

    **D. `get_articles_without_digest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]`**:
    - **Goal:** Return a unified list of content (Videos + Articles) that haven't been summarized yet.
    - **Logic:**
        1. Fetch all existing `Digest` entries and build a set of seen IDs (format: `"{type}:{id}"`).
        2. Fetch valid YouTube videos (has transcript AND transcript != "__UNAVAILABLE__").
        3. Fetch OpenAI articles.
        4. Fetch Anthropic articles (must have markdown).
        5. Filter out items whose ID is already in the `seen_ids` set.
        6. Normalize the output into a dictionary: `{"type": "...", "id": "...", "title": "...", "url": "...", "content": "...", "published_at": "..."}`.
        7. Apply limit if provided and return.

    **E. Digest Methods**:
    - `create_digest(article_type, article_id, url, title, summary, published_at)`:
        - Generate ID = `f"{article_type}:{article_id}"`.
        - Ensure `created_at`/`published_at` is timezone-aware (UTC).
        - Check existence, add, and commit.
    - `get_recent_digests(hours=24)`: Return digests created in the last X hours, ordered by newest first.

# Style Guide
- Use `self.session.query(...)` syntax.
- Ensure strict Type Hinting.
```

---

Prompt_07

```
# Task_4
Generate the file `app/database/create_tables.py`.
This script initializes the database schema by creating all tables defined in the models.

# Context
- This script is intended to be run directly (e.g., `python app/database/create_tables.py`).
- It must handle python path resolution to allow importing from the `app` package.

# Code Requirements

1.  **Path Configuration**:
    - Import `sys` and `pathlib.Path`.
    - Insert the project root directory (parent of parent of the current file) into `sys.path` at index 0. This is crucial for resolving imports like `from app.database...`.

2.  **Imports**:
    - From `app.database.models`, import `Base`.
    - From `app.database.connection`, import `engine`.

3.  **Execution**:
    - Inside a `if __name__ == "__main__":` block:
        - Call `Base.metadata.create_all(engine)` to create the tables in the database.
        - Print "Tables created successfully" to the console.

```