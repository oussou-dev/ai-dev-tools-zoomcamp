from typing import List

from app.config import YOUTUBE_CHANNELS
from app.scrapers.youtube import YouTubeScraper
from app.scrapers.openai import OpenAIScraper
from app.scrapers.anthropic import AnthropicScraper
from app.database.repository import Repository


def run_scrapers(hours: int = 24) -> dict:
    """Run all scrapers and persist raw data to database.

    Args:
        hours: Number of hours to look back for content

    Returns:
        Dictionary with scraped objects: {"youtube": [...], "openai": [...], "anthropic": [...]}
    """
    youtube_scraper = YouTubeScraper()
    openai_scraper = OpenAIScraper()
    anthropic_scraper = AnthropicScraper()
    repo = Repository()

    youtube_videos = []
    openai_articles = []
    anthropic_articles = []

    # YouTube Logic
    for channel_id in YOUTUBE_CHANNELS:
        videos = youtube_scraper.get_latest_videos(channel_id, hours=hours)

        # Convert Pydantic models to dictionaries
        video_dicts = [
            {
                "video_id": video.video_id,
                "title": video.title,
                "url": video.url,
                "channel_id": video.channel_id,
                "published_at": video.published_at,
                "description": video.description,
                "transcript": video.transcript,
            }
            for video in videos
        ]

        repo.bulk_create_youtube_videos(video_dicts)
        youtube_videos.extend(videos)

    # OpenAI Logic
    openai_articles_models = openai_scraper.get_articles(hours=hours)
    openai_dicts = [
        {
            "guid": article.guid,
            "title": article.title,
            "url": article.url,
            "description": article.description,
            "published_at": article.published_at,
            "category": article.category,
        }
        for article in openai_articles_models
    ]
    repo.bulk_create_openai_articles(openai_dicts)
    openai_articles.extend(openai_articles_models)

    # Anthropic Logic
    anthropic_articles_models = anthropic_scraper.get_articles(hours=hours)
    anthropic_dicts = [
        {
            "guid": article.guid,
            "title": article.title,
            "url": article.url,
            "description": article.description,
            "published_at": article.published_at,
            "category": article.category,
            "markdown": article.markdown,
        }
        for article in anthropic_articles_models
    ]
    repo.bulk_create_anthropic_articles(anthropic_dicts)
    anthropic_articles.extend(anthropic_articles_models)

    return {
        "youtube": youtube_videos,
        "openai": openai_articles,
        "anthropic": anthropic_articles,
    }


if __name__ == "__main__":
    results = run_scrapers()
    print(f"Scraper Results:")
    print(f"  YouTube: {len(results['youtube'])} videos")
    print(f"  OpenAI: {len(results['openai'])} articles")
    print(f"  Anthropic: {len(results['anthropic'])} articles")
