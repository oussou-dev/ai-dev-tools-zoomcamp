Prompt_12
```
# Task_1
Generate the file `app/profiles/user_profile.py`.
This file contains the configuration dictionary defining the user's interests for the AI Curator.

# Content
Create a dictionary constant named `USER_PROFILE` with the following specific data:

- **Name:** "Ouskä"
- **Title:** "AI Engineer, Data Engineer"
- **Background:** "AI/Data engineer with deep interest in practical AI applications, research breakthroughs and production-ready systems"
- **Interests (List):**
  - "Large Language Models (LLMs) and their applications"
  - "Retrieval-Augmented Generation (RAG) systems"
  - "AI agent architectures and frameworks"
  - "Multimodal AI and vision-language models"
  - "AI safety and alignment research"
  - "Production AI systems and MLOps"
  - "Production Gen AI systems and LLMOps"
  - "Real-world AI applications and case studies"
  - "Technical tutorials and implementation guides"
  - "Research papers with practical implications"
  - "AI infrastructure and scaling challenges"
  - "No-code, low-code & AI tools"
- **Preferences (Dict):**
  - prefer_practical: True
  - prefer_technical_depth: True
  - prefer_research_breakthroughs: True
  - prefer_production_focus: True
  - avoid_marketing_hype: True
- **Expertise Level:** "Intermediate"

# Style Guide
- Ensure it is a valid Python dictionary exported as a constant.

```

---

Prompt_13

```
# Task_2
Generate the file `app/agents/digest_agent.py`.
This agent uses an LLM to summarize technical content (articles/transcripts) into concise digests.

# Technical Stack
- **Library:** `openai`, `pydantic`, `dotenv`.
- **Model:** Uses `gpt-4o-mini` (optimized for speed/cost).

# Code Requirements

1.  **Imports**:
    - `os`, `typing.Optional`.
    - `openai.OpenAI`.
    - `pydantic.BaseModel`.
    - `dotenv.load_dotenv` (call immediately).

2.  **Data Models**:
    - `DigestOutput(BaseModel)`: Fields `title` (str), `summary` (str).

3.  **Constants**:
    - `PROMPT`: A multi-line string defining the "Expert AI news analyst" persona.
      - Role: Summarize technical articles, research papers, and video content.
      - Guidelines: Compelling title (5-10 words), 2-3 sentence summary, focus on actionable insights, avoid fluff.

4.  **Class `DigestAgent`**:
    - **`__init__(self)`**:
        - Initialize `self.client` using `OpenAI` and `OPENAI_API_KEY`.
        - Set `self.model = "gpt-4o-mini"`.
        - Set `self.system_prompt = PROMPT`.

    - **`generate_digest(self, title: str, content: str, article_type: str) -> Optional[DigestOutput]`**:
        - **Input Processing**: Construct `user_prompt` using the format: "Create a digest for this {article_type}: \n Title: {title} \n Content: {content[:8000]}".
        - **Important**: Note the slicing `[:8000]` on content to manage token limits.
        - **API Call**:
            - Use a `try/except` block.
            - Call `self.client.responses.parse(...)`.
            - Args: `model`, `instructions` (system_prompt), `temperature=0.7`, `input` (user_prompt), `text_format=DigestOutput`.
            - Return `response.output_parsed`.
        - **Error Handling**: Print error and return `None` on exception.

# Style Guide
- Maintain the specific API call syntax (`client.responses.parse`) as requested.
```

---

Prompt_14

```
# Task_3
Generate the file `app/agents/curator_agent.py`.
This agent acts as an expert news curator, ranking a list of summaries based on a specific User Profile.

# Technical Stack
- **Library:** `openai` (for the Client), `pydantic`, `dotenv`.
- **Model:** Uses `gpt-4.1` (or the specific model defined in code).

# Code Requirements

1.  **Imports**:
    - `os`, `typing.List`.
    - `openai.OpenAI`.
    - `pydantic.BaseModel`, `pydantic.Field`.
    - `dotenv.load_dotenv` (call it immediately).

2.  **Data Models (Pydantic)**:
    - **`RankedArticle`**:
        - `digest_id`: str (description="The ID of the digest (article_type:article_id)").
        - `relevance_score`: float (0.0 to 10.0).
        - `rank`: int (ge=1).
        - `reasoning`: str.
    - **`RankedDigestList`**:
        - `articles`: List[RankedArticle].

3.  **Constants**:
    - **`CURATOR_PROMPT`**: Define a multi-line string containing the persona and scoring guidelines.
      - Role: "Expert AI news curator specializing in personalized content ranking".
      - Criteria: Relevance, Technical depth, Novelty, Alignment, Actionability.
      - Scoring Guidelines: 9.0-10.0 (High), 7.0-8.9 (Very), 5.0-6.9 (Moderate), etc.

4.  **Class `CuratorAgent`**:
    - **`__init__(self, user_profile: dict)`**:
        - Initialize `self.client = OpenAI(...)` using `OPENAI_API_KEY`.
        - Set `self.model = "gpt-4.1"`.
        - Store `user_profile`.
        - Set `self.system_prompt` by calling `_build_system_prompt()`.

    - **`_build_system_prompt(self) -> str`**:
        - Format the `user_profile` dictionary (keys: name, background, expertise_level, interests, preferences) into a readable string.
        - Combine `CURATOR_PROMPT` with this user profile data.

    - **`rank_digests(self, digests: List[dict]) -> List[RankedArticle]`**:
        - Return empty list if input is empty.
        - Format the input `digests` list into a single string `digest_list` (Format: "ID: ... Title: ... Summary: ... Type: ...").
        - **API Call Logic**:
            - Construct `user_prompt` asking to rank the digests.
            - Wrap in a `try/except` block.
            - **Important:** Use the specific syntax `self.client.responses.parse(...)`.
            - Arguments: `model`, `instructions` (system_prompt), `temperature=0.3`, `input` (user_prompt), `text_format=RankedDigestList`.
            - Parse the response (`response.output_parsed`) and return the list of articles.
            - Return empty list on Exception.

# Style Guide
- Ensure the API call strictly follows the `client.responses.parse` signature as requested, not the standard `chat.completions.create`.
```

---

Prompt_15

```
# Task_4
Generate the file `app/agents/email_agent.py`.
This agent generates the personalized introduction and structures the final email content.

# Technical Stack
- **Library:** `openai`, `pydantic` (`BaseModel`, `Field`), `dotenv`.
- **Model:** Uses `gpt-4o-mini`.

# Code Requirements

1.  **Imports**: Standard imports plus `datetime` from `datetime`.

2.  **Data Models (Pydantic)**:
    - **`EmailIntroduction`**: `greeting` (str), `introduction` (str).
    - **`RankedArticleDetail`**: `digest_id`, `rank`, `relevance_score`, `title`, `summary`, `url`, `article_type`, `reasoning` (Optional).
    - **`EmailDigestResponse`**:
        - Fields: `introduction` (EmailIntroduction), `articles` (List[RankedArticleDetail]), `total_ranked` (int), `top_n` (int).
        - **Method**: `to_markdown(self) -> str`.
            - Logic: formatting the greeting, intro, and iterating through articles to create a Markdown string with headers, summaries, and links ("Read more →"). Separators: `---`.
    - **`EmailDigest`**: `introduction` (EmailIntroduction), `ranked_articles` (List[dict]).

3.  **Constants**:
    - **`EMAIL_PROMPT`**: Persona definition for an "expert email writer".
      - Role: Write a warm, professional introduction for a daily AI news digest.
      - Requirements: Greet by name, include date, preview top 10 articles.

4.  **Class `EmailAgent`**:
    - **`__init__(self, user_profile: dict)`**:
        - Initialize `self.client` (OpenAI), `self.model` ("gpt-4o-mini"), and `self.user_profile`.

    - **`generate_introduction(self, ranked_articles: List) -> EmailIntroduction`**:
        - **Handle Empty**: If no articles, return a generic "No articles were ranked today" intro.
        - **Prepare Context**: Take top 10 articles. Format a string listing Title + Score for the LLM context.
        - **API Call**:
            - Construct prompt with User Name, Date, and Article Summaries.
            - Call `self.client.responses.parse` with `EmailIntroduction` format.
        - **Post-Processing**: Check if `greeting` starts with `f"Hey {name}"`. If not, force overwrite it with a standard greeting (consistency check).
        - **Error Handling**: Return a fallback `EmailIntroduction` on exception.

    - **`create_email_digest(self, ranked_articles: List[dict], limit: int = 10) -> EmailDigest`**:
        - Wrapper that calls `generate_introduction` and returns `EmailDigest` object.

    - **`create_email_digest_response(self, ranked_articles: List[RankedArticleDetail], total_ranked: int, limit: int = 10) -> EmailDigestResponse`**:
        - Wrapper that calls `generate_introduction` and returns `EmailDigestResponse` object.

# Style Guide
- Ensure `to_markdown` produces clean, readable markdown.
- Use `datetime.now().strftime('%B %d, %Y')` for dates.
```
