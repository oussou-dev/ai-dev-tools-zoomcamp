import sys
from pathlib import Path
import logging
from typing import Optional

# Add project root to Python path for proper imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.agents.digest_agent import DigestAgent
from app.database.repository import Repository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def process_digests(limit: Optional[int] = None) -> dict:
    """
    Generate AI summaries for all unprocessed content (YouTube videos, articles).
    
    This function identifies content that hasn't been summarized yet and uses
    the DigestAgent to generate concise summaries using an LLM.
    
    Args:
        limit: Maximum number of items to process (None for all)
        
    Returns:
        Dictionary with processing statistics:
        - total: Total items to process
        - processed: Items successfully summarized
        - failed: Items that failed to process
    """
    # Initialize agent and repository
    agent = DigestAgent()
    repo = Repository()
    
    # Fetch articles without digests
    logger.info("Fetching articles without digests...")
    articles = repo.get_articles_without_digest(limit=limit)
    
    total = len(articles)
    processed = 0
    failed = 0
    
    logger.info(f"Starting digest generation for {total} items...")
    
    # Loop through articles and generate digests
    for i, article in enumerate(articles, 1):
        # Truncate title for readability in logs
        title_display = article['title'][:60]
        if len(article['title']) > 60:
            title_display += "..."
        
        logger.info(f"[{i}/{total}] Processing: {title_display}")
        
        try:
            # Generate digest using the agent
            digest = agent.generate_digest(
                title=article['title'],
                content=article['content'],
                article_type=article['type']
            )
            
            if digest:
                # Create digest entry in database
                repo.create_digest(
                    article_type=article['type'],
                    article_id=article['id'],
                    url=article['url'],
                    title=digest.title,
                    summary=digest.summary,
                    published_at=article['published_at']
                )
                processed += 1
                logger.info(f"  ✓ Digest created: {digest.title[:50]}...")
            else:
                # Agent returned None
                failed += 1
                logger.warning(f"  ✗ Failed to generate digest (agent returned None)")
                
        except Exception as e:
            # Error occurred during generation or saving
            failed += 1
            logger.error(f"  ✗ Error: {e}")
    
    # Log completion summary
    logger.info("=" * 60)
    logger.info("Digest generation complete!")
    logger.info(f"Total items: {total}")
    logger.info(f"✓ Processed: {processed}")
    logger.info(f"✗ Failed: {failed}")
    logger.info("=" * 60)
    
    # Return statistics
    return {
        "total": total,
        "processed": processed,
        "failed": failed
    }


if __name__ == "__main__":
    # Run digest processing
    logger.info("Starting digest processing service...")
    
    stats = process_digests()
    
    print("\n" + "=" * 60)
    print("Processing Summary:")
    print(f"Total items: {stats['total']}")
    print(f"✓ Processed: {stats['processed']}")
    print(f"✗ Failed: {stats['failed']}")
    print("=" * 60)
