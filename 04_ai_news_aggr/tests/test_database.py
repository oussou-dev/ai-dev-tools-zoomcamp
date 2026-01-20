from datetime import datetime, timezone

import pytest

from app.database.repository import Repository
from app.database.models import YouTubeVideo, OpenAIArticle, AnthropicArticle


class TestYouTubeRepository:
    """Test YouTube video operations."""

    def test_create_youtube_video(self, test_db):
        """Test inserting a YouTube video and retrieving it."""
        repo = Repository(session=test_db)

        video_data = {
            "video_id": "test_video_1",
            "title": "Test Video",
            "url": "https://youtube.com/watch?v=test_video_1",
            "channel_id": "UCtest123",
            "published_at": datetime.now(timezone.utc),
            "description": "Test description",
            "transcript": None,
        }

        # Create video
        created_video = repo.create_youtube_video(**video_data)
        assert created_video.video_id == "test_video_1"
        assert created_video.title == "Test Video"

        # Retrieve video
        retrieved = test_db.query(YouTubeVideo).filter_by(video_id="test_video_1").first()
        assert retrieved is not None
        assert retrieved.title == "Test Video"

    def test_youtube_video_deduplication(self, test_db):
        """Test that inserting the same video twice doesn't cause issues."""
        repo = Repository(session=test_db)

        video_data = {
            "video_id": "test_video_dup",
            "title": "Test Video",
            "url": "https://youtube.com/watch?v=test_video_dup",
            "channel_id": "UCtest123",
            "published_at": datetime.now(timezone.utc),
            "description": "Test description",
        }

        # Create video twice
        first = repo.create_youtube_video(**video_data)
        second = repo.create_youtube_video(**video_data)

        # Both should return the same video
        assert first.video_id == second.video_id
        assert first.video_id == "test_video_dup"

        # Check that only one entry exists in database
        count = test_db.query(YouTubeVideo).filter_by(video_id="test_video_dup").count()
        assert count == 1

    def test_bulk_create_youtube_videos(self, test_db):
        """Test bulk creating YouTube videos."""
        repo = Repository(session=test_db)

        videos = [
            {
                "video_id": f"video_{i}",
                "title": f"Video {i}",
                "url": f"https://youtube.com/watch?v=video_{i}",
                "channel_id": "UCtest123",
                "published_at": datetime.now(timezone.utc),
                "description": f"Description {i}",
            }
            for i in range(3)
        ]

        added = repo.bulk_create_youtube_videos(videos)
        assert added == 3

        # Verify all videos exist
        count = test_db.query(YouTubeVideo).count()
        assert count == 3


class TestOpenAIRepository:
    """Test OpenAI article operations."""

    def test_create_openai_article(self, test_db):
        """Test inserting an OpenAI article and retrieving it."""
        repo = Repository(session=test_db)

        article_data = {
            "guid": "openai_article_1",
            "title": "OpenAI Article",
            "url": "https://openai.com/news/article-1",
            "published_at": datetime.now(timezone.utc),
            "description": "Test article",
            "category": "research",
        }

        # Create article
        created = repo.create_openai_article(**article_data)
        assert created.guid == "openai_article_1"
        assert created.title == "OpenAI Article"

        # Retrieve article
        retrieved = test_db.query(OpenAIArticle).filter_by(guid="openai_article_1").first()
        assert retrieved is not None
        assert retrieved.title == "OpenAI Article"

    def test_openai_article_deduplication(self, test_db):
        """Test that inserting the same article twice doesn't cause issues."""
        repo = Repository(session=test_db)

        article_data = {
            "guid": "openai_article_dup",
            "title": "OpenAI Article",
            "url": "https://openai.com/news/article-dup",
            "published_at": datetime.now(timezone.utc),
            "description": "Test article",
        }

        # Create article twice
        first = repo.create_openai_article(**article_data)
        second = repo.create_openai_article(**article_data)

        # Both should return the same article
        assert first.guid == second.guid

        # Check that only one entry exists
        count = test_db.query(OpenAIArticle).filter_by(guid="openai_article_dup").count()
        assert count == 1

    def test_bulk_create_openai_articles(self, test_db):
        """Test bulk creating OpenAI articles."""
        repo = Repository(session=test_db)

        articles = [
            {
                "guid": f"article_{i}",
                "title": f"Article {i}",
                "url": f"https://openai.com/news/article-{i}",
                "published_at": datetime.now(timezone.utc),
                "description": f"Description {i}",
            }
            for i in range(3)
        ]

        added = repo.bulk_create_openai_articles(articles)
        assert added == 3

        # Verify all articles exist
        count = test_db.query(OpenAIArticle).count()
        assert count == 3


class TestAnthropicRepository:
    """Test Anthropic article operations."""

    def test_create_anthropic_article(self, test_db):
        """Test inserting an Anthropic article and retrieving it."""
        repo = Repository(session=test_db)

        article_data = {
            "guid": "anthropic_article_1",
            "title": "Anthropic Article",
            "url": "https://anthropic.com/research/article-1",
            "published_at": datetime.now(timezone.utc),
            "description": "Test article",
            "category": "research",
            "markdown": None,
        }

        # Create article
        created = repo.create_anthropic_article(**article_data)
        assert created.guid == "anthropic_article_1"
        assert created.title == "Anthropic Article"

        # Retrieve article
        retrieved = test_db.query(AnthropicArticle).filter_by(guid="anthropic_article_1").first()
        assert retrieved is not None
        assert retrieved.title == "Anthropic Article"

    def test_anthropic_article_deduplication(self, test_db):
        """Test that inserting the same Anthropic article twice doesn't cause issues."""
        repo = Repository(session=test_db)

        article_data = {
            "guid": "anthropic_article_dup",
            "title": "Anthropic Article",
            "url": "https://anthropic.com/research/article-dup",
            "published_at": datetime.now(timezone.utc),
            "description": "Test article",
        }

        # Create article twice
        first = repo.create_anthropic_article(**article_data)
        second = repo.create_anthropic_article(**article_data)

        # Both should return the same article
        assert first.guid == second.guid

        # Check that only one entry exists
        count = test_db.query(AnthropicArticle).filter_by(guid="anthropic_article_dup").count()
        assert count == 1

    def test_bulk_create_anthropic_articles(self, test_db):
        """Test bulk creating Anthropic articles."""
        repo = Repository(session=test_db)

        articles = [
            {
                "guid": f"article_{i}",
                "title": f"Article {i}",
                "url": f"https://anthropic.com/research/article-{i}",
                "published_at": datetime.now(timezone.utc),
                "description": f"Description {i}",
            }
            for i in range(3)
        ]

        added = repo.bulk_create_anthropic_articles(articles)
        assert added == 3

        # Verify all articles exist
        count = test_db.query(AnthropicArticle).count()
        assert count == 3
