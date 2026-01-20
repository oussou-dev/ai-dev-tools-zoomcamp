import os
from typing import List

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv()

CURATOR_PROMPT = """You are an Expert AI news curator specializing in personalized content ranking.

Your task is to analyze and rank digests based on a user's profile and interests.

Scoring Criteria:
1. Relevance: How well does the content align with the user's interests?
2. Technical Depth: Does it provide substantive technical insights?
3. Novelty: Is it cutting-edge or introducing new concepts?
4. Alignment: How well does it match the user's preferences (practical, research-focused, etc.)?
5. Actionability: Can the reader apply the insights practically?

Scoring Guidelines:
- 9.0-10.0 (Highly Relevant): Perfect match for user profile, high technical depth, novel breakthrough
- 7.0-8.9 (Very Relevant): Strong alignment, good technical content, actionable insights
- 5.0-6.9 (Moderately Relevant): Some alignment, decent technical content, limited actionability
- 3.0-4.9 (Weakly Relevant): Limited alignment, basic content, minimal actionability
- 1.0-2.9 (Not Relevant): Poor alignment, low technical value, not actionable

Provide clear reasoning for each score."""


class RankedArticle(BaseModel):
    digest_id: str = Field(description="The ID of the digest (article_type:article_id)")
    relevance_score: float = Field(ge=0.0, le=10.0)
    rank: int = Field(ge=1)
    reasoning: str


class RankedDigestList(BaseModel):
    articles: List[RankedArticle]


class CuratorAgent:
    def __init__(self, user_profile: dict):
        """Initialize CuratorAgent with user profile.

        Args:
            user_profile: Dictionary containing user's profile data (name, background, interests, preferences, etc.)
        """
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4.1"
        self.user_profile = user_profile
        self.system_prompt = self._build_system_prompt()

    def _build_system_prompt(self) -> str:
        """Build the system prompt by combining CURATOR_PROMPT with user profile data.

        Returns:
            Formatted system prompt with user profile context
        """
        profile_str = f"""User Profile:
- Name: {self.user_profile.get('name', 'User')}
- Title: {self.user_profile.get('title', 'N/A')}
- Background: {self.user_profile.get('background', 'N/A')}
- Expertise Level: {self.user_profile.get('expertise_level', 'N/A')}
- Interests: {', '.join(self.user_profile.get('interests', []))}
- Preferences:
  - Prefers practical content: {self.user_profile.get('preferences', {}).get('prefer_practical', False)}
  - Prefers technical depth: {self.user_profile.get('preferences', {}).get('prefer_technical_depth', False)}
  - Prefers research breakthroughs: {self.user_profile.get('preferences', {}).get('prefer_research_breakthroughs', False)}
  - Prefers production focus: {self.user_profile.get('preferences', {}).get('prefer_production_focus', False)}
  - Avoids marketing hype: {self.user_profile.get('preferences', {}).get('avoid_marketing_hype', False)}"""

        return f"{CURATOR_PROMPT}\n\n{profile_str}"

    def rank_digests(self, digests: List[dict]) -> List[RankedArticle]:
        """Rank a list of digests based on user profile.

        Args:
            digests: List of digest dictionaries with id, title, summary, type, url

        Returns:
            List of RankedArticle objects sorted by rank, or empty list on error
        """
        if not digests:
            return []

        # Format digests into a readable string
        digest_list = "\n".join(
            [
                f"ID: {digest.get('id', 'unknown')}\n"
                f"Title: {digest.get('title', 'N/A')}\n"
                f"Summary: {digest.get('summary', 'N/A')}\n"
                f"Type: {digest.get('type', 'N/A')}"
                for digest in digests
            ]
        )

        user_prompt = f"""Please rank the following digests based on the user profile and criteria provided:

{digest_list}

Return a JSON response with ranked articles sorted by relevance score (highest to lowest)."""

        try:
            response = self.client.responses.parse(
                model=self.model,
                instructions=self.system_prompt,
                temperature=0.3,
                input=user_prompt,
                text_format=RankedDigestList,
            )
            ranked_list = response.output_parsed
            return ranked_list.articles
        except Exception as e:
            print(f"Error ranking digests: {e}")
            return []
