from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel
from docling.document_converter import DocumentConverter


class OpenAIArticle(BaseModel):
    """Model for OpenAI news articles."""
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class OpenAIScraper:
    """Scraper for fetching news from the official OpenAI RSS feed."""
    
    def __init__(self):
        """Initialize the OpenAI scraper with RSS URL and document converter."""
        self.rss_url = "https://openai.com/news/rss.xml"
        self.converter = DocumentConverter()
    
    def get_articles(self, hours: int = 24) -> List[OpenAIArticle]:
        """
        Fetch articles from the OpenAI RSS feed published within the specified time window.
        
        Args:
            hours: Number of hours to look back (default: 24)
            
        Returns:
            List of OpenAIArticle objects
        """
        # Parse the RSS feed
        feed = feedparser.parse(self.rss_url)
        
        # Return empty list if no entries found
        if not feed.entries:
            return []
        
        # Calculate cutoff time in UTC
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        articles = []
        
        for entry in feed.entries:
            # Parse published time safely
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            else:
                # Skip entries without valid publication time
                continue
            
            # Filter by time - only keep articles within the specified hours
            if published_time >= cutoff_time:
                # Extract category from tags if available
                category = None
                if hasattr(entry, 'tags') and entry.tags:
                    category = entry.tags[0].get('term', None)
                
                article = OpenAIArticle(
                    title=entry.title,
                    description=entry.get('summary', ''),
                    url=entry.link,
                    guid=entry.get('id', entry.link),
                    published_at=published_time,
                    category=category
                )
                articles.append(article)
        
        return articles


if __name__ == "__main__":
    # Test the scraper
    print("Testing OpenAI scraper...")
    scraper = OpenAIScraper()
    
    # Fetch articles from the last 50 hours
    articles = scraper.get_articles(hours=50)
    
    print(f"Found {len(articles)} articles")
    
    # Print details of the articles
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article.title}")
        print(f"   URL: {article.url}")
        print(f"   Published: {article.published_at}")
        print(f"   Category: {article.category or 'N/A'}")
        print(f"   Description: {article.description[:100]}..." if len(article.description) > 100 else f"   Description: {article.description}")
