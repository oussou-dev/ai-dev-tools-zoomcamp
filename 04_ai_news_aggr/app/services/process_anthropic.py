import sys
from pathlib import Path
from typing import Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.scrapers.anthropic import AnthropicScraper
from app.database.repository import Repository


def process_anthropic_markdown(limit: Optional[int] = None) -> dict:
    """Process Anthropic articles and convert them to markdown.

    Args:
        limit: Maximum number of articles to process

    Returns:
        Dictionary with stats: total, processed, failed
    """
    scraper = AnthropicScraper()
    repo = Repository()

    # Fetch articles without markdown
    articles = repo.get_anthropic_articles_without_markdown(limit)

    processed = 0
    failed = 0

    for article in articles:
        try:
            markdown = scraper.url_to_markdown(article.url)

            if markdown:
                repo.update_anthropic_article_markdown(article.guid, markdown)
                processed += 1
            else:
                print(f"No markdown generated for article {article.guid}: {article.title}")
                failed += 1
        except Exception as e:
            print(f"Error processing article {article.guid}: {e}")
            failed += 1

    return {
        "total": len(articles),
        "processed": processed,
        "failed": failed,
    }


if __name__ == "__main__":
    stats = process_anthropic_markdown()
    print(f"Anthropic Markdown Processing Stats:")
    print(f"  Total: {stats['total']}")
    print(f"  Processed: {stats['processed']}")
    print(f"  Failed: {stats['failed']}")
