#!/bin/bash

# AI-Powered Resume Analyzer Startup Script

echo "🚀 Starting AI-Powered Resume Analyzer..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip first."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip3 install --upgrade pip

# Install dependencies
echo "📚 Installing dependencies..."
pip3 install -r requirements.txt
pip3 install -r requirements-optional.txt

# Download spaCy models
echo "📥 Downloading spaCy models..."
python -m spacy download en_core_web_sm
python -m spacy download en_core_web_lg

# Start the server
echo "🌟 Starting FastAPI server..."
echo "📖 API Documentation will be available at: http://127.0.0.1:8000/docs"
echo "🔄 Press Ctrl+C to stop the server"
echo ""

uvicorn main:app --reload --host 127.0.0.1 --port 8000
