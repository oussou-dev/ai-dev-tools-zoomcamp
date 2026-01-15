import os
from datetime import datetime
from typing import List, Optional
from openai import OpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# System prompt for email introduction generation
EMAIL_PROMPT = """You are an expert email writer specializing in personalized technical newsletters.

Your role is to write a warm, professional introduction for a daily AI news digest email.

Requirements:
- Greet the user by name in a friendly, professional tone
- Include the current date in a natural way
- Provide a brief preview of the top articles being shared
- Keep the tone conversational but professional
- Show enthusiasm for the curated content
- Keep it concise (2-3 paragraphs maximum)
"""


class EmailIntroduction(BaseModel):
    """Model for email greeting and introduction."""
    greeting: str
    introduction: str


class RankedArticleDetail(BaseModel):
    """Detailed model for ranked articles in email digest."""
    digest_id: str
    rank: int
    relevance_score: float
    title: str
    summary: str
    url: str
    article_type: str
    reasoning: Optional[str] = None


class EmailDigestResponse(BaseModel):
    """Complete email digest response with markdown export capability."""
    introduction: EmailIntroduction
    articles: List[RankedArticleDetail]
    total_ranked: int
    top_n: int
    
    def to_markdown(self) -> str:
        """
        Convert the email digest to a formatted Markdown string.
        
        Returns:
            Markdown-formatted email content
        """
        # Start with greeting and introduction
        markdown = f"{self.introduction.greeting}\n\n"
        markdown += f"{self.introduction.introduction}\n\n"
        markdown += "---\n\n"
        
        # Add articles
        for article in self.articles:
            markdown += f"## #{article.rank} - {article.title}\n\n"
            markdown += f"**Relevance Score:** {article.relevance_score:.1f}/10.0\n\n"
            markdown += f"{article.summary}\n\n"
            markdown += f"[Read more →]({article.url})\n\n"
            
            if article.reasoning:
                markdown += f"*Why this matters: {article.reasoning}*\n\n"
            
            markdown += "---\n\n"
        
        # Add footer
        markdown += f"*Showing top {self.top_n} of {self.total_ranked} ranked articles*\n"
        
        return markdown


class EmailDigest(BaseModel):
    """Simple email digest model."""
    introduction: EmailIntroduction
    ranked_articles: List[dict]


class EmailAgent:
    """Agent for generating personalized email digest content."""
    
    def __init__(self, user_profile: dict):
        """
        Initialize the email agent with user profile.
        
        Args:
            user_profile: Dictionary containing user's name and preferences
        """
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.user_profile = user_profile
    
    def generate_introduction(self, ranked_articles: List) -> EmailIntroduction:
        """
        Generate a personalized email introduction based on ranked articles.
        
        Args:
            ranked_articles: List of ranked article dictionaries or objects
            
        Returns:
            EmailIntroduction object with greeting and introduction
        """
        user_name = self.user_profile.get('name', 'there')
        
        # Handle empty articles case
        if not ranked_articles:
            return EmailIntroduction(
                greeting=f"Hey {user_name}!",
                introduction="No articles were ranked today. Check back tomorrow for your personalized AI news digest!"
            )
        
        # Take top 10 articles for context
        top_articles = ranked_articles[:10]
        
        # Format article summaries for the LLM
        article_context = ""
        for i, article in enumerate(top_articles, 1):
            # Handle both dict and object formats
            if isinstance(article, dict):
                title = article.get('title', 'Untitled')
                score = article.get('relevance_score', 0)
            else:
                title = getattr(article, 'title', 'Untitled')
                score = getattr(article, 'relevance_score', 0)
            
            article_context += f"{i}. {title} (Score: {score:.1f})\n"
        
        # Get current date
        current_date = datetime.now().strftime('%B %d, %Y')
        
        # Construct prompt
        user_prompt = f"""Write a personalized email introduction for an AI news digest.

User Name: {user_name}
Date: {current_date}
Number of Articles: {len(top_articles)}

Top Articles Being Shared:
{article_context}

Create a warm greeting and introduction that previews these articles.
"""
        
        try:
            # Call OpenAI API with structured output
            response = self.client.responses.parse(
                model=self.model,
                instructions=EMAIL_PROMPT,
                temperature=0.7,
                input=user_prompt,
                text_format=EmailIntroduction
            )
            
            introduction = response.output_parsed
            
            # Post-processing: Ensure consistent greeting format
            if not introduction.greeting.startswith(f"Hey {user_name}"):
                # Force standard greeting for consistency
                introduction.greeting = f"Hey {user_name}!"
            
            return introduction
            
        except Exception as e:
            print(f"Error generating introduction: {e}")
            # Return fallback introduction
            return EmailIntroduction(
                greeting=f"Hey {user_name}!",
                introduction=f"Here's your personalized AI news digest for {current_date}. I've curated {len(top_articles)} articles based on your interests."
            )
    
    def create_email_digest(self, ranked_articles: List[dict], limit: int = 10) -> EmailDigest:
        """
        Create a complete email digest with introduction and articles.
        
        Args:
            ranked_articles: List of ranked article dictionaries
            limit: Maximum number of articles to include (default: 10)
            
        Returns:
            EmailDigest object
        """
        # Generate introduction
        introduction = self.generate_introduction(ranked_articles[:limit])
        
        return EmailDigest(
            introduction=introduction,
            ranked_articles=ranked_articles[:limit]
        )
    
    def create_email_digest_response(
        self,
        ranked_articles: List[RankedArticleDetail],
        total_ranked: int,
        limit: int = 10
    ) -> EmailDigestResponse:
        """
        Create a complete email digest response with all metadata.
        
        Args:
            ranked_articles: List of RankedArticleDetail objects
            total_ranked: Total number of articles that were ranked
            limit: Maximum number of articles to include (default: 10)
            
        Returns:
            EmailDigestResponse object with markdown export capability
        """
        # Generate introduction
        introduction = self.generate_introduction(ranked_articles[:limit])
        
        return EmailDigestResponse(
            introduction=introduction,
            articles=ranked_articles[:limit],
            total_ranked=total_ranked,
            top_n=min(limit, len(ranked_articles))
        )
