from datetime import datetime, timezone
import pytest

from app.database.repository import Repository


class TestYouTubeVideos:
    """Tests for YouTube video repository operations."""
    
    def test_create_youtube_video(self, test_repository):
        """Test inserting a YouTube video and retrieving it."""
        # Create a test video
        video = test_repository.create_youtube_video(
            video_id="test_video_123",
            title="Test Video Title",
            url="https://youtube.com/watch?v=test_video_123",
            channel_id="test_channel_456",
            published_at=datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc),
            description="This is a test video description",
            transcript="This is a test transcript"
        )
        
        # Verify video was created
        assert video is not None
        assert video.video_id == "test_video_123"
        assert video.title == "Test Video Title"
        assert video.transcript == "This is a test transcript"
    
    def test_youtube_video_deduplication(self, test_repository):
        """Test that inserting the same video twice doesn't crash (idempotency)."""
        # Insert video first time
        video1 = test_repository.create_youtube_video(
            video_id="duplicate_video",
            title="Duplicate Video",
            url="https://youtube.com/watch?v=duplicate_video",
            channel_id="test_channel",
            published_at=datetime.now(timezone.utc),
            description="Test description"
        )
        
        assert video1 is not None
        
        # Try to insert same video again
        video2 = test_repository.create_youtube_video(
            video_id="duplicate_video",
            title="Duplicate Video",
            url="https://youtube.com/watch?v=duplicate_video",
            channel_id="test_channel",
            published_at=datetime.now(timezone.utc),
            description="Test description"
        )
        
        # Should return None (not crash)
        assert video2 is None
    
    def test_get_youtube_videos_without_transcript(self, test_repository):
        """Test retrieving videos that lack transcripts."""
        # Create video without transcript
        test_repository.create_youtube_video(
            video_id="no_transcript_1",
            title="Video Without Transcript",
            url="https://youtube.com/watch?v=no_transcript_1",
            channel_id="test_channel",
            published_at=datetime.now(timezone.utc),
            description="Test",
            transcript=None
        )
        
        # Create video with transcript
        test_repository.create_youtube_video(
            video_id="with_transcript_1",
            title="Video With Transcript",
            url="https://youtube.com/watch?v=with_transcript_1",
            channel_id="test_channel",
            published_at=datetime.now(timezone.utc),
            description="Test",
            transcript="I have a transcript"
        )
        
        # Get videos without transcript
        videos = test_repository.get_youtube_videos_without_transcript()
        
        # Should only return the one without transcript
        assert len(videos) == 1
        assert videos[0].video_id == "no_transcript_1"
    
    def test_update_youtube_video_transcript(self, test_repository):
        """Test updating a video's transcript."""
        # Create video without transcript
        test_repository.create_youtube_video(
            video_id="update_test",
            title="Update Test",
            url="https://youtube.com/watch?v=update_test",
            channel_id="test_channel",
            published_at=datetime.now(timezone.utc),
            description="Test"
        )
        
        # Update transcript
        success = test_repository.update_youtube_video_transcript(
            "update_test",
            "This is the updated transcript"
        )
        
        assert success is True


class TestOpenAIArticles:
    """Tests for OpenAI article repository operations."""
    
    def test_create_openai_article(self, test_repository):
        """Test inserting an OpenAI article and retrieving it."""
        article = test_repository.create_openai_article(
            guid="openai_article_123",
            title="Test OpenAI Article",
            url="https://openai.com/blog/test-article",
            published_at=datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc),
            description="Test article description",
            category="Research"
        )
        
        assert article is not None
        assert article.guid == "openai_article_123"
        assert article.title == "Test OpenAI Article"
        assert article.category == "Research"
    
    def test_openai_article_deduplication(self, test_repository):
        """Test that inserting the same article twice doesn't crash."""
        # Insert first time
        article1 = test_repository.create_openai_article(
            guid="duplicate_openai",
            title="Duplicate OpenAI Article",
            url="https://openai.com/blog/duplicate",
            published_at=datetime.now(timezone.utc),
            description="Test"
        )
        
        assert article1 is not None
        
        # Insert again (should return None)
        article2 = test_repository.create_openai_article(
            guid="duplicate_openai",
            title="Duplicate OpenAI Article",
            url="https://openai.com/blog/duplicate",
            published_at=datetime.now(timezone.utc),
            description="Test"
        )
        
        assert article2 is None


class TestAnthropicArticles:
    """Tests for Anthropic article repository operations."""
    
    def test_create_anthropic_article(self, test_repository):
        """Test inserting an Anthropic article."""
        article = test_repository.create_anthropic_article(
            guid="anthropic_article_123",
            title="Test Anthropic Article",
            url="https://anthropic.com/blog/test-article",
            published_at=datetime(2024, 1, 15, 12, 0, 0, tzinfo=timezone.utc),
            description="Test article description",
            category="News"
        )
        
        assert article is not None
        assert article.guid == "anthropic_article_123"
        assert article.title == "Test Anthropic Article"
        assert article.category == "News"
    
    def test_anthropic_article_deduplication(self, test_repository):
        """Test idempotency of Anthropic article insertion."""
        # Insert first time
        article1 = test_repository.create_anthropic_article(
            guid="duplicate_anthropic",
            title="Duplicate Anthropic Article",
            url="https://anthropic.com/blog/duplicate",
            published_at=datetime.now(timezone.utc),
            description="Test"
        )
        
        assert article1 is not None
        
        # Insert again (should return None)
        article2 = test_repository.create_anthropic_article(
            guid="duplicate_anthropic",
            title="Duplicate Anthropic Article",
            url="https://anthropic.com/blog/duplicate",
            published_at=datetime.now(timezone.utc),
            description="Test"
        )
        
        assert article2 is None
    
    def test_get_anthropic_articles_without_markdown(self, test_repository):
        """Test retrieving Anthropic articles without markdown."""
        # Create article without markdown
        test_repository.create_anthropic_article(
            guid="no_markdown_1",
            title="Article Without Markdown",
            url="https://anthropic.com/blog/no-markdown",
            published_at=datetime.now(timezone.utc),
            description="Test",
            markdown=None
        )
        
        # Create article with markdown
        test_repository.create_anthropic_article(
            guid="with_markdown_1",
            title="Article With Markdown",
            url="https://anthropic.com/blog/with-markdown",
            published_at=datetime.now(timezone.utc),
            description="Test",
            markdown="# Test Markdown"
        )
        
        # Get articles without markdown
        articles = test_repository.get_anthropic_articles_without_markdown()
        
        assert len(articles) == 1
        assert articles[0].guid == "no_markdown_1"
    
    def test_update_anthropic_article_markdown(self, test_repository):
        """Test updating an article's markdown content."""
        # Create article
        test_repository.create_anthropic_article(
            guid="markdown_update_test",
            title="Markdown Update Test",
            url="https://anthropic.com/blog/markdown-test",
            published_at=datetime.now(timezone.utc),
            description="Test"
        )
        
        # Update markdown
        success = test_repository.update_anthropic_article_markdown(
            "markdown_update_test",
            "# Updated Markdown\n\nThis is the updated content."
        )
        
        assert success is True


class TestBulkOperations:
    """Tests for bulk create operations."""
    
    def test_bulk_create_youtube_videos(self, test_repository):
        """Test bulk insertion of YouTube videos."""
        videos = [
            {
                "video_id": "bulk_1",
                "title": "Bulk Video 1",
                "url": "https://youtube.com/watch?v=bulk_1",
                "channel_id": "test_channel",
                "published_at": datetime.now(timezone.utc),
                "description": "Test 1"
            },
            {
                "video_id": "bulk_2",
                "title": "Bulk Video 2",
                "url": "https://youtube.com/watch?v=bulk_2",
                "channel_id": "test_channel",
                "published_at": datetime.now(timezone.utc),
                "description": "Test 2"
            }
        ]
        
        added_count = test_repository.bulk_create_youtube_videos(videos)
        assert added_count == 2
        
        # Trying to add again should return 0
        added_count = test_repository.bulk_create_youtube_videos(videos)
        assert added_count == 0
    
    def test_bulk_create_openai_articles(self, test_repository):
        """Test bulk insertion of OpenAI articles."""
        articles = [
            {
                "guid": "bulk_openai_1",
                "title": "Bulk OpenAI 1",
                "url": "https://openai.com/blog/bulk-1",
                "published_at": datetime.now(timezone.utc),
                "description": "Test 1"
            },
            {
                "guid": "bulk_openai_2",
                "title": "Bulk OpenAI 2",
                "url": "https://openai.com/blog/bulk-2",
                "published_at": datetime.now(timezone.utc),
                "description": "Test 2"
            }
        ]
        
        added_count = test_repository.bulk_create_openai_articles(articles)
        assert added_count == 2
    
    def test_bulk_create_anthropic_articles(self, test_repository):
        """Test bulk insertion of Anthropic articles."""
        articles = [
            {
                "guid": "bulk_anthropic_1",
                "title": "Bulk Anthropic 1",
                "url": "https://anthropic.com/blog/bulk-1",
                "published_at": datetime.now(timezone.utc),
                "description": "Test 1"
            },
            {
                "guid": "bulk_anthropic_2",
                "title": "Bulk Anthropic 2",
                "url": "https://anthropic.com/blog/bulk-2",
                "published_at": datetime.now(timezone.utc),
                "description": "Test 2"
            }
        ]
        
        added_count = test_repository.bulk_create_anthropic_articles(articles)
        assert added_count == 2
