"""Database models placeholder.

This file provides lightweight SQLAlchemy model placeholders for the
reorganized layout. Replace or extend with your actual models as needed.
"""
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ResumeRecord:
    id: int
    filename: str
    uploaded_at: datetime
    text_excerpt: str


__all__ = ["ResumeRecord"]
