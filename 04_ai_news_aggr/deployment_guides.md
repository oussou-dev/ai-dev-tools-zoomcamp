# 📚 Complete Deployment Guides

Master guide for deploying the **AI News Aggregator** across all platforms.

---

## 📖 Table of Contents

1. [🏠 Local Deployment](#-local-deployment)
2. [🚂 Railway Deployment](#-railway-deployment)
3. [🎨 Render Deployment](#-render-deployment)
4. [☁️ AWS ECS/Fargate Deployment](#-aws-ecsfargate-deployment)
5. [🔵 Google Cloud Deployment](#-google-cloud-deployment)
6. [🔷 Azure Cloud Deployment](#-azure-cloud-deployment)
7. [🟣 Heroku Deployment](#-heroku-deployment)
8. [Platform Comparison](#-platform-comparison)

---

# 🏠 Local Deployment

**File**: `deployment_guide_local.md`

Complete guide to run the **AI News Aggregator** locally using Docker Compose.

## Quick Start

```bash
# 1. Clone and setup
git clone <repo-url>
cd 04_ai_news_aggr

# 2. Configure environment
cp app/example.env .env
# Edit .env with your API keys

# 3. Start all services
docker-compose up --build

# 4. Access services
# Frontend: http://localhost:8501
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Prerequisites
- Docker installed
- Docker Compose installed
- 4GB RAM minimum
- Environment variables configured

## Services
- 🐘 PostgreSQL (port 5432)
- 🔌 FastAPI Backend (port 8000)
- 🎨 Streamlit Frontend (port 8501)

## Key Commands

```bash
docker-compose ps                    # View running services
docker-compose logs -f               # Follow logs
docker-compose exec backend pytest   # Run tests
docker-compose down -v               # Stop and clean
```

📖 **[→ Full Local Deployment Guide](deployment_guide_local.md)**

---

# 🚂 Railway Deployment

**File**: `deployment_guide_railway.md`

Deploy on Railway (Simple, $19-29/month)

## Quick Start

1. Go to https://railway.app
2. Create new project from GitHub
3. Add PostgreSQL service
4. Deploy Backend service with `docker/Dockerfile.api`
5. Deploy Frontend service with `docker/Dockerfile.frontend`
6. **CRITICAL**: Set Frontend `API_URL` environment variable

```bash
# Example API_URL
API_URL=https://api-production-xyz.railway.app
```

## Steps

1. **Create Project** - Connect GitHub repo
2. **Deploy PostgreSQL** - Add from marketplace
3. **Deploy Backend**
   - New service → GitHub repo
   - Dockerfile: `docker/Dockerfile.api`
   - Port: 8000
   - Environment variables for database & API keys

4. **Deploy Frontend**
   - New service → GitHub repo
   - Dockerfile: `docker/Dockerfile.frontend`
   - Port: 8501
   - **Set API_URL to backend URL**

## Environment Variables

**Backend:**
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
DATABASE_URL=postgresql://... (auto from PostgreSQL)
```

**Frontend:**
```
API_URL=https://api-production-xyz.railway.app
```

## Access
- Frontend: https://frontend-xyz.railway.app
- API: https://api-xyz.railway.app
- API Docs: https://api-xyz.railway.app/docs

📖 **[→ Full Railway Deployment Guide](deployment_guide_railway.md)**

---

# 🎨 Render Deployment

**File**: `deployment_guide_render.md`

Deploy on Render (Simple, $22+/month)

## Quick Start

1. Go to https://render.com
2. Create PostgreSQL database
3. Deploy Backend → Web Service
4. Deploy Frontend → Web Service with API_URL

## Key Steps

1. **PostgreSQL** - Create database ($0-15/month)
2. **Backend Service**
   - GitHub repo → Web Service
   - Dockerfile: `docker/Dockerfile.api`
   - Set environment variables
   - Free tier services sleep after 15min

3. **Frontend Service**
   - GitHub repo → Web Service
   - Dockerfile: `docker/Dockerfile.frontend`
   - Set `API_URL` to backend URL
   - Free tier services sleep

## Cost
- Free tier: $0 (sleeps after 15min)
- Paid tier: $7/month per service minimum
- PostgreSQL: $15+/month

## Access
- Frontend: https://ai-news-frontend.onrender.com
- Backend: https://ai-news-api.onrender.com

📖 **[→ Full Render Deployment Guide](deployment_guide_render.md)**

---

# ☁️ AWS ECS/Fargate Deployment

**File**: `deployment_guide_aws.md`

Deploy on AWS with ECS and Fargate (Enterprise, ~$46/month)

## Quick Start

```bash
# 1. Push images to ECR
docker push xxx.dkr.ecr.us-east-1.amazonaws.com/ai-news-api:latest
docker push xxx.dkr.ecr.us-east-1.amazonaws.com/ai-news-frontend:latest

# 2. Create RDS PostgreSQL
# 3. Create ECS cluster
# 4. Create task definitions
# 5. Create services
# 6. Create load balancer
```

## Architecture
- **RDS PostgreSQL** - Database
- **ECS Fargate** - Containerized services
- **Application Load Balancer** - Traffic routing
- **ECR** - Container registry

## Key Components

1. **RDS Database**
   - PostgreSQL 15+
   - db.t3.micro (free tier) or larger
   - Public access for dev, private for prod

2. **ECR Repositories**
   - `ai-news-api`
   - `ai-news-frontend`

3. **ECS Cluster**
   - Fargate launch type
   - 2 task definitions
   - 2 services

4. **Load Balancer**
   - Application Load Balancer
   - Target groups for backend (8000) and frontend (8501)
   - Listeners on ports 8000 and 8501

## Environment Variables

**Backend Task Definition:**
```
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
POSTGRES_HOST=xxx.rds.amazonaws.com
```

**Frontend Task Definition:**
```
API_URL=http://alb-dns:8000
```

## Cost Estimation
- ECS Fargate: ~$10/month
- RDS PostgreSQL: ~$15/month
- ALB: ~$16/month
- **Total: ~$46/month**

📖 **[→ Full AWS Deployment Guide](deployment_guide_aws.md)**

---

# 🔵 Google Cloud Deployment

**File**: `deployment_guide_gcp.md`

Deploy on Google Cloud with Cloud Run (Serverless, ~$19-29/month)

## Quick Start

```bash
# 1. Enable APIs
gcloud services enable run.googleapis.com sqladmin.googleapis.com

# 2. Create Cloud SQL PostgreSQL instance
gcloud sql instances create ai-news-db

# 3. Deploy backend
gcloud run deploy ai-news-api --image gcr.io/$PROJECT_ID/ai-news-api:latest

# 4. Deploy frontend with API_URL
gcloud run deploy ai-news-frontend \
  --set-env-vars API_URL=https://ai-news-api-xxx.run.app
```

## Architecture
- **Cloud SQL** - PostgreSQL database
- **Cloud Run** - Serverless containers
- **Container Registry** - Image storage
- **VPC Connector** - Secure database access

## Key Components

1. **Cloud SQL PostgreSQL**
   - Shared core (0.5 CPUs, 1.75 GB) for dev
   - Public or private access

2. **Cloud Run Services**
   - Backend: `ai-news-api` (port 8000)
   - Frontend: `ai-news-frontend` (port 8501)
   - Managed scaling

3. **VPC Connector**
   - Secure communication to Cloud SQL

## Environment Variables

**Backend:**
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
```

**Frontend:**
```
API_URL=https://ai-news-api-xxx.run.app
```

## Cost Estimation
- Cloud Run: ~$5-15/month
- Cloud SQL: ~$4/month
- **Total: ~$19-29/month**

📖 **[→ Full Google Cloud Deployment Guide](deployment_guide_gcp.md)**

---

# 🔷 Azure Cloud Deployment

**File**: `deployment_guide_azure.md`

Deploy on Azure Container Instances (~$58/month)

## Quick Start

```bash
# 1. Create resource group
az group create --name ai-news-rg --location eastus

# 2. Create Azure Container Registry
az acr create --resource-group ai-news-rg --name ainewsacr --sku Basic

# 3. Push images
az acr build --registry ainewsacr --image ai-news-api:latest -f docker/Dockerfile.api .

# 4. Create PostgreSQL
az postgres server create --resource-group ai-news-rg --name ai-news-db

# 5. Deploy containers
az container create --resource-group ai-news-rg --name ai-news-api ...
```

## Architecture
- **Azure Database for PostgreSQL** - Database
- **Container Instances** - Containerized services
- **Container Registry** - Image storage
- **Virtual Network** - Networking

## Key Components

1. **PostgreSQL Server**
   - B_Gen5_1 SKU (~$30/month)
   - 51GB storage

2. **Container Instances**
   - Backend container (1 CPU, 1 GB memory)
   - Frontend container (1 CPU, 1 GB memory)
   - Auto-restart enabled

3. **Container Registry**
   - Store images
   - Basic tier ($5/month)

## Environment Variables

**Backend:**
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
```

**Frontend:**
```
API_URL=http://ai-news-api.eastus.azurecontainer.io:8000
```

## Cost Estimation
- Container Instances: ~$20/month
- PostgreSQL: ~$30/month
- **Total: ~$58/month**

📖 **[→ Full Azure Deployment Guide](deployment_guide_azure.md)**

---

# 🟣 Heroku Deployment

**File**: `deployment_guide_heroku.md`

Deploy on Heroku (Free-$150+/month)

## Quick Start

```bash
# 1. Login
heroku login

# 2. Create apps
heroku create ai-news-api
heroku create ai-news-frontend

# 3. Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev --app ai-news-api

# 4. Create Procfile
echo "web: uvicorn app.api.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# 5. Deploy
git push heroku main:main --app ai-news-api
git push heroku main:main --app ai-news-frontend

# 6. Set API_URL on frontend
heroku config:set API_URL=https://ai-news-api.herokuapp.com --app ai-news-frontend
```

## Architecture
- **Heroku PostgreSQL** - Database (free or paid)
- **Heroku Dynos** - Container runtime
- **Procfile** - Start command configuration
- **Git-based deployment** - Push to deploy

## Key Components

1. **Procfile**
   - Backend: `web: uvicorn app.api.main:app --host 0.0.0.0 --port $PORT`
   - Frontend: `web: streamlit run app/frontend/main.py --server.port=$PORT --server.address=0.0.0.0`

2. **PostgreSQL Add-on**
   - hobby-dev: Free tier (512MB)
   - standard-0: $50+/month

3. **Dynos**
   - Free: $0 (sleeps after 30min)
   - Paid: $7-50/month each

## Environment Variables

**Backend:**
```
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://... (auto)
```

**Frontend:**
```
API_URL=https://ai-news-api.herokuapp.com
```

## Cost Estimation
- Free tier: $0 (sleeps)
- Production (2 dynos): $75-150+/month

## Scheduler for Automation

```bash
# Add scheduler for daily pipeline runs
heroku addons:create scheduler:standard --app ai-news-api
# Schedule: heroku run python main.py
```

📖 **[→ Full Heroku Deployment Guide](deployment_guide_heroku.md)**

---

# 📊 Platform Comparison

## Quick Comparison Table

| Platform | Ease | Cold Start | Cost (Min) | Auto-Scale | Best For |
|----------|------|-----------|------------|-----------|----------|
| **Local** | ⭐⭐⭐⭐⭐ | Instant | $0 | No | Development |
| **Railway** | ⭐⭐⭐⭐⭐ | 5-10s | $19 | Yes | Quick deploy |
| **Render** | ⭐⭐⭐⭐ | 10-15s | $22 | Limited | Simple deployment |
| **Heroku** | ⭐⭐⭐⭐⭐ | 30s (free) | $0 | Yes | Simplicity |
| **AWS ECS** | ⭐⭐⭐ | 5s | $46 | Yes | Enterprise |
| **GCP** | ⭐⭐⭐⭐ | 2-5s | $19 | Yes | Serverless |
| **Azure** | ⭐⭐⭐ | 10s | $58 | Limited | Microsoft eco |

## Features Comparison

| Feature | Railway | Render | AWS | GCP | Azure | Heroku |
|---------|---------|--------|-----|-----|-------|--------|
| Free Tier | ❌ | ❌ | ⭐ | ❌ | ❌ | ✅ |
| Auto-deploy | ✅ | ✅ | ⭐ | ✅ | ⭐ | ✅ |
| Database | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Custom Domain | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| SSL/HTTPS | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Monitoring | ⭐ | ⭐ | ✅ | ✅ | ✅ | ⭐ |
| Scaling | ✅ | Limited | ✅ | ✅ | Limited | ✅ |
| Learning Curve | Easiest | Easy | Hard | Medium | Hard | Easiest |

## Cost Comparison (12 months)

| Platform | Min Cost | Production Cost |
|----------|----------|-----------------|
| Local | $0 | N/A |
| Railway | $228 | $500+ |
| Render | $264 | $500+ |
| Heroku | $0 | $900-1800 |
| AWS | $552 | $1200+ |
| GCP | $228 | $500+ |
| Azure | $696 | $1200+ |

## Recommendation by Use Case

### 🎓 **Learning / Development**
→ **Local** or **Heroku Free Tier**
- No cost, full control
- Best for experimentation

### 🚀 **Quick Prototype / MVP**
→ **Railway** or **Render**
- $19-22/month
- 5 minute setup
- Auto-deploy from GitHub

### 💼 **Production (Low Traffic)**
→ **GCP** or **Railway**
- $19-29/month
- Reliable performance
- Good scaling options

### 🏢 **Enterprise / High Traffic**
→ **AWS** or **Google Cloud**
- Full control and flexibility
- Advanced monitoring
- Unlimited scaling

---

## 🎯 Decision Tree

```
Start Here
    ↓
Want to develop locally?
├─ YES → Use Local (Docker Compose)
└─ NO → Continue...

Ready for production?
├─ NO → Use Heroku Free or Railway (cheapest)
└─ YES → Continue...

Need enterprise features?
├─ YES → Use AWS or GCP
└─ NO → Continue...

Want simplicity?
├─ YES → Use Railway or Render
└─ NO → Use AWS, GCP, or Azure
```

---

## 📝 Environment Variables Reference

### Common to All Platforms

**API Keys (Required):**
```
OPENAI_API_KEY=sk-xxx...
ANTHROPIC_API_KEY=claude-xxx...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
```

**Database (Generated per platform):**
```
DATABASE_URL=postgresql://user:password@host:port/db
POSTGRES_HOST=xxx
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=xxx
POSTGRES_DB=ai_news_aggregator
```

**Frontend (Critical!):**
```
API_URL=https://backend-url (without trailing slash)
```

---

## 🔗 Quick Navigation

| Platform | Detailed Guide | Status |
|----------|---|--------|
| 🏠 Local | [deployment_guide_local.md](deployment_guide_local.md) | ✅ |
| 🚂 Railway | [deployment_guide_railway.md](deployment_guide_railway.md) | ✅ |
| 🎨 Render | [deployment_guide_render.md](deployment_guide_render.md) | ✅ |
| ☁️ AWS | [deployment_guide_aws.md](deployment_guide_aws.md) | ✅ |
| 🔵 GCP | [deployment_guide_gcp.md](deployment_guide_gcp.md) | ✅ |
| 🔷 Azure | [deployment_guide_azure.md](deployment_guide_azure.md) | ✅ |
| 🟣 Heroku | [deployment_guide_heroku.md](deployment_guide_heroku.md) | ✅ |

---

## ✅ Common Deployment Checklist

Use this checklist for any platform:

- [ ] Clone repository
- [ ] Copy and configure `.env` file
- [ ] Set all environment variables
- [ ] Deploy backend service
- [ ] Verify backend health: `curl <backend>/health`
- [ ] Deploy database (if not managed)
- [ ] Deploy frontend service
- [ ] **CRITICAL**: Set `API_URL` environment variable on frontend
- [ ] Access frontend URL in browser
- [ ] Verify "🟢 Backend Status: Online"
- [ ] Test pipeline: Click "🚀 Run Pipeline"
- [ ] Check logs for errors
- [ ] Verify digests populate

---

## 🆘 Common Issues Across All Platforms

### Frontend Shows "🔴 Offline"

1. Check `API_URL` is set correctly
2. Verify backend is running
3. Test endpoint: `curl <API_URL>/health`
4. Restart frontend service

### Database Connection Fails

1. Verify `DATABASE_URL` format
2. Check database server is running
3. Verify credentials in environment
4. Check firewall/network rules

### Services Won't Start

1. Check logs for error messages
2. Verify all required environment variables are set
3. Check available system resources (memory, CPU)
4. Try rebuilding from scratch

### Slow Response Times

1. Check service logs
2. Monitor resource usage (CPU, memory)
3. Upgrade instance size if needed
4. Check network connectivity

### API_URL Not Working

1. Ensure URL has no trailing slash
2. Verify CORS is enabled (already configured)
3. Test backend directly: `curl <URL>/health`
4. Restart frontend service

---

## 🚀 Next Steps

1. **Choose a platform** - See [Platform Comparison](#-platform-comparison)
2. **Read the detailed guide** - Follow the link in quick reference
3. **Set up environment** - Configure `.env` file
4. **Deploy services** - Follow step-by-step instructions
5. **Verify deployment** - Test endpoints and frontend
6. **Run pipeline** - Click button or call API
7. **Monitor logs** - Watch for errors

---

## 📚 Additional Resources

- **Main README**: See `README.md` for project overview
- **Vibe Coding Guide**: See `vibe_coding.md` for project recreation
- **Implementation Plan**: See `implementation_plan/` for detailed specifications
- **Individual Guides**: Use specific guide files for deep dives

---

**You now have complete deployment documentation for all platforms!** 🎉

Choose your platform, follow the guide, and deploy with confidence!
