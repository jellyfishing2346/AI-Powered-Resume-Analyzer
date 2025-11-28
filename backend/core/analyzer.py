"""Resume analysis engine (wrapper).

This module re-exports analysis functions from the legacy `main.py` so other
backend modules can import `backend.core.analyzer` rather than touching `main.py`.
"""
from . import (
    extract_skills,
    analyze_resume_vs_job,
    extract_summary,
    extract_entities,
    extract_education,
    extract_experience,
)

__all__ = [
    "extract_skills",
    "analyze_resume_vs_job",
    "extract_summary",
    "extract_entities",
    "extract_education",
    "extract_experience",
]
