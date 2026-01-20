from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

import pytest

from app.agents.digest_agent import DigestOutput
from app.runner import run_scrapers
from app.daily_runner import run_daily_pipeline


class TestScrapersMocked:
    """Test scrapers with mocked data."""

    @patch("app.runner.YouTubeScraper")
    @patch("app.runner.OpenAIScraper")
    @patch("app.runner.AnthropicScraper")
    @patch("app.runner.Repository")
    def test_run_scrapers_with_mocked_data(
        self,
        mock_repo_class,
        mock_anthropic_scraper_class,
        mock_openai_scraper_class,
        mock_youtube_scraper_class,
    ):
        """Test run_scrapers with mocked scrapers returning fake data."""
        # Mock YouTube scraper
        mock_youtube = MagicMock()
        mock_youtube_scraper_class.return_value = mock_youtube

        from app.scrapers.youtube import ChannelVideo

        mock_youtube.get_latest_videos.return_value = [
            ChannelVideo(
                title="Test Video 1",
                url="https://youtube.com/watch?v=test1",
                video_id="test1",
                published_at=datetime.now(timezone.utc),
                description="Test video description",
            ),
            ChannelVideo(
                title="Test Video 2",
                url="https://youtube.com/watch?v=test2",
                video_id="test2",
                published_at=datetime.now(timezone.utc),
                description="Test video description 2",
            ),
        ]

        # Mock OpenAI scraper
        mock_openai = MagicMock()
        mock_openai_scraper_class.return_value = mock_openai

        from app.scrapers.openai import OpenAIArticle as OpenAIArticleModel

        mock_openai.get_articles.return_value = [
            OpenAIArticleModel(
                title="OpenAI News",
                description="OpenAI article",
                url="https://openai.com/news/article1",
                guid="openai_1",
                published_at=datetime.now(timezone.utc),
            ),
        ]

        # Mock Anthropic scraper
        mock_anthropic = MagicMock()
        mock_anthropic_scraper_class.return_value = mock_anthropic

        from app.scrapers.anthropic import AnthropicArticle as AnthropicArticleModel

        mock_anthropic.get_articles.return_value = [
            AnthropicArticleModel(
                title="Anthropic Research",
                description="Anthropic article",
                url="https://anthropic.com/research/article1",
                guid="anthropic_1",
                published_at=datetime.now(timezone.utc),
            ),
        ]

        # Mock Repository
        mock_repo = MagicMock()
        mock_repo_class.return_value = mock_repo
        mock_repo.bulk_create_youtube_videos.return_value = 2
        mock_repo.bulk_create_openai_articles.return_value = 1
        mock_repo.bulk_create_anthropic_articles.return_value = 1

        # Run scrapers
        result = run_scrapers(hours=24)

        # Verify results
        assert len(result["youtube"]) == 2
        assert len(result["openai"]) == 1
        assert len(result["anthropic"]) == 1

        # Verify bulk creates were called
        assert mock_repo.bulk_create_youtube_videos.called
        assert mock_repo.bulk_create_openai_articles.called
        assert mock_repo.bulk_create_anthropic_articles.called


class TestPipelineWithMocks:
    """Test the full pipeline with mocked external services."""

    @patch("app.daily_runner.send_digest_email")
    @patch("app.daily_runner.process_digests")
    @patch("app.daily_runner.process_youtube_transcripts")
    @patch("app.daily_runner.process_anthropic_markdown")
    @patch("app.daily_runner.run_scrapers")
    def test_daily_pipeline_with_mocked_services(
        self,
        mock_run_scrapers,
        mock_anthropic,
        mock_youtube,
        mock_digests,
        mock_email,
    ):
        """Test the daily pipeline with all external services mocked."""
        # Mock scraper results
        from app.scrapers.youtube import ChannelVideo

        mock_run_scrapers.return_value = {
            "youtube": [
                ChannelVideo(
                    title="Test Video",
                    url="https://youtube.com/watch?v=test",
                    video_id="test_video",
                    published_at=datetime.now(timezone.utc),
                    description="Test",
                )
            ],
            "openai": [],
            "anthropic": [],
        }

        # Mock processing results
        mock_anthropic.return_value = {"total": 0, "processed": 0, "failed": 0}
        mock_youtube.return_value = {"total": 1, "processed": 1, "unavailable": 0, "failed": 0}
        mock_digests.return_value = {"total": 1, "processed": 1, "failed": 0}

        # Mock email sending (success)
        mock_email.return_value = {
            "success": True,
            "subject": "Daily AI News Digest - January 20, 2025",
            "articles_count": 1,
        }

        # Run pipeline
        result = run_daily_pipeline(hours=24, top_n=10)

        # Verify success
        assert result["success"] is True

        # Verify all steps were called
        assert mock_run_scrapers.called
        assert mock_anthropic.called
        assert mock_youtube.called
        assert mock_digests.called
        assert mock_email.called

        # Verify results structure
        assert "scraping" in result
        assert "processing" in result
        assert "digests" in result
        assert "email" in result

    @patch("app.daily_runner.send_digest_email")
    @patch("app.daily_runner.process_digests")
    @patch("app.daily_runner.process_youtube_transcripts")
    @patch("app.daily_runner.process_anthropic_markdown")
    @patch("app.daily_runner.run_scrapers")
    def test_daily_pipeline_handles_email_failure(
        self,
        mock_run_scrapers,
        mock_anthropic,
        mock_youtube,
        mock_digests,
        mock_email,
    ):
        """Test that pipeline handles email sending failure gracefully."""
        # Mock scraper results
        from app.scrapers.youtube import ChannelVideo

        mock_run_scrapers.return_value = {
            "youtube": [
                ChannelVideo(
                    title="Test Video",
                    url="https://youtube.com/watch?v=test",
                    video_id="test_video",
                    published_at=datetime.now(timezone.utc),
                    description="Test",
                )
            ],
            "openai": [],
            "anthropic": [],
        }

        # Mock processing results
        mock_anthropic.return_value = {"total": 0, "processed": 0, "failed": 0}
        mock_youtube.return_value = {"total": 1, "processed": 1, "unavailable": 0, "failed": 0}
        mock_digests.return_value = {"total": 1, "processed": 1, "failed": 0}

        # Mock email sending (failure)
        mock_email.return_value = {
            "success": False,
            "error": "Email credentials not configured",
        }

        # Run pipeline
        result = run_daily_pipeline(hours=24, top_n=10)

        # Verify failure
        assert result["success"] is False

        # Verify email result in results
        assert "email" in result
        assert result["email"]["success"] is False


class TestDigestAgentMocked:
    """Test digest generation with mocked LLM."""

    @patch("app.agents.digest_agent.DigestAgent.generate_digest")
    def test_mocked_digest_generation(self, mock_generate):
        """Test that digest agent can be mocked to return static summaries."""
        from app.agents.digest_agent import DigestAgent

        # Mock the generate_digest method to return a static response
        mock_generate.return_value = DigestOutput(
            title="Test Article Summary",
            summary="This is a test summary of the article.",
        )

        agent = DigestAgent()
        result = agent.generate_digest(
            title="Original Article",
            content="This is the original article content.",
            article_type="test",
        )

        # Verify mocked result
        assert result.title == "Test Article Summary"
        assert result.summary == "This is a test summary of the article."

        # Verify mock was called
        assert mock_generate.called
