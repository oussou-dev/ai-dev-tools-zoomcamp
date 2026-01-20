# 🔵 Google Cloud Deployment Guide

Complete guide to deploy the **AI News Aggregator** on Google Cloud Platform using Cloud Run and Cloud SQL.

---

## 📋 Prerequisites

- Google Cloud account (https://cloud.google.com)
- `gcloud` CLI installed and configured
- Project created in GCP
- Docker images ready for Cloud Run
- Cloud SQL PostgreSQL instance
- API keys configured

---

## **Step 1: Enable Required APIs**

```bash
# Set your project ID
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID

# Enable required APIs
gcloud services enable \
  cloudbuild.googleapis.com \
  run.googleapis.com \
  sql-component.googleapis.com \
  sqladmin.googleapis.com \
  servicenetworking.googleapis.com \
  containerregistry.googleapis.com
```

---

## **Step 2: Create Cloud SQL PostgreSQL Instance**

### via Google Cloud Console:
1. Go to **Cloud SQL** → **"Create Instance"**
2. Select **"PostgreSQL"**
3. Configure:
   - **Instance ID**: `ai-news-db`
   - **Database Version**: PostgreSQL 15
   - **Region**: `us-central1` (or closer to you)
   - **Zonal availability**: Single zone (free tier)
   - **Machine type**: Shared core (0.5 CPUs, 1.75 GB)
4. Click **"Create Instance"**

### Create Database:
1. In instance details → **"Databases"** tab
2. Click **"Create database"**
3. Name: `ai_news_aggregator`

### Create User:
1. In instance details → **"Users"** tab
2. Click **"Create user account"**
3. **Username**: `postgres`
4. **Password**: Your secure password

### Get Connection String:
```bash
# Get instance connection name
gcloud sql instances describe ai-news-db --format="value(connectionName)"
# Format: project:region:instance

# Connection string:
postgresql://postgres:password@/ai_news_aggregator?host=/cloudsql/project:region:ai-news-db
```

---

## **Step 3: Create VPC Connector (Optional but Recommended)**

For Cloud Run to access Cloud SQL securely:

```bash
gcloud compute networks vpc-access connectors create ai-news-connector \
  --region=us-central1 \
  --subnet=default
```

---

## **Step 4: Deploy Backend to Cloud Run**

### Build and Push to Container Registry:

```bash
# Build backend image
gcloud builds submit \
  --config=docker/Dockerfile.api \
  --tag gcr.io/$PROJECT_ID/ai-news-api:latest

# Or manually:
docker build -t gcr.io/$PROJECT_ID/ai-news-api:latest -f docker/Dockerfile.api .
docker push gcr.io/$PROJECT_ID/ai-news-api:latest
```

### Deploy to Cloud Run:

```bash
gcloud run deploy ai-news-api \
  --image gcr.io/$PROJECT_ID/ai-news-api:latest \
  --region us-central1 \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --port 8000 \
  --allow-unauthenticated \
  --vpc-connector ai-news-connector \
  --set-env-vars \
    OPENAI_API_KEY=sk-xxx...,\
    ANTHROPIC_API_KEY=claude-xxx...,\
    MY_EMAIL=your-email@gmail.com,\
    APP_PASSWORD=your-app-password,\
    DATABASE_URL=postgresql://postgres:password@/ai_news_aggregator?host=/cloudsql/project:region:ai-news-db,\
    POSTGRES_USER=postgres,\
    POSTGRES_PASSWORD=your-db-password,\
    POSTGRES_DB=ai_news_aggregator,\
    POSTGRES_HOST=/cloudsql/project:region:ai-news-db,\
    POSTGRES_PORT=5432
```

### Grant Cloud Run Service Account Access to Cloud SQL:

```bash
# Get default service account
export SA_EMAIL=$(gcloud iam service-accounts list --format='value(email)' --filter='displayName:Compute default service account')

# Grant Cloud SQL Client role
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$SA_EMAIL \
  --role roles/cloudsql.client
```

### Get Backend URL:
```bash
gcloud run services describe ai-news-api --region us-central1 --format='value(status.url)'
# Example: https://ai-news-api-xxx.run.app
```

### Verify Backend:
```bash
curl https://ai-news-api-xxx.run.app/health
# Response: {"status": "ok"}
```

---

## **Step 5: Deploy Frontend to Cloud Run**

### Build and Push Frontend:

```bash
gcloud builds submit \
  --config=docker/Dockerfile.frontend \
  --tag gcr.io/$PROJECT_ID/ai-news-frontend:latest
```

### ✨ **CRITICAL: Deploy with API_URL**

```bash
gcloud run deploy ai-news-frontend \
  --image gcr.io/$PROJECT_ID/ai-news-frontend:latest \
  --region us-central1 \
  --platform managed \
  --memory 512Mi \
  --cpu 1 \
  --port 8501 \
  --allow-unauthenticated \
  --set-env-vars API_URL=https://ai-news-api-xxx.run.app
```

Replace `ai-news-api-xxx.run.app` with your actual backend URL from Step 4.

### Get Frontend URL:
```bash
gcloud run services describe ai-news-frontend --region us-central1 --format='value(status.url)'
# Example: https://ai-news-frontend-xxx.run.app
```

---

## **Step 6: Verify Deployment**

### Check Services:
```bash
gcloud run services list --region us-central1
```

### Access Frontend:
```bash
https://ai-news-frontend-xxx.run.app
# Should show: 🟢 Backend Status: Online
```

### Check Backend Health:
```bash
curl https://ai-news-api-xxx.run.app/health
# Response: {"status": "ok"}
```

---

## **Step 7: Update Frontend if Backend URL Changes**

```bash
gcloud run deploy ai-news-frontend \
  --region us-central1 \
  --update-env-vars API_URL=https://ai-news-api-xxx.run.app
```

---

## **Quick Reference: GCP Environment Variables**

### **Backend Service:**
```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=claude-...
MY_EMAIL=your-email@gmail.com
APP_PASSWORD=your-app-password
DATABASE_URL=postgresql://postgres:password@/ai_news_aggregator?host=/cloudsql/project:region:ai-news-db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=...
POSTGRES_DB=ai_news_aggregator
```

### **Frontend Service:**
```
API_URL=https://ai-news-api-xxx.run.app
```

---

## **Complete GCP Architecture**

```
┌──────────────────────────────────────────────┐
│        Google Cloud Platform                 │
├──────────────────────────────────────────────┤
│                                              │
│  ┌──────────────┐    ┌──────────────┐      │
│  │  Cloud SQL   │ ←→ │  Cloud Run   │      │
│  │  PostgreSQL  │    │  (Backend)   │      │
│  └──────────────┘    └──────┬───────┘      │
│       ▲                     │              │
│       │          (VPC Connector)           │
│       │                     │              │
│       └─────────────────────┘              │
│                              ↓             │
│                       ┌──────────────┐    │
│                       │  Cloud Run   │    │
│                       │  (Frontend)  │    │
│                       └──────────────┘    │
│                                              │
└──────────────────────────────────────────────┘

      ↓ (External HTTPS Access)
  https://ai-news-frontend-xxx.run.app
  https://ai-news-api-xxx.run.app
```

---

## **Troubleshooting on GCP**

### ❌ Cloud Run service failed to deploy

**Check build logs:**
```bash
gcloud builds log --stream=false
```

**Common causes:**
- Docker image build failed
- Missing environment variables
- API quota exceeded

### ❌ Cannot connect to Cloud SQL

**Check VPC Connector:**
```bash
gcloud compute networks vpc-access connectors list
```

**Verify service account permissions:**
```bash
gcloud projects get-iam-policy $PROJECT_ID \
  --flatten="bindings[].members" \
  --filter="bindings.members:$SA_EMAIL"
```

**Solution**: Grant Cloud SQL Client role:
```bash
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member serviceAccount:$SA_EMAIL \
  --role roles/cloudsql.client
```

### ❌ Frontend shows "🔴 Offline"

**Check environment variables:**
```bash
gcloud run services describe ai-news-frontend --region us-central1
# Look for API_URL in env vars
```

**Update API_URL:**
```bash
gcloud run deploy ai-news-frontend \
  --region us-central1 \
  --update-env-vars API_URL=https://ai-news-api-xxx.run.app
```

### ❌ Slow startup or timeouts

**Increase memory and CPU:**
```bash
gcloud run deploy ai-news-api \
  --region us-central1 \
  --memory 1Gi \
  --cpu 2
```

**Increase timeout:**
```bash
gcloud run deploy ai-news-api \
  --region us-central1 \
  --timeout 600
```

---

## **Production Tips**

### 1. **Enable Cloud Monitoring**
```bash
gcloud run deploy ai-news-api \
  --region us-central1 \
  --no-gen2  # Use gen1 for better monitoring support
```

### 2. **Set Up Cloud Logging**
```bash
# View logs
gcloud run logs read ai-news-api --region us-central1

# Stream logs
gcloud run logs read ai-news-api --region us-central1 --follow
```

### 3. **Use Cloud Scheduler for Periodic Tasks**
```bash
gcloud scheduler jobs create http daily-pipeline \
  --schedule="0 6 * * *" \
  --uri=https://ai-news-api-xxx.run.app/pipeline/run \
  --http-method=POST \
  --location=us-central1 \
  --time-zone=UTC
```

### 4. **Enable Cold Start Optimization**
- Keep minimum 1 instance warm
- Use Cloud Tasks for async operations

### 5. **Use Secret Manager for Sensitive Data**
```bash
# Create secret
echo -n "sk-xxx" | gcloud secrets create openai-api-key --data-file=-

# Grant access to service account
gcloud secrets add-iam-policy-binding openai-api-key \
  --member serviceAccount:$SA_EMAIL \
  --role roles/secretmanager.secretAccessor

# Reference in Cloud Run
gcloud run deploy ai-news-api \
  --region us-central1 \
  --set-env-vars OPENAI_API_KEY=/secrets/openai-api-key/openai-api-key
```

---

## **Cost Estimation**

| Resource | Monthly Cost |
|----------|--------------|
| Cloud Run (2 services) | ~$5-15 |
| Cloud SQL (shared core) | ~$4 |
| Network (VPC Connector) | ~$7 |
| Data transfer | ~$3 |
| **Total** | **~$19-29/month** |

---

## **CLI Commands Summary**

```bash
# Deploy backend
gcloud run deploy ai-news-api \
  --image gcr.io/$PROJECT_ID/ai-news-api:latest \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_URL=<backend-url>

# Deploy frontend
gcloud run deploy ai-news-frontend \
  --image gcr.io/$PROJECT_ID/ai-news-frontend:latest \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars API_URL=<backend-url>

# View services
gcloud run services list --region us-central1

# View logs
gcloud run logs read <service-name> --region us-central1 --follow

# Update environment variables
gcloud run deploy <service-name> \
  --region us-central1 \
  --update-env-vars KEY=value
```

---

## **Next Steps**

After deployment:

1. **Test the pipeline** - Click "🚀 Run Pipeline" in frontend
2. **Check Cloud Logging** - Monitor for errors
3. **View digests** - Should populate after pipeline runs
4. **Set up monitoring** - Use Cloud Monitoring dashboard
5. **Configure custom domain** - Use Cloud Domains or CNAME

```
Frontend: https://ai-news-frontend-xxx.run.app
API Docs: https://ai-news-api-xxx.run.app/docs
```

---

## **Need Help?**

If you get stuck:

1. **Check Cloud Logging**: Cloud Run service logs
2. **Verify API_URL**: Service details → Environment variables
3. **Test backend**: `curl https://api-url/health`
4. **GCP support**: https://cloud.google.com/support
5. **Repository README**: See main README.md for more context

---

**You're all set!** 🚀 Your application is now deployed on Google Cloud!
