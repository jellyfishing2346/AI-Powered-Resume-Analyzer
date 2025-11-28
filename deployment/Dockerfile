FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck and any other necessary apt packages
RUN apt-get update && \
    apt-get install -y curl git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy application files
COPY main.py ./
COPY requirements.txt ./
COPY backend/data/skills.txt ./skills.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model and NLTK data
RUN python -m spacy download en_core_web_sm
RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -c "import nltk; nltk.download('punkt')"

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8001}/ || exit 1

CMD gunicorn main:app --bind 0.0.0.0:${PORT:-8001} --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 300
