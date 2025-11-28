"""Enhanced skills detection wrapper.

This module is intentionally small — it proxies to the robust extractor
implemented in the repo's root `main.py` for backward compatibility.
"""
from .analyzer import extract_skills

def extract_skills_set(text: str):
    return set(extract_skills(text))

__all__ = ["extract_skills_set", "extract_skills"]
