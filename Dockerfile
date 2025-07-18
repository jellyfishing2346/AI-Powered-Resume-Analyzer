FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Copy all necessary files
COPY main.py .
COPY database.py* ./
COPY requirements.txt .

# Install all dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8001}/ || exit 1

CMD gunicorn main:app --bind 0.0.0.0:${PORT:-8001} --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 120