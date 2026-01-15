from typing import List

from .config import YOUTUBE_CHANNELS
from .scrapers.youtube import YouTubeScraper, ChannelVideo
from .scrapers.openai import OpenAIScraper, OpenAIArticle
from .scrapers.anthropic import AnthropicScraper, AnthropicArticle
from .database.repository import Repository


def run_scrapers(hours: int = 24) -> dict:
    """
    Execute all scrapers and persist raw data to the database.
    
    This function acts as a registry that runs all configured scrapers
    (YouTube, OpenAI, Anthropic) and saves the collected data to the database.
    
    Args:
        hours: Number of hours to look back for new content (default: 24)
        
    Returns:
        Dictionary containing lists of scraped items for each source:
        - youtube: List of ChannelVideo objects
        - openai: List of OpenAIArticle objects
        - anthropic: List of AnthropicArticle objects
    """
    # Initialize scrapers and repository
    youtube_scraper = YouTubeScraper()
    openai_scraper = OpenAIScraper()
    anthropic_scraper = AnthropicScraper()
    repo = Repository()
    
    # Results storage
    youtube_videos: List[ChannelVideo] = []
    openai_articles: List[OpenAIArticle] = []
    anthropic_articles: List[AnthropicArticle] = []
    
    # ==================== YouTube Scraping ====================
    print(f"Scraping YouTube channels ({len(YOUTUBE_CHANNELS)} channels)...")
    
    for channel_id in YOUTUBE_CHANNELS:
        print(f"  Fetching videos from channel: {channel_id}")
        videos = youtube_scraper.get_latest_videos(channel_id, hours=hours)
        youtube_videos.extend(videos)
        print(f"    Found {len(videos)} videos")
    
    # Convert Pydantic models to dictionaries for database
    if youtube_videos:
        video_dicts = []
        for video in youtube_videos:
            video_dicts.append({
                'video_id': video.video_id,
                'title': video.title,
                'url': video.url,
                'channel_id': video.channel_id,
                'published_at': video.published_at,
                'description': video.description,
                'transcript': video.transcript
            })
        
        # Bulk save to database
        saved_count = repo.bulk_create_youtube_videos(video_dicts)
        print(f"  ✓ Saved {saved_count} new YouTube videos to database")
    else:
        print(f"  ⚠ No YouTube videos found")
    
    # ==================== OpenAI Scraping ====================
    print(f"\nScraping OpenAI news...")
    openai_articles = openai_scraper.get_articles(hours=hours)
    print(f"  Found {len(openai_articles)} articles")
    
    # Convert Pydantic models to dictionaries
    if openai_articles:
        article_dicts = []
        for article in openai_articles:
            article_dicts.append({
                'guid': article.guid,
                'title': article.title,
                'url': article.url,
                'description': article.description,
                'published_at': article.published_at,
                'category': article.category
            })
        
        # Bulk save to database
        saved_count = repo.bulk_create_openai_articles(article_dicts)
        print(f"  ✓ Saved {saved_count} new OpenAI articles to database")
    else:
        print(f"  ⚠ No OpenAI articles found")
    
    # ==================== Anthropic Scraping ====================
    print(f"\nScraping Anthropic news...")
    anthropic_articles = anthropic_scraper.get_articles(hours=hours)
    print(f"  Found {len(anthropic_articles)} articles")
    
    # Convert Pydantic models to dictionaries
    if anthropic_articles:
        article_dicts = []
        for article in anthropic_articles:
            article_dicts.append({
                'guid': article.guid,
                'title': article.title,
                'url': article.url,
                'description': article.description,
                'published_at': article.published_at,
                'category': article.category,
                'markdown': None  # Will be populated by process_anthropic service
            })
        
        # Bulk save to database
        saved_count = repo.bulk_create_anthropic_articles(article_dicts)
        print(f"  ✓ Saved {saved_count} new Anthropic articles to database")
    else:
        print(f"  ⚠ No Anthropic articles found")
    
    # Return all scraped data
    return {
        "youtube": youtube_videos,
        "openai": openai_articles,
        "anthropic": anthropic_articles
    }


if __name__ == "__main__":
    print("=" * 60)
    print("Running News Scrapers")
    print("=" * 60)
    print()
    
    results = run_scrapers(hours=24)
    
    print()
    print("=" * 60)
    print("Scraping Complete!")
    print("=" * 60)
    print(f"YouTube videos: {len(results['youtube'])}")
    print(f"OpenAI articles: {len(results['openai'])}")
    print(f"Anthropic articles: {len(results['anthropic'])}")
    print(f"Total items: {len(results['youtube']) + len(results['openai']) + len(results['anthropic'])}")
    print("=" * 60)
