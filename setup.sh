#!/bin/bash

# AI Resume Analyzer - Setup Script
# This script helps set up the development environment

set -e

echo "🚀 AI Resume Analyzer - Setup Script"
echo "======================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Visit: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker and Docker Compose are installed"
echo ""

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env file from template..."
    cp backend/.env.example backend/.env
    echo "✅ Created backend/.env"
    echo "⚠️  IMPORTANT: Edit backend/.env and add your OpenAI API key!"
    echo ""
else
    echo "✅ backend/.env already exists"
    echo ""
fi

# Create required directories
echo "📁 Creating required directories..."
mkdir -p backend/data/uploads
mkdir -p backend/data/temp
mkdir -p backend/data/chroma
echo "✅ Directories created"
echo ""

# Ask user if they want to start with Docker Compose
read -p "🐳 Do you want to start the services with Docker Compose? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🐳 Starting services with Docker Compose..."
    docker-compose up -d
    echo ""
    echo "✅ Services started successfully!"
    echo ""
    echo "📍 Access points:"
    echo "   - Backend API: http://localhost:8000"
    echo "   - API Docs: http://localhost:8000/api/v1/docs"
    echo "   - Celery Flower: http://localhost:5555"
    echo "   - Frontend: http://localhost:3000 (coming soon)"
    echo ""
    echo "📊 View logs:"
    echo "   docker-compose logs -f backend"
    echo ""
    echo "🛑 Stop services:"
    echo "   docker-compose down"
    echo ""
else
    echo ""
    echo "📝 Manual setup instructions:"
    echo ""
    echo "1. Install Poetry (if not installed):"
    echo "   curl -sSL https://install.python-poetry.org | python3 -"
    echo ""
    echo "2. Install backend dependencies:"
    echo "   cd backend && poetry install"
    echo ""
    echo "3. Download spaCy model:"
    echo "   poetry run python -m spacy download en_core_web_lg"
    echo ""
    echo "4. Start PostgreSQL and Redis:"
    echo "   docker-compose up -d postgres redis"
    echo ""
    echo "5. Run database migrations:"
    echo "   poetry run alembic upgrade head"
    echo ""
    echo "6. Start the backend server:"
    echo "   poetry run uvicorn app.main:app --reload"
    echo ""
    echo "7. Start Celery worker (in another terminal):"
    echo "   poetry run celery -A app.tasks.celery_app worker --loglevel=info"
    echo ""
fi

echo "✨ Setup complete! Happy coding! ✨"
