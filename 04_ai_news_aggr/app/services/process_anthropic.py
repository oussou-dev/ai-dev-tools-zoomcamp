import sys
from pathlib import Path
from typing import Optional

# Add project root to Python path for proper imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from app.scrapers.anthropic import AnthropicScraper
from app.database.repository import Repository


def process_anthropic_markdown(limit: Optional[int] = None) -> dict:
    """
    Process Anthropic articles that lack markdown content by fetching and storing it.
    
    This function fetches markdown-converted content for articles already in the database
    that don't have markdown content yet. It uses docling to convert web pages to markdown.
    
    Args:
        limit: Maximum number of articles to process (None for all)
        
    Returns:
        Dictionary with processing statistics:
        - total: Total articles processed
        - processed: Articles with successfully fetched markdown
        - failed: Articles where conversion failed
    """
    # Initialize scraper and repository
    scraper = AnthropicScraper()
    repo = Repository()
    
    # Fetch articles without markdown
    articles = repo.get_anthropic_articles_without_markdown(limit=limit)
    
    # Initialize counters
    total = len(articles)
    processed = 0
    failed = 0
    
    print(f"Processing {total} Anthropic articles without markdown...")
    
    # Loop through articles and fetch markdown content
    for i, article in enumerate(articles, 1):
        print(f"[{i}/{total}] Processing: {article.title[:60]}...")
        
        try:
            # Attempt to convert URL to markdown
            markdown_content = scraper.url_to_markdown(article.url)
            
            if markdown_content:
                # Success: Update database with markdown content
                success = repo.update_anthropic_article_markdown(article.guid, markdown_content)
                
                if success:
                    processed += 1
                    print(f"  ✓ Markdown fetched ({len(markdown_content)} characters)")
                else:
                    failed += 1
                    print(f"  ✗ Failed to update database for GUID: {article.guid}")
            else:
                # Conversion returned None
                failed += 1
                print(f"  ✗ Failed to convert URL to markdown")
                
        except Exception as e:
            # Error occurred during conversion or update
            failed += 1
            print(f"  ✗ Error processing GUID {article.guid}: {e}")
    
    # Return statistics
    return {
        "total": total,
        "processed": processed,
        "failed": failed
    }


if __name__ == "__main__":
    # Run markdown processing
    print("Starting Anthropic markdown processing...")
    print("=" * 60)
    
    stats = process_anthropic_markdown()
    
    print("=" * 60)
    print("\nProcessing Complete!")
    print(f"Total articles: {stats['total']}")
    print(f"✓ Processed: {stats['processed']}")
    print(f"✗ Failed: {stats['failed']}")
