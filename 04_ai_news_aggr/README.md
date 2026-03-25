# 🤖 AI News Aggregator

> **🚨 Vibe Coding / Recreation Guide**
>
> This project was built using AI-assisted development ('Vibe Coding'). If you want to recreate it from scratch or understand the exact prompts used to build it, please refer to the **[Developer Guide (vibe_coding.md)](./vibe_coding.md)**.
>
> The `implementation_plan/` folder contains the complete "DNA" of the project—detailed specifications for each phase and component.

---

## 📖 About

A full-stack AI-powered news platform that scrapes, summarizes, and serves AI trends via a FastAPI backend and a Streamlit dashboard. Powered by OpenAI's GPT models and built with production-grade practices.

### Key Capabilities
- **Multi-Source Scraping**: Automatically fetches content from YouTube, OpenAI, and Anthropic
- **Smart Summarization**: Uses GPT-4o-mini to generate concise, actionable summaries
- **Intelligent Curation**: Ranks digests based on personalized user profiles
- **Interactive Dashboard**: Beautiful Streamlit UI for browsing and triggering pipelines
- **REST API**: Fully documented FastAPI backend with Swagger UI
- **Containerized**: Complete Docker Compose setup for one-command deployment

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  ┌─────────────┐      ┌──────────────┐    ┌──────────┐   │
│  │  Scrapers   │──→   │  PostgreSQL  │ ←──│  FastAPI │   │
│  │ (YT, OAI,   │      │   Database   │    │ Backend  │   │
│  │  Anthropic) │      └──────────────┘    └─-──┬─────┘   │
│  └─────────────┘                               │         │
│                                                │         │
│  ┌─────────────────────────────────────────--─-┴─┐       │
│  │                                               │       │
│  │        AI Agents (Digest, Curator, Email)     │       │
│  │               (run in background)             │       │
│  │                                               │       │
│  └──────────────────────────────────────────-─┬─-┘       │
│                                               │          │
│                                          ┌────▼────-─┐   │
│                                          │ Streamlit │   │
│                                          │ Frontend  │   │
│                                          └───────────┘   │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

**Data Flow**:
1. Scrapers fetch raw content from multiple sources
2. Data persists to PostgreSQL
3. Background services enrich content (transcripts, markdown, summaries)
4. AI agents rank and personalize digests
5. FastAPI exposes data via REST endpoints
6. Streamlit dashboard displays results and allows pipeline triggering

---

## ✨ Features

### 📰 Multi-Source Scraping
- **YouTube**: Extracts video metadata and auto-generated transcripts
- **OpenAI**: Fetches official news feed with category tagging
- **Anthropic**: Scrapes research papers and converts to markdown

### 🧠 Intelligent Processing
- **Digest Agent**: Summarizes articles/videos into 2-3 sentence digests
- **Curator Agent**: Ranks content based on personalized user profile
- **Email Agent**: Generates warm, personalized introduction and email formatting

### 🎯 User Personalization
- Customizable interest profiles (LLMs, RAG, ML systems, etc.)
- Preference settings (practical, research-focused, production-focus, etc.)
- Relevance scoring from 0-10

### 🌐 REST API
- `GET /health` - Health check
- `POST /pipeline/run` - Trigger full pipeline in background
- `GET /digests` - Fetch recent digests with pagination
- Interactive Swagger docs at `/docs`

### 🎨 Interactive Dashboard
- Real-time backend status indicator
- One-click pipeline trigger with visual feedback
- Beautiful card-based digest display
- Article source icons (🎥 YouTube, 🤖 OpenAI, 🧠 Anthropic)
- Published date and direct links to original content

### 🐳 Containerized Stack
- Single `docker-compose up --build` command
- PostgreSQL 17 with persistent volumes
- FastAPI backend service
- Streamlit frontend service
- Automatic service health checks and dependencies

---

## 🚀 Quick Start

### Prerequisites
- **Docker & Docker Compose** (recommended)
- **Python 3.12+** (for local development)
- **OpenAI API Key** (get one at [platform.openai.com](https://platform.openai.com))

### 🎯 The Magic Command

```bash
# Step 1: Clone the repository
git clone <repo-url>
cd 04_ai_news_aggr

# Step 2: Set up environment
cp app/example.env .env
# Edit .env and fill in:
#   - OPENAI_API_KEY=<your-key>
#   - ANTHROPIC_API_KEY=<your-key> (optional)
#   - MY_EMAIL=<your-email>
#   - APP_PASSWORD=<your-app-password>

# Step 3: Run the stack
docker-compose up --build
```

### 📱 Access the Application

- **Frontend Dashboard**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **API Health**: http://localhost:8000/health

---

## 💻 Local Development

### Setup

```bash
# Install dependencies
uv sync

# Create and initialize database
python -m app.database.create_tables

# (Optional) Set up pre-commit hooks
pip install pre-commit
```

### Running Components

```bash
# Terminal 1: Start database (requires Docker)
docker-compose -f docker/docker-compose.yml up postgres

# Terminal 2: Start FastAPI backend
uv run uvicorn app.api.main:app --reload

# Terminal 3: Start Streamlit frontend
uv run streamlit run app/frontend/main.py

# Terminal 4 (optional): Run the CLI pipeline
uv run python main.py

# Terminal 5 (optional): Run tests
uv run pytest tests/ -v
```

### Environment Variables

Copy `app/example.env` to `.env` and configure:

```bash
# API Keys
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...

# Email Configuration
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-specific-password

# Database Configuration
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Frontend
API_URL=http://localhost:8000
```

---

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test module
uv run pytest tests/test_api.py -v

# Watch mode
uv run pytest-watch tests/
```

**Test Coverage**:
- ✅ Unit tests for database operations
- ✅ Integration tests for pipeline flow (with mocked APIs)
- ✅ API endpoint tests with real database
- ✅ Full HTTP request-response validation

---

## 📦 Tech Stack

![Python](https://img.shields.io/badge/Python-3.12+-3776ab?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110+-009688?style=flat&logo=fastapi&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-ff0000?style=flat&logo=streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-336791?style=flat&logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Latest-2496ed?style=flat&logo=docker&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0+-d32f2f?style=flat)

### Backend
- **FastAPI** - Modern async web framework
- **SQLAlchemy** - ORM for database operations
- **Pydantic** - Data validation and serialization
- **OpenAI SDK** - GPT-4o-mini for summarization and curation
- **youtube-transcript-api** - YouTube transcript extraction
- **feedparser** - RSS feed parsing
- **docling** - Document to markdown conversion

### Frontend
- **Streamlit** - Interactive web dashboard
- **Requests** - HTTP client for API communication

### Infrastructure
- **PostgreSQL 17** - Primary data store
- **Docker** - Containerization
- **GitHub Actions** - CI/CD automation
- **Pytest** - Testing framework

---

## 📁 Project Structure

```
04_ai_news_aggr/
├── app/
│   ├── api/                 # FastAPI backend
│   ├── agents/              # AI agents (digest, curator, email)
│   ├── database/            # ORM models & repository
│   ├── frontend/            # Streamlit dashboard
│   ├── profiles/            # User profile configuration
│   ├── scrapers/            # Content scrapers (YouTube, OpenAI, Anthropic)
│   ├── services/            # Background processors
│   ├── config.py            # Configuration constants
│   ├── daily_runner.py      # Daily pipeline orchestrator
│   ├── runner.py            # Scraper registry
│   └── schemas.py           # Pydantic DTOs
├── tests/                   # Test suites
├── docker/
│   └── docker-compose.yml   # Service orchestration
├── .github/workflows/
│   └── ci.yml               # GitHub Actions CI/CD
├── Dockerfile               # Container image definition
├── main.py                  # CLI entry point
├── init_packages.py         # Package initialization script
├── pyproject.toml           # Project metadata & dependencies
└── README.md                # This file
```

---

## 🔄 Pipeline Workflow

### Manual Trigger (CLI)
```bash
# Run with defaults (24 hours, top 10 articles)
uv run python main.py

# Custom parameters
uv run python main.py 48 5  # 48 hours, top 5 articles
```

### API Trigger
```bash
curl -X POST http://localhost:8000/pipeline/run?hours=24&top_n=10
```

### Dashboard Trigger
Click the "🚀 Run Pipeline" button in the Streamlit sidebar.

### Pipeline Steps
1. **Scraping** - Fetch from YouTube, OpenAI, Anthropic
2. **Processing** - Extract transcripts, convert to markdown
3. **Summarization** - Generate digests using GPT-4o-mini
4. **Curation** - Rank by relevance (0-10)
5. **Email** - Format and send personalized digest

---

## 🛠️ Development Workflows

### Adding a New Scraper
1. Create `app/scrapers/new_source.py` with Pydantic models
2. Implement scraper class with `get_articles()` method
3. Add to `app/runner.py`
4. Update `app/services/process_*.py` if needed

### Customizing User Profile
Edit `app/profiles/user_profile.py`:
- Modify interests list
- Adjust preferences (practical, research-focused, etc.)
- Update expertise level

### Extending Agents
Modify agent classes in `app/agents/`:
- `digest_agent.py` - Change summarization prompt
- `curator_agent.py` - Adjust ranking criteria
- `email_agent.py` - Customize email template

---

## 🚨 Troubleshooting

### API Connection Issues
```
❌ Cannot connect to backend API. Is it running?
```
**Solution**: Ensure FastAPI is running on port 8000
```bash
uv run uvicorn app.api.main:app --reload
```

### Database Connection Errors
```
Could not connect to PostgreSQL
```
**Solution**: Check `.env` file and ensure postgres container is healthy
```bash
docker-compose ps
docker-compose logs postgres
```

### OpenAI API Errors
```
OpenAI API Key not configured
```
**Solution**: Set `OPENAI_API_KEY` in `.env` and restart services

### Port Already in Use
```
Port 8000 already in use
```
**Solution**: Change port or kill the process using it
```bash
# Change in app/api/main.py or use:
uv run uvicorn app.api.main:app --port 8001
```

---

## 📊 Performance

- **Scraping**: ~10-30 seconds depending on feed size
- **Transcript Processing**: ~2-5 seconds per video
- **Summarization**: ~1-2 seconds per article (GPT-4o-mini)
- **Curation**: ~3-5 seconds for 50 digests
- **Total Pipeline**: ~60-120 seconds

---

## 📝 License

MIT License - See LICENSE file for details

---

## 👥 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🙋 Support

For issues, questions, or suggestions:
- Open an issue on GitHub
- Check existing documentation in `implementation_plan/`
- Review the `vibe_coding.md` for recreation instructions

---

**Built with ❤️ using AI-assisted development**
