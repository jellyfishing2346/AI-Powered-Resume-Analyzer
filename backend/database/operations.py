"""Database operations placeholder.

Provide simple in-memory operations for quick development and tests.
"""
from .models import ResumeRecord
from datetime import datetime
from typing import List

_storage: List[ResumeRecord] = []
_next_id = 1

def save_resume(filename: str, text_excerpt: str):
    global _next_id
    rec = ResumeRecord(id=_next_id, filename=filename, uploaded_at=datetime.utcnow(), text_excerpt=text_excerpt)
    _storage.append(rec)
    _next_id += 1
    return rec

def list_resumes():
    return list(_storage)

__all__ = ["save_resume", "list_resumes"]
