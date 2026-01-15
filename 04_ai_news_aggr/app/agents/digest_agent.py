import os
from typing import Optional
from openai import OpenAI
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# System prompt defining the agent's role and guidelines
PROMPT = """You are an expert AI news analyst specializing in technical content summarization.

Your role is to summarize technical articles, research papers, and video content into concise, compelling digests.

Guidelines:
- Create a compelling title (5-10 words) that captures the essence of the content
- Write a 2-3 sentence summary that highlights the key insights and takeaways
- Focus on actionable insights and practical implications
- Avoid marketing fluff and promotional language
- Use clear, technical language appropriate for an expert audience
- Highlight novel contributions, breakthroughs, or unique perspectives
"""


class DigestOutput(BaseModel):
    """Output model for generated digests."""
    title: str
    summary: str


class DigestAgent:
    """Agent for generating concise digests from technical content using LLM."""
    
    def __init__(self):
        """Initialize the digest agent with OpenAI client."""
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
        self.system_prompt = PROMPT
    
    def generate_digest(
        self,
        title: str,
        content: str,
        article_type: str
    ) -> Optional[DigestOutput]:
        """
        Generate a digest for the given content using LLM.
        
        Args:
            title: Original title of the content
            content: Full content text (will be truncated to 8000 chars)
            article_type: Type of content (e.g., "youtube", "openai", "anthropic")
            
        Returns:
            DigestOutput object if successful, None otherwise
        """
        # Construct user prompt with content truncated to manage token limits
        user_prompt = f"""Create a digest for this {article_type}:

Title: {title}

Content: {content[:8000]}"""
        
        try:
            # Call OpenAI API with structured output
            response = self.client.responses.parse(
                model=self.model,
                instructions=self.system_prompt,
                temperature=0.7,
                input=user_prompt,
                text_format=DigestOutput
            )
            
            return response.output_parsed
            
        except Exception as e:
            print(f"Error generating digest: {e}")
            return None
