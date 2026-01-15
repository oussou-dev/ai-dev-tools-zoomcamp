import sys
from pathlib import Path
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.agents.email_agent import EmailAgent, RankedArticleDetail, EmailDigestResponse
from app.agents.curator_agent import CuratorAgent
from app.profiles.user_profile import USER_PROFILE
from app.database.repository import Repository
from app.services.email import send_email, digest_to_html

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def generate_email_digest(hours: int = 24, top_n: int = 10) -> EmailDigestResponse:
    """
    Generate a personalized email digest by fetching, ranking, and formatting news.
    
    This function orchestrates the complete digest generation pipeline:
    1. Fetch recent digests from database
    2. Rank them using the curator agent based on user profile
    3. Reconstruct full article details
    4. Generate email content with personalized introduction
    
    Args:
        hours: Number of hours to look back for digests (default: 24)
        top_n: Number of top articles to include in email (default: 10)
        
    Returns:
        EmailDigestResponse object with formatted content
        
    Raises:
        ValueError: If no digests found or ranking fails
    """
    logger.info(f"Generating email digest (last {hours} hours, top {top_n})...")
    
    # Initialize agents and repository
    curator = CuratorAgent(USER_PROFILE)
    email_agent = EmailAgent(USER_PROFILE)
    repo = Repository()
    
    # Fetch recent digests
    logger.info("Fetching recent digests...")
    digests = repo.get_recent_digests(hours=hours)
    
    if not digests:
        raise ValueError(f"No digests found in the last {hours} hours")
    
    logger.info(f"Found {len(digests)} digests")
    
    # Prepare digests for ranking
    digest_list = []
    for digest in digests:
        digest_list.append({
            'id': digest.id,
            'title': digest.title,
            'summary': digest.summary,
            'type': digest.article_type
        })
    
    # Rank digests
    logger.info("Ranking digests based on user profile...")
    ranked_articles = curator.rank_digests(digest_list)
    
    if not ranked_articles:
        raise ValueError("Ranking failed - no articles were ranked")
    
    logger.info(f"Successfully ranked {len(ranked_articles)} articles")
    
    # Data reconstruction: Build RankedArticleDetail objects
    # The ranked articles only have IDs and scores, we need to reconstruct full details
    logger.info("Reconstructing article details...")
    detailed_articles = []
    
    for ranked in ranked_articles:
        # Find the matching digest
        matching_digest = next(
            (d for d in digests if d.id == ranked.digest_id),
            None
        )
        
        if matching_digest:
            # Create RankedArticleDetail with all information
            detailed_article = RankedArticleDetail(
                digest_id=ranked.digest_id,
                rank=ranked.rank,
                relevance_score=ranked.relevance_score,
                title=matching_digest.title,
                summary=matching_digest.summary,
                url=matching_digest.url,
                article_type=matching_digest.article_type,
                reasoning=ranked.reasoning
            )
            detailed_articles.append(detailed_article)
        else:
            logger.warning(f"Could not find digest for ID: {ranked.digest_id}")
    
    # Generate email digest response
    logger.info("Generating email content...")
    email_response = email_agent.create_email_digest_response(
        ranked_articles=detailed_articles,
        total_ranked=len(ranked_articles),
        limit=top_n
    )
    
    # Log the generated content
    logger.info("=" * 80)
    logger.info(f"Greeting: {email_response.introduction.greeting}")
    logger.info(f"Introduction: {email_response.introduction.introduction[:100]}...")
    logger.info("=" * 80)
    
    return email_response


def send_digest_email(hours: int = 24, top_n: int = 10) -> dict:
    """
    Generate and send the personalized email digest.
    
    This function wraps the entire email pipeline including generation,
    formatting, and delivery.
    
    Args:
        hours: Number of hours to look back for digests (default: 24)
        top_n: Number of top articles to include (default: 10)
        
    Returns:
        Dictionary with send results:
        - success: Boolean indicating if email was sent
        - subject: Email subject line
        - articles_sent: Number of articles included
        - error: Error message if failed
    """
    try:
        # Generate the email digest
        logger.info("Starting email digest pipeline...")
        email_response = generate_email_digest(hours=hours, top_n=top_n)
        
        # Convert to markdown and HTML
        logger.info("Converting to markdown and HTML...")
        markdown_body = email_response.to_markdown()
        html_body = digest_to_html(email_response)
        
        # Extract date from introduction for subject line
        # Try to extract date from greeting (e.g., "for January 15, 2026")
        subject_date = "Today"
        try:
            intro_text = email_response.introduction.introduction
            if "for " in intro_text:
                # Extract text after "for "
                date_part = intro_text.split("for ")[-1].split(".")[0].split("!")[0].strip()
                if date_part:
                    subject_date = date_part
        except Exception:
            # Keep default "Today" if extraction fails
            pass
        
        subject = f"Daily AI News Digest - {subject_date}"
        
        # Send email
        logger.info(f"Sending email: {subject}")
        send_email(
            subject=subject,
            body_text=markdown_body,
            body_html=html_body
        )
        
        logger.info("✓ Email sent successfully!")
        
        return {
            "success": True,
            "subject": subject,
            "articles_sent": len(email_response.articles),
            "total_ranked": email_response.total_ranked
        }
        
    except Exception as e:
        logger.error(f"✗ Error sending digest email: {e}")
        return {
            "success": False,
            "error": str(e)
        }


if __name__ == "__main__":
    # Run email digest pipeline
    logger.info("=" * 80)
    logger.info("STARTING EMAIL DIGEST PIPELINE")
    logger.info("=" * 80)
    
    result = send_digest_email(hours=24, top_n=10)
    
    print("\n" + "=" * 80)
    print("EMAIL DIGEST PIPELINE RESULT")
    print("=" * 80)
    
    if result.get('success'):
        print(f"✓ Success!")
        print(f"  Subject: {result['subject']}")
        print(f"  Articles sent: {result['articles_sent']}")
        print(f"  Total ranked: {result['total_ranked']}")
    else:
        print(f"✗ Failed!")
        print(f"  Error: {result.get('error', 'Unknown error')}")
    
    print("=" * 80)
