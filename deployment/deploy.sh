#!/bin/bash

# AI-Powered Resume Analyzer Deployment Script (moved into deployment/)
# This script sets up and deploys the resume analyzer in production mode

set -e  # Exit on any error

echo "🚀 Starting AI-Powered Resume Analyzer Deployment..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if we're in the right directory
if [ ! -f "backend/api/main.py" ]; then
    print_error "backend/api/main.py not found. Please run this script from the project root directory."
    exit 1
fi

# Check Python version
print_status "Checking Python version..."
python3_version=$(python3 --version 2>&1 | cut -d' ' -f2)
print_success "Python $python3_version detected"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
    print_success "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt
if [ -f "requirements-optional.txt" ]; then
    pip install -r requirements-optional.txt
fi

# Install additional production packages
print_status "Installing additional production packages..."
pip install reportlab openpyxl gunicorn

# Download spaCy models
print_status "Downloading spaCy models..."
python -m spacy download en_core_web_sm 2>/dev/null || print_warning "en_core_web_sm already installed"
python -m spacy download en_core_web_lg 2>/dev/null || print_warning "en_core_web_lg already installed"

# Initialize database
print_status "Initializing database..."
python3 -c "from backend.database.operations import db_manager; db_manager.init_database(); print('Database initialized successfully')"

# Kill any existing processes
print_status "Stopping any existing servers..."
pkill -f "backend/api/main.py" 2>/dev/null || true
pkill -f "uvicorn.*backend.api.main" 2>/dev/null || true

# Wait a moment for processes to stop
sleep 2

# Start the API server
print_status "Starting API server on port 8001..."
nohup uvicorn backend.api.main:app --host 0.0.0.0 --port 8001 > api_server.log 2>&1 &
API_PID=$!

# Wait for server to start
print_status "Waiting for API server to start..."
for i in {1..30}; do
    if curl -s http://localhost:8001/health > /dev/null 2>&1; then
        print_success "API server is running (PID: $API_PID)"
        break
    fi
    if [ $i -eq 30 ]; then
        print_error "API server failed to start within 30 seconds"
        cat api_server.log
        exit 1
    fi
    sleep 1
done

# Test API endpoints
print_status "Testing API endpoints..."
if curl -s http://localhost:8001/health | grep -q "healthy"; then
    print_success "Health endpoint working"
else
    print_error "Health endpoint failed"
    exit 1
fi

# Install Node.js dependencies for frontend
if [ -d "frontend" ]; then
    print_status "Setting up React frontend..."
    cd frontend
    
    # Check if npm is available
    if command -v npm &> /dev/null; then
        npm install
        print_status "Starting React development server..."
        nohup npm start > ../frontend.log 2>&1 &
        FRONTEND_PID=$!
        cd ..
        
        # Wait for frontend to start
        print_status "Waiting for frontend to start..."
        for i in {1..30}; do
            if curl -s http://localhost:3000 > /dev/null 2>&1; then
                print_success "Frontend is running (PID: $FRONTEND_PID)"
                break
            fi
            if [ $i -eq 30 ]; then
                print_warning "Frontend failed to start within 30 seconds"
                print_warning "You can manually start it with: cd frontend && npm start"
            fi
            sleep 1
        done
    else
        cd ..
        print_warning "npm not found. Frontend will not be started automatically."
        print_warning "Please install Node.js and run: cd frontend && npm install && npm start"
    fi
fi

# Create a process management script
print_status "Creating process management scripts..."

cat > stop_servers.sh << 'EOF'
#!/bin/bash
echo "Stopping AI-Powered Resume Analyzer servers..."
pkill -f "backend/api/main.py" 2>/dev/null && echo "API server stopped"
pkill -f "npm start" 2>/dev/null && echo "Frontend server stopped"
pkill -f "react-scripts start" 2>/dev/null
echo "All servers stopped."
EOF

cat > start_servers.sh << 'EOF'
#!/bin/bash
echo "Starting AI-Powered Resume Analyzer servers..."
source venv/bin/activate
nohup uvicorn backend.api.main:app --host 0.0.0.0 --port 8001 > api_server.log 2>&1 &
echo "API server starting... (check api_server.log for details)"
if [ -d "frontend" ] && command -v npm &> /dev/null; then
    cd frontend
    nohup npm start > ../frontend.log 2>&1 &
    cd ..
    echo "Frontend server starting... (check frontend.log for details)"
fi
echo "Servers started. Use ./stop_servers.sh to stop them."
EOF

cat > check_status.sh << 'EOF'
#!/bin/bash
echo "=== AI-Powered Resume Analyzer Status ==="
echo ""
echo "🔍 Checking API Server (port 8001):"
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "  ✅ API server is running"
    curl -s http://localhost:8001/ | python3 -m json.tool 2>/dev/null || echo "  📊 API response received"
else
    echo "  ❌ API server is not responding"
fi

echo ""
echo "🌐 Checking Frontend (port 3000):"
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo "  ✅ Frontend is running"
else
    echo "  ❌ Frontend is not responding"
fi

echo ""
echo "📊 Process Information:"
ps aux | grep -E "(backend/api/main|npm start|react-scripts)" | grep -v grep | while read line; do
    echo "  $line"
done
EOF

chmod +x stop_servers.sh start_servers.sh check_status.sh

print_success "Management scripts created:"
print_success "  - ./start_servers.sh  : Start both servers"
print_success "  - ./stop_servers.sh   : Stop both servers"
print_success "  - ./check_status.sh   : Check server status"

# Final status check
print_status "Final deployment status:"
./check_status.sh

print_success "🎉 Deployment completed successfully!"
echo ""
echo "📖 Access the application:"
echo "  • API Documentation: http://localhost:8001/docs"
echo "  • Frontend UI: http://localhost:3000"
echo "  • API Health: http://localhost:8001/health"
echo ""
echo "📝 Log files:"
echo "  • API Server: api_server.log"
echo "  • Frontend: frontend.log"
echo ""
echo "🔧 Management commands:"
echo "  • Check status: ./check_status.sh"
echo "  • Stop servers: ./stop_servers.sh"
echo "  • Restart servers: ./stop_servers.sh && ./start_servers.sh"

# Save deployment info
cat > DEPLOYMENT_INFO.md << EOF
# AI-Powered Resume Analyzer - Deployment Information

## Deployment Date
$(date)

## Services
- **API Server**: http://localhost:8001
  - Documentation: http://localhost:8001/docs
  - Health Check: http://localhost:8001/health
- **Frontend**: http://localhost:3000

## Features Enabled
- ✅ Resume Analysis (PDF, DOCX, TXT)
- ✅ Multi-candidate Ranking
- ✅ Database Integration (SQLite)
- ✅ Skill Extraction (184+ skills)
- ✅ Named Entity Recognition
- ✅ Semantic Similarity Matching
- ✅ Export Capabilities (PDF, Excel)
- ✅ Modern React UI

## Management Commands
```bash
# Check server status
./check_status.sh

# Stop all servers
./stop_servers.sh

# Start all servers
./start_servers.sh

# View API logs
tail -f api_server.log

# View frontend logs
tail -f frontend.log
```

## API Endpoints
- POST /analyze - Analyze single resume
- POST /rank - Rank multiple candidates
- GET /health - Health check
- GET / - API information

## Dependencies
- Python 3.x with spaCy, FastAPI, sentence-transformers
- Node.js with React (for frontend)
- SQLite database

## Files
- Main API: backend/api/main.py
- Database: backend/database/operations.py
- Frontend: frontend/
- Skills DB: backend/data/skills.txt
- Docker: deployment/Dockerfile, deployment/docker-compose.yml
EOF

print_success "Deployment information saved to DEPLOYMENT_INFO.md"
