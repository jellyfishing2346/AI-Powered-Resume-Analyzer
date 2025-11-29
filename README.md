# 🚀 AI Resume Analyzer 2.0

**Modern, AI-powered resume analysis and job matching system built with cutting-edge technologies.**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14+-black.svg)](https://nextjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5+-blue.svg)](https://www.typescriptlang.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE.txt)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Quick Start](#quick-start)
- [Architecture](#architecture)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## ✨ Features

### 🤖 AI-Powered Analysis
- **GPT-4 Integration** - Deep resume understanding and intelligent insights
- **Semantic Matching** - Vector-based similarity search using embeddings
- **Smart Skill Extraction** - Automatically identify technical and soft skills
- **ATS Optimization** - Score and improve resumes for Applicant Tracking Systems
- **Resume Enhancement** - AI-generated suggestions for improvement

### 📊 Advanced Matching
- **Multi-Factor Scoring** - Semantic similarity, skills, experience, and education
- **Candidate Ranking** - Intelligent ranking of multiple candidates
- **Gap Analysis** - Identify missing skills and experience
- **Detailed Reports** - Comprehensive match analysis with explanations

### 💾 Modern Architecture
- **Async Everything** - Full async/await support for maximum performance
- **Real-time Updates** - WebSocket support for live analysis
- **Background Processing** - Celery for long-running tasks
- **Vector Search** - PostgreSQL with pgvector for semantic search
- **Caching** - Redis for high-performance caching

### 🔐 Enterprise Ready
- **Authentication** - JWT + OAuth2 (Google, GitHub, LinkedIn)
- **Multi-tenant** - User isolation and data security
- **Rate Limiting** - Prevent abuse and ensure fair usage
- **Monitoring** - Structured logging and error tracking
- **Scalable** - Horizontal scaling with Docker and Kubernetes

---

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI 0.109+ (Async Python web framework)
- **AI/ML**: 
  - LangChain (LLM orchestration)
  - OpenAI GPT-4 (Advanced analysis)
  - Anthropic Claude (Alternative LLM)
  - sentence-transformers (Embeddings)
  - spaCy (NLP and NER)
  - ChromaDB (Vector database)
- **Database**: PostgreSQL 15+ with pgvector extension
- **Cache/Queue**: Redis + Celery
- **ORM**: SQLAlchemy 2.0 (Async)
- **Migrations**: Alembic

### Frontend (Coming Soon)
- **Framework**: Next.js 14+ (React with App Router)
- **Language**: TypeScript 5+
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: Zustand + TanStack Query
- **Forms**: React Hook Form + Zod
- **Real-time**: WebSockets / SSE

### DevOps
- **Containerization**: Docker + Docker Compose
- **Testing**: pytest, pytest-asyncio, Playwright
- **Code Quality**: Ruff, Black, mypy
- **CI/CD**: GitHub Actions
- **Monitoring**: Structlog, Sentry

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 15+ with pgvector extension
- Redis 7+
- Docker & Docker Compose (recommended)
- OpenAI API Key (required for AI features)

### Option 1: Docker Compose (Recommended)

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/AI-Powered-Resume-Analyzer.git
cd AI-Powered-Resume-Analyzer
```

2. **Configure environment**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your OpenAI API key
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Access the application**
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/api/v1/docs
- Celery Flower: http://localhost:5555
- Frontend (coming soon): http://localhost:3000

### Option 2: Local Development

#### Backend Setup

1. **Install Poetry** (Python dependency manager)
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. **Install dependencies**
```bash
cd backend
poetry install
```

3. **Download spaCy model**
```bash
poetry run python -m spacy download en_core_web_lg
```

4. **Set up environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Start PostgreSQL and Redis** (via Docker)
```bash
docker-compose up -d postgres redis
```

6. **Run database migrations**
```bash
poetry run alembic upgrade head
```

7. **Start the backend server**
```bash
poetry run uvicorn app.main:app --reload
```

8. **Start Celery worker** (in a new terminal)
```bash
poetry run celery -A app.tasks.celery_app worker --loglevel=info
```

9. **Access the API**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/api/v1/docs
- ReDoc: http://localhost:8000/api/v1/redoc

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         Frontend (Next.js)                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Dashboard  │  │    Upload    │  │   Matching   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬────────────────────────────────┘
                             │ HTTP / WebSocket
┌────────────────────────────┴────────────────────────────────┐
│                    Backend API (FastAPI)                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │   Auth   │  │ Resumes  │  │   Jobs   │  │ Matches  │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘   │
└───┬────────────────┬────────────────┬─────────────────┬────┘
    │                │                │                 │
┌───▼──────────┐ ┌──▼───────────┐ ┌──▼──────────┐ ┌───▼─────────┐
│  PostgreSQL  │ │     Redis    │ │   Celery    │ │  AI Services│
│  (pgvector)  │ │   (Cache)    │ │  (Tasks)    │ │  (GPT-4)    │
└──────────────┘ └──────────────┘ └─────────────┘ └─────────────┘
```

### Key Components

- **FastAPI Backend**: Async REST API with automatic OpenAPI documentation
- **PostgreSQL**: Primary database with pgvector for semantic search
- **Redis**: Caching, rate limiting, and Celery message broker
- **Celery**: Async task queue for resume processing
- **AI Services**: LangChain + OpenAI/Claude for intelligent analysis
- **ChromaDB**: Vector store for embeddings

---

## 📚 API Documentation

### Authentication

```bash
# Register a new user
POST /api/v1/auth/register
{
  "email": "user@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}

# Login
POST /api/v1/auth/login
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### Resume Management

```bash
# Upload a resume
POST /api/v1/resumes/upload
Content-Type: multipart/form-data
file: resume.pdf

# Get resume analysis
GET /api/v1/resumes/{resume_id}

# List user's resumes
GET /api/v1/resumes
```

### Job Matching

```bash
# Create a job description
POST /api/v1/jobs
{
  "title": "Senior Python Developer",
  "description": "We are looking for...",
  "required_skills": ["Python", "FastAPI", "PostgreSQL"]
}

# Match resumes to a job
POST /api/v1/matches/job/{job_id}
{
  "resume_ids": [1, 2, 3]
}

# Get match results
GET /api/v1/matches/{match_id}
```

**Full API documentation available at**: http://localhost:8000/api/v1/docs

---

## 💻 Development

### Project Structure

```
AI-Powered-Resume-Analyzer/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API endpoints
│   │   ├── core/            # Core utilities
│   │   ├── db/              # Database config
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── tasks/           # Celery tasks
│   │   ├── config.py        # Configuration
│   │   └── main.py          # FastAPI app
│   ├── tests/               # Tests
│   ├── alembic/             # Database migrations
│   ├── pyproject.toml       # Dependencies
│   └── Dockerfile
├── frontend/                # Next.js frontend (coming soon)
├── docker-compose.yml       # Docker orchestration
└── README.md
```

### Running Tests

```bash
cd backend

# Run all tests with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_resumes.py

# Run with verbose output
poetry run pytest -vv
```

### Code Quality

```bash
# Format code
poetry run black app tests

# Lint code
poetry run ruff check app tests

# Type checking
poetry run mypy app

# Run all quality checks
poetry run pre-commit run --all-files
```

### Database Migrations

```bash
# Create a new migration
poetry run alembic revision --autogenerate -m "Add new field"

# Apply migrations
poetry run alembic upgrade head

# Rollback one migration
poetry run alembic downgrade -1

# Check current version
poetry run alembic current
```

---

## 🚢 Deployment

### Production Checklist

- [ ] Set strong `SECRET_KEY` in environment
- [ ] Configure production database (PostgreSQL)
- [ ] Set up Redis (managed service or cluster)
- [ ] Configure CORS origins to your frontend domain
- [ ] Add OpenAI API key
- [ ] Enable HTTPS
- [ ] Set up monitoring (Sentry)
- [ ] Configure backups
- [ ] Set up CI/CD pipeline

### Environment Variables (Production)

```bash
# Application
ENVIRONMENT=production
DEBUG=false

# Security
SECRET_KEY=<generate-strong-random-key>

# Database
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname

# Redis
REDIS_URL=redis://:<password>@host:6379/0

# AI Services
OPENAI_API_KEY=sk-...

# Monitoring
SENTRY_DSN=https://...
```

### Docker Production Deployment

```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Start services
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f backend

# Stop services
docker-compose -f docker-compose.prod.yml down
```

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guide
- Add type hints to all functions
- Update documentation as needed
- Keep commits atomic and well-described

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE.txt](LICENSE.txt) file for details.

---

## 🙏 Acknowledgments

- FastAPI for the amazing async framework
- OpenAI for GPT-4 capabilities
- LangChain for LLM orchestration
- The open-source community

---

## 📧 Contact

For questions or support, please open an issue on GitHub.

**Built with ❤️ using modern technologies**
