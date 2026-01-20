# 🚂 Railway Deployment Guide

Complete guide to deploy the **AI News Aggregator** on Railway with proper `API_URL` configuration.

---

## 📋 Prerequisites

- Railway account (https://railway.app)
- GitHub repository connected to Railway
- Environment variables ready (`.env` file)
- OpenAI and Anthropic API keys (optional)

---

## **Step 1: Create Railway Project**

1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub"**
4. Connect your GitHub repo and select `04_ai_news_aggr`
5. Railway auto-detects the project

---

## **Step 2: Deploy PostgreSQL Database**

1. In Railway dashboard, click **"Add Service"** → **"Add from Market"**
2. Search and select **"PostgreSQL"**
3. Railway creates a Postgres instance automatically
4. Note the generated connection URL (visible in the Variables tab)

---

## **Step 3: Deploy Backend Service**

### Create Backend Service:
1. Click **"New Service"** → **"Deploy from GitHub repo"**
2. Select your repo again
3. Configure:
   - **Name**: `api` (or `backend`)
   - **Root Directory**: `/` (project root)
   - **Dockerfile**: `docker/Dockerfile.api`

### Set Backend Environment Variables:

Click on the `api` service → **"Variables"** tab → **"Add Variable"**

Add these variables (get values from your `.env`):

```
OPENAI_API_KEY=sk-xxx...
ANTHROPIC_API_KEY=claude-xxx...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password

POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=<railway-postgres-url>
POSTGRES_PORT=5432
```

Or use Railway's automatic linking:
- Click **"PostgreSQL"** service → **"Connect"** in the `api` service
- Railway auto-adds `DATABASE_URL`

### Check Backend Service:

```bash
# Get the public URL from Railway
# Example: https://api-production-xyz.railway.app

# Verify it's working
curl https://api-production-xyz.railway.app/health
# Should return: {"status": "ok"}
```

---

## **Step 4: Deploy Frontend Service**

### Create Frontend Service:
1. Click **"New Service"** → **"Deploy from GitHub repo"**
2. Select your repo
3. Configure:
   - **Name**: `frontend` (or `ui`)
   - **Root Directory**: `/`
   - **Dockerfile**: `docker/Dockerfile.frontend`

### ✨ **CRITICAL: Set API_URL Variable**

In the `frontend` service → **"Variables"** tab → **"Add Variable"**

**Add this variable:**

| Key | Value |
|-----|-------|
| `API_URL` | `https://api-production-xyz.railway.app` |

Replace `api-production-xyz.railway.app` with your actual backend URL from Step 3.

### Complete Frontend Variables:

```
API_URL=https://api-production-xyz.railway.app
```

That's it! The frontend will automatically use this URL.

---

## **Step 5: Configure Service Dependencies**

### Set Deploy Order:
1. Go to `frontend` service → **"Deploy"** settings
2. Under **"Start Command"**: Keep default
3. Under **"Healthcheck"**: Keep default (already configured in Dockerfile)

**Note**: Railway automatically handles service startup order when you reference environment variables.

---

## **Step 6: Verify Deployment**

### Check Frontend is Running:
```bash
# Open in browser
https://frontend-production-xyz.railway.app

# Should show:
# ✅ 🟢 Backend Status: Online
# 🚀 Run Pipeline button
# News feed
```

### Check Backend Health:
```bash
curl https://api-production-xyz.railway.app/health
# Response: {"status": "ok"}
```

### View Logs:
In Railway dashboard:
1. Click `api` service → **"Logs"** tab
2. Click `frontend` service → **"Logs"** tab
3. Look for any connection errors

---

## **Step 7: Common Railway Environment Variables**

If you need to set more variables in Railway:

```bash
# Via Railway CLI (if installed)
railway variables set \
  OPENAI_API_KEY=sk-xxx \
  ANTHROPIC_API_KEY=claude-xxx \
  MY_EMAIL=your-email@gmail.com \
  APP_PASSWORD=password \
  API_URL=https://api-production-xyz.railway.app
```

Or manually in dashboard for each service.

---

## **Quick Reference: Railway Dashboard Variables**

### **`api` Service Variables:**
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
DATABASE_URL=postgresql://... (auto-linked from Postgres)
POSTGRES_HOST=<postgres-container-host>
POSTGRES_PORT=5432
```

### **`frontend` Service Variables:**
```
API_URL=https://api-production-xyz.railway.app
```

---

## **Troubleshooting on Railway**

### ❌ Frontend shows "🔴 Offline"

**Check 1: API_URL is set correctly**
```bash
# In Railway dashboard
Frontend Service → Variables → API_URL should show:
https://api-production-xyz.railway.app
```

**Check 2: Backend is running**
```bash
# Test in browser or terminal
https://api-production-xyz.railway.app/health
```

**Check 3: View frontend logs**
```bash
# In Railway dashboard
frontend-service → Logs (scroll for errors)
```

### ❌ Database connection errors

**Check 1: Database is running**
```bash
# In Railway, PostgreSQL service should show "Running"
```

**Check 2: CONNECTION_URL is correct**
```bash
# PostgreSQL service → Variables → DATABASE_URL
# Should look like: postgresql://user:pass@host:port/db
```

**Check 3: Backend can access database**
```bash
# Backend service logs should show successful connection
# If not, check POSTGRES_HOST and POSTGRES_PORT
```

### ❌ API_URL not being picked up

**Solution**: Restart frontend service
```bash
# In Railway dashboard
frontend-service → Redeploy
```

---

## **Complete Railway Architecture**

```
┌─────────────────────────────────────────────┐
│         Railway Project                     │
├─────────────────────────────────────────────┤
│                                             │
│  ┌──────────────┐     ┌──────────────┐    │
│  │  PostgreSQL  │ ←── │  Backend API │    │
│  │   Database   │     │  Service     │    │
│  └──────────────┘     └──────┬───────┘    │
│                              │            │
│                              ↓            │
│                       ┌──────────────┐    │
│                       │  Frontend    │    │
│                       │  Service     │    │
│                       │ (Streamlit)  │    │
│                       └──────────────┘    │
│                                             │
└─────────────────────────────────────────────┘

          ↓ (External Access)
    https://frontend-xyz.railway.app
    https://api-xyz.railway.app
```

---

## **Deploy & Monitor**

### **After First Deployment:**

1. ✅ Check **Dashboard** - all services should show "Running" (green)
2. ✅ Open frontend URL in browser
3. ✅ Verify backend status shows "🟢 Online"
4. ✅ Click "🚀 Run Pipeline" to test

### **Monitor Deployments:**

In Railway dashboard:
- **"Deployments"** tab - see deployment history
- **"Logs"** tab - view service logs in real-time
- **"Metrics"** tab - CPU, memory usage

---

## **Production Tips**

### 1. **Auto-redeploy on GitHub push**
Railway automatically redeploys when you push to GitHub (no manual intervention needed!)

### 2. **Update API_URL when backend URL changes**
If you redeploy backend, get the new URL and update:
```
frontend service → Variables → API_URL
```

### 3. **Scale services if needed**
- Railway → Service → **"Settings"** → Instances
- Can run multiple replicas for high traffic

### 4. **Environment variables secrets**
Store sensitive keys securely:
- Never commit `.env` to GitHub
- Use Railway's Variables section (encrypted)

---

## **Next Steps**

After deployment:

1. **Test the pipeline** - Click "🚀 Run Pipeline" in frontend
2. **Check logs** - Verify no errors in backend logs
3. **View digests** - Should start populating once pipeline runs
4. **Share the URL** - Give others access to the dashboard

```
Frontend: https://your-frontend-xyz.railway.app
API Docs: https://your-api-xyz.railway.app/docs
```

---

## **Common Issues & Solutions**

### Service won't start
- Check logs for error messages
- Verify all environment variables are set
- Ensure Dockerfile path is correct

### Timeout errors
- Increase Railway's timeout setting
- Check if services are properly waiting for dependencies
- Verify network connectivity between services

### API calls failing from frontend
- Verify API_URL is correctly set
- Check CORS is enabled in FastAPI (already configured)
- Test backend health endpoint directly

### Database connection pooling issues
- Reduce database connection timeout
- Check Railway's connection limits
- Monitor active connections in logs

---

## **Need Help?**

If you get stuck:

1. **Check Railway logs**: Service → Logs tab
2. **Verify API_URL**: frontend Service → Variables → API_URL
3. **Test backend directly**: `curl https://api-xyz.railway.app/health`
4. **Railway support**: https://docs.railway.app
5. **Repository README**: See main README.md for more context

---

**You're all set!** 🚀 Your application should now be live on Railway with proper API communication between frontend and backend!
