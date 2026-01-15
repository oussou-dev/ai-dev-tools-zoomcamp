import os
import smtplib
from html import escape
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, List
import markdown
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Email configuration from environment
MY_EMAIL = os.getenv("MY_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def send_email(
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    recipients: Optional[List[str]] = None
) -> None:
    """
    Send an email via Gmail SMTP with both plain text and HTML versions.
    
    Args:
        subject: Email subject line
        body_text: Plain text version of the email body
        body_html: Optional HTML version of the email body
        recipients: List of recipient email addresses (defaults to MY_EMAIL)
        
    Raises:
        ValueError: If email credentials are missing or recipients list is empty
    """
    # Validate environment variables
    if not MY_EMAIL or not APP_PASSWORD:
        raise ValueError("Email credentials (MY_EMAIL, APP_PASSWORD) must be set in environment variables")
    
    # Default to sending to self if no recipients specified
    if recipients is None:
        recipients = [MY_EMAIL]
    
    if not recipients:
        raise ValueError("Recipients list cannot be empty")
    
    # Create message with alternative parts (text and HTML)
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = MY_EMAIL
    message["To"] = ", ".join(recipients)
    
    # Attach plain text version
    text_part = MIMEText(body_text, "plain")
    message.attach(text_part)
    
    # Attach HTML version if provided
    if body_html:
        html_part = MIMEText(body_html, "html")
        message.attach(html_part)
    
    # Connect to Gmail SMTP server and send
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(MY_EMAIL, APP_PASSWORD)
        server.send_message(message)


def markdown_to_html(markdown_text: str) -> str:
    """
    Convert Markdown text to a styled HTML document.
    
    Args:
        markdown_text: Markdown-formatted text
        
    Returns:
        Complete HTML document with inline CSS styling
    """
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_text, extensions=['extra', 'nl2br'])
    
    # Wrap in complete HTML structure with CSS
    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Digest</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #555;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }}
        .greeting {{
            font-size: 1.1em;
            font-weight: 600;
        }}
        .relevance-score {{
            color: #27ae60;
            font-weight: bold;
        }}
        .article-link {{
            display: inline-block;
            margin-top: 10px;
            padding: 8px 16px;
            background-color: #3498db;
            color: white !important;
            border-radius: 4px;
            text-decoration: none;
        }}
        .article-link:hover {{
            background-color: #2980b9;
        }}
        .reasoning {{
            font-style: italic;
            color: #666;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
    
    return html_document


def digest_to_html(digest_response) -> str:
    """
    Convert an EmailDigestResponse object to styled HTML.
    
    Args:
        digest_response: EmailDigestResponse object or any object with to_markdown() method
        
    Returns:
        Complete HTML document with inline CSS styling
    """
    # Import here to avoid circular dependency
    from app.agents.email_agent import EmailDigestResponse
    
    # Fallback to markdown conversion if not the expected type
    if not isinstance(digest_response, EmailDigestResponse):
        if hasattr(digest_response, 'to_markdown'):
            return markdown_to_html(digest_response.to_markdown())
        else:
            return markdown_to_html(str(digest_response))
    
    # Build HTML content from EmailDigestResponse
    html_parts = []
    
    # Add greeting
    html_parts.append(f'<p class="greeting">{escape(digest_response.introduction.greeting)}</p>')
    
    # Add introduction
    intro_lines = digest_response.introduction.introduction.split('\n')
    for line in intro_lines:
        if line.strip():
            html_parts.append(f'<p>{escape(line)}</p>')
    
    html_parts.append('<hr>')
    
    # Add articles
    for article in digest_response.articles:
        # Article title
        html_parts.append(f'<h2>#{article.rank} - {escape(article.title)}</h2>')
        
        # Relevance score
        html_parts.append(f'<p class="relevance-score">Relevance Score: {article.relevance_score:.1f}/10.0</p>')
        
        # Summary
        html_parts.append(f'<p>{escape(article.summary)}</p>')
        
        # Read more link
        html_parts.append(f'<a href="{escape(article.url)}" class="article-link">Read more →</a>')
        
        # Reasoning (if available)
        if article.reasoning:
            html_parts.append(f'<p class="reasoning">Why this matters: {escape(article.reasoning)}</p>')
        
        html_parts.append('<hr>')
    
    # Add footer
    html_parts.append(f'<p><em>Showing top {digest_response.top_n} of {digest_response.total_ranked} ranked articles</em></p>')
    
    # Combine all parts
    html_content = '\n'.join(html_parts)
    
    # Wrap in complete HTML structure
    html_document = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Digest</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
            background-color: #f9f9f9;
        }}
        a {{
            color: #0066cc;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
        }}
        h3 {{
            color: #555;
        }}
        hr {{
            border: none;
            border-top: 1px solid #ddd;
            margin: 30px 0;
        }}
        .greeting {{
            font-size: 1.1em;
            font-weight: 600;
            color: #2c3e50;
        }}
        .relevance-score {{
            color: #27ae60;
            font-weight: bold;
        }}
        .article-link {{
            display: inline-block;
            margin-top: 10px;
            padding: 8px 16px;
            background-color: #3498db;
            color: white !important;
            border-radius: 4px;
            text-decoration: none;
        }}
        .article-link:hover {{
            background-color: #2980b9;
            text-decoration: none;
        }}
        .reasoning {{
            font-style: italic;
            color: #666;
            margin-top: 10px;
            padding: 10px;
            background-color: #ecf0f1;
            border-left: 3px solid #3498db;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""
    
    return html_document


def send_email_to_self(subject: str, body: str) -> None:
    """
    Simple wrapper to send an email to yourself.
    
    Args:
        subject: Email subject line
        body: Plain text email body
    """
    send_email(subject, body, recipients=[MY_EMAIL])


if __name__ == "__main__":
    # Test email sending
    print("Sending test email...")
    
    test_markdown = """
# Test AI News Digest

Hey there!

This is a test email to verify the email service is working correctly.

## Article 1: Test Article

This is a summary of a test article about AI and machine learning.

[Read more →](https://example.com)

---

*End of test digest*
"""
    
    try:
        html_body = markdown_to_html(test_markdown)
        send_email(
            subject="Test: AI News Digest Service",
            body_text=test_markdown,
            body_html=html_body
        )
        print("✓ Test email sent successfully!")
    except Exception as e:
        print(f"✗ Error sending test email: {e}")
