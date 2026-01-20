from datetime import datetime, timedelta, timezone
from typing import List, Optional

import feedparser
from docling.document_converter import DocumentConverter
from pydantic import BaseModel


class AnthropicArticle(BaseModel):
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class AnthropicScraper:
    def __init__(self):
        """Initialize AnthropicScraper with DocumentConverter and RSS feed URLs."""
        self.converter = DocumentConverter()
        self.rss_urls = [
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        ]

    def get_articles(self, hours: int = 24) -> List[AnthropicArticle]:
        """Fetch articles from Anthropic RSS feeds within the specified hours."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        articles = []
        seen_guids = set()

        for rss_url in self.rss_urls:
            feed = feedparser.parse(rss_url)

            for entry in feed.entries:
                # Parse published time safely
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    published_dt = datetime(*entry.published_parsed[:6]).replace(tzinfo=timezone.utc)
                else:
                    continue

                # Filter by time
                if published_dt < cutoff_time:
                    continue

                # Get GUID or use link as fallback
                guid = entry.get("id") or entry.get("link")
                if not guid or guid in seen_guids:
                    continue

                seen_guids.add(guid)

                # Extract category from tags if available
                category = None
                if hasattr(entry, "tags") and entry.tags:
                    category = entry.tags[0].get("term")

                article = AnthropicArticle(
                    title=entry.get("title", ""),
                    description=entry.get("summary", ""),
                    url=entry.get("link", ""),
                    guid=guid,
                    published_at=published_dt,
                    category=category,
                )
                articles.append(article)

        return articles

    def url_to_markdown(self, url: str) -> Optional[str]:
        """Convert a URL to markdown using DocumentConverter."""
        try:
            result = self.converter.convert(url)
            return result.document.export_to_markdown()
        except Exception:
            return None


if __name__ == "__main__":
    scraper = AnthropicScraper()
    articles = scraper.get_articles(hours=100)
    print(f"Found {len(articles)} Anthropic articles")

    if len(articles) > 1:
        second_article = articles[1]
        markdown = scraper.url_to_markdown(second_article.url)
        if markdown:
            print(f"\nMarkdown of '{second_article.title}':")
            print(markdown[:500])
        else:
            print(f"\nCould not convert '{second_article.title}' to markdown")
