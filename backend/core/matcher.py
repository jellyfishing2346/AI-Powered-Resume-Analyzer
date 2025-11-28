"""Job-resume matching utilities (compatibility wrapper).

This module exposes `analyze_resume_vs_job` from the legacy code and provides
an alias `match_resume_to_job` for clarity.
"""
from .analyzer import analyze_resume_vs_job

def match_resume_to_job(resume_text: str, job_text: str):
    """Return the analysis/match dict for a resume vs a job description."""
    return analyze_resume_vs_job(resume_text, job_text)

__all__ = ["match_resume_to_job", "analyze_resume_vs_job"]
