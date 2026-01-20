import logging
import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.agents.digest_agent import DigestAgent
from app.database.repository import Repository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def process_digests(limit: Optional[int] = None) -> dict:
    """Generate digests for all unprocessed articles and videos.

    Args:
        limit: Maximum number of items to process

    Returns:
        Dictionary with stats: total, processed, failed
    """
    agent = DigestAgent()
    repo = Repository()

    articles = repo.get_articles_without_digest(limit=limit)

    logger.info(f"Starting digest generation for {len(articles)} items")

    processed = 0
    failed = 0

    for idx, article in enumerate(articles, 1):
        try:
            title_display = article.get("title", "Unknown")[:60]
            logger.info(f"[{idx}/{len(articles)}] Processing: {title_display}")

            digest_output = agent.generate_digest(
                title=article.get("title", ""),
                content=article.get("content", ""),
                article_type=article.get("type", "unknown"),
            )

            if digest_output:
                repo.create_digest(
                    article_type=article.get("type", "unknown"),
                    article_id=article.get("id", ""),
                    url=article.get("url", ""),
                    title=digest_output.title,
                    summary=digest_output.summary,
                    published_at=article.get("published_at"),
                )
                processed += 1
                logger.info(f"✓ Digest created: {digest_output.title}")
            else:
                failed += 1
                logger.warning(f"✗ Failed to generate digest for: {title_display}")

        except Exception as e:
            failed += 1
            logger.error(f"✗ Error processing article: {e}")

    logger.info(f"Digest processing completed. Processed: {processed}, Failed: {failed}")

    return {
        "total": len(articles),
        "processed": processed,
        "failed": failed,
    }


if __name__ == "__main__":
    stats = process_digests()
    print(f"\nDigest Generation Stats:")
    print(f"  Total: {stats['total']}")
    print(f"  Processed: {stats['processed']}")
    print(f"  Failed: {stats['failed']}")
