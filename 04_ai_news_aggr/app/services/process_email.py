import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

# Setup path and load env
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))
load_dotenv()

from app.agents.email_agent import EmailAgent, RankedArticleDetail, EmailDigestResponse
from app.agents.curator_agent import CuratorAgent
from app.profiles.user_profile import USER_PROFILE
from app.database.repository import Repository
from app.services.email import send_email, digest_to_html

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def generate_email_digest(hours: int = 24, top_n: int = 10) -> EmailDigestResponse:
    """Generate email digest from curated content.

    Args:
        hours: Number of hours to look back
        top_n: Number of top articles to include

    Returns:
        EmailDigestResponse object

    Raises:
        ValueError: If no digests or ranked articles found
    """
    curator = CuratorAgent(USER_PROFILE)
    email_agent = EmailAgent(USER_PROFILE)
    repo = Repository()

    # Fetch recent digests
    digests = repo.get_recent_digests(hours=hours)
    if not digests:
        raise ValueError(f"No digests found in the last {hours} hours")

    # Convert to dict format
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

    # Rank digests
    ranked_articles = curator.rank_digests(digest_dicts)
    if not ranked_articles:
        raise ValueError("No ranked articles returned from curator")

    # Reconstruct RankedArticleDetail objects with full information
    ranked_article_details = []
    for ranked_article in ranked_articles:
        # Find matching digest
        matching_digest = next(
            (d for d in digest_dicts if d["id"] == ranked_article.digest_id),
            None,
        )

        if matching_digest:
            detail = RankedArticleDetail(
                digest_id=ranked_article.digest_id,
                rank=ranked_article.rank,
                relevance_score=ranked_article.relevance_score,
                title=matching_digest["title"],
                summary=matching_digest["summary"],
                url=matching_digest["url"],
                article_type=matching_digest["type"],
                reasoning=ranked_article.reasoning,
            )
            ranked_article_details.append(detail)

    # Generate email digest response
    response = email_agent.create_email_digest_response(
        ranked_article_details,
        total_ranked=len(ranked_articles),
        limit=top_n,
    )

    logger.info(f"Email digest generated:")
    logger.info(f"  Greeting: {response.introduction.greeting}")
    logger.info(f"  Articles included: {len(response.articles)}/{response.total_ranked}")

    return response


def send_digest_email(hours: int = 24, top_n: int = 10) -> dict:
    """Generate and send digest email.

    Args:
        hours: Number of hours to look back
        top_n: Number of top articles to include

    Returns:
        Dictionary with success status and metadata
    """
    try:
        # Generate digest
        digest_response = generate_email_digest(hours=hours, top_n=top_n)

        # Convert to markdown and HTML
        markdown_body = digest_response.to_markdown()
        html_body = digest_to_html(digest_response)

        # Extract date for subject line
        # Parse from greeting (e.g., "Hey Ouskä! - January 15, 2025")
        greeting = digest_response.introduction.greeting
        date_part = "Today"
        if " - " in greeting:
            date_part = greeting.split(" - ")[-1]

        subject = f"Daily AI News Digest - {date_part}"

        # Send email
        send_email(subject, markdown_body, body_html=html_body)

        logger.info(f"Digest email sent successfully!")

        return {
            "success": True,
            "subject": subject,
            "articles_count": len(digest_response.articles),
        }

    except Exception as e:
        logger.error(f"Failed to send digest email: {e}")
        return {
            "success": False,
            "error": str(e),
        }


if __name__ == "__main__":
    result = send_digest_email()
    print(f"\nEmail Send Result:")
    print(f"  Success: {result.get('success', False)}")
    if result.get("success"):
        print(f"  Subject: {result.get('subject')}")
        print(f"  Articles: {result.get('articles_count')}")
    else:
        print(f"  Error: {result.get('error')}")
