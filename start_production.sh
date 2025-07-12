#!/bin/bash

# Start script for production deployment
echo "Starting AI-Powered Resume Analyzer..."
echo "PORT: ${PORT:-8001}"
echo "DATABASE_URL: ${DATABASE_URL:-'Not set'}"
echo "ENVIRONMENT: ${ENVIRONMENT:-'development'}"

# Start the application
exec gunicorn main:app \
    --host 0.0.0.0 \
    --port ${PORT:-8001} \
    --worker-class uvicorn.workers.UvicornWorker \
    --workers 1 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile - \
    --log-level info
