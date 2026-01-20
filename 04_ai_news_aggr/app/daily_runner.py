import logging
from datetime import datetime

from dotenv import load_dotenv

from app.runner import run_scrapers
from app.services.process_anthropic import process_anthropic_markdown
from app.services.process_youtube import process_youtube_transcripts
from app.services.process_digest import process_digests
from app.services.process_email import send_digest_email

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def run_daily_pipeline(hours: int = 24, top_n: int = 10) -> dict:
    """Run the complete daily AI news aggregator pipeline.

    Args:
        hours: Number of hours to look back for content
        top_n: Number of top articles to include in email

    Returns:
        Dictionary with results and success status
    """
    start_time = datetime.now()

    results = {
        "scraping": {},
        "processing": {},
        "digests": {},
        "email": {},
        "success": False,
    }

    try:
        logger.info("=" * 60)
        logger.info("Starting Daily AI News Aggregator Pipeline")
        logger.info("=" * 60)

        # Step 1: Scraping
        logger.info("[1/5] Running scrapers...")
        scraped = run_scrapers(hours=hours)
        results["scraping"] = {
            "youtube": len(scraped["youtube"]),
            "openai": len(scraped["openai"]),
            "anthropic": len(scraped["anthropic"]),
        }
        logger.info(
            f"✓ Scraped: YouTube {results['scraping']['youtube']}, "
            f"OpenAI {results['scraping']['openai']}, "
            f"Anthropic {results['scraping']['anthropic']}"
        )

        # Step 2: Process Anthropic Markdown
        logger.info("[2/5] Processing Anthropic markdown...")
        anthropic_stats = process_anthropic_markdown()
        results["processing"]["anthropic"] = anthropic_stats
        logger.info(
            f"✓ Processed: {anthropic_stats['processed']} articles, "
            f"Failed: {anthropic_stats['failed']}"
        )

        # Step 3: Process YouTube Transcripts
        logger.info("[3/5] Processing YouTube transcripts...")
        youtube_stats = process_youtube_transcripts()
        results["processing"]["youtube"] = youtube_stats
        logger.info(
            f"✓ Processed: {youtube_stats['processed']} transcripts, "
            f"Unavailable: {youtube_stats['unavailable']}"
        )

        # Step 4: Generate Digests
        logger.info("[4/5] Generating digests...")
        digest_stats = process_digests()
        results["digests"] = digest_stats
        logger.info(
            f"✓ Generated: {digest_stats['processed']} digests, "
            f"Failed: {digest_stats['failed']}/{digest_stats['total']}"
        )

        # Step 5: Send Email
        logger.info("[5/5] Sending digest email...")
        email_result = send_digest_email(hours=hours, top_n=top_n)
        results["email"] = email_result

        if email_result.get("success"):
            results["success"] = True
            logger.info(f"✓ Email sent: {email_result.get('subject')}")
        else:
            logger.error(f"✗ Email failed: {email_result.get('error')}")

    except Exception as e:
        logger.error(f"Pipeline error: {e}", exc_info=True)
        results["error"] = str(e)

    # Summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    logger.info("=" * 60)
    logger.info("Pipeline Summary")
    logger.info("=" * 60)
    logger.info(f"Duration: {duration:.2f} seconds")
    logger.info(f"Success: {results['success']}")
    logger.info(f"Scraped: {results['scraping']}")
    logger.info(f"Processing: {results['processing']}")
    logger.info(f"Digests: {results['digests']}")
    logger.info(f"Email: {results['email']}")
    logger.info("=" * 60)

    return results


if __name__ == "__main__":
    result = run_daily_pipeline()
    exit(0 if result["success"] else 1)
