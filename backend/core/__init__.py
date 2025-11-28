"""Backend core package exposing analysis utilities.

This package provides thin wrappers around the existing logic in the repository's
`main.py` for compatibility while enabling a clearer project layout.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import main as legacy_main  # noqa: E402

extract_skills = getattr(legacy_main, "extract_skills")
analyze_resume_vs_job = getattr(legacy_main, "analyze_resume_vs_job")
extract_summary = getattr(legacy_main, "extract_summary")
extract_entities = getattr(legacy_main, "extract_entities")
extract_education = getattr(legacy_main, "extract_education")
extract_experience = getattr(legacy_main, "extract_experience")

__all__ = [
    "extract_skills",
    "analyze_resume_vs_job",
    "extract_summary",
    "extract_entities",
    "extract_education",
    "extract_experience",
]
