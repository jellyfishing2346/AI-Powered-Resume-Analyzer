"""Compatibility shim for legacy import paths.

This module re-exports the `db_manager` and `DatabaseManager` from
`backend.database.operations` so older import paths continue to work during
migration.
"""

from backend.database.operations import DatabaseManager, db_manager  # re-export

__all__ = ["DatabaseManager", "db_manager"]
