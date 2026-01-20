import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

PROMPT = """You are an Expert AI news analyst specializing in summarizing technical content.

Your role is to:
- Analyze technical articles, research papers, and video transcripts
- Create compelling, concise digests for AI professionals

Guidelines:
- Title: 5-10 words, compelling and specific
- Summary: 2-3 sentences capturing the essence
- Focus on actionable insights and practical implications
- Avoid marketing hype, fluff, and unnecessary jargon
- Highlight novel contributions or breakthroughs
- Include practical takeaways when relevant"""


class DigestOutput(BaseModel):
    title: str
    summary: str


class DigestAgent:
    def __init__(self):
        """Initialize DigestAgent with OpenAI client and model configuration."""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "gpt-4o-mini"
        self.system_prompt = PROMPT

    def generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]:
        """Generate a digest for given content.

        Args:
            title: The title of the article/video
            content: The content to summarize (will be truncated to 8000 chars)
            article_type: Type of content (e.g., 'youtube', 'openai', 'anthropic')

        Returns:
            DigestOutput with title and summary, or None if generation fails
        """
        user_prompt = f"Create a digest for this {article_type}: \n Title: {title} \n Content: {content[:8000]}"

        try:
            response = self.client.responses.parse(
                model=self.model,
                instructions=self.system_prompt,
                temperature=0.7,
                input=user_prompt,
                text_format=DigestOutput,
            )
            return response.output_parsed
        except Exception as e:
            print(f"Error generating digest: {e}")
            return None
