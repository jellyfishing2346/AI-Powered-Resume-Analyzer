"""
Main API v1 router that aggregates all endpoint routers.
"""

from fastapi import APIRouter

# Import individual routers
# from app.api.v1.endpoints import auth, resumes, jobs, matches

# Create main API router
api_router = APIRouter()

# Include sub-routers
# api_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
# api_router.include_router(resumes.router, prefix="/resumes", tags=["Resumes"])
# api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
# api_router.include_router(matches.router, prefix="/matches", tags=["Matches"])


# Placeholder endpoints for now
@api_router.get("/status")
async def api_status():
    """Check API status."""
    return {
        "status": "operational",
        "version": "2.0.0",
        "endpoints": {
            "resumes": "Coming soon",
            "jobs": "Coming soon",
            "matches": "Coming soon",
        },
    }
