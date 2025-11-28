"""Analyze endpoints (placeholder).

These should be migrated from the legacy `main.py` into proper routers.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/analyze", tags=["Resume Analysis"])

@router.get("/ping")
def ping():
    return {"status": "ok", "route": "analyze"}
