"""File processing helpers for PDF/DOCX/TXT extraction.

These helpers proxy to the existing extraction logic inside `main.py`.
"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import main as legacy_main  # noqa: E402

def extract_text_from_uploadfile(upload_file):
    return legacy_main.extract_text(upload_file)

__all__ = ["extract_text_from_uploadfile"]
