# Deployment Guide for 02_code_itws

## Architecture Overview
- **Frontend**: React (Vite) + CodeMirror + Pyodide (WASM)
- **Backend**: Django + Channels (WebSockets)
- **Database**: SQLite (Dev) -> **PostgreSQL** (Prod)
- **Real-time**: InMemory (Dev) -> **Redis** (Prod)
- **Server**: Daphne (ASGI)

## Top 3 Deployment Solutions

### 1. Railway (Recommended)
**Why**: Easiest setup for Django + Redis + Postgres. Native Docker support.
- **Pros**: Zero-config for many things, easy add-ons for Redis/Postgres, good WebSocket support.
- **Cons**: Can get expensive as you scale.

### 2. Fly.io
**Why**: Runs containers as microVMs. Excellent for real-time apps.
- **Pros**: Global distribution, very fast, great WebSocket support.
- **Cons**: Slightly steeper learning curve (CLI-based).

### 3. Render
**Why**: Simple "Heroku-like" experience.
- **Pros**: Free tier (for static/services), easy to use.
- **Cons**: Free tier spins down (bad for WebSockets), Redis is paid.

---

## Implementation Steps (Railway)

### Prerequisites
1.  **GitHub Repository**: Push your code to GitHub.
2.  **Railway Account**: Sign up at railway.app.

### Step 1: Prepare for Production
We need to update `settings.py` to use environment variables for secrets, database, and Redis.

#### 1. Update `backend/requirements.txt`
Add production dependencies:
```text
psycopg2-binary
dj-database-url
channels_redis
gunicorn
uvicorn
```

#### 2. Create `backend/production_settings.py` (Optional) or Update `settings.py`
Modify `backend/settings.py` to read from env vars:

```python
import os
import dj_database_url

# ... existing imports ...

SECRET_KEY = os.environ.get('SECRET_KEY', 'default-dev-key')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'),
        conn_max_age=600
    )
}

# Channels
if os.environ.get('REDIS_URL'):
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [os.environ.get('REDIS_URL')],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels.layers.InMemoryChannelLayer"
        }
    }
```

### Step 2: Deploy on Railway

1.  **New Project**: Click "New Project" -> "Deploy from GitHub repo".
2.  **Select Repo**: Choose your `ai-dev-tools-zoomcamp` repo.
3.  **Add Database**: Right-click the canvas -> "New" -> "Database" -> "PostgreSQL".
4.  **Add Redis**: Right-click the canvas -> "New" -> "Database" -> "Redis".
5.  **Configure Variables**:
    *   Click on your application service.
    *   Go to "Variables".
    *   Add `SECRET_KEY` (generate a random string).
    *   Add `DEBUG` = `False`.
    *   Railway automatically injects `DATABASE_URL` and `REDIS_URL` if you link the services.
6.  **Build Command**: Railway reads the `Dockerfile`.
    *   Ensure the `Dockerfile` is in the root or specify the path in settings.
    *   Since your project is in `02_code_itws`, you might need to set the **Root Directory** in Railway settings to `02_code_itws`.

### Step 3: Verify
1.  Open the provided URL.
2.  Create a room.
3.  Test real-time collaboration (open two tabs).
