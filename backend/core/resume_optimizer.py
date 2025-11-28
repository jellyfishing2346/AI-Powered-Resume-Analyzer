"""Resume optimization helpers (placeholder).

This file is a starting point for AI-driven resume customization features.
For now it provides a tiny helper that returns recommended keywords based on
job description skills.
"""
from .analyzer import extract_skills

def recommend_keywords_for_resume(job_description: str, top_n: int = 10):
    skills = extract_skills(job_description)
    # naive ranking: return up to top_n skills
    return list(skills)[:top_n]

__all__ = ["recommend_keywords_for_resume"]
