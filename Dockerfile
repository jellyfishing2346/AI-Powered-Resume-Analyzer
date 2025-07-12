# Ultra-minimal Dockerfile for Render free tier
FROM python:3.11-slim

WORKDIR /app

# Install only curl for health checks
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy only the essential files
COPY main_simple.py main.py
COPY database.py* ./

# Install minimal Python packages (no ML libraries)
RUN pip install --no-cache-dir \
    fastapi==0.104.1 \
    uvicorn[standard]==0.24.0 \
    python-multipart==0.0.6 \
    pydantic==2.5.0 \
    python-dotenv==1.0.0 \
    gunicorn==21.2.0

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8001}/ || exit 1

# Start command
CMD gunicorn main:app --bind 0.0.0.0:${PORT:-8001} --workers 1 --timeout 120
