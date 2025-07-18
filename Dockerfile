FROM python:3.11-slim

WORKDIR /app

# Install curl for healthcheck and any other necessary apt packages
# Also install git, which might be needed by some pip packages (e.g., pyresparser's dependencies)
# and build-essential for compiling some Python packages with C extensions
RUN apt-get update && \
    apt-get install -y curl git build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy all necessary files
COPY main.py .
COPY database.py* ./
COPY requirements.txt .
COPY skills.txt . 

# Install all dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# --- IMPORTANT: Download only the smaller spaCy model to save memory ---
# As main.py now explicitly loads 'en_core_web_sm'
RUN python -m spacy download en_core_web_sm

# --- IMPORTANT: Download NLTK data after pip install ---
# These are required for pyresparser (or any other NLTK usage) that relies on specific corpora.
RUN python -c "import nltk; nltk.download('stopwords')"
RUN python -c "import nltk; nltk.download('punkt')"

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8001}/ || exit 1

# Increased timeout to allow more time for model loading and application startup
CMD gunicorn main:app --bind 0.0.0.0:${PORT:-8001} --workers 1 --worker-class uvicorn.workers.UvicornWorker --timeout 300