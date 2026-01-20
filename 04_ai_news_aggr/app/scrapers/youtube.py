import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from urllib.parse import urlparse, parse_qs

import feedparser
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from youtube_transcript_api.proxies import WebshareProxyConfig


class Transcript(BaseModel):
    text: str


class ChannelVideo(BaseModel):
    title: str
    url: str
    video_id: str
    published_at: datetime
    description: str
    transcript: Optional[str] = None


class YouTubeScraper:
    def __init__(self):
        """Initialize YouTubeScraper with optional proxy configuration."""
        proxy_username = os.getenv("PROXY_USERNAME")
        proxy_password = os.getenv("PROXY_PASSWORD")

        if proxy_username and proxy_password:
            self.proxy_config = WebshareProxyConfig(
                http=f"http://{proxy_username}:{proxy_password}@proxy.webshare.io:80",
                https=f"http://{proxy_username}:{proxy_password}@proxy.webshare.io:80",
            )
            self.api = YouTubeTranscriptApi(proxies=self.proxy_config)
        else:
            self.api = YouTubeTranscriptApi

    def _extract_video_id(self, video_url: str) -> str:
        """Extract video_id from various YouTube URL formats."""
        # Handle youtube.com/watch?v=
        if "youtube.com/watch" in video_url:
            parsed = urlparse(video_url)
            return parse_qs(parsed.query).get("v", [None])[0]

        # Handle youtube.com/shorts/
        if "youtube.com/shorts/" in video_url:
            return video_url.split("youtube.com/shorts/")[1].split("?")[0]

        # Handle youtu.be/
        if "youtu.be/" in video_url:
            return video_url.split("youtu.be/")[1].split("?")[0]

        return ""

    def get_transcript(self, video_id: str) -> Optional[Transcript]:
        """Fetch transcript for a given video_id."""
        try:
            transcript_list = self.api.get_transcript(video_id)
            text = " ".join([item["text"] for item in transcript_list])
            return Transcript(text=text)
        except (TranscriptsDisabled, NoTranscriptFound):
            return None
        except Exception:
            return None

    def get_latest_videos(self, channel_id: str, hours: int = 24) -> list[ChannelVideo]:
        """Fetch latest videos from a channel's RSS feed."""
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        feed = feedparser.parse(rss_url)

        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        videos = []

        for entry in feed.entries:
            # Ignore shorts
            if "/shorts/" in entry.link:
                continue

            # Parse published time
            published_dt = datetime(*entry.published_parsed[:6]).replace(tzinfo=timezone.utc)

            # Filter by time
            if published_dt < cutoff_time:
                continue

            video_id = entry.yt_videoid
            video = ChannelVideo(
                title=entry.title,
                url=entry.link,
                video_id=video_id,
                published_at=published_dt,
                description=entry.summary or "",
            )
            videos.append(video)

        return videos

    def scrape_channel(self, channel_id: str, hours: int = 150) -> list[ChannelVideo]:
        """Orchestrator method to scrape a channel with transcripts."""
        videos = self.get_latest_videos(channel_id, hours=hours)

        result = []
        for video in videos:
            transcript_obj = self.get_transcript(video.video_id)
            transcript_text = transcript_obj.text if transcript_obj else None
            updated_video = video.model_copy(update={"transcript": transcript_text})
            result.append(updated_video)

        return result


if __name__ == "__main__":
    scraper = YouTubeScraper()

    # Test fetching a transcript for a known ID
    test_video_id = "dQw4w9WgXcQ"  # Example video ID
    transcript = scraper.get_transcript(test_video_id)
    if transcript:
        print(f"Transcript fetched: {transcript.text[:100]}...")
    else:
        print("No transcript available")

    # Test scrape_channel with a sample Channel ID
    from app.config import YOUTUBE_CHANNELS

    if YOUTUBE_CHANNELS:
        channel_id = YOUTUBE_CHANNELS[0]
        print(f"\nScraping channel: {channel_id}")
        videos = scraper.scrape_channel(channel_id)
        print(f"Found {len(videos)} videos")
        for video in videos[:3]:
            print(f"  - {video.title} (ID: {video.video_id})")
