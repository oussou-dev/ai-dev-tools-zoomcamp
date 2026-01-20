# 🟣 Heroku Deployment Guide

Complete guide to deploy the **AI News Aggregator** on Heroku using Heroku Container Registry and Heroku PostgreSQL.

---

## 📋 Prerequisites

- Heroku account (https://www.heroku.com)
- Heroku CLI installed (`brew install heroku` or `npm install -g heroku`)
- GitHub repository ready
- Git configured locally

---

## **Step 1: Create Heroku App**

```bash
# Login to Heroku
heroku login

# Set app name
export HEROKU_APP=ai-news-aggregator

# Create app
heroku create $HEROKU_APP

# Or use existing app
heroku apps:list
```

---

## **Step 2: Provision PostgreSQL Database**

```bash
# Add Postgres add-on (Standard tier minimum for production)
heroku addons:create heroku-postgresql:standard-0 \
  --app $HEROKU_APP

# Or use free tier (not recommended for production)
heroku addons:create heroku-postgresql:hobby-dev \
  --app $HEROKU_APP

# Get database URL
heroku config:get DATABASE_URL --app $HEROKU_APP
# Format: postgresql://user:password@host:port/dbname
```

---

## **Step 3: Configure Environment Variables**

```bash
# Set all required environment variables
heroku config:set \
  OPENAI_API_KEY=sk-xxx... \
  ANTHROPIC_API_KEY=claude-xxx... \
  MY_EMAIL=your-email@gmail.com \
  APP_PASSWORD=your-app-password \
  --app $HEROKU_APP

# Verify variables set
heroku config --app $HEROKU_APP
```

---

## **Step 4: Create Procfile**

Create a `Procfile` in project root (no extension):

```
web: uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
```

For both services, create `Procfile.backend` and `Procfile.frontend`:

**Procfile.backend:**
```
web: uvicorn app.api.main:app --host 0.0.0.0 --port $PORT
```

**Procfile.frontend:**
```
web: streamlit run app/frontend/main.py --server.port=$PORT --server.address=0.0.0.0
```

---

## **Step 5: Deploy Backend Service**

### Option A: Using Heroku CLI (Recommended)

```bash
# Set backend app
export BACKEND_APP=ai-news-api

# Create backend app
heroku create $BACKEND_APP

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev --app $BACKEND_APP

# Set environment variables
heroku config:set \
  OPENAI_API_KEY=sk-xxx... \
  ANTHROPIC_API_KEY=claude-xxx... \
  MY_EMAIL=your-email@gmail.com \
  APP_PASSWORD=your-app-password \
  --app $BACKEND_APP

# Create Procfile
echo "web: uvicorn app.api.main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Deploy via Git
git push heroku main:main --app $BACKEND_APP

# Or deploy via Container Registry
heroku container:login
heroku container:push web -a $BACKEND_APP
heroku container:release web -a $BACKEND_APP

# Get backend URL
heroku apps:info $BACKEND_APP --json | grep -o '"web_url":"[^"]*' | cut -d'"' -f4
# Format: https://ai-news-api.herokuapp.com/
```

### Verify Backend:

```bash
BACKEND_URL=$(heroku apps:info $BACKEND_APP --json | grep -o '"web_url":"[^"]*' | cut -d'"' -f4)
curl ${BACKEND_URL}health
# Response: {"status": "ok"}
```

---

## **Step 6: Deploy Frontend Service**

### Create Frontend App:

```bash
# Set frontend app
export FRONTEND_APP=ai-news-frontend

# Create frontend app
heroku create $FRONTEND_APP

# ✨ **CRITICAL: Set API_URL pointing to backend**
BACKEND_URL=$(heroku apps:info $BACKEND_APP --json | grep -o '"web_url":"[^"]*' | cut -d'"' -f4 | sed 's:/$::')

heroku config:set \
  API_URL=$BACKEND_URL \
  --app $FRONTEND_APP

# Create Procfile for frontend
echo "web: streamlit run app/frontend/main.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile

# Deploy via Git
git push heroku main:main --app $FRONTEND_APP

# Or deploy via Container Registry
heroku container:login
heroku container:push web -a $FRONTEND_APP
heroku container:release web -a $FRONTEND_APP

# Get frontend URL
heroku apps:info $FRONTEND_APP --json | grep -o '"web_url":"[^"]*' | cut -d'"' -f4
# Format: https://ai-news-frontend.herokuapp.com/
```

---

## **Step 7: Verify Deployment**

### Check Both Apps:

```bash
# List apps
heroku apps

# Check backend logs
heroku logs --tail --app $BACKEND_APP

# Check frontend logs
heroku logs --tail --app $FRONTEND_APP
```

### Access Frontend:

```bash
FRONTEND_URL=$(heroku apps:info $FRONTEND_APP --json | grep -o '"web_url":"[^"]*' | cut -d'"' -f4)
echo "Open in browser: ${FRONTEND_URL}"
```

Should show:
- ✅ 🟢 Backend Status: Online
- 🚀 Run Pipeline button
- News feed

### Check Backend Health:

```bash
BACKEND_URL=$(heroku apps:info $BACKEND_APP --json | grep -o '"web_url":"[^"]*' | cut -d'"' -f4 | sed 's:/$::')
curl ${BACKEND_URL}/health
# Response: {"status": "ok"}
```

---

## **Step 8: Create Heroku.yml for Container Deployment**

Create `heroku.yml` for better container management:

```yaml
build:
  docker:
    web: docker/Dockerfile.api

run:
  web: uvicorn app.api.main:app --host 0.0.0.0 --port $PORT

release:
  image: web
  command:
    - python
    - -m
    - app.database.create_tables
```

Deploy:
```bash
git add heroku.yml
git commit -m "Add Heroku configuration"
git push heroku main:main --app $BACKEND_APP
```

---

## **Quick Reference: Heroku Environment Variables**

### **Backend App:**
```bash
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
# DATABASE_URL is auto-generated by Heroku
```

### **Frontend App:**
```bash
API_URL=https://ai-news-api.herokuapp.com
```

Set via:
```bash
heroku config:set KEY=value --app app-name
```

---

## **Complete Heroku Architecture**

```
┌─────────────────────────────────────────────┐
│           Heroku Platform                   │
├─────────────────────────────────────────────┤
│                                             │
│  Backend App (`ai-news-api`)                │
│  ┌──────────────────────────────┐          │
│  │  ┌──────────────────────┐    │          │
│  │  │ Heroku PostgreSQL    │    │          │
│  │  │ (Shared or Dedicated)│    │          │
│  │  └──────────────────────┘    │          │
│  │          ▲                    │          │
│  │  ┌──────┴─────────────────┐  │          │
│  │  │  FastAPI Container     │  │          │
│  │  │  (uvicorn running)     │  │          │
│  │  └──────────────────────┘  │          │
│  └──────────────────────────────┘          │
│                                             │
│  Frontend App (`ai-news-frontend`)          │
│  ┌──────────────────────────────┐          │
│  │  Streamlit Container         │          │
│  │  (Communicates to Backend)   │          │
│  └──────────────────────────────┘          │
│                                             │
└─────────────────────────────────────────────┘

   ↓ (External HTTPS Access)
https://ai-news-api.herokuapp.com
https://ai-news-frontend.herokuapp.com
```

---

## **Troubleshooting on Heroku**

### ❌ App won't start

**Check logs:**
```bash
heroku logs --tail --app $BACKEND_APP
```

**Common causes:**
- Missing environment variables
- Database connection failed
- Port binding issue

**Solution:**
```bash
# View config
heroku config --app $BACKEND_APP

# Add missing variable
heroku config:set VAR_NAME=value --app $BACKEND_APP
```

### ❌ Database connection error

**Check DATABASE_URL:**
```bash
heroku config:get DATABASE_URL --app $BACKEND_APP
```

**Reset database:**
```bash
heroku pg:reset DATABASE --app $BACKEND_APP
```

**Run migrations:**
```bash
heroku run python -m app.database.create_tables --app $BACKEND_APP
```

### ❌ Frontend shows "🔴 Offline"

**Check API_URL:**
```bash
heroku config:get API_URL --app $FRONTEND_APP
```

**Update if needed:**
```bash
BACKEND_URL=$(heroku apps:info $BACKEND_APP --json | grep -o '"web_url":"[^"]*' | cut -d'"' -f4 | sed 's:/$::')
heroku config:set API_URL=$BACKEND_URL --app $FRONTEND_APP
```

**Redeploy frontend:**
```bash
git push heroku main:main --app $FRONTEND_APP
```

### ❌ Slow startup (cold start)

**Upgrade dyno type:**
```bash
# Free dyos go to sleep, use paid
heroku dyos:type standard-1x --app $BACKEND_APP
heroku dyos:type standard-1x --app $FRONTEND_APP
```

**Or keep app warm with scheduler:**
```bash
# Add Heroku Scheduler
heroku addons:create scheduler:standard --app $BACKEND_APP

# Schedule daily ping
heroku addons:open scheduler --app $BACKEND_APP
# Add job: curl https://ai-news-api.herokuapp.com/health
```

---

## **Production Tips**

### 1. **Use Custom Domain**
```bash
# Add domain
heroku domains:add www.your-domain.com --app $BACKEND_APP

# Point DNS to Heroku
# CNAME: www.your-domain.com -> ai-news-api.herokuapp.com
```

### 2. **Enable SSL/TLS**
```bash
# Automatic (included with Heroku)
heroku certs:auto:enable --app $BACKEND_APP
```

### 3. **Monitor Performance**
```bash
# View metrics
heroku apps:info $BACKEND_APP

# Monitor logs
heroku logs --tail --app $BACKEND_APP
```

### 4. **Use Heroku Scheduler for Pipelines**
```bash
# Add Scheduler add-on
heroku addons:create scheduler:standard --app $BACKEND_APP

# Schedule daily pipeline runs
heroku addons:open scheduler --app $BACKEND_APP

# Add job:
# heroku run python main.py --app ai-news-api (runs once daily)
```

### 5. **Scale Dynos if Needed**
```bash
# Scale backend
heroku ps:scale web=2 --app $BACKEND_APP

# Scale frontend
heroku ps:scale web=2 --app $FRONTEND_APP

# Check running dynos
heroku ps --app $BACKEND_APP
```

---

## **Cost Estimation**

| Resource | Monthly Cost |
|----------|--------------|
| Free dyno (web) | $0 (sleeps after 30min inactivity) |
| Standard-1X dyno | $7-50/month each |
| PostgreSQL hobby-dev | $0 (free, limited) |
| PostgreSQL standard | $50+/month |
| **Total (Free)** | **$0** |
| **Total (Production)** | **$75-150+/month** |

---

## **CLI Commands Summary**

```bash
# Setup
heroku login
heroku create app-name
heroku addons:create heroku-postgresql:hobby-dev --app app-name

# Deploy
git push heroku main:main --app app-name

# Configuration
heroku config --app app-name
heroku config:set KEY=value --app app-name
heroku config:unset KEY --app app-name

# Logs & Monitoring
heroku logs --tail --app app-name
heroku ps --app app-name

# Running Commands
heroku run "command" --app app-name

# Scaling
heroku ps:scale web=2 --app app-name

# Domain & SSL
heroku domains:add domain.com --app app-name
heroku certs:auto:enable --app app-name
```

---

## **Next Steps**

After deployment:

1. **Test the pipeline** - Click "🚀 Run Pipeline" in frontend
2. **Check logs** - Monitor for errors: `heroku logs --tail`
3. **View digests** - Should populate after pipeline runs
4. **Set up monitoring** - Use Heroku dashboard or New Relic
5. **Configure custom domain** - Add domain and SSL certificate

```
Frontend: https://ai-news-frontend.herokuapp.com
Backend: https://ai-news-api.herokuapp.com
API Docs: https://ai-news-api.herokuapp.com/docs
```

---

## **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| App crashes on startup | Check logs, verify env vars, increase dyno size |
| Database connection fails | Check DATABASE_URL, run `heroku pg:reset DATABASE` |
| API_URL not working | Update frontend config var, redeploy |
| Slow response times | Upgrade dyno type from free tier |
| File uploads don't persist | Use S3 or external storage (Heroku has ephemeral filesystem) |

---

## **Deploying Updates**

```bash
# After making changes locally
git add .
git commit -m "Update code"

# Deploy backend changes
git push heroku main:main --app ai-news-api

# Deploy frontend changes
git push heroku main:main --app ai-news-frontend

# Or deploy specific branch
git push heroku mybranch:main --app app-name
```

---

## **Need Help?**

If you get stuck:

1. **Check Heroku logs**: `heroku logs --tail --app app-name`
2. **Verify API_URL**: `heroku config --app app-name`
3. **Test backend**: `curl https://api-url/health`
4. **Heroku support**: https://devcenter.heroku.com
5. **Repository README**: See main README.md for more context

---

**You're all set!** 🚀 Your application is now deployed on Heroku!
