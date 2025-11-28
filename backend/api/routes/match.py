"""Match endpoints (placeholder)."""
from fastapi import APIRouter

router = APIRouter(prefix="/match", tags=["Job Matching"])

@router.get("/ping")
def ping():
    return {"status": "ok", "route": "match"}
