Prompt_16
```
# Task_1
Generate the file `app/services/email.py`.
This module handles SMTP email sending and HTML formatting for the newsletter.

# Technical Stack
- **Libs:** `smtplib`, `html`, `email.mime` (`MIMEText`, `MIMEMultipart`), `markdown`, `dotenv`.
- **Environment:** `MY_EMAIL`, `APP_PASSWORD`.

# Code Requirements

1.  **Setup**:
    - Load `.env` variables immediately.
    - Define constants `MY_EMAIL` and `APP_PASSWORD`.

2.  **`send_email(subject, body_text, body_html=None, recipients=None)`**:
    - **Validation**: Raise `ValueError` if env vars are missing or if recipients list is empty. Default recipient = `MY_EMAIL`.
    - **SMTP Logic**:
        - Use `MIMEMultipart("alternative")`.
        - Attach plain text version.
        - If `body_html` exists, attach HTML version.
        - Connect to `smtp.gmail.com` on port **465** (SSL).
        - Login and send.

3.  **`markdown_to_html(markdown_text: str) -> str`**:
    - Convert text using `markdown.markdown(..., extensions=['extra', 'nl2br'])`.
    - Wrap the result in a complete HTML structure (`<!DOCTYPE html>...`).
    - **CSS Styling**: Include inline CSS for:
        - `body`: max-width 600px, centered, sans-serif fonts.
        - `a`: color #0066cc.
        - `h2`, `h3`: clean headers.
        - `hr`: distinct separator.

4.  **`digest_to_html(digest_response) -> str`**:
    - **Import**: Local import `from app.agent.email_agent import EmailDigestResponse` to avoid circular dependency issues at module level.
    - **Logic**:
        - If input is not `EmailDigestResponse`, fallback to `markdown_to_html`.
        - If it is a valid object:
            - Convert Greeting and Intro to HTML.
            - Iterate through `digest_response.articles`.
            - For each article: Add Title (`h3`), Summary (HTML), and "Read more →" link.
            - Separate items with `<hr>`.
            - Wrap everything in the same HTML/CSS template as above.

5.  **`send_email_to_self(subject, body)`**:
    - Simple wrapper sending to `MY_EMAIL`.

6.  **Test**:
    - Add `if __name__ == "__main__":` block to send a test email.

# Style Guide
- Ensure the CSS is responsive (`meta name="viewport"`).
- Handle HTML escaping for user content (titles/urls).
```

---

Prompt_17

```
# Task_2
Generate the file `app/services/process_youtube.py`.
This script orchestrates the fetching of transcripts for YouTube videos that are already in the database but lack content.

# Technical Stack
- **Dependencies:** `app.scrapers.youtube`, `app.database.repository`.
- **System:** Uses `sys.path` modification to allow standalone execution.

# Code Requirements

1.  **Path Configuration**:
    - Import `sys` and `pathlib`.
    - Insert the project root into `sys.path` (parent.parent.parent of current file) to ensure `from app...` imports work.

2.  **Imports**:
    - `typing.Optional`.
    - `YouTubeScraper` from `app.scrapers.youtube`.
    - `Repository` from `app.database.repository`.

3.  **Constants**:
    - `TRANSCRIPT_UNAVAILABLE_MARKER = "__UNAVAILABLE__"`.
    - This marker is used to flag videos where no transcript exists, preventing infinite retry loops.

4.  **Function `process_youtube_transcripts(limit: Optional[int] = None) -> dict`**:
    - Initialize `scraper` and `repo`.
    - Fetch videos using `repo.get_youtube_videos_without_transcript(limit)`.
    - Initialize counters: `processed`, `unavailable`, `failed`.
    - **Loop Logic**:
        - Iterate through videos.
        - Try to fetch transcript using `scraper.get_transcript(video.video_id)`.
        - **Success**: If transcript exists, update DB with the text. Increment `processed`.
        - **Failure (No Transcript)**: If result is None, update DB with `TRANSCRIPT_UNAVAILABLE_MARKER`. Increment `unavailable`.
        - **Exception**: Catch generic `Exception`. Print error. Update DB with `TRANSCRIPT_UNAVAILABLE_MARKER` (to skip next time). Increment `unavailable`.
    - Return a dict with stats: `total`, `processed`, `unavailable`, `failed`.

5.  **Execution**:
    - Add `if __name__ == "__main__":` block to run the function and print the stats.

# Style Guide
- Ensure robust error handling so one bad video doesn't crash the batch.
```

---

Prompt_18

```
# Task_3
Generate the file `app/services/process_anthropic.py`.
This script handles the fetching and saving of Markdown content for Anthropic articles.

# Technical Stack
- **Dependencies:** `app.scrapers.anthropic`, `app.database.repository`.
- **System:** Uses `sys.path` modification to allow standalone execution.

# Code Requirements

1.  **Path Configuration**:
    - Import `sys` and `pathlib`.
    - Insert the project root into `sys.path` (parent.parent.parent).

2.  **Imports**:
    - `typing.Optional`.
    - `AnthropicScraper` from `app.scrapers.anthropic`.
    - `Repository` from `app.database.repository`.

3.  **Function `process_anthropic_markdown(limit: Optional[int] = None) -> dict`**:
    - Initialize `scraper` and `repo`.
    - Fetch target articles using `repo.get_anthropic_articles_without_markdown(limit)`.
    - Initialize stats counters (`processed`, `failed`).
    - **Loop Logic**:
        - For each article:
        - Call `scraper.url_to_markdown(article.url)`.
        - **Try/Except Block**:
            - If `markdown` is returned: Update DB (`repo.update_anthropic_article_markdown`), increment `processed`.
            - If `None` or Error: Increment `failed`. Log/Print error with article GUID.
    - Return stats dict.

4.  **Execution**:
    - Add `if __name__ == "__main__":` block to run and print stats.

# Style Guide
- Ensure the Try/Except block is tight around the conversion/update logic to prevent the whole batch from crashing on one bad URL.
```

---

Prompt_19

```
# Task_4
Generate the file `app/services/process_digest.py`.
This script orchestrates the generation of AI summaries for all unprocessed content (YouTube videos, Blog articles).

# Technical Stack
- **Dependencies:** `app.agent.digest_agent`, `app.database.repository`.
- **System:** Uses `sys.path` modification for standalone execution.
- **Logging:** Uses standard `logging` library.

# Code Requirements

1.  **Path Configuration**:
    - Import `sys` and `pathlib`.
    - Insert project root into `sys.path`.

2.  **Imports**:
    - `logging`, `typing.Optional`.
    - `DigestAgent` from `app.agent.digest_agent`.
    - `Repository` from `app.database.repository`.

3.  **Logging Setup**:
    - Configure `logging.basicConfig`: Level INFO, format including timestamp (`%(asctime)s`), datefmt `'%Y-%m-%d %H:%M:%S'`.
    - Initialize `logger`.

4.  **Function `process_digests(limit: Optional[int] = None) -> dict`**:
    - Initialize `agent` and `repo`.
    - Fetch items using `repo.get_articles_without_digest(limit=limit)`.
    - Log start of processing.
    - **Loop Logic**:
        - Iterate with index/enumeration.
        - Log current item being processed (truncate title to 60 chars for readability).
        - **Try/Except Block**:
            - Call `agent.generate_digest(title, content, article_type)`.
            - **If Result**:
                - Call `repo.create_digest` with: `article_type`, `article_id`, `url`, `title`, `summary`, and `published_at`.
                - Increment `processed`.
                - Log success (use "✓" symbol).
            - **If None**:
                - Increment `failed`.
                - Log warning (use "✗" symbol).
        - **Exception**: Catch generic errors, increment `failed`, log error.
    - Log completion summary.
    - Return stats dict (`total`, `processed`, `failed`).

5.  **Execution**:
    - Add `if __name__ == "__main__":` block to run and print stats.

# Style Guide
- Use informative logging to track progress in long batches.
```

---

Prompt_20

```
# Task_5
Generate the file `app/services/process_curator.py`.
This script handles the ranking of news digests based on the user's profile.

# Technical Stack
- **Dependencies:** `app.agent.curator_agent`, `app.profiles.user_profile`, `app.database.repository`.
- **System:** Uses `sys.path` modification.
- **Logging:** Standard logging configuration.

# Code Requirements

1.  **Setup & Imports**:
    - Import `logging`, `sys`, `pathlib`.
    - Import `load_dotenv` and call it.
    - Insert project root into `sys.path`.
    - Import `CuratorAgent` from `app.agent.curator_agent`.
    - Import `USER_PROFILE` from `app.profiles.user_profile`.
    - Import `Repository` from `app.database.repository`.

2.  **Logging**:
    - Configure `logging.basicConfig` (INFO level, timestamp format).
    - Initialize `logger`.

3.  **Function `curate_digests(hours: int = 24) -> dict`**:
    - Initialize `curator` (passing `USER_PROFILE`) and `repo`.
    - Fetch digests via `repo.get_recent_digests(hours)`.
    - **Empty Check**: If no digests found, log warning and return `{"total": 0, "ranked": 0}`.
    - Log start of curation (mention user name/background from profile).
    - **Ranking**: Call `curator.rank_digests(digests)`.
    - **Failure Check**: If no articles returned, log error and return 0 stats.
    - **Logging Top 10**:
        - Iterate through top 10 ranked articles.
        - Find corresponding digest details (title, type) using `digest_id`.
        - Log Rank, Score, Title, Type, and Reasoning clearly.
    - **Return**: A dict containing `total`, `ranked` count, and a list of simplified article dicts (`digest_id`, `rank`, `score`, `reasoning`).

4.  **Execution**:
    - Add `if __name__ == "__main__":` block to run `curate_digests` and print summary.

# Style Guide
- Ensure the logs provide good visibility into *why* an article was ranked (display the reasoning).
```

---

Prompt_21

```
# Task_6
Generate the file `app/services/process_email.py`.
This script orchestrates the full email generation pipeline: fetching news, ranking them, formatting the email, and sending it.

# Technical Stack
- **Dependencies:** `app.agent.email_agent`, `app.agent.curator_agent`, `app.profiles.user_profile`, `app.database.repository`, `app.services.email`.
- **Logging:** Standard logging configuration.

# Code Requirements

1.  **Imports**:
    - `logging`, `load_dotenv`.
    - `EmailAgent`, `RankedArticleDetail`, `EmailDigestResponse` from `app.agent.email_agent`.
    - `CuratorAgent` from `app.agent.curator_agent`.
    - `USER_PROFILE` from `app.profiles.user_profile`.
    - `Repository` from `app.database.repository`.
    - `send_email`, `digest_to_html` from `app.services.email`.

2.  **Function `generate_email_digest(hours: int = 24, top_n: int = 10) -> EmailDigestResponse`**:
    - Initialize agents (`CuratorAgent`, `EmailAgent` with `USER_PROFILE`) and `Repository`.
    - Fetch digests via `repo.get_recent_digests`. Raise ValueError if empty.
    - Rank digests via `curator.rank_digests`. Raise ValueError if empty.
    - **Data Reconstruction Logic (Crucial)**:
        - The ranked articles only have IDs and scores. You must reconstruct `RankedArticleDetail` objects.
        - Iterate through `ranked_articles`.
        - For each, find the matching original digest in the `digests` list (match by ID) to retrieve `title`, `summary`, `url`, `article_type`.
        - Create a list of `RankedArticleDetail` objects.
    - Generate the response object using `email_agent.create_email_digest_response`.
    - Log the generated Greeting and Introduction.
    - Return the `EmailDigestResponse`.

3.  **Function `send_digest_email(hours: int = 24, top_n: int = 10) -> dict`**:
    - Call `generate_email_digest`.
    - Convert result to Markdown (`.to_markdown()`) and HTML (`digest_to_html()`).
    - **Subject Line Logic**: extract the date part from the greeting (e.g., split by "for " and take the last part, or default to "Today"). Format: "Daily AI News Digest - {Date}".
    - Call `send_email`.
    - Return success dict with subject and article count.
    - Handle exceptions (log error and return success=False).

4.  **Execution**:
    - Add `if __name__ == "__main__":` block to run `send_digest_email` and print result.

# Style Guide
- Ensure the data reconstruction step uses efficient lookups (like `next(...)` generators) to find matching digests.
```
