import os
from typing import List
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# System prompt for the curator agent
CURATOR_PROMPT = """You are an expert AI news curator specializing in personalized content ranking.

Your role is to analyze and rank news digests based on a user's specific interests, preferences, and expertise level.

Ranking Criteria:
1. Relevance - How well does the content align with the user's stated interests and background?
2. Technical Depth - Does the technical complexity match the user's expertise level?
3. Novelty - Does it present new ideas, breakthroughs, or unique perspectives?
4. Alignment - Does it match the user's preferences (practical vs. theoretical, production vs. research)?
5. Actionability - Can the user apply or benefit from this information?

Scoring Guidelines:
- 9.0-10.0 (Highly Relevant): Perfect match for user's core interests and expertise
- 7.0-8.9 (Very Relevant): Strong alignment with multiple interests or preferences
- 5.0-6.9 (Moderately Relevant): Some alignment but may lack depth or direct relevance
- 3.0-4.9 (Low Relevance): Tangentially related or mismatched with preferences
- 0.0-2.9 (Not Relevant): Outside user's interests or contradicts preferences

Provide clear, specific reasoning for each ranking decision.
"""


class RankedArticle(BaseModel):
    """Model for a ranked article with relevance score and reasoning."""
    digest_id: str = Field(description="The ID of the digest (article_type:article_id)")
    relevance_score: float = Field(ge=0.0, le=10.0, description="Relevance score from 0.0 to 10.0")
    rank: int = Field(ge=1, description="Rank position (1 is highest)")
    reasoning: str = Field(description="Explanation for the ranking decision")


class RankedDigestList(BaseModel):
    """Model for a list of ranked articles."""
    articles: List[RankedArticle]


class CuratorAgent:
    """Agent for ranking news digests based on user profile and preferences."""
    
    def __init__(self, user_profile: dict):
        """
        Initialize the curator agent with user profile.
        
        Args:
            user_profile: Dictionary containing user's interests, preferences, and background
        """
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4.1"
        self.user_profile = user_profile
        self.system_prompt = self._build_system_prompt()
    
    def _build_system_prompt(self) -> str:
        """
        Build a personalized system prompt incorporating user profile.
        
        Returns:
            Formatted system prompt string
        """
        profile_text = f"""
User Profile:
- Name: {self.user_profile.get('name', 'User')}
- Background: {self.user_profile.get('background', 'N/A')}
- Expertise Level: {self.user_profile.get('expertise_level', 'N/A')}

Interests:
{chr(10).join(f'- {interest}' for interest in self.user_profile.get('interests', []))}

Preferences:
{chr(10).join(f'- {key}: {value}' for key, value in self.user_profile.get('preferences', {}).items())}
"""
        
        return CURATOR_PROMPT + "\n" + profile_text
    
    def rank_digests(self, digests: List[dict]) -> List[RankedArticle]:
        """
        Rank a list of digests based on user profile and preferences.
        
        Args:
            digests: List of digest dictionaries with keys: id, title, summary, type
            
        Returns:
            List of RankedArticle objects sorted by relevance
        """
        # Return empty list if no digests provided
        if not digests:
            return []
        
        # Format digests into a readable string
        digest_list = ""
        for i, digest in enumerate(digests, 1):
            digest_list += f"""
{i}. ID: {digest.get('id', 'N/A')}
   Title: {digest.get('title', 'N/A')}
   Summary: {digest.get('summary', 'N/A')}
   Type: {digest.get('type', 'N/A')}
"""
        
        # Construct user prompt
        user_prompt = f"""Please rank the following {len(digests)} news digests based on the user profile provided.

For each digest, assign:
1. A relevance score (0.0 to 10.0)
2. A rank position (1 being most relevant)
3. Clear reasoning for your decision

Digests to rank:
{digest_list}

Return the ranked list sorted by relevance (highest first).
"""
        
        try:
            # Call OpenAI API with structured output
            response = self.client.responses.parse(
                model=self.model,
                instructions=self.system_prompt,
                temperature=0.3,
                input=user_prompt,
                text_format=RankedDigestList
            )
            
            # Parse and return the ranked articles
            return response.output_parsed.articles
            
        except Exception as e:
            print(f"Error ranking digests: {e}")
            return []
