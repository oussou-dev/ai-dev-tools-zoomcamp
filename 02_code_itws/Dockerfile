# Stage 1: Build the frontend
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package*.json ./
RUN npm install

COPY frontend/ .
RUN npm run build

# Stage 2: Setup the backend and serve
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies (if any needed for python packages)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install daphne whitenoise

# Copy backend code
COPY backend/ .

# Copy built frontend assets from the builder stage
COPY --from=frontend-builder /app/frontend/dist /app/frontend/dist

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port
EXPOSE 8000

# Run the application
# We use Daphne for ASGI (WebSocket) support
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "backend.asgi:application"]
