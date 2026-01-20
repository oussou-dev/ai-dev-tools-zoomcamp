# 🏠 Local Deployment Guide

Complete guide to run the **AI News Aggregator** locally using Docker Compose.

---

## 📋 Prerequisites

- Docker installed (https://www.docker.com/products/docker-desktop)
- Docker Compose installed
- Git installed
- 4GB RAM minimum
- Environment variables configured

---

## **Step 1: Clone Repository**

```bash
# Clone the repo
git clone https://github.com/your-username/ai-news-aggregator.git
cd 04_ai_news_aggr
```

---

## **Step 2: Configure Environment Variables**

```bash
# Copy example environment file
cp app/example.env .env

# Edit .env and add your keys
# nano .env  or  code .env

# Required variables:
OPENAI_API_KEY=sk-xxx...
ANTHROPIC_API_KEY=claude-xxx...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password

# Database (default values usually fine):
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
```

---

## **Step 3: Build and Start Services**

### Option A: Full Stack (Recommended)

Start all services with one command:

```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up -d --build
```

This starts:
- 🐘 PostgreSQL database (port 5432)
- 🔌 FastAPI backend (port 8000)
- 🎨 Streamlit frontend (port 8501)

### Option B: Start Individual Components

```bash
# Start only database
docker-compose up postgres -d

# Start backend
docker-compose up backend -d

# Start frontend
docker-compose up frontend -d

# View all running containers
docker-compose ps
```

---

## **Step 4: Access Services**

### Frontend Dashboard
```bash
# Open in browser
http://localhost:8501

# Should show:
# ✅ 🟢 Backend Status: Online
# 🚀 Run Pipeline button
# News feed
```

### Backend API
```bash
# Health check
curl http://localhost:8000/health
# Response: {"status": "ok"}

# API Documentation
http://localhost:8000/docs

# View available endpoints
http://localhost:8000/redoc
```

### Database
```bash
# Connect to database directly
psql -h localhost -U postgres -d ai_news_aggregator

# Or use pgAdmin (optional)
docker-compose up pgadmin -d
# Access: http://localhost:5050
```

---

## **Step 5: Verify Deployment**

### Check Container Logs

```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Follow logs in real-time
docker-compose logs --follow backend
```

### Check Health

```bash
# Test backend API
curl -X GET http://localhost:8000/health

# Test database connection
docker-compose exec backend python -c "from app.database.connection import engine; print(engine)"

# Check frontend connection
curl -X GET http://localhost:8501 | head -20
```

---

## **Step 6: Run the Pipeline**

### Via API
```bash
# Trigger pipeline
curl -X POST http://localhost:8000/pipeline/run?hours=24&top_n=10

# Or with custom parameters
curl -X POST "http://localhost:8000/pipeline/run?hours=48&top_n=5"
```

### Via CLI
```bash
# Run inside container
docker-compose exec backend python main.py

# Or with parameters
docker-compose exec backend python main.py 48 5
```

### Via Dashboard
1. Open http://localhost:8501
2. Click **"🚀 Run Pipeline"** button
3. Watch sidebar for progress: "Agents are working..."
4. Refresh feed to see digests

---

## **Step 7: Develop Locally**

### Code Changes Auto-Reload

```bash
# Backend auto-reloads with --reload flag (already configured)
docker-compose up backend -d

# Make changes to Python files
# Changes apply automatically within 1-2 seconds

# Frontend hot-reloads automatically (Streamlit feature)
# Make changes to app/frontend/main.py
# Refresh browser to see changes
```

### Database Initialization

```bash
# Create tables
docker-compose exec backend python -m app.database.create_tables

# Or via Python
docker-compose exec backend python -c "from app.database.models import Base; from app.database.connection import engine; Base.metadata.create_all(engine)"
```

---

## **Step 8: Run Tests Locally**

```bash
# Run all tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest tests/test_api.py

# Run with verbose output
docker-compose exec backend pytest -v

# Run with coverage
docker-compose exec backend pytest --cov=app

# Watch mode (requires pytest-watch)
docker-compose exec backend pytest-watch
```

---

## **Quick Reference: Local Architecture**

```
┌─────────────────────────────────────────────┐
│         Local Docker Compose Stack          │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐    ┌──────────────┐     │
│  │  PostgreSQL  │ ←──│  FastAPI     │     │
│  │  Database    │    │  Backend     │     │
│  │ (port 5432)  │    │ (port 8000)  │     │
│  └──────────────┘    └──────┬───────┘     │
│                             │             │
│                     ┌───────▼────────┐   │
│                     │  Streamlit     │   │
│                     │  Frontend      │   │
│                     │ (port 8501)    │   │
│                     └────────────────┘   │
│                                             │
└─────────────────────────────────────────────┘

         ↓ (Local Access)
    http://localhost:8501 (Frontend)
    http://localhost:8000 (Backend)
    localhost:5432 (Database)
```

---

## **Troubleshooting**

### ❌ Port Already in Use

```bash
# Find process using port
lsof -i :8000  # Backend
lsof -i :8501  # Frontend
lsof -i :5432  # Database

# Kill process
kill -9 <PID>

# Or change port in docker-compose.yml
```

### ❌ Database Connection Error

```bash
# Check if postgres is running
docker-compose ps postgres

# View postgres logs
docker-compose logs postgres

# Reset database
docker-compose down -v  # Remove volumes
docker-compose up postgres -d
```

### ❌ API Shows "Cannot connect"

```bash
# Check if backend is running
docker-compose ps backend

# Check backend logs
docker-compose logs backend

# Restart backend
docker-compose restart backend
```

### ❌ Out of Memory

```bash
# Check Docker resources
docker stats

# Increase Docker memory allocation
# Docker Desktop → Preferences → Resources → Memory (increase GB)

# Or restart services with less memory
docker-compose down
docker-compose up --build
```

### ❌ Module Not Found Error

```bash
# Rebuild containers
docker-compose build --no-cache

# Restart services
docker-compose up --build
```

---

## **Development Workflow**

### 1. **Create Feature Branch**
```bash
git checkout -b feature/new-feature
```

### 2. **Make Code Changes**
```bash
# Edit files locally
# Docker will auto-reload
# Refresh browser to see changes
```

### 3. **Run Tests**
```bash
docker-compose exec backend pytest tests/ -v
```

### 4. **Test Pipeline**
```bash
# Via dashboard or API
curl -X POST http://localhost:8000/pipeline/run?hours=24&top_n=5
```

### 5. **Commit and Push**
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

---

## **Useful Docker Compose Commands**

```bash
# Start services
docker-compose up                 # Foreground
docker-compose up -d              # Background
docker-compose up --build         # Rebuild images

# Stop services
docker-compose stop               # Gracefully stop
docker-compose down               # Stop and remove containers
docker-compose down -v            # Stop and remove volumes (clean slate)

# View services
docker-compose ps                 # List running containers
docker-compose logs -f            # Follow logs
docker-compose config             # Show configuration

# Execute commands
docker-compose exec backend bash  # Access container shell
docker-compose exec backend python -c "..."  # Run Python command
docker-compose run --rm backend pytest  # Run one-off command

# Database
docker-compose exec postgres psql -U postgres -d ai_news_aggregator  # Connect to DB

# Networking
docker-compose exec backend curl http://frontend:8501  # Services communicate internally

# Health checks
docker-compose ps                 # Shows health status
```

---

## **Local Environment Variables**

### **Required (.env file)**
```
OPENAI_API_KEY=sk-xxx...
ANTHROPIC_API_KEY=claude-xxx...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
```

### **Database (auto-configured)**
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=localhost (or 'postgres' inside containers)
POSTGRES_PORT=5432
```

### **API Communication (auto-configured)**
```
API_URL=http://backend:8000 (inside containers)
API_URL=http://localhost:8000 (from host machine)
```

---

## **Performance Tips**

### 1. **Use Named Volumes for Database**
```yaml
# In docker-compose.yml
volumes:
  postgres_data:
    driver: local
```

### 2. **Limit Log Output**
```bash
# Don't keep too many old logs
docker system prune -a --volumes
```

### 3. **Use `.dockerignore`**
Speeds up builds by excluding unnecessary files:
```
.git
.env.local
__pycache__
.pytest_cache
.venv
```

### 4. **Multi-Stage Builds**
Use smaller base images and multi-stage Dockerfiles to reduce image size.

---

## **Accessing Container Shell**

```bash
# Access backend container
docker-compose exec backend bash

# Access database container
docker-compose exec postgres bash

# Run Python interactively
docker-compose exec backend python

# Example: Check database contents
docker-compose exec backend python << 'EOF'
from app.database.repository import Repository
repo = Repository()
digests = repo.get_recent_digests(hours=1000)
print(f"Total digests: {len(digests)}")
EOF
```

---

## **Next Steps**

After successful local deployment:

1. ✅ **Verify all services running** - `docker-compose ps`
2. ✅ **Test backend API** - `curl http://localhost:8000/health`
3. ✅ **Access frontend** - Open http://localhost:8501
4. ✅ **Run pipeline** - Click "🚀 Run Pipeline" button
5. ✅ **Check digests** - Should populate in 1-2 minutes
6. ✅ **View logs** - `docker-compose logs -f`

---

## **Stop Services**

```bash
# Stop all services (keeps data)
docker-compose stop

# Stop and remove containers (keeps data)
docker-compose down

# Stop, remove containers, and delete volumes (CLEAN SLATE)
docker-compose down -v

# Remove everything including images
docker-compose down -v --rmi all
```

---

## **Production Deployment**

Once you're happy with local development:

1. Read the platform-specific deployment guides:
   - 🚂 [Railway Deployment](deployment_guide_railway.md)
   - 🎨 [Render Deployment](deployment_guide_render.md)
   - ☁️ [AWS Deployment](deployment_guide_aws.md)
   - 🔵 [Google Cloud Deployment](deployment_guide_gcp.md)
   - 🔷 [Azure Deployment](deployment_guide_azure.md)
   - 🟣 [Heroku Deployment](deployment_guide_heroku.md)

2. Choose a platform and follow the deployment steps

3. Set environment variables on the cloud platform

4. Deploy your application

---

## **Need Help?**

If you get stuck:

1. **Check logs**: `docker-compose logs -f service-name`
2. **Check running services**: `docker-compose ps`
3. **Verify environment**: `cat .env | grep -v "^#"`
4. **Test connectivity**: `curl http://localhost:8000/health`
5. **Read main README**: See main README.md for more context

---

**Local deployment is ready!** 🚀 Now you can develop and test locally before deploying to production.
