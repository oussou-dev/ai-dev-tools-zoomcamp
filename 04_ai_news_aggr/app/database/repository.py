from datetime import datetime, timedelta, timezone
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from .models import YouTubeVideo, OpenAIArticle, AnthropicArticle, Digest
from .connection import get_session


class Repository:
    """Repository class implementing the Repository Pattern for database operations."""
    
    def __init__(self, session: Optional[Session] = None):
        """
        Initialize the repository with a database session.
        
        Args:
            session: Optional SQLAlchemy session. If None, creates a new session.
        """
        self.session = session if session is not None else get_session()
    
    # ==================== YouTube Methods ====================
    
    def create_youtube_video(
        self,
        video_id: str,
        title: str,
        url: str,
        channel_id: str,
        published_at: datetime,
        description: Optional[str] = None,
        transcript: Optional[str] = None
    ) -> Optional[YouTubeVideo]:
        """
        Create a new YouTube video entry if it doesn't exist.
        
        Args:
            video_id: Unique video identifier
            title: Video title
            url: Video URL
            channel_id: YouTube channel identifier
            published_at: Publication datetime
            description: Video description
            transcript: Video transcript (optional)
            
        Returns:
            YouTubeVideo object if created, None if already exists
        """
        existing = self.session.query(YouTubeVideo).filter_by(video_id=video_id).first()
        if existing:
            return None
        
        video = YouTubeVideo(
            video_id=video_id,
            title=title,
            url=url,
            channel_id=channel_id,
            published_at=published_at,
            description=description,
            transcript=transcript
        )
        self.session.add(video)
        self.session.commit()
        return video
    
    def bulk_create_youtube_videos(self, videos: List[dict]) -> int:
        """
        Bulk create YouTube videos, skipping those that already exist.
        
        Args:
            videos: List of video dictionaries with required fields
            
        Returns:
            Number of videos added
        """
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
        """
        Get YouTube videos that don't have transcripts yet.
        
        Args:
            limit: Maximum number of videos to return
            
        Returns:
            List of YouTubeVideo objects without transcripts
        """
        query = self.session.query(YouTubeVideo).filter(YouTubeVideo.transcript.is_(None))
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def update_youtube_video_transcript(self, video_id: str, transcript: str) -> bool:
        """
        Update the transcript for a YouTube video.
        
        Args:
            video_id: Video identifier
            transcript: Transcript text
            
        Returns:
            True if updated, False if video not found
        """
        video = self.session.query(YouTubeVideo).filter_by(video_id=video_id).first()
        if not video:
            return False
        
        video.transcript = transcript
        self.session.commit()
        return True
    
    # ==================== OpenAI Methods ====================
    
    def create_openai_article(
        self,
        guid: str,
        title: str,
        url: str,
        published_at: datetime,
        description: Optional[str] = None,
        category: Optional[str] = None
    ) -> Optional[OpenAIArticle]:
        """
        Create a new OpenAI article entry if it doesn't exist.
        
        Args:
            guid: Unique article identifier
            title: Article title
            url: Article URL
            published_at: Publication datetime
            description: Article description
            category: Article category
            
        Returns:
            OpenAIArticle object if created, None if already exists
        """
        existing = self.session.query(OpenAIArticle).filter_by(guid=guid).first()
        if existing:
            return None
        
        article = OpenAIArticle(
            guid=guid,
            title=title,
            url=url,
            published_at=published_at,
            description=description,
            category=category
        )
        self.session.add(article)
        self.session.commit()
        return article
    
    def bulk_create_openai_articles(self, articles: List[dict]) -> int:
        """
        Bulk create OpenAI articles, skipping those that already exist.
        
        Args:
            articles: List of article dictionaries with required fields
            
        Returns:
            Number of articles added
        """
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
    
    # ==================== Anthropic Methods ====================
    
    def create_anthropic_article(
        self,
        guid: str,
        title: str,
        url: str,
        published_at: datetime,
        description: Optional[str] = None,
        category: Optional[str] = None,
        markdown: Optional[str] = None
    ) -> Optional[AnthropicArticle]:
        """
        Create a new Anthropic article entry if it doesn't exist.
        
        Args:
            guid: Unique article identifier
            title: Article title
            url: Article URL
            published_at: Publication datetime
            description: Article description
            category: Article category
            markdown: Converted markdown content
            
        Returns:
            AnthropicArticle object if created, None if already exists
        """
        existing = self.session.query(AnthropicArticle).filter_by(guid=guid).first()
        if existing:
            return None
        
        article = AnthropicArticle(
            guid=guid,
            title=title,
            url=url,
            published_at=published_at,
            description=description,
            category=category,
            markdown=markdown
        )
        self.session.add(article)
        self.session.commit()
        return article
    
    def bulk_create_anthropic_articles(self, articles: List[dict]) -> int:
        """
        Bulk create Anthropic articles, skipping those that already exist.
        
        Args:
            articles: List of article dictionaries with required fields
            
        Returns:
            Number of articles added
        """
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
        """
        Get Anthropic articles that don't have markdown content yet.
        
        Args:
            limit: Maximum number of articles to return
            
        Returns:
            List of AnthropicArticle objects without markdown
        """
        query = self.session.query(AnthropicArticle).filter(AnthropicArticle.markdown.is_(None))
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    def update_anthropic_article_markdown(self, guid: str, markdown: str) -> bool:
        """
        Update the markdown content for an Anthropic article.
        
        Args:
            guid: Article identifier
            markdown: Markdown content
            
        Returns:
            True if updated, False if article not found
        """
        article = self.session.query(AnthropicArticle).filter_by(guid=guid).first()
        if not article:
            return False
        
        article.markdown = markdown
        self.session.commit()
        return True
    
    # ==================== Complex Aggregation ====================
    
    def get_articles_without_digest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get a unified list of articles and videos that haven't been summarized yet.
        
        This method:
        1. Fetches all existing digests to build a set of already-processed IDs
        2. Fetches valid YouTube videos (must have transcript and transcript != "__UNAVAILABLE__")
        3. Fetches all OpenAI articles
        4. Fetches Anthropic articles (must have markdown)
        5. Filters out items already in digests
        6. Normalizes output format
        
        Args:
            limit: Maximum number of items to return
            
        Returns:
            List of dictionaries with normalized article/video data
        """
        # Step 1: Build set of already-processed IDs
        digests = self.session.query(Digest).all()
        seen_ids = {f"{d.article_type}:{d.article_id}" for d in digests}
        
        results = []
        
        # Step 2: Fetch valid YouTube videos
        youtube_videos = self.session.query(YouTubeVideo).filter(
            YouTubeVideo.transcript.isnot(None),
            YouTubeVideo.transcript != "__UNAVAILABLE__"
        ).all()
        
        for video in youtube_videos:
            video_key = f"youtube:{video.video_id}"
            if video_key not in seen_ids:
                results.append({
                    "type": "youtube",
                    "id": video.video_id,
                    "title": video.title,
                    "url": video.url,
                    "content": video.transcript,
                    "published_at": video.published_at
                })
        
        # Step 3: Fetch OpenAI articles
        openai_articles = self.session.query(OpenAIArticle).all()
        
        for article in openai_articles:
            article_key = f"openai:{article.guid}"
            if article_key not in seen_ids:
                results.append({
                    "type": "openai",
                    "id": article.guid,
                    "title": article.title,
                    "url": article.url,
                    "content": article.description or "",
                    "published_at": article.published_at
                })
        
        # Step 4: Fetch Anthropic articles (must have markdown)
        anthropic_articles = self.session.query(AnthropicArticle).filter(
            AnthropicArticle.markdown.isnot(None)
        ).all()
        
        for article in anthropic_articles:
            article_key = f"anthropic:{article.guid}"
            if article_key not in seen_ids:
                results.append({
                    "type": "anthropic",
                    "id": article.guid,
                    "title": article.title,
                    "url": article.url,
                    "content": article.markdown,
                    "published_at": article.published_at
                })
        
        # Step 5: Apply limit if provided
        if limit:
            results = results[:limit]
        
        return results
    
    # ==================== Digest Methods ====================
    
    def create_digest(
        self,
        article_type: str,
        article_id: str,
        url: str,
        title: str,
        summary: str,
        published_at: datetime
    ) -> Optional[Digest]:
        """
        Create a digest entry for a summarized article/video.
        
        Args:
            article_type: Type of content ("youtube", "openai", "anthropic")
            article_id: ID of the original article/video
            url: URL of the content
            title: Title of the content
            summary: LLM-generated summary
            published_at: Publication datetime
            
        Returns:
            Digest object if created, None if already exists
        """
        # Generate compound ID
        digest_id = f"{article_type}:{article_id}"
        
        # Check if digest already exists
        existing = self.session.query(Digest).filter_by(id=digest_id).first()
        if existing:
            return None
        
        # Ensure datetime is timezone-aware (UTC)
        if published_at.tzinfo is None:
            published_at = published_at.replace(tzinfo=timezone.utc)
        
        digest = Digest(
            id=digest_id,
            article_type=article_type,
            article_id=article_id,
            url=url,
            title=title,
            summary=summary,
            created_at=datetime.now(timezone.utc)
        )
        self.session.add(digest)
        self.session.commit()
        return digest
    
    def get_recent_digests(self, hours: int = 24) -> List[Digest]:
        """
        Get digests created within the last N hours.
        
        Args:
            hours: Number of hours to look back (default: 24)
            
        Returns:
            List of Digest objects, ordered by newest first
        """
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        digests = self.session.query(Digest).filter(
            Digest.created_at >= cutoff_time
        ).order_by(Digest.created_at.desc()).all()
        
        return digests
