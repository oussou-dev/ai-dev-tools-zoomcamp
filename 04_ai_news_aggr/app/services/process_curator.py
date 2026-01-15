import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path for proper imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.agents.curator_agent import CuratorAgent
from app.profiles.user_profile import USER_PROFILE
from app.database.repository import Repository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def curate_digests(hours: int = 24) -> dict:
    """
    Rank news digests based on user profile and preferences.
    
    This function fetches recent digests and uses the CuratorAgent to rank them
    according to the user's interests, expertise level, and preferences.
    
    Args:
        hours: Number of hours to look back for digests (default: 24)
        
    Returns:
        Dictionary with curation results:
        - total: Total digests found
        - ranked: Number of digests successfully ranked
        - articles: List of ranked articles with scores and reasoning
    """
    # Initialize curator with user profile and repository
    curator = CuratorAgent(USER_PROFILE)
    repo = Repository()
    
    # Fetch recent digests
    logger.info(f"Fetching digests from the last {hours} hours...")
    digests = repo.get_recent_digests(hours=hours)
    
    # Check if any digests found
    if not digests:
        logger.warning("No digests found in the specified time window")
        return {"total": 0, "ranked": 0}
    
    logger.info(f"Found {len(digests)} digests to curate")
    
    # Log user profile information
    user_name = USER_PROFILE.get('name', 'User')
    user_background = USER_PROFILE.get('background', 'N/A')
    logger.info(f"Curating for: {user_name} - {user_background}")
    
    # Prepare digests for ranking (convert to dict format)
    digest_list = []
    for digest in digests:
        digest_list.append({
            'id': digest.id,
            'title': digest.title,
            'summary': digest.summary,
            'type': digest.article_type
        })
    
    # Rank digests using curator agent
    logger.info("Starting curation process...")
    ranked_articles = curator.rank_digests(digest_list)
    
    # Check if ranking succeeded
    if not ranked_articles:
        logger.error("Curation failed - no articles were ranked")
        return {"total": len(digests), "ranked": 0}
    
    logger.info(f"Successfully ranked {len(ranked_articles)} articles")
    logger.info("=" * 80)
    logger.info("TOP 10 RANKED ARTICLES:")
    logger.info("=" * 80)
    
    # Log top 10 ranked articles with details
    top_articles = ranked_articles[:10]
    for article in top_articles:
        # Find corresponding digest to get full details
        digest = next((d for d in digests if d.id == article.digest_id), None)
        
        if digest:
            logger.info(f"\nRank #{article.rank}")
            logger.info(f"  Score: {article.relevance_score:.2f}/10.0")
            logger.info(f"  Title: {digest.title}")
            logger.info(f"  Type: {digest.article_type}")
            logger.info(f"  Reasoning: {article.reasoning}")
        else:
            logger.warning(f"  Could not find digest details for ID: {article.digest_id}")
    
    logger.info("\n" + "=" * 80)
    
    # Prepare simplified results
    results = []
    for article in ranked_articles:
        results.append({
            'digest_id': article.digest_id,
            'rank': article.rank,
            'score': article.relevance_score,
            'reasoning': article.reasoning
        })
    
    return {
        "total": len(digests),
        "ranked": len(ranked_articles),
        "articles": results
    }


if __name__ == "__main__":
    # Run curation process
    logger.info("Starting digest curation service...")
    logger.info("=" * 80)
    
    stats = curate_digests(hours=24)
    
    print("\n" + "=" * 80)
    print("Curation Summary:")
    print(f"Total digests: {stats['total']}")
    print(f"Successfully ranked: {stats['ranked']}")
    if stats.get('articles'):
        print(f"Top score: {max(a['score'] for a in stats['articles']):.2f}")
        print(f"Average score: {sum(a['score'] for a in stats['articles']) / len(stats['articles']):.2f}")
    print("=" * 80)
