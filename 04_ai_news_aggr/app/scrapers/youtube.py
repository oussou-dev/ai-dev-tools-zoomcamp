import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from pydantic import BaseModel
import feedparser
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.proxies import WebshareProxyConfig


class Transcript(BaseModel):
    """Model for a video transcript."""
    text: str


class ChannelVideo(BaseModel):
    """Model for a YouTube video with metadata."""
    title: str
    url: str
    video_id: str
    published_at: datetime
    description: str
    transcript: Optional[str] = None


class YouTubeScraper:
    """Scraper for fetching YouTube video metadata and transcripts."""
    
    def __init__(self):
        """Initialize the YouTube scraper with optional proxy configuration."""
        # Check for proxy credentials in environment
        proxy_username = os.getenv("PROXY_USERNAME")
        proxy_password = os.getenv("PROXY_PASSWORD")
        
        if proxy_username and proxy_password:
            # Configure WebshareProxyConfig
            proxy_config = WebshareProxyConfig(
                username=proxy_username,
                password=proxy_password
            )
            self.api = YouTubeTranscriptApi(proxies={"http": proxy_config, "https": proxy_config})
        else:
            # Initialize without proxies
            self.api = YouTubeTranscriptApi()
    
    def _extract_video_id(self, video_url: str) -> str:
        """
        Extract video ID from various YouTube URL formats.
        
        Args:
            video_url: YouTube video URL
            
        Returns:
            Video ID string
        """
        # Handle three URL formats:
        # 1. Standard: youtube.com/watch?v=VIDEO_ID
        # 2. Shorts: youtube.com/shorts/VIDEO_ID
        # 3. Shortened: youtu.be/VIDEO_ID
        
        if "youtube.com/watch?v=" in video_url:
            return video_url.split("v=")[1].split("&")[0]
        elif "youtube.com/shorts/" in video_url:
            return video_url.split("shorts/")[1].split("?")[0]
        elif "youtu.be/" in video_url:
            return video_url.split("youtu.be/")[1].split("?")[0]
        else:
            # Assume the URL is already a video ID
            return video_url
    
    def get_transcript(self, video_id: str) -> Optional[Transcript]:
        """
        Fetch the transcript for a YouTube video.
        
        Args:
            video_id: YouTube video identifier
            
        Returns:
            Transcript object if available, None otherwise
        """
        try:
            # Fetch transcript
            transcript_list = self.api.get_transcript(video_id)
            
            # Join all text snippets into a single string
            full_text = " ".join([entry["text"] for entry in transcript_list])
            
            return Transcript(text=full_text)
            
        except TranscriptsDisabled:
            # Transcripts are disabled for this video
            return None
        except NoTranscriptFound:
            # No transcript found for this video
            return None
        except Exception as e:
            # Handle any other exceptions
            print(f"Error fetching transcript for {video_id}: {e}")
            return None
    
    def get_latest_videos(self, channel_id: str, hours: int = 24) -> list[ChannelVideo]:
        """
        Fetch the latest videos from a YouTube channel via RSS feed.
        
        Args:
            channel_id: YouTube channel identifier
            hours: Number of hours to look back (default: 24)
            
        Returns:
            List of ChannelVideo objects (without transcripts)
        """
        # Parse RSS feed
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        feed = feedparser.parse(rss_url)
        
        # Calculate cutoff time in UTC
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        videos = []
        
        for entry in feed.entries:
            # Filter out shorts
            video_url = entry.link
            if "/shorts/" in video_url:
                continue
            
            # Parse published time
            published_time = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            
            # Filter by time - only keep videos within the specified hours
            if published_time >= cutoff_time:
                video_id = self._extract_video_id(video_url)
                
                video = ChannelVideo(
                    title=entry.title,
                    url=video_url,
                    video_id=video_id,
                    published_at=published_time,
                    description=entry.get("summary", ""),
                    transcript=None
                )
                videos.append(video)
        
        return videos
    
    def scrape_channel(self, channel_id: str, hours: int = 150) -> list[ChannelVideo]:
        """
        Scrape a YouTube channel for videos and their transcripts.
        
        This is an orchestrator method that fetches videos and their transcripts.
        
        Args:
            channel_id: YouTube channel identifier
            hours: Number of hours to look back (default: 150)
            
        Returns:
            List of ChannelVideo objects with transcripts
        """
        # First get the latest videos
        videos = self.get_latest_videos(channel_id, hours)
        
        # Then fetch transcripts for each video
        videos_with_transcripts = []
        for video in videos:
            transcript = self.get_transcript(video.video_id)
            
            # Update the video with the transcript
            if transcript:
                updated_video = video.model_copy(update={"transcript": transcript.text})
            else:
                # Mark as unavailable if no transcript found
                updated_video = video.model_copy(update={"transcript": "__UNAVAILABLE__"})
            
            videos_with_transcripts.append(updated_video)
        
        return videos_with_transcripts


if __name__ == "__main__":
    # Test the scraper
    scraper = YouTubeScraper()
    
    # Test fetching a transcript for a known video ID
    print("Testing transcript fetch...")
    test_video_id = "dQw4w9WgXcQ"  # Example video ID
    transcript = scraper.get_transcript(test_video_id)
    if transcript:
        print(f"Transcript length: {len(transcript.text)} characters")
        print(f"First 200 characters: {transcript.text[:200]}")
    else:
        print("No transcript available for test video")
    
    print("\n" + "="*50 + "\n")
    
    # Test scraping a channel
    print("Testing channel scrape...")
    test_channel_id = "UCawZsQWqfGSbCI5yjkdVkTA"  # Matthew Berman
    videos = scraper.scrape_channel(test_channel_id, hours=168)  # Last week
    
    print(f"Found {len(videos)} videos")
    for i, video in enumerate(videos[:3], 1):  # Show first 3
        print(f"\n{i}. {video.title}")
        print(f"   URL: {video.url}")
        print(f"   Published: {video.published_at}")
        transcript_status = "Available" if video.transcript and video.transcript != "__UNAVAILABLE__" else "Unavailable"
        print(f"   Transcript: {transcript_status}")
