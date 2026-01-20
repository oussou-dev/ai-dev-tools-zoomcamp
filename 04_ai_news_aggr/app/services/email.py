import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from html import escape
from typing import List, Optional

import markdown
from dotenv import load_dotenv

load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")


def markdown_to_html(markdown_text: str) -> str:
    """Convert markdown text to HTML with styling."""
    html_content = markdown.markdown(markdown_text, extensions=["extra", "nl2br"])

    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
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
        h2 {{
            color: #222;
            border-bottom: 2px solid #0066cc;
            padding-bottom: 10px;
        }}
        h3 {{
            color: #444;
            margin-top: 20px;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>"""

    return html_template


def digest_to_html(digest_response) -> str:
    """Convert EmailDigestResponse to HTML with styling.

    Args:
        digest_response: EmailDigestResponse object or any object with to_markdown method

    Returns:
        HTML string
    """
    # Local import to avoid circular dependency
    from app.agents.email_agent import EmailDigestResponse

    # If not an EmailDigestResponse, fallback to markdown conversion
    if not isinstance(digest_response, EmailDigestResponse):
        if hasattr(digest_response, "to_markdown"):
            return markdown_to_html(digest_response.to_markdown())
        return markdown_to_html(str(digest_response))

    # Build HTML for EmailDigestResponse
    articles_html = []

    # Add greeting and introduction
    greeting = escape(digest_response.introduction.greeting)
    introduction = escape(digest_response.introduction.introduction)

    articles_html.append(f"<h1>{greeting}</h1>")
    articles_html.append(f"<p>{introduction}</p>")
    articles_html.append("<hr>")

    # Add articles
    for article in digest_response.articles:
        title = escape(article.title)
        score = article.relevance_score
        article_type = escape(article.article_type)
        summary = escape(article.summary)
        url = escape(article.url)
        reasoning = article.reasoning or ""
        if reasoning:
            reasoning = escape(reasoning)

        articles_html.append(f"<h3>#{article.rank}. {title}</h3>")
        articles_html.append(f"<p><strong>Score:</strong> {score}/10 | <strong>Type:</strong> {article_type}</p>")
        articles_html.append(f"<p>{summary}</p>")
        articles_html.append(f'<p><a href="{url}">Read more →</a></p>')
        if reasoning:
            articles_html.append(f"<p><em>Why curated: {reasoning}</em></p>")
        articles_html.append("<hr>")

    articles_content = "\n".join(articles_html)

    html_template = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
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
            color: #0066cc;
            margin-bottom: 10px;
        }}
        h3 {{
            color: #222;
            margin-top: 20px;
        }}
        hr {{
            border: none;
            border-top: 2px solid #ddd;
            margin: 30px 0;
        }}
        strong {{
            color: #222;
        }}
    </style>
</head>
<body>
    {articles_content}
</body>
</html>"""

    return html_template


def send_email(
    subject: str,
    body_text: str,
    body_html: Optional[str] = None,
    recipients: Optional[List[str]] = None,
) -> None:
    """Send email via Gmail SMTP.

    Args:
        subject: Email subject
        body_text: Plain text email body
        body_html: Optional HTML email body
        recipients: List of recipient emails (default: [MY_EMAIL])

    Raises:
        ValueError: If email config is missing or recipients list is empty
    """
    if not MY_EMAIL or not APP_PASSWORD:
        raise ValueError("MY_EMAIL or APP_PASSWORD not configured in environment variables")

    if recipients is None:
        recipients = [MY_EMAIL]

    if not recipients:
        raise ValueError("Recipients list cannot be empty")

    # Create message
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = MY_EMAIL
    msg["To"] = ", ".join(recipients)

    # Attach plain text
    msg.attach(MIMEText(body_text, "plain"))

    # Attach HTML if provided
    if body_html:
        msg.attach(MIMEText(body_html, "html"))

    # Send via Gmail
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(MY_EMAIL, APP_PASSWORD)
            server.sendmail(MY_EMAIL, recipients, msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise


def send_email_to_self(subject: str, body: str) -> None:
    """Simple wrapper to send email to self.

    Args:
        subject: Email subject
        body: Email body (plain text)
    """
    send_email(subject, body, recipients=[MY_EMAIL])


if __name__ == "__main__":
    # Test email sending
    try:
        test_subject = "Test Email from AI News Aggregator"
        test_body = "This is a test email."
        send_email_to_self(test_subject, test_body)
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error sending test email: {e}")
