from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any

from sqlalchemy.orm import Session

from .models import YouTubeVideo, OpenAIArticle, AnthropicArticle, Digest
from .connection import get_session


class Repository:
    def __init__(self, session: Optional[Session] = None):
        self.session = session if session is not None else get_session()

    # YouTube Methods
    def create_youtube_video(
        self,
        video_id: str,
        title: str,
        url: str,
        channel_id: str,
        published_at: datetime,
        description: Optional[str] = None,
        transcript: Optional[str] = None,
    ) -> YouTubeVideo:
        """Create a YouTube video record if it doesn't exist."""
        existing = self.session.query(YouTubeVideo).filter_by(video_id=video_id).first()
        if existing:
            return existing

        video = YouTubeVideo(
            video_id=video_id,
            title=title,
            url=url,
            channel_id=channel_id,
            published_at=published_at,
            description=description,
            transcript=transcript,
        )
        self.session.add(video)
        self.session.commit()
        return video

    def bulk_create_youtube_videos(self, videos: List[dict]) -> int:
        """Bulk create YouTube videos, checking existence for each."""
        added_count = 0
        for video_data in videos:
            video_id = video_data.get("video_id")
            existing = self.session.query(YouTubeVideo).filter_by(video_id=video_id).first()
            if not existing:
                video = YouTubeVideo(**video_data)
                self.session.add(video)
                added_count += 1

        self.session.commit()
        return added_count

    def get_youtube_videos_without_transcript(self, limit: Optional[int] = None) -> List[YouTubeVideo]:
        """Fetch YouTube videos that don't have a transcript."""
        query = self.session.query(YouTubeVideo).filter(YouTubeVideo.transcript.is_(None))
        if limit:
            query = query.limit(limit)
        return query.all()

    def update_youtube_video_transcript(self, video_id: str, transcript: str) -> None:
        """Update the transcript for a YouTube video."""
        video = self.session.query(YouTubeVideo).filter_by(video_id=video_id).first()
        if video:
            video.transcript = transcript
            self.session.commit()

    # OpenAI Methods
    def create_openai_article(
        self,
        guid: str,
        title: str,
        url: str,
        published_at: datetime,
        description: Optional[str] = None,
        category: Optional[str] = None,
    ) -> OpenAIArticle:
        """Create an OpenAI article record if it doesn't exist."""
        existing = self.session.query(OpenAIArticle).filter_by(guid=guid).first()
        if existing:
            return existing

        article = OpenAIArticle(
            guid=guid,
            title=title,
            url=url,
            published_at=published_at,
            description=description,
            category=category,
        )
        self.session.add(article)
        self.session.commit()
        return article

    def bulk_create_openai_articles(self, articles: List[dict]) -> int:
        """Bulk create OpenAI articles, checking existence for each."""
        added_count = 0
        for article_data in articles:
            guid = article_data.get("guid")
            existing = self.session.query(OpenAIArticle).filter_by(guid=guid).first()
            if not existing:
                article = OpenAIArticle(**article_data)
                self.session.add(article)
                added_count += 1

        self.session.commit()
        return added_count

    # Anthropic Methods
    def create_anthropic_article(
        self,
        guid: str,
        title: str,
        url: str,
        published_at: datetime,
        description: Optional[str] = None,
        category: Optional[str] = None,
        markdown: Optional[str] = None,
    ) -> AnthropicArticle:
        """Create an Anthropic article record if it doesn't exist."""
        existing = self.session.query(AnthropicArticle).filter_by(guid=guid).first()
        if existing:
            return existing

        article = AnthropicArticle(
            guid=guid,
            title=title,
            url=url,
            published_at=published_at,
            description=description,
            category=category,
            markdown=markdown,
        )
        self.session.add(article)
        self.session.commit()
        return article

    def bulk_create_anthropic_articles(self, articles: List[dict]) -> int:
        """Bulk create Anthropic articles, checking existence for each."""
        added_count = 0
        for article_data in articles:
            guid = article_data.get("guid")
            existing = self.session.query(AnthropicArticle).filter_by(guid=guid).first()
            if not existing:
                article = AnthropicArticle(**article_data)
                self.session.add(article)
                added_count += 1

        self.session.commit()
        return added_count

    def get_anthropic_articles_without_markdown(self, limit: Optional[int] = None) -> List[AnthropicArticle]:
        """Fetch Anthropic articles that don't have markdown."""
        query = self.session.query(AnthropicArticle).filter(AnthropicArticle.markdown.is_(None))
        if limit:
            query = query.limit(limit)
        return query.all()

    def update_anthropic_article_markdown(self, guid: str, markdown: str) -> None:
        """Update the markdown for an Anthropic article."""
        article = self.session.query(AnthropicArticle).filter_by(guid=guid).first()
        if article:
            article.markdown = markdown
            self.session.commit()

    # Digest Methods
    def create_digest(
        self,
        article_type: str,
        article_id: str,
        url: str,
        title: str,
        summary: str,
        published_at: datetime,
    ) -> Digest:
        """Create a digest record."""
        digest_id = f"{article_type}:{article_id}"

        # Ensure published_at is timezone-aware (UTC)
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)

        existing = self.session.query(Digest).filter_by(id=digest_id).first()
        if existing:
            return existing

        digest = Digest(
            id=digest_id,
            article_type=article_type,
            article_id=article_id,
            url=url,
            title=title,
            summary=summary,
        )
        self.session.add(digest)
        self.session.commit()
        return digest

    def get_articles_without_digest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Return unified list of content (Videos + Articles) that haven't been summarized yet."""
        # Fetch all existing Digest entries and build a set of seen IDs
        existing_digests = self.session.query(Digest).all()
        seen_ids = {digest.id for digest in existing_digests}

        # Fetch valid YouTube videos (has transcript AND transcript != "__UNAVAILABLE__")
        youtube_videos = self.session.query(YouTubeVideo).filter(
            YouTubeVideo.transcript.isnot(None),
            YouTubeVideo.transcript != "__UNAVAILABLE__",
        ).all()

        # Fetch OpenAI articles
        openai_articles = self.session.query(OpenAIArticle).all()

        # Fetch Anthropic articles (must have markdown)
        anthropic_articles = self.session.query(AnthropicArticle).filter(
            AnthropicArticle.markdown.isnot(None)
        ).all()

        # Normalize output into dictionaries
        results = []

        for video in youtube_videos:
            video_id = f"youtube:{video.video_id}"
            if video_id not in seen_ids:
                results.append(
                    {
                        "type": "youtube",
                        "id": video.video_id,
                        "title": video.title,
                        "url": video.url,
                        "content": video.transcript,
                        "published_at": video.published_at,
                    }
                )

        for article in openai_articles:
            article_id = f"openai:{article.guid}"
            if article_id not in seen_ids:
                results.append(
                    {
                        "type": "openai",
                        "id": article.guid,
                        "title": article.title,
                        "url": article.url,
                        "content": article.description,
                        "published_at": article.published_at,
                    }
                )

        for article in anthropic_articles:
            article_id = f"anthropic:{article.guid}"
            if article_id not in seen_ids:
                results.append(
                    {
                        "type": "anthropic",
                        "id": article.guid,
                        "title": article.title,
                        "url": article.url,
                        "content": article.markdown,
                        "published_at": article.published_at,
                    }
                )

        # Apply limit if provided
        if limit:
            results = results[:limit]

        return results

    def get_recent_digests(self, hours: int = 24) -> List[Digest]:
        """Return digests created in the last X hours, ordered by newest first."""
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        return (
            self.session.query(Digest)
            .filter(Digest.created_at >= cutoff_time)
            .order_by(Digest.created_at.desc())
            .all()
        )
