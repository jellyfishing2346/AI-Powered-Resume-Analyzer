"""
Main FastAPI application entry point.
"""

from contextlib import asynccontextmanager

import structlog
from app.core.exceptions import add_exception_handlers
from app.core.logging import setup_logging
from app.db.session import close_db, create_db_and_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import ORJSONResponse

from app.config import settings

# Setup logging
setup_logging()
logger = structlog.get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("starting_application", environment=settings.ENVIRONMENT)

    # Initialize database
    await create_db_and_tables()
    logger.info("database_initialized")

    # Initialize AI services (lazy loading)
    if settings.ENABLE_AI_FEATURES:
        logger.info("ai_features_enabled")

    yield

    # Shutdown
    logger.info("shutting_down_application")
    await close_db()
    logger.info("application_shutdown_complete")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Modern AI-powered resume analysis and matching system",
    docs_url=f"{settings.API_PREFIX}/docs",
    redoc_url=f"{settings.API_PREFIX}/redoc",
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

# ========== Middleware ==========

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
)

# GZip compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add exception handlers
add_exception_handlers(app)

# ========== Routes ==========


# Health check endpoint (outside API prefix)
@app.get("/health")
async def health_check():
    """Health check endpoint for load balancers."""
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": f"{settings.API_PREFIX}/docs",
        "health": "/health",
    }


# Import and include API routers
from app.api.v1.router import api_router

app.include_router(api_router, prefix=settings.API_PREFIX)


# ========== Startup Event ==========

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD and settings.is_development,
        workers=settings.WORKERS,
        log_config=None,  # Use our custom logging
    )
