import sys
from pathlib import Path
from typing import Optional

# Add project root to Python path for proper imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.scrapers.youtube import YouTubeScraper
from app.database.repository import Repository

# Constant to mark videos where transcripts are unavailable
TRANSCRIPT_UNAVAILABLE_MARKER = "__UNAVAILABLE__"


def process_youtube_transcripts(limit: Optional[int] = None) -> dict:
    """
    Process YouTube videos that lack transcripts by fetching and storing them.
    
    This function fetches transcripts for videos already in the database that
    don't have transcript content. It marks videos without available transcripts
    to prevent infinite retry loops.
    
    Args:
        limit: Maximum number of videos to process (None for all)
        
    Returns:
        Dictionary with processing statistics:
        - total: Total videos processed
        - processed: Videos with successfully fetched transcripts
        - unavailable: Videos where transcripts weren't available
        - failed: Videos that encountered errors
    """
    # Initialize scraper and repository
    scraper = YouTubeScraper()
    repo = Repository()
    
    # Fetch videos without transcripts
    videos = repo.get_youtube_videos_without_transcript(limit=limit)
    
    # Initialize counters
    total = len(videos)
    processed = 0
    unavailable = 0
    failed = 0
    
    print(f"Processing {total} videos without transcripts...")
    
    # Loop through videos and fetch transcripts
    for i, video in enumerate(videos, 1):
        print(f"[{i}/{total}] Processing: {video.title[:60]}...")
        
        try:
            # Try to fetch transcript
            transcript = scraper.get_transcript(video.video_id)
            
            if transcript:
                # Success: Update database with transcript text
                repo.update_youtube_video_transcript(video.video_id, transcript.text)
                processed += 1
                print(f"  ✓ Transcript fetched ({len(transcript.text)} characters)")
            else:
                # No transcript available: Mark as unavailable to skip in future
                repo.update_youtube_video_transcript(video.video_id, TRANSCRIPT_UNAVAILABLE_MARKER)
                unavailable += 1
                print(f"  ⚠ Transcript not available")
                
        except Exception as e:
            # Error occurred: Mark as unavailable and skip
            print(f"  ✗ Error: {e}")
            try:
                repo.update_youtube_video_transcript(video.video_id, TRANSCRIPT_UNAVAILABLE_MARKER)
            except Exception as update_error:
                print(f"  ✗ Failed to update database: {update_error}")
            unavailable += 1
    
    # Return statistics
    return {
        "total": total,
        "processed": processed,
        "unavailable": unavailable,
        "failed": failed
    }


if __name__ == "__main__":
    # Run transcript processing
    print("Starting YouTube transcript processing...")
    print("=" * 60)
    
    stats = process_youtube_transcripts()
    
    print("=" * 60)
    print("\nProcessing Complete!")
    print(f"Total videos: {stats['total']}")
    print(f"✓ Processed: {stats['processed']}")
    print(f"⚠ Unavailable: {stats['unavailable']}")
    print(f"✗ Failed: {stats['failed']}")
