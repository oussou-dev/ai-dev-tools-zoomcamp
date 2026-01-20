# 🎨 Render Deployment Guide

Complete guide to deploy the **AI News Aggregator** on Render with proper `API_URL` configuration.

---

## 📋 Prerequisites

- Render account (https://render.com)
- GitHub repository connected to Render
- PostgreSQL database (Render provides)
- Environment variables ready (`.env` file)
- OpenAI and Anthropic API keys

---

## **Step 1: Create PostgreSQL Database on Render**

1. Go to https://render.com/dashboard
2. Click **"New"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `ai-news-db`
   - **Database**: `ai_news_aggregator`
   - **User**: `postgres`
   - **Region**: Choose closest to you
   - **Plan**: Free or Paid (as needed)
4. Click **"Create Database"**
5. Save the **Internal Database URL** (for backend)

Example format:
```
postgresql://user:password@dpg-xxxxx.render.com/ai_news_aggregator
```

---

## **Step 2: Deploy Backend API Service**

### Create Backend Service:
1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `ai-news-api`
   - **Environment**: `Docker`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Dockerfile Path**: `docker/Dockerfile.api`
   - **Instance Type**: Free or Paid

### Set Backend Environment Variables:

In the service settings → **"Environment"** → **"Add Environment Variable"**

Add these variables:

```
OPENAI_API_KEY=sk-xxx...
ANTHROPIC_API_KEY=claude-xxx...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password

DATABASE_URL=postgresql://user:password@dpg-xxxxx.render.com/ai_news_aggregator
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-db-password
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=dpg-xxxxx.render.com
POSTGRES_PORT=5432
```

### Deploy:
1. Click **"Create Web Service"**
2. Render automatically builds and deploys from `docker/Dockerfile.api`
3. Wait for deployment to complete (5-10 minutes)
4. Note the backend URL: `https://ai-news-api.onrender.com`

### Verify Backend:
```bash
curl https://ai-news-api.onrender.com/health
# Response: {"status": "ok"}
```

---

## **Step 3: Deploy Frontend Service**

### Create Frontend Service:
1. Click **"New"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `ai-news-frontend`
   - **Environment**: `Docker`
   - **Region**: Same as backend & database
   - **Branch**: `main`
   - **Dockerfile Path**: `docker/Dockerfile.frontend`
   - **Instance Type**: Free or Paid

### ✨ **CRITICAL: Set API_URL Variable**

In the service settings → **"Environment"** → **"Add Environment Variable"**

**Add this variable:**

```
API_URL=https://ai-news-api.onrender.com
```

Replace `ai-news-api.onrender.com` with your actual backend URL from Step 2.

### Deploy:
1. Click **"Create Web Service"**
2. Render builds and deploys from `docker/Dockerfile.frontend`
3. Wait for deployment (5-10 minutes)
4. Frontend URL: `https://ai-news-frontend.onrender.com`

---

## **Step 4: Verify Deployment**

### Check Frontend is Running:
```bash
# Open in browser
https://ai-news-frontend.onrender.com

# Should show:
# ✅ 🟢 Backend Status: Online
# 🚀 Run Pipeline button
# News feed
```

### Check Backend Health:
```bash
curl https://ai-news-api.onrender.com/health
# Response: {"status": "ok"}
```

### View Service Logs:
In Render dashboard:
1. Click service → **"Logs"** tab
2. Scroll for any error messages
3. Check connection to database

---

## **Step 5: Configure Auto-Deploy**

Both services automatically redeploy when you push to GitHub (if connected).

To disable or enable:
1. Service → **"Settings"**
2. Under **"Deploy"** → Toggle **"Auto-Deploy"**

---

## **Quick Reference: Render Environment Variables**

### **`ai-news-api` Service:**
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
DATABASE_URL=postgresql://...
POSTGRES_USER=postgres
POSTGRES_PASSWORD=...
POSTGRES_DB=ai_news_aggregator
POSTGRES_HOST=dpg-xxxxx.render.com
POSTGRES_PORT=5432
```

### **`ai-news-frontend` Service:**
```
API_URL=https://ai-news-api.onrender.com
```

---

## **Complete Render Architecture**

```
┌─────────────────────────────────────────────┐
│         Render Project                      │
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
    https://ai-news-frontend.onrender.com
    https://ai-news-api.onrender.com
```

---

## **Troubleshooting on Render**

### ❌ Frontend shows "🔴 Offline"

**Check 1: API_URL is set correctly**
```bash
# In Render dashboard
Frontend Service → Environment
API_URL should be: https://ai-news-api.onrender.com
```

**Check 2: Backend is running**
```bash
curl https://ai-news-api.onrender.com/health
```

**Check 3: View logs**
```bash
# Frontend Service → Logs
# Look for connection errors
```

**Solution**: Redeploy frontend
```bash
# Service → Manual Deploy
```

### ❌ Database connection errors

**Check 1: DATABASE_URL format**
- Should be: `postgresql://user:pass@host/db`
- Not: `postgres://` (deprecated)

**Check 2: Network connectivity**
- Backend service logs should show successful database connection
- If not, verify POSTGRES_HOST is correct

**Check 3: Connection pooling**
- Render PostgreSQL has connection limits
- Monitor active connections in database dashboard

### ❌ Cold start issues

Render puts free tier services to sleep after 15 minutes of inactivity.

**Solution**: Use paid tier or set up wake-up service
- https://github.com/marketplace/actions/render-action

---

## **Production Tips**

### 1. **Use Paid Tier for Production**
- Free tier services go to sleep
- Use $7/month instance type minimum

### 2. **Auto-Deploy from GitHub**
- Already enabled by default
- Every push to `main` triggers redeploy

### 3. **Monitor Logs**
- Service → **"Logs"** tab shows real-time output
- Set up alerts for errors

### 4. **Scale Vertical**
- Service → **"Settings"** → Upgrade instance type
- More CPU and RAM available

### 5. **Custom Domain**
- Service → **"Settings"** → **"Custom Domain"**
- Point your domain to Render

---

## **Environment Variables Best Practices**

1. **Never commit secrets to GitHub**
   - Use Render's Environment variables section
   - All variables are encrypted

2. **Use .env locally only**
   - `.env` in `.gitignore` (already configured)

3. **Update API_URL when backend redeploys**
   - URL stays the same on Render (stable)
   - But if you change service name, update it

---

## **Next Steps**

After deployment:

1. **Test the pipeline** - Click "🚀 Run Pipeline" in frontend
2. **Check logs** - Verify no errors in both services
3. **View digests** - Should populate after pipeline runs
4. **Share the URL** - Give others access to dashboard

```
Frontend: https://ai-news-frontend.onrender.com
API Docs: https://ai-news-api.onrender.com/docs
```

---

## **Common Issues & Solutions**

| Issue | Solution |
|-------|----------|
| Service won't start | Check Dockerfile path and logs |
| API_URL not working | Redeploy frontend after updating variable |
| Database won't connect | Verify DATABASE_URL format and POSTGRES_HOST |
| Slow startup | Cold start on free tier - use paid tier |
| Memory errors | Upgrade to higher instance type |

---

## **Cost Comparison**

| Component | Free Tier | Paid Tier |
|-----------|-----------|-----------|
| Web Service | $0 (sleeps after 15min) | $7+/month |
| PostgreSQL | $0 (512MB) | $15+/month |
| Total | $0 | $22+/month |

---

## **Need Help?**

If you get stuck:

1. **Check Render logs**: Service → Logs tab
2. **Verify environment variables**: Service → Environment
3. **Test backend directly**: `curl https://api-url/health`
4. **Render support**: https://docs.render.com
5. **Repository README**: See main README.md for more context

---

**You're all set!** 🚀 Your application is now live on Render!
