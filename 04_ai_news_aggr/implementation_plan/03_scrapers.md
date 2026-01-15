Prompt_08
```
# Task_1
Generate the file `app/config.py`.

# Content of the file

YOUTUBE_CHANNELS = [
    "UCawZsQWqfGSbCI5yjkdVkTA", # Matthew Berman
]

```

---

Prompt_09

```
# Task_2
Generate the file `app/scrapers/youtube.py`.
This module fetches video metadata via RSS and retrieves transcripts using the `youtube-transcript-api`.

# Technical Stack
- **Libs:** `feedparser`, `pydantic`, `youtube_transcript_api` (specifically `YouTubeTranscriptApi`, `TranscriptsDisabled`, `NoTranscriptFound`, and `proxies.WebshareProxyConfig`).

# Code Requirements

1.  **Data Models (Pydantic)**:
    - `Transcript`: Field `text` (str).
    - `ChannelVideo`: Fields `title`, `url`, `video_id`, `published_at` (datetime), `description`, `transcript` (Optional[str], default None).

2.  **Class `YouTubeScraper`**:
    - **`__init__`**:
        - Check for environment variables `PROXY_USERNAME` and `PROXY_PASSWORD`.
        - If present, configure `WebshareProxyConfig` and pass it to `YouTubeTranscriptApi`.
        - If not, initialize API without proxies.
    - **`_extract_video_id(self, video_url: str) -> str`**:
        - Handle three URL formats: Standard (`youtube.com/watch?v=`), Shorts (`youtube.com/shorts/`), and Shortened (`youtu.be/`).
    - **`get_transcript(self, video_id: str) -> Optional[Transcript]`**:
        - Fetch transcript.
        - Logic: Join all text snippets into a single string.
        - Error Handling: Catch `TranscriptsDisabled`, `NoTranscriptFound` (return None). Catch generic Exception (return None).
    - **`get_latest_videos(self, channel_id: str, hours: int = 24) -> list[ChannelVideo]`**:
        - Parse RSS feed: `https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}`.
        - Filter: Ignore videos containing `/shorts/`.
        - Filter: Only keep videos published within the last `hours` (UTC).
        - Return list of `ChannelVideo` (without transcript yet).
    - **`scrape_channel(self, channel_id: str, hours: int = 150) -> list[ChannelVideo]`**:
        - Orchestrator method.
        - First call `get_latest_videos`.
        - Then iterate through results and call `get_transcript` for each.
        - Use `video.model_copy(update={"transcript": ...})` to return the updated object.

3.  **Testing**:
    - Add `if __name__ == "__main__":` block.
    - Test fetching a transcript for a known ID.
    - Test `scrape_channel` with a sample Channel ID.

# Logic Specifics
- Ensure strict UTC timezone handling for `published_at`.
- Use `os.getenv` for secrets.

```

---

Prompt_10

```
# Task_3
Generate the file `app/scrapers/openai.py`.
This module fetches news from the official OpenAI RSS feed and prepares it for processing.

# Technical Stack
- **Libraries:** `feedparser`, `pydantic`, `docling` (DocumentConverter).

# Code Requirements

1.  **Imports**:
    - Standard: `datetime`, `timedelta`, `timezone`, `typing` (List, Optional).
    - Third-party: `feedparser`, `docling.document_converter`, `pydantic`.

2.  **Data Model**:
    - Create a Pydantic model named `OpenAIArticle`.
    - Fields: `title`, `description`, `url`, `guid`, `published_at` (datetime), `category` (Optional[str]).

3.  **Class `OpenAIScraper`**:
    - **`__init__`**:
        - Initialize `self.rss_url` to `"https://openai.com/news/rss.xml"`.
        - Initialize `self.converter` as an instance of `DocumentConverter`.
    - **`get_articles(self, hours: int = 24) -> List[OpenAIArticle]`**:
        - Parse the RSS feed using `feedparser`.
        - Return an empty list if `feed.entries` is empty.
        - Calculate `cutoff_time` based on `datetime.now(timezone.utc)`.
        - Iterate through entries and filter by `published_time` >= `cutoff_time`.
        - Handle date parsing safely using `published_parsed`.
        - Extract the category from tags if available.
        - Return a list of `OpenAIArticle` objects.

4.  **Testing**:
    - Add a `if __name__ == "__main__":` block.
    - Instantiate the scraper and call `get_articles(hours=50)`.
    - (Optional) Print the number of articles found.

# Style Guide
- Maintain strict type hinting.
- Ensure the code structure mirrors the `AnthropicScraper` for consistency.
```

---

Prompt_11

```
# Task_4
Generate the file `app/scrapers/anthropic.py`.
This module fetches blog articles from Anthropic using specific RSS feeds hosted on GitHub and converts the content into Markdown.

# Technical Stack
- **Libraries:** `feedparser`, `pydantic`, `docling` (specifically `DocumentConverter`).

# Code Requirements

1.  **Imports**:
    - Standard: `datetime`, `timedelta`, `timezone` from `datetime`, `typing` (List, Optional).
    - Third-party: `feedparser`, `docling.document_converter`, `pydantic`.

2.  **Data Model**:
    - Create a Pydantic model named `AnthropicArticle`.
    - Fields: `title` (str), `description` (str), `url` (str), `guid` (str), `published_at` (datetime), `category` (Optional[str], default None).

3.  **Class `AnthropicScraper`**:
    - **`__init__`**:
        - Initialize `self.converter` as an instance of `DocumentConverter`.
        - Initialize `self.rss_urls` with this specific list of RSS feeds:
          - `"https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml"`
          - `"https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml"`
          - `"https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml"`
    - **`get_articles(self, hours: int = 24) -> List[AnthropicArticle]`**:
        - Calculate `cutoff_time` based on `datetime.now(timezone.utc)`.
        - Iterate through `self.rss_urls` and parse them using `feedparser`.
        - Filter entries: Only keep those where `published_parsed` converts to a datetime newer than `cutoff_time`.
        - Deduplication: Use a set to track seen GUIDs (`entry.get("id")` or `entry.get("link")`).
        - Map valid entries to `AnthropicArticle` objects. For `category`, try to extract it from `entry.get("tags")[0]`.
    - **`url_to_markdown(self, url: str) -> Optional[str]`**:
        - Use `self.converter.convert(url)` to process the page.
        - Return `result.document.export_to_markdown()`.
        - Wrap in a try/except block to return `None` on failure.

4.  **Testing**:
    - Add a `if __name__ == "__main__":` block at the end.
    - Instantiate the scraper, call `get_articles(hours=100)`, and print the markdown of the second article found.

# Style Guide
- Use Type Hinting everywhere.
- Ensure strict UTC timezone handling for date comparisons.
```

