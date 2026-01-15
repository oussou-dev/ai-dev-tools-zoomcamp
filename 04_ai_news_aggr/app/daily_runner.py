import logging
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from app.runner import run_scrapers
from app.services.process_anthropic import process_anthropic_markdown
from app.services.process_youtube import process_youtube_transcripts
from app.services.process_digest import process_digests
from app.services.process_email import send_digest_email

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def run_daily_pipeline(hours: int = 24, top_n: int = 10) -> dict:
    """
    Execute the complete daily AI news aggregator pipeline.
    
    This function orchestrates all pipeline steps:
    1. Scraping - Fetch new content from all sources
    2. Processing - Convert content to usable formats
    3. Digests - Generate AI summaries
    4. Email - Rank, format, and send personalized digest
    
    Args:
        hours: Number of hours to look back for new content (default: 24)
        top_n: Number of top articles to include in email (default: 10)
        
    Returns:
        Dictionary with results from each pipeline step and overall success status
    """
    start_time = datetime.now()
    
    logger.info("=" * 80)
    logger.info("STARTING DAILY AI NEWS AGGREGATOR PIPELINE")
    logger.info("=" * 80)
    logger.info(f"Configuration: hours={hours}, top_n={top_n}")
    logger.info("")
    
    # Initialize results structure
    results = {
        "scraping": {},
        "processing": {
            "anthropic": {},
            "youtube": {}
        },
        "digests": {},
        "email": {},
        "success": False,
        "error": None
    }
    
    try:
        # ==================== STEP 1: SCRAPING ====================
        logger.info("[1/5] SCRAPING - Fetching content from all sources...")
        
        scraping_results = run_scrapers(hours=hours)
        results["scraping"] = {
            "youtube": len(scraping_results.get("youtube", [])),
            "openai": len(scraping_results.get("openai", [])),
            "anthropic": len(scraping_results.get("anthropic", []))
        }
        
        logger.info(f"✓ Scraping complete:")
        logger.info(f"  - YouTube: {results['scraping']['youtube']} videos")
        logger.info(f"  - OpenAI: {results['scraping']['openai']} articles")
        logger.info(f"  - Anthropic: {results['scraping']['anthropic']} articles")
        logger.info("")
        
        # ==================== STEP 2: PROCESS ANTHROPIC ====================
        logger.info("[2/5] PROCESSING - Converting Anthropic articles to markdown...")
        
        anthropic_stats = process_anthropic_markdown()
        results["processing"]["anthropic"] = anthropic_stats
        
        logger.info(f"✓ Anthropic processing complete:")
        logger.info(f"  - Processed: {anthropic_stats['processed']}")
        logger.info(f"  - Failed: {anthropic_stats['failed']}")
        logger.info("")
        
        # ==================== STEP 3: PROCESS YOUTUBE ====================
        logger.info("[3/5] PROCESSING - Fetching YouTube transcripts...")
        
        youtube_stats = process_youtube_transcripts()
        results["processing"]["youtube"] = youtube_stats
        
        logger.info(f"✓ YouTube processing complete:")
        logger.info(f"  - Processed: {youtube_stats['processed']}")
        logger.info(f"  - Unavailable: {youtube_stats['unavailable']}")
        logger.info("")
        
        # ==================== STEP 4: GENERATE DIGESTS ====================
        logger.info("[4/5] DIGESTS - Generating AI summaries...")
        
        digest_stats = process_digests()
        results["digests"] = digest_stats
        
        logger.info(f"✓ Digest generation complete:")
        logger.info(f"  - Total items: {digest_stats['total']}")
        logger.info(f"  - Processed: {digest_stats['processed']}")
        logger.info(f"  - Failed: {digest_stats['failed']}")
        logger.info("")
        
        # ==================== STEP 5: SEND EMAIL ====================
        logger.info("[5/5] EMAIL - Ranking, formatting, and sending digest...")
        
        email_result = send_digest_email(hours=hours, top_n=top_n)
        results["email"] = email_result
        
        if email_result.get("success"):
            results["success"] = True
            logger.info(f"✓ Email sent successfully!")
            logger.info(f"  - Subject: {email_result.get('subject')}")
            logger.info(f"  - Articles sent: {email_result.get('articles_sent')}")
            logger.info(f"  - Total ranked: {email_result.get('total_ranked')}")
        else:
            logger.error(f"✗ Email sending failed:")
            logger.error(f"  - Error: {email_result.get('error')}")
        
        logger.info("")
        
    except Exception as e:
        logger.error("=" * 80)
        logger.error("PIPELINE FAILED WITH ERROR")
        logger.error("=" * 80)
        logger.error(f"Error: {e}", exc_info=True)
        results["error"] = str(e)
        results["success"] = False
    
    # ==================== PIPELINE SUMMARY ====================
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    logger.info("=" * 80)
    logger.info("PIPELINE SUMMARY")
    logger.info("=" * 80)
    logger.info(f"Duration: {duration:.2f} seconds")
    logger.info(f"Status: {'✓ SUCCESS' if results['success'] else '✗ FAILED'}")
    logger.info("")
    logger.info("Step Results:")
    logger.info(f"  1. Scraping:")
    logger.info(f"     - YouTube: {results['scraping'].get('youtube', 0)} videos")
    logger.info(f"     - OpenAI: {results['scraping'].get('openai', 0)} articles")
    logger.info(f"     - Anthropic: {results['scraping'].get('anthropic', 0)} articles")
    logger.info(f"  2. Anthropic Processing:")
    logger.info(f"     - Processed: {results['processing']['anthropic'].get('processed', 0)}")
    logger.info(f"  3. YouTube Processing:")
    logger.info(f"     - Processed: {results['processing']['youtube'].get('processed', 0)}")
    logger.info(f"  4. Digest Generation:")
    logger.info(f"     - Created: {results['digests'].get('processed', 0)}")
    logger.info(f"  5. Email Delivery:")
    logger.info(f"     - Status: {'✓ Sent' if results['email'].get('success') else '✗ Failed'}")
    logger.info("=" * 80)
    
    return results


if __name__ == "__main__":
    # Run the daily pipeline
    result = run_daily_pipeline(hours=24, top_n=10)
    
    # Exit with appropriate code
    exit(0 if result["success"] else 1)
