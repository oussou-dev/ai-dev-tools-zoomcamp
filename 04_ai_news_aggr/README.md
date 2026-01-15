# AI News Aggregator

![Python](https://img.shields.io/badge/python-3.12+-blue.svg)
![Docker](https://img.shields.io/badge/docker-enabled-blue.svg)
![PostgreSQL](https://img.shields.io/badge/postgresql-17-316192.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg)

An automated pipeline that scrapes AI news from YouTube, OpenAI, and Anthropic, generates intelligent summaries using LLMs, ranks them based on a personalized user profile, and sends a beautifully formatted daily email digest.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         DATA COLLECTION                          │
├─────────────────────────────────────────────────────────────────┤
│  YouTube Scraper  │  OpenAI Scraper  │  Anthropic Scraper       │
│  (RSS + API)      │  (RSS Feed)      │  (RSS + Docling)         │
└──────────┬────────┴──────────┬───────┴──────────┬───────────────┘
           │                   │                   │
           └───────────────────┼───────────────────┘
                               ↓
                    ┌──────────────────────┐
                    │   PostgreSQL DB      │
                    │  (4 Tables)          │
                    └──────────┬───────────┘
                               ↓
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ↓                   ↓                   ↓
    ┌─────────────┐   ┌──────────────┐   ┌──────────────┐
    │  Digest     │   │  Curator     │   │  Email       │
    │  Agent      │→  │  Agent       │→  │  Agent       │
    │ (GPT-4o-mini)│   │ (GPT-4.1)    │   │(GPT-4o-mini) │
    └─────────────┘   └──────────────┘   └──────┬───────┘
                                                 ↓
                                        ┌────────────────┐
                                        │  HTML Email    │
                                        │  Newsletter    │
                                        └────────────────┘
```

**Flow:**
1. **Scrapers** → Fetch content from multiple sources
2. **PostgreSQL** → Store raw data and processing state
3. **Digest Agent** → Generate AI summaries (GPT-4o-mini)
4. **Curator Agent** → Rank by user interests (GPT-4.1)
5. **Email Agent** → Format and send personalized newsletter

## ✨ Features

- **🔍 Multi-Source Scraping**: Automatically fetches content from:
  - YouTube video transcripts
  - OpenAI official blog (RSS)
  - Anthropic blog (News, Research, Engineering via RSS)

- **🤖 Intelligent Summarization**: Uses GPT-4o-mini to generate concise, technical summaries of articles and videos

- **🎯 Personalized Curation**: Ranks news based on your specific interests, expertise level, and preferences defined in `user_profile.py`

- **📧 Daily Email Digest**: Sends beautifully formatted HTML newsletters with top-ranked articles

- **🛠️ Robust Engineering**:
  - Dockerized PostgreSQL database
  - Pydantic validation for data integrity
  - Comprehensive error handling and retry logic
  - Structured logging throughout the pipeline

- **🚀 Vibe Coding Ready**: Includes a complete `implementation_plan/` folder with exact prompts to recreate the entire project with AI assistance

## 🔧 Tech Stack

- **Language**: Python 3.12+
- **AI**: OpenAI API (GPT-4.1, GPT-4o-mini)
- **Database**: PostgreSQL 17 (via Docker)
- **Key Libraries**:
  - `SQLAlchemy` - ORM and database management
  - `Pydantic` - Data validation
  - `feedparser` - RSS feed parsing
  - `youtube-transcript-api` - YouTube transcript extraction
  - `docling` - Web page to Markdown conversion
  - `markdown` - Markdown to HTML conversion

## 📦 Installation & Setup

### Prerequisites

- Docker and Docker Compose
- Python 3.12+
- UV (recommended) or pip

### Step 1: Clone & Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd ai_news_aggr

# Install dependencies with UV (recommended)
uv sync

# Or with pip
pip install -e .
```

### Step 2: Environment Configuration

```bash
# Copy the example environment file
cp app/example.env app/.env

# Edit app/.env and configure your secrets:
# - OPENAI_API_KEY (required)
# - ANTHROPIC_API_KEY (optional)
# - MY_EMAIL (for receiving digests)
# - APP_PASSWORD (Gmail app password)
# - Proxy credentials (optional)
```

### Step 3: Initialize Python Packages

```bash
# Ensure all directories have __init__.py files
python init_packages.py
```

### Step 4: Start Database

```bash
# Start PostgreSQL container
docker compose -f docker/docker-compose.yml up -d

# Create database tables
python app/database/create_tables.py
```

## 🚀 Usage

### Run the Complete Pipeline

```bash
# Run with defaults (last 24 hours, top 10 articles)
python main.py

# Look back 48 hours, send top 15 articles
python main.py 48 15

# Custom: last 72 hours, top 20 articles
python main.py 72 20
```

### Run Individual Services

```bash
# Run scrapers only
python -m app.runner

# Process YouTube transcripts
python -m app.services.process_youtube

# Process Anthropic markdown
python -m app.services.process_anthropic

# Generate digests
python -m app.services.process_digest

# Test email service
python -m app.services.email
```

### Run Tests

```bash
pytest
```

## 📁 Project Structure

```
ai_news_aggr/
├── app/
│   ├── agents/              # AI agents (Digest, Curator, Email)
│   │   ├── curator_agent.py
│   │   ├── digest_agent.py
│   │   └── email_agent.py
│   ├── database/            # Database layer
│   │   ├── connection.py
│   │   ├── create_tables.py
│   │   ├── models.py
│   │   └── repository.py
│   ├── profiles/            # User profile configuration
│   │   └── user_profile.py
│   ├── scrapers/            # Data collection
│   │   ├── anthropic.py
│   │   ├── openai.py
│   │   └── youtube.py
│   ├── services/            # Processing services
│   │   ├── email.py
│   │   ├── process_anthropic.py
│   │   ├── process_curator.py
│   │   ├── process_digest.py
│   │   ├── process_email.py
│   │   └── process_youtube.py
│   ├── config.py            # Application configuration
│   ├── daily_runner.py      # Daily pipeline orchestrator
│   ├── example.env          # Environment template
│   └── runner.py            # Scraper registry
├── docker/
│   └── docker-compose.yml   # Database container definition
├── implementation_plan/     # AI recreation prompts
│   ├── 00_ROADMAP.md
│   ├── 01_infra.md
│   ├── 02_database.md
│   ├── 03_scrapers.md
│   ├── 04_agents.md
│   ├── 05_services.md
│   ├── 06_runners.md
│   ├── 07_finalization.md
│   └── 08_tests.md
├── init_packages.py         # Package initialization utility
├── main.py                  # CLI entry point
├── pyproject.toml           # Project metadata & dependencies
└── README.md                # This file
```

## 🏗️ Developer Guide: Recreating with AI

This project includes a complete `implementation_plan/` folder containing the **exact prompts** used to build the entire application. You can recreate or extend this project using an AI coding assistant by following the prompts in order.

### How It Works

Each markdown file in `implementation_plan/` contains numbered prompts (e.g., `Prompt_01`, `Prompt_02`) with:
- **Task description**: What to build
- **Technical requirements**: Dependencies, APIs, data models
- **Code specifications**: Exact implementation details

### Execution Order

Follow this phase-by-phase execution order:

#### **Phase 1: Infrastructure Setup** (`01_infra.md`)
- **Prompt_01** → Generate `pyproject.toml`
- **Prompt_02** → Generate `docker/docker-compose.yml`
- **Prompt_03** → Generate `app/example.env`
- **Manual Action**: Run `docker compose -f docker/docker-compose.yml up -d`

#### **Phase 2: Database Layer** (`02_database.md`)
- **Prompt_04** → Generate `app/database/connection.py`
- **Prompt_05** → Generate `app/database/models.py`
- **Prompt_06** → Generate `app/database/repository.py`
- **Prompt_07** → Generate `app/database/create_tables.py`
- **Manual Action**: Run `python app/database/create_tables.py`

#### **Phase 3: Scrapers** (`03_scrapers.md`)
- **Prompt_08** → Generate `app/config.py`
- **Prompt_09** → Generate `app/scrapers/youtube.py`
- **Prompt_10** → Generate `app/scrapers/openai.py`
- **Prompt_11** → Generate `app/scrapers/anthropic.py`

#### **Phase 4: AI Agents** (`04_agents.md`)
- **Prompt_12** → Generate `app/profiles/user_profile.py`
- **Prompt_13** → Generate `app/agents/digest_agent.py`
- **Prompt_14** → Generate `app/agents/curator_agent.py`
- **Prompt_15** → Generate `app/agents/email_agent.py`

#### **Phase 5: Services** (`05_services.md`)
- **Prompt_16** → Generate `app/services/email.py`
- **Prompt_17** → Generate `app/services/process_youtube.py`
- **Prompt_18** → Generate `app/services/process_anthropic.py`
- **Prompt_19** → Generate `app/services/process_digest.py`
- **Prompt_20** → Generate `app/services/process_curator.py`
- **Prompt_21** → Generate `app/services/process_email.py`

#### **Phase 6: Runners** (`06_runners.md`)
- **Prompt_22** → Generate `app/runner.py`
- **Prompt_23** → Generate `app/daily_runner.py`
- **Prompt_24** → Generate `main.py`

#### **Phase 7: Finalization** (`07_finalization.md`)
- **Prompt_25** → Generate `init_packages.py`
- **Manual Action**: Run `python init_packages.py`
- **Prompt_26** → Generate `README.md` (this file)

#### **Phase 8: Testing** (`08_tests.md`)
- Follow prompts to generate test files

### Critical Manual Steps

Between AI-generated code, you must perform these actions:

1. **After Phase 1**: Start database with `docker compose up -d`
2. **After Prompt_07**: Create tables with `python app/database/create_tables.py`
3. **After Phase 7**: Initialize packages with `python init_packages.py`
4. **Environment Setup**: Configure `app/.env` with API keys before running

### Using the Prompts

Simply copy-paste each prompt into your AI assistant (e.g., Cursor, GitHub Copilot, Claude) in the order specified. The prompts are self-contained and include all necessary context.

## 📝 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- Built as part of the AI Dev Tools Zoomcamp
- Inspired by modern AI engineering practices and vibe coding workflows

---

**Happy coding! 🚀** If you have questions or improvements, feel free to open an issue or contribute to the project.
