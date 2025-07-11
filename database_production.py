"""
Production database configuration for deployment
Supports both SQLite (development) and PostgreSQL (production)
"""

import os
import sqlite3
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Check if we're in production (Railway/Render provide DATABASE_URL)
DATABASE_URL = os.getenv('DATABASE_URL')
USE_POSTGRESQL = DATABASE_URL is not None

if USE_POSTGRESQL:
    try:
        import psycopg2
        import psycopg2.extras
        logger.info("PostgreSQL support enabled")
    except ImportError:
        logger.warning("psycopg2 not installed. Falling back to SQLite.")
        USE_POSTGRESQL = False

class ProductionDatabaseManager:
    def __init__(self):
        self.use_postgresql = USE_POSTGRESQL
        if self.use_postgresql:
            self.database_url = DATABASE_URL
            logger.info("Using PostgreSQL database")
        else:
            self.db_path = "resume_analyzer.db"
            logger.info("Using SQLite database")
        
        self.init_database()
    
    def get_connection(self):
        """Get database connection based on environment."""
        if self.use_postgresql:
            return psycopg2.connect(self.database_url)
        else:
            return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Initialize database with appropriate SQL for the database type."""
        if self.use_postgresql:
            self._init_postgresql()
        else:
            self._init_sqlite()
    
    def _init_postgresql(self):
        """Initialize PostgreSQL database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create analyses table (PostgreSQL syntax)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analyses (
                        id SERIAL PRIMARY KEY,
                        filename VARCHAR(255) NOT NULL,
                        job_description TEXT,
                        word_count INTEGER,
                        entities JSONB,
                        skills JSONB,
                        skill_count INTEGER,
                        match_score REAL,
                        file_size INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create rankings table (PostgreSQL syntax)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rankings (
                        id SERIAL PRIMARY KEY,
                        job_description TEXT NOT NULL,
                        total_candidates INTEGER,
                        ranked_results JSONB,
                        top_candidate VARCHAR(255),
                        top_score REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("PostgreSQL database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing PostgreSQL database: {e}")
            raise
    
    def _init_sqlite(self):
        """Initialize SQLite database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Create analyses table (SQLite syntax)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analyses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        job_description TEXT,
                        word_count INTEGER,
                        entities TEXT,
                        skills TEXT,
                        skill_count INTEGER,
                        match_score REAL,
                        file_size INTEGER,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create rankings table (SQLite syntax)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rankings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_description TEXT NOT NULL,
                        total_candidates INTEGER,
                        ranked_results TEXT,
                        top_candidate TEXT,
                        top_score REAL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("SQLite database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing SQLite database: {e}")
            raise
    
    def save_analysis(self, filename: str, job_description: str, analysis_result: dict) -> int:
        """Save analysis result to database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.use_postgresql:
                    # PostgreSQL with JSONB
                    cursor.execute("""
                        INSERT INTO analyses 
                        (filename, job_description, word_count, entities, skills, skill_count, match_score, file_size)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        filename,
                        job_description,
                        analysis_result.get('word_count', 0),
                        psycopg2.extras.Json(analysis_result.get('entities', [])),
                        psycopg2.extras.Json(analysis_result.get('skills', [])),
                        analysis_result.get('skill_count', 0),
                        analysis_result.get('match_score', 0.0),
                        analysis_result.get('file_size', 0)
                    ))
                    analysis_id = cursor.fetchone()[0]
                else:
                    # SQLite with JSON strings
                    import json
                    cursor.execute("""
                        INSERT INTO analyses 
                        (filename, job_description, word_count, entities, skills, skill_count, match_score, file_size)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        filename,
                        job_description,
                        analysis_result.get('word_count', 0),
                        json.dumps(analysis_result.get('entities', [])),
                        json.dumps(analysis_result.get('skills', [])),
                        analysis_result.get('skill_count', 0),
                        analysis_result.get('match_score', 0.0),
                        analysis_result.get('file_size', 0)
                    ))
                    analysis_id = cursor.lastrowid
                
                conn.commit()
                logger.info(f"Analysis saved with ID: {analysis_id}")
                return analysis_id
                
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            raise
    
    def save_ranking(self, job_description: str, ranking_result: dict) -> int:
        """Save ranking result to database."""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                if self.use_postgresql:
                    cursor.execute("""
                        INSERT INTO rankings 
                        (job_description, total_candidates, ranked_results, top_candidate, top_score)
                        VALUES (%s, %s, %s, %s, %s)
                        RETURNING id
                    """, (
                        job_description,
                        ranking_result.get('total_candidates', 0),
                        psycopg2.extras.Json(ranking_result.get('ranked_candidates', [])),
                        ranking_result.get('metadata', {}).get('top_candidate'),
                        ranking_result.get('metadata', {}).get('top_score', 0.0)
                    ))
                    ranking_id = cursor.fetchone()[0]
                else:
                    import json
                    cursor.execute("""
                        INSERT INTO rankings 
                        (job_description, total_candidates, ranked_results, top_candidate, top_score)
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        job_description,
                        ranking_result.get('total_candidates', 0),
                        json.dumps(ranking_result.get('ranked_candidates', [])),
                        ranking_result.get('metadata', {}).get('top_candidate'),
                        ranking_result.get('metadata', {}).get('top_score', 0.0)
                    ))
                    ranking_id = cursor.lastrowid
                
                conn.commit()
                logger.info(f"Ranking saved with ID: {ranking_id}")
                return ranking_id
                
        except Exception as e:
            logger.error(f"Error saving ranking: {e}")
            raise

# Create global instance
production_db_manager = ProductionDatabaseManager()

# For backward compatibility, alias the original db_manager
db_manager = production_db_manager
