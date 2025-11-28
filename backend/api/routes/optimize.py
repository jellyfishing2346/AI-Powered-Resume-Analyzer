"""Optimize endpoints (placeholder)."""
from fastapi import APIRouter

router = APIRouter(prefix="/optimize", tags=["Resume Optimization"])

@router.get("/ping")
def ping():
    return {"status": "ok", "route": "optimize"}
