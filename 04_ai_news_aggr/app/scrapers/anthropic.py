from datetime import datetime, timedelta, timezone
from typing import List, Optional
import feedparser
from pydantic import BaseModel
from docling.document_converter import DocumentConverter


class AnthropicArticle(BaseModel):
    """Model for Anthropic blog articles."""
    title: str
    description: str
    url: str
    guid: str
    published_at: datetime
    category: Optional[str] = None


class AnthropicScraper:
    """Scraper for fetching blog articles from Anthropic using RSS feeds."""
    
    def __init__(self):
        """Initialize the Anthropic scraper with document converter and RSS feed URLs."""
        self.converter = DocumentConverter()
        self.rss_urls = [
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_research.xml",
            "https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_engineering.xml",
        ]
    
    def get_articles(self, hours: int = 24) -> List[AnthropicArticle]:
        """
        Fetch articles from Anthropic RSS feeds published within the specified time window.
        
        Args:
            hours: Number of hours to look back (default: 24)
            
        Returns:
            List of AnthropicArticle objects (deduplicated)
        """
        # Calculate cutoff time in UTC
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        articles = []
        seen_guids = set()  # For deduplication
        
        # Iterate through all RSS feeds
        for rss_url in self.rss_urls:
            # Parse the RSS feed
            feed = feedparser.parse(rss_url)
            
            # Process entries if feed is valid
            if not hasattr(feed, 'entries'):
                continue
            
            for entry in feed.entries:
                # Parse published time safely
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                else:
                    # Skip entries without valid publication time
                    continue
                
                # Filter by time - only keep articles within the specified hours
                if published_time < cutoff_time:
                    continue
                
                # Extract GUID for deduplication
                guid = entry.get('id') or entry.get('link')
                
                # Skip if we've already seen this article
                if guid in seen_guids:
                    continue
                
                seen_guids.add(guid)
                
                # Extract category from tags if available
                category = None
                if hasattr(entry, 'tags') and entry.tags:
                    try:
                        category = entry.tags[0].get('term', None)
                    except (IndexError, AttributeError):
                        category = None
                
                article = AnthropicArticle(
                    title=entry.title,
                    description=entry.get('summary', ''),
                    url=entry.link,
                    guid=guid,
                    published_at=published_time,
                    category=category
                )
                articles.append(article)
        
        return articles
    
    def url_to_markdown(self, url: str) -> Optional[str]:
        """
        Convert a web page URL to Markdown format using docling.
        
        Args:
            url: URL of the page to convert
            
        Returns:
            Markdown content string if successful, None otherwise
        """
        try:
            # Convert the URL to a document
            result = self.converter.convert(url)
            
            # Export to markdown
            markdown_content = result.document.export_to_markdown()
            
            return markdown_content
            
        except Exception as e:
            print(f"Error converting {url} to markdown: {e}")
            return None


if __name__ == "__main__":
    # Test the scraper
    print("Testing Anthropic scraper...")
    scraper = AnthropicScraper()
    
    # Fetch articles from the last 100 hours
    articles = scraper.get_articles(hours=100)
    
    print(f"Found {len(articles)} articles")
    
    # Print details of the articles
    for i, article in enumerate(articles, 1):
        print(f"\n{i}. {article.title}")
        print(f"   URL: {article.url}")
        print(f"   Published: {article.published_at}")
        print(f"   Category: {article.category or 'N/A'}")
        print(f"   Description: {article.description[:100]}..." if len(article.description) > 100 else f"   Description: {article.description}")
    
    # Test markdown conversion on the second article if available
    if len(articles) >= 2:
        print("\n" + "="*80)
        print("Testing markdown conversion on second article...")
        print("="*80)
        
        markdown = scraper.url_to_markdown(articles[1].url)
        if markdown:
            print(f"\nMarkdown content (first 500 characters):")
            print(markdown[:500])
            print(f"\n... (Total length: {len(markdown)} characters)")
        else:
            print("Failed to convert article to markdown")
