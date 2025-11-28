"""Compatibility FastAPI entry that re-uses existing top-level `main.py` app.

This file exposes `app` by importing the legacy `main.py` from the repo root.
It keeps the same FastAPI app object so existing deployments can point here.
"""
from pathlib import Path
import sys

# Ensure repo root is on sys.path so we can import the legacy main module
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    import main as legacy_main
except Exception as e:
    raise RuntimeError(f"Failed to import legacy main.py: {e}")

# Re-export the FastAPI app from the legacy module
app = getattr(legacy_main, "app", None)
if app is None:
    raise RuntimeError("Legacy main.py does not expose `app`. Please check main.py.")

__all__ = ["app"]
