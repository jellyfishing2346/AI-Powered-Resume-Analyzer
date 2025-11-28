"""Text cleaning and utility helpers (placeholder).

Provide small helpers used by backend modules.
"""
import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    s = text.replace('\r', '\n')
    s = re.sub(r'\s+', ' ', s)
    return s.strip()

__all__ = ["clean_text"]
