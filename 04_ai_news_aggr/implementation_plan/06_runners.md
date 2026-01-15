Prompt_22
```
# Task_1
Generate the file `app/runner.py`.
This script acts as the "Registry" that executes all scrapers and persists the raw data into the database.

# Technical Stack
- **Dependencies:** `app.config`, `app.scrapers`, `app.database.repository`.
- **Input:** Uses `YOUTUBE_CHANNELS` list from config.

# Code Requirements

1.  **Imports**:
    - `typing.List`.
    - `YOUTUBE_CHANNELS` from `.config`.
    - Scrapers: `YouTubeScraper`, `OpenAIScraper`, `AnthropicScraper`.
    - Models: `ChannelVideo`, `OpenAIArticle`, `AnthropicArticle`.
    - `Repository` from `.database.repository`.

2.  **Function `run_scrapers(hours: int = 24) -> dict`**:
    - Initialize all 3 scrapers and the `Repository`.
    - **YouTube Logic**:
        - Iterate through `YOUTUBE_CHANNELS`.
        - Fetch videos using `get_latest_videos`.
        - **Data Conversion**: The repository expects dictionaries, but scrapers return Pydantic models. Create a list of dictionaries (`video_dicts`) by manually mapping fields (`video_id`, `title`, `url`, `channel_id`, `published_at`, `description`, `transcript`).
        - Save using `repo.bulk_create_youtube_videos`.
    - **OpenAI Logic**:
        - Fetch articles.
        - Convert to dictionaries (mapping `guid`, `title`, `url`, etc.).
        - Save using `repo.bulk_create_openai_articles`.
    - **Anthropic Logic**:
        - Fetch articles.
        - Convert to dictionaries.
        - Save using `repo.bulk_create_anthropic_articles`.
    - **Return**: A dict containing the lists of scraped objects: `{"youtube": ..., "openai": ..., "anthropic": ...}`.

3.  **Execution**:
    - Add `if __name__ == "__main__":` block to run the function and print the counts of items found.

```

---

Prompt_23

```
# Task_2
Generate the file `app/daily_runner.py`.
This script orchestrates the full daily pipeline (Scraping -> Processing -> Digest -> Email).

# Technical Stack
- **Dependencies:** `app.runner`, `app.services` (anthropic, youtube, digest, email).
- **Libraries:** `logging`, `datetime`, `dotenv`.

# Code Requirements

1.  **Setup & Imports**:
    - Import `logging` and `datetime` (from datetime).
    - Import and call `load_dotenv()` immediately.
    - Import `run_scrapers` from `app.runner`.
    - Import processors: `process_anthropic_markdown`, `process_youtube_transcripts`, `process_digests`, `send_digest_email` from their respective `app.services` modules.

2.  **Logging Configuration**:
    - Configure `logging.basicConfig` with level INFO.
    - Format: `'%(asctime)s - %(levelname)s - %(message)s'`.
    - Date format: `'%Y-%m-%d %H:%M:%S'`.
    - Initialize `logger`.

3.  **Function `run_daily_pipeline(hours: int = 24, top_n: int = 10) -> dict`**:
    - Capture `start_time`.
    - Log a header ("Starting Daily AI News Aggregator Pipeline").
    - Initialize a `results` dictionary structure (`scraping`, `processing`, `digests`, `email`, `success`=False).
    
    - **Pipeline Execution (Wrap in Try/Except)**:
        - **Step 1 [1/5]**: Call `run_scrapers(hours)`. Store counts in results. Log with checkmark (`✓`) showing counts for each source.
        - **Step 2 [2/5]**: Call `process_anthropic_markdown()`. Update results. Log processed/failed counts.
        - **Step 3 [3/5]**: Call `process_youtube_transcripts()`. Update results. Log processed/unavailable counts.
        - **Step 4 [4/5]**: Call `process_digests()`. Update results. Log processed/failed/total.
        - **Step 5 [5/5]**: Call `send_digest_email(hours, top_n)`. Update results.
            - If success: Set `results["success"] = True`. Log success.
            - If failure: Log error with cross (`✗`).
            
    - **Error Handling**: Catch generic exceptions, log with `exc_info=True`, and add error to results.
    
    - **Summary & Return**:
        - Calculate `duration` in seconds.
        - Log a "Pipeline Summary" block displaying duration and stats for each step.
        - Return the `results` dictionary.

4.  **Execution**:
    - Add `if __name__ == "__main__":` block.
    - Run the pipeline.
    - Call `exit(0)` if success, `exit(1)` if failure.

# Style Guide
- Use specific logging markers (e.g., `[1/5]`, `✓`, `✗`) to make the console output readable.
```

---

Prompt_24

```
# Task_3
Generate the file `main.py` at the root of the project.
This script serves as the command-line entry point for the application, allowing arguments for customization.

# Technical Stack
- **Dependencies:** `app.daily_runner` (`run_daily_pipeline`).
- **Standard Libs:** `sys`.

# Code Requirements

1.  **Function `main(hours: int = 24, top_n: int = 10)`**:
    - Simply calls and returns `run_daily_pipeline(hours=hours, top_n=top_n)`.

2.  **Execution Block (`if __name__ == "__main__":`)**:
    - Import `sys`.
    - Set default values: `hours = 24`, `top_n = 10`.
    - **Argument Parsing**:
        - Check `sys.argv`: if an argument exists at index 1, parse it as `int` for `hours`.
        - Check `sys.argv`: if an argument exists at index 2, parse it as `int` for `top_n`.
    - Call `main` with these values.
    - Exit with code 0 if `result["success"]` is True, else 1.

# Content
```python
from app.daily_runner import run_daily_pipeline


def main(hours: int = 24, top_n: int = 10):
    return run_daily_pipeline(hours=hours, top_n=top_n)


if __name__ == "__main__":
    import sys
    
    hours = 24
    top_n = 10
    
    if len(sys.argv) > 1:
        hours = int(sys.argv[1])
    if len(sys.argv) > 2:
        top_n = int(sys.argv[2])
    
    result = main(hours=hours, top_n=top_n)
    exit(0 if result["success"] else 1)
```
