from datetime import datetime, timedelta, timezone
from typing import List, Optional

import feedparser
from docling.document_converter import DocumentConverter
from pydantic import BaseModel


class OpenAIArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class OpenAIScraper:
    def __init__(self):
        """Initialize OpenAIScraper with RSS URL and DocumentConverter."""
        self.rss_url = "https://openai.com/news/rss.xml"
        self.converter = DocumentConverter()

    def get_articles(self, hours: int = 24) -> List[OpenAIArticle]:
        """Fetch articles from OpenAI RSS feed within the specified hours."""
        feed = feedparser.parse(self.rss_url)

        if not feed.entries:
            return []

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        articles = []

        for entry in feed.entries:
            # Parse published time safely
            if hasattr(entry, "published_parsed") and entry.published_parsed:
                published_dt = datetime(*entry.published_parsed[:6]).replace(tzinfo=timezone.utc)
            else:
                continue

            # Filter by time
            if published_dt < cutoff_time:
                continue

            # Extract category from tags if available
            category = None
            if hasattr(entry, "tags") and entry.tags:
                category = entry.tags[0].get("term")

            article = OpenAIArticle(
                title=entry.get("title", ""),
                description=entry.get("summary", ""),
                url=entry.get("link", ""),
                guid=entry.get("id", ""),
                published_at=published_dt,
                category=category,
            )
            articles.append(article)

        return articles


if __name__ == "__main__":
    scraper = OpenAIScraper()
    articles = scraper.get_articles(hours=50)
    print(f"Found {len(articles)} OpenAI articles")
    for article in articles[:5]:
        print(f"  - {article.title}")
