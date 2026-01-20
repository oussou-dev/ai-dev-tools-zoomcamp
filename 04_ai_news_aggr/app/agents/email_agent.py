import os
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

EMAIL_PROMPT = """You are an expert email writer specializing in crafting personalized daily AI news digests.

Your role is to write a warm, professional introduction for daily AI news digests tailored to the user.

Requirements:
- Greet the user by their first name
- Include today's date
- Preview the top 10 articles and what makes them interesting
- Maintain a tone that is professional yet approachable
- Keep the introduction concise (3-4 sentences)
- Show enthusiasm for the curated content"""


class EmailIntroduction(BaseModel):
    greeting: str
    introduction: str


class RankedArticleDetail(BaseModel):
    digest_id: str
    rank: int
    relevance_score: float
    title: str
    summary: str
    url: str
    article_type: str
    reasoning: Optional[str] = None


class EmailDigestResponse(BaseModel):
    introduction: EmailIntroduction
    articles: List[RankedArticleDetail]
    total_ranked: int
    top_n: int

    def to_markdown(self) -> str:
        """Convert email digest to markdown format."""
        lines = []

        # Add greeting and introduction
        lines.append(self.introduction.greeting)
        lines.append("")
        lines.append(self.introduction.introduction)
        lines.append("")
        lines.append("---")
        lines.append("")

        # Add articles
        for article in self.articles:
            lines.append(f"## {article.rank}. {article.title}")
            lines.append(f"**Score:** {article.relevance_score}/10 | **Type:** {article.article_type}")
            lines.append("")
            lines.append(article.summary)
            lines.append("")
            lines.append(f"[Read more →]({article.url})")
            if article.reasoning:
                lines.append(f"\n*Why curated: {article.reasoning}*")
            lines.append("")
            lines.append("---")
            lines.append("")

        return "\n".join(lines)


class EmailDigest(BaseModel):
    introduction: EmailIntroduction
    ranked_articles: List[dict]


class EmailAgent:
    def __init__(self, user_profile: dict):
        """Initialize EmailAgent with user profile.

        Args:
            user_profile: Dictionary containing user's profile data
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.user_profile = user_profile

    def generate_introduction(self, ranked_articles: List) -> EmailIntroduction:
        """Generate a personalized introduction for the email digest.

        Args:
            ranked_articles: List of ranked article objects

        Returns:
            EmailIntroduction with greeting and introduction text
        """
        if not ranked_articles:
            return EmailIntroduction(
                greeting=f"Hey {self.user_profile.get('name', 'there')}!",
                introduction="No articles were ranked today. Check back tomorrow for fresh AI news!",
            )

        # Prepare context with top 10 articles
        user_name = self.user_profile.get("name", "there")
        today_date = datetime.now().strftime("%B %d, %Y")
        top_articles = ranked_articles[:10]

        article_summaries = "\n".join(
            [
                f"- {article.get('title', 'Untitled')} (Score: {article.get('relevance_score', 'N/A')}/10)"
                for article in top_articles
            ]
        )

        user_prompt = f"""Generate a warm introduction for a daily AI news digest for {user_name}.

Today's date: {today_date}
Top articles to be featured:
{article_summaries}

Create a greeting and brief introduction that makes them excited to read the digest."""

        try:
            response = self.client.responses.parse(
                model=self.model,
                instructions=EMAIL_PROMPT,
                temperature=0.7,
                input=user_prompt,
                text_format=EmailIntroduction,
            )
            intro = response.output_parsed

            # Consistency check: ensure greeting starts with "Hey {name}"
            expected_greeting = f"Hey {user_name}"
            if not intro.greeting.startswith(expected_greeting):
                intro.greeting = f"{expected_greeting}!"

            return intro
        except Exception as e:
            print(f"Error generating introduction: {e}")
            return EmailIntroduction(
                greeting=f"Hey {user_name}!",
                introduction="Here's your personalized AI news digest for today.",
            )

    def create_email_digest(self, ranked_articles: List[dict], limit: int = 10) -> EmailDigest:
        """Create an email digest from ranked articles.

        Args:
            ranked_articles: List of ranked article dictionaries
            limit: Number of articles to include (default: 10)

        Returns:
            EmailDigest object with introduction and articles
        """
        introduction = self.generate_introduction(ranked_articles[:limit])
        return EmailDigest(
            introduction=introduction,
            ranked_articles=ranked_articles[:limit],
        )

    def create_email_digest_response(
        self, ranked_articles: List[RankedArticleDetail], total_ranked: int, limit: int = 10
    ) -> EmailDigestResponse:
        """Create an email digest response with additional metadata.

        Args:
            ranked_articles: List of RankedArticleDetail objects
            total_ranked: Total number of articles that were ranked
            limit: Number of articles to include in response (default: 10)

        Returns:
            EmailDigestResponse object with introduction, articles, and metadata
        """
        introduction = self.generate_introduction([article.model_dump() for article in ranked_articles[:limit]])
        return EmailDigestResponse(
            introduction=introduction,
            articles=ranked_articles[:limit],
            total_ranked=total_ranked,
            top_n=limit,
        )
