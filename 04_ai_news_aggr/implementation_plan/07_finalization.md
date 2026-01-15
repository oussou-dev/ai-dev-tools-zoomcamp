Prompt_25
```
# Task_1
Generate a utility script named `init_packages.py` at the root of the project.

# Goal
This script ensures that every subdirectory inside the `app/` folder contains an `__init__.py` file, making them proper Python packages.

# Logic
1.  Import `pathlib`.
2.  Define the root directory as the current directory.
3.  Target specific directories: `app`, `app/agents`, `app/database`, `app/profiles`, `app/scrapers`, `app/services`, `docker`.
4.  For each directory:
    - Check if it exists.
    - Check if `__init__.py` exists inside it.
    - If not, create an empty `__init__.py` file.
    - Print a message: "Created __init__.py in {path}" or "Already exists in {path}".

# Execution
Add `if __name__ == "__main__":` to run the logic immediately.
```

---

Prompt_26

```
# Task_2
Generate a comprehensive `README.md` file for the "AI News Aggregator" project.

# Content Requirements

1.  **Project Title & Description**:
    - Title: **AI News Aggregator**
    - Description: An automated pipeline that scrapes AI news (YouTube, OpenAI, Anthropic), generates summaries using LLMs, ranks them based on a personalized User Profile, and sends a daily email digest.

2.  **Architecture Diagram (Text-based)**:
    - Describe the flow: Scrapers -> PostgreSQL -> Digest Agent -> Curator Agent -> Email Agent.

3.  **Features**:
    - **Multi-Source Scraping**: YouTube Transcripts, Official Blogs (RSS).
    - **Intelligent Summarization**: Uses GPT-4o-mini to summarize technical content.
    - **Personalized Curation**: Ranks news based on `user_profile.py` interests.
    - **Daily Email**: Sends a beautifully formatted HTML newsletter.
    - **Robust Engineering**: Dockerized Database, Pydantic validation, Retry logic.
    - **Vibe Coding Ready**: Includes a full `implementation_plan` to recreate the project with AI.

4.  **Tech Stack**:
    - **Language**: Python 3.12+
    - **AI**: OpenAI API (GPT-4o/mini).
    - **Database**: PostgreSQL (via Docker).
    - **Libs**: SQLAlchemy, Pydantic, Feedparser, YouTube Transcript API.

5.  **Installation & Setup**:
    - **Prerequisites**: Docker, Python 3.12+, UV (or Pip).
    - **Step 1: Clone & Install**: `git clone ...`, `uv sync`.
    - **Step 2: Environment**: Copy `app/example.env` to `.env`. Configure Keys.
    - **Step 3: Database**: `docker-compose up -d`, then `python -m app.database.create_tables`.

6.  **Usage**:
    - **Run Pipeline**: `python main.py` (optional args: hours, top_n).
    - **Run Tests**: `pytest`.

7.  **Project Structure**:
    - Provide a simplified tree view of the `app/` folder.

8.  **🏗️ Developer Guide: Recreating with AI (New Section)**:
    - Add a detailed section explaining how to use the `implementation_plan/` folder.
    - Explain that this folder contains the exact prompts used to build the project.
    - **List the Execution Order**: Create a structured list (Phase 1 to Phase 8) mapping the Prompts (e.g., Prompt 01, Prompt 02) to the Files they generate, and identifying the critical manual actions (like `uv sync`, `docker up`, `python init_packages.py`) that must be performed between steps.
    - Mention that prompts are grouped by context files (e.g., `01_infra.md`).

# Style
- Use Markdown badges (Python, Docker, PostgreSQL).
- Keep it clean, professional, and easy to read.
```