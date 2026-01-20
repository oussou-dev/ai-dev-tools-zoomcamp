import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

# Setup path and load env
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
load_dotenv()

from app.agents.curator_agent import CuratorAgent
from app.profiles.user_profile import USER_PROFILE
from app.database.repository import Repository

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def curate_digests(hours: int = 24) -> dict:
    """Curate and rank digests based on user profile.

    Args:
        hours: Number of hours to look back for recent digests

    Returns:
        Dictionary with stats: total, ranked, and articles list
    """
    curator = CuratorAgent(USER_PROFILE)
    repo = Repository()

    # Fetch recent digests
    digests = repo.get_recent_digests(hours=hours)

    if not digests:
        logger.warning(f"No digests found in the last {hours} hours")
        return {"total": 0, "ranked": 0, "articles": []}

    # Convert digests to dict format for curator
    digest_dicts = [
        {
            "id": digest.id,
            "title": digest.title,
            "summary": digest.summary,
            "type": digest.article_type,
            "url": digest.url,
        }
        for digest in digests
    ]

    user_name = USER_PROFILE.get("name", "User")
    user_background = USER_PROFILE.get("background", "N/A")
    logger.info(f"Curating digests for {user_name} ({user_background})")

    # Rank digests
    ranked_articles = curator.rank_digests(digest_dicts)

    if not ranked_articles:
        logger.error("Curator returned no ranked articles")
        return {"total": len(digests), "ranked": 0, "articles": []}

    # Log top 10
    logger.info("Top 10 Ranked Articles:")
    articles_output = []

    for ranked_article in ranked_articles[:10]:
        # Find original digest to get title and type
        matching_digest = next(
            (d for d in digest_dicts if d["id"] == ranked_article.digest_id),
            None,
        )

        if matching_digest:
            title = matching_digest["title"]
            article_type = matching_digest["type"]
            logger.info(
                f"  #{ranked_article.rank}. {title} (Score: {ranked_article.relevance_score}/10, Type: {article_type})"
            )
            logger.info(f"     Reasoning: {ranked_article.reasoning}")

            articles_output.append(
                {
                    "digest_id": ranked_article.digest_id,
                    "rank": ranked_article.rank,
                    "score": ranked_article.relevance_score,
                    "reasoning": ranked_article.reasoning,
                }
            )

    return {
        "total": len(digests),
        "ranked": len(ranked_articles),
        "articles": articles_output,
    }


if __name__ == "__main__":
    result = curate_digests()
    print(f"\nCuration Summary:")
    print(f"  Total digests: {result['total']}")
    print(f"  Ranked: {result['ranked']}")
    print(f"  Top articles returned: {len(result['articles'])}")
