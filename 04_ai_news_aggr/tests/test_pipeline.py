from datetime import datetime, timezone
from unittest.mock import Mock, patch, MagicMock
import pytest

from app.scrapers.youtube import ChannelVideo
from app.scrapers.openai import OpenAIArticle
from app.scrapers.anthropic import AnthropicArticle
from app.agents.digest_agent import DigestOutput


class TestScraperPipeline:
    """Tests for the scraper pipeline with mocked data."""
    
    @patch('app.runner.YouTubeScraper')
    @patch('app.runner.OpenAIScraper')
    @patch('app.runner.AnthropicScraper')
    @patch('app.runner.Repository')
    def test_run_scrapers_with_mock_data(
        self, 
        mock_repo_class, 
        mock_anthropic_scraper, 
        mock_openai_scraper, 
        mock_youtube_scraper
    ):
        """Test that run_scrapers handles fake data correctly."""
        from app.runner import run_scrapers
        
        # Create mock scraper instances
        youtube_instance = Mock()
        openai_instance = Mock()
        anthropic_instance = Mock()
        repo_instance = Mock()
        
        # Set up mock returns
        mock_youtube_scraper.return_value = youtube_instance
        mock_openai_scraper.return_value = openai_instance
        mock_anthropic_scraper.return_value = anthropic_instance
        mock_repo_class.return_value = repo_instance
        
        # Mock scraped data
        fake_youtube_videos = [
            ChannelVideo(
                video_id="test_123",
                title="Mocked YouTube Video",
                url="https://youtube.com/watch?v=test_123",
                channel_id="test_channel",
                published_at=datetime.now(timezone.utc),
                description="Mocked description",
                transcript=None
            )
        ]
        
        fake_openai_articles = [
            OpenAIArticle(
                guid="openai_test_123",
                title="Mocked OpenAI Article",
                url="https://openai.com/blog/test",
                description="Mocked description",
                published_at=datetime.now(timezone.utc),
                category="Research"
            )
        ]
        
        fake_anthropic_articles = [
            AnthropicArticle(
                guid="anthropic_test_123",
                title="Mocked Anthropic Article",
                url="https://anthropic.com/blog/test",
                description="Mocked description",
                published_at=datetime.now(timezone.utc),
                category="News"
            )
        ]
        
        # Configure mock scrapers to return fake data
        youtube_instance.get_latest_videos.return_value = fake_youtube_videos
        openai_instance.get_articles.return_value = fake_openai_articles
        anthropic_instance.get_articles.return_value = fake_anthropic_articles
        
        # Configure mock repository to simulate saves
        repo_instance.bulk_create_youtube_videos.return_value = len(fake_youtube_videos)
        repo_instance.bulk_create_openai_articles.return_value = len(fake_openai_articles)
        repo_instance.bulk_create_anthropic_articles.return_value = len(fake_anthropic_articles)
        
        # Run the scrapers
        results = run_scrapers(hours=24)
        
        # Verify the results contain the mocked data
        assert len(results['youtube']) == 1
        assert len(results['openai']) == 1
        assert len(results['anthropic']) == 1
        
        # Verify scrapers were called
        youtube_instance.get_latest_videos.assert_called()
        openai_instance.get_articles.assert_called_once_with(hours=24)
        anthropic_instance.get_articles.assert_called_once_with(hours=24)
        
        # Verify repository save methods were called
        repo_instance.bulk_create_youtube_videos.assert_called_once()
        repo_instance.bulk_create_openai_articles.assert_called_once()
        repo_instance.bulk_create_anthropic_articles.assert_called_once()


class TestDigestAgent:
    """Tests for the DigestAgent with mocked LLM calls."""
    
    @patch('app.agents.digest_agent.OpenAI')
    def test_digest_agent_with_mocked_llm(self, mock_openai_class):
        """Test DigestAgent returns static summary instead of calling OpenAI."""
        from app.agents.digest_agent import DigestAgent
        
        # Create mock OpenAI client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Mock the response structure
        mock_response = Mock()
        mock_response.output_parsed = DigestOutput(
            title="This is a mocked title",
            summary="This is a test summary"
        )
        
        # Configure mock to return our static response
        mock_client.responses.parse.return_value = mock_response
        
        # Create agent and generate digest
        agent = DigestAgent()
        result = agent.generate_digest(
            title="Original Title",
            content="This is some test content that would normally be sent to OpenAI.",
            article_type="youtube"
        )
        
        # Verify we got the mocked response
        assert result is not None
        assert result.title == "This is a mocked title"
        assert result.summary == "This is a test summary"
        
        # Verify OpenAI was called (but with mocked implementation)
        mock_client.responses.parse.assert_called_once()
        
        # Verify the call included our content (truncated to 8000 chars)
        call_kwargs = mock_client.responses.parse.call_args[1]
        assert "youtube" in call_kwargs['input']
        assert "Original Title" in call_kwargs['input']


class TestDailyPipeline:
    """Tests for the complete daily pipeline with mocked components."""
    
    @patch('app.daily_runner.run_scrapers')
    @patch('app.daily_runner.process_anthropic_markdown')
    @patch('app.daily_runner.process_youtube_transcripts')
    @patch('app.daily_runner.process_digests')
    @patch('app.daily_runner.send_digest_email')
    def test_daily_pipeline_with_mocks(
        self,
        mock_send_email,
        mock_process_digests,
        mock_process_youtube,
        mock_process_anthropic,
        mock_run_scrapers
    ):
        """Test that the daily pipeline orchestrates all steps correctly."""
        from app.daily_runner import run_daily_pipeline
        
        # Mock return values for each step
        mock_run_scrapers.return_value = {
            "youtube": [Mock()],  # 1 video
            "openai": [Mock()],   # 1 article
            "anthropic": [Mock()] # 1 article
        }
        
        mock_process_anthropic.return_value = {
            "total": 1,
            "processed": 1,
            "failed": 0
        }
        
        mock_process_youtube.return_value = {
            "total": 1,
            "processed": 1,
            "unavailable": 0,
            "failed": 0
        }
        
        mock_process_digests.return_value = {
            "total": 3,
            "processed": 3,
            "failed": 0
        }
        
        mock_send_email.return_value = {
            "success": True,
            "subject": "Daily AI News Digest - Test",
            "articles_sent": 10
        }
        
        # Run the pipeline
        result = run_daily_pipeline(hours=24, top_n=10)
        
        # Verify all steps were called
        mock_run_scrapers.assert_called_once_with(hours=24)
        mock_process_anthropic.assert_called_once()
        mock_process_youtube.assert_called_once()
        mock_process_digests.assert_called_once()
        mock_send_email.assert_called_once_with(hours=24, top_n=10)
        
        # Verify pipeline succeeded
        assert result["success"] is True
        
        # Verify results structure
        assert "scraping" in result
        assert "processing" in result
        assert "digests" in result
        assert "email" in result
        
        # Verify scraping counts
        assert result["scraping"]["youtube"] == 1
        assert result["scraping"]["openai"] == 1
        assert result["scraping"]["anthropic"] == 1
    
    @patch('app.daily_runner.run_scrapers')
    def test_daily_pipeline_handles_errors(self, mock_run_scrapers):
        """Test that the pipeline handles errors gracefully."""
        from app.daily_runner import run_daily_pipeline
        
        # Make scraper raise an exception
        mock_run_scrapers.side_effect = Exception("Mocked scraper error")
        
        # Run the pipeline (should not crash)
        result = run_daily_pipeline(hours=24, top_n=10)
        
        # Verify pipeline failed gracefully
        assert result["success"] is False
        assert "error" in result
        assert "Mocked scraper error" in result["error"]


class TestCuratorAgent:
    """Tests for the CuratorAgent with mocked LLM calls."""
    
    @patch('app.agents.curator_agent.OpenAI')
    def test_curator_agent_with_mocked_ranking(self, mock_openai_class):
        """Test that CuratorAgent can rank digests without calling real API."""
        from app.agents.curator_agent import CuratorAgent, RankedArticle
        from app.profiles.user_profile import USER_PROFILE
        
        # Create mock OpenAI client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Mock the response with ranked articles
        mock_response = Mock()
        mock_response.output_parsed.articles = [
            RankedArticle(
                digest_id="test:123",
                relevance_score=9.5,
                rank=1,
                reasoning="Highly relevant to user's interests"
            ),
            RankedArticle(
                digest_id="test:456",
                relevance_score=7.2,
                rank=2,
                reasoning="Moderately relevant"
            )
        ]
        
        mock_client.responses.parse.return_value = mock_response
        
        # Create curator and rank digests
        curator = CuratorAgent(USER_PROFILE)
        
        test_digests = [
            {
                "id": "test:123",
                "title": "Test Article 1",
                "summary": "Test summary 1",
                "type": "youtube"
            },
            {
                "id": "test:456",
                "title": "Test Article 2",
                "summary": "Test summary 2",
                "type": "openai"
            }
        ]
        
        ranked = curator.rank_digests(test_digests)
        
        # Verify rankings
        assert len(ranked) == 2
        assert ranked[0].rank == 1
        assert ranked[0].relevance_score == 9.5
        assert ranked[1].rank == 2
        assert ranked[1].relevance_score == 7.2


class TestEmailAgent:
    """Tests for the EmailAgent with mocked LLM calls."""
    
    @patch('app.agents.email_agent.OpenAI')
    def test_email_agent_with_mocked_introduction(self, mock_openai_class):
        """Test EmailAgent generates introduction without calling real API."""
        from app.agents.email_agent import EmailAgent, EmailIntroduction
        from app.profiles.user_profile import USER_PROFILE
        
        # Create mock OpenAI client
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        # Mock the response
        mock_response = Mock()
        mock_response.output_parsed = EmailIntroduction(
            greeting="Hey Test User!",
            introduction="Here's your personalized AI news digest with 5 top articles."
        )
        
        mock_client.responses.parse.return_value = mock_response
        
        # Create email agent
        agent = EmailAgent(USER_PROFILE)
        
        # Generate introduction with mock articles
        mock_articles = [
            {"title": f"Article {i}", "relevance_score": 9.0 - i} 
            for i in range(5)
        ]
        
        intro = agent.generate_introduction(mock_articles)
        
        # Verify we got the mocked introduction
        assert intro.greeting == "Hey Test User!"
        assert "5 top articles" in intro.introduction
