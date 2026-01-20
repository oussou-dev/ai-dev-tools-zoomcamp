import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.scrapers.youtube import YouTubeScraper
from app.database.repository import Repository

TRANSCRIPT_UNAVAILABLE_MARKER = "__UNAVAILABLE__"


def process_youtube_transcripts(limit: Optional[int] = None) -> dict:
    """Process YouTube videos and fetch their transcripts.

    Args:
        limit: Maximum number of videos to process

    Returns:
        Dictionary with stats: total, processed, unavailable, failed
    """
    scraper = YouTubeScraper()
    repo = Repository()

    # Fetch videos without transcripts
    videos = repo.get_youtube_videos_without_transcript(limit)

    processed = 0
    unavailable = 0
    failed = 0

    for video in videos:
        try:
            transcript = scraper.get_transcript(video.video_id)

            if transcript:
                # Success: update with transcript text
                repo.update_youtube_video_transcript(video.video_id, transcript.text)
                processed += 1
            else:
                # No transcript available
                repo.update_youtube_video_transcript(video.video_id, TRANSCRIPT_UNAVAILABLE_MARKER)
                unavailable += 1
        except Exception as e:
            print(f"Error processing video {video.video_id}: {e}")
            repo.update_youtube_video_transcript(video.video_id, TRANSCRIPT_UNAVAILABLE_MARKER)
            unavailable += 1

    return {
        "total": len(videos),
        "processed": processed,
        "unavailable": unavailable,
        "failed": failed,
    }


if __name__ == "__main__":
    stats = process_youtube_transcripts()
    print(f"YouTube Transcript Processing Stats:")
    print(f"  Total: {stats['total']}")
    print(f"  Processed: {stats['processed']}")
    print(f"  Unavailable: {stats['unavailable']}")
    print(f"  Failed: {stats['failed']}")
