FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install uv

# Copy project files
COPY pyproject.toml .

# Install dependencies
RUN uv sync

# Copy the rest of the code
COPY . .

# Set PATH for uv
ENV PATH="/root/.local/bin:$PATH"

# Default command (can be overridden)
CMD ["uv", "run", "python", "main.py"]
