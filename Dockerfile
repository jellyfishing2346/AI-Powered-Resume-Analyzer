# Simplified Dockerfile for Railway deployment
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app files
COPY main.py .
COPY database.py .
COPY database_production.py .

# Download only the small spacy model
RUN python -m spacy download en_core_web_sm

# Expose port
EXPOSE 8001

# Simple health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8001}/ || exit 1

# Start command
CMD gunicorn main:app --host 0.0.0.0 --port ${PORT:-8001} --worker-class uvicorn.workers.UvicornWorker --workers 1 --timeout 120
