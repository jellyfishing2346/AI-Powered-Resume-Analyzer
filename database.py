"""
Database models and operations for the Resume Analyzer
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "resume_analyzer.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create analyses table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS analyses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        filename TEXT NOT NULL,
                        job_description TEXT,
                        match_score REAL,
                        word_count INTEGER,
                        skill_count INTEGER,
                        entity_count INTEGER,
                        skills TEXT,  -- JSON array
                        entities TEXT,  -- JSON array
                        resume_text TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create rankings table
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS rankings (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        job_description TEXT NOT NULL,
                        total_candidates INTEGER,
                        ranking_results TEXT,  -- JSON array of ranked candidates
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                # Create users table (for future user management)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Error initializing database: {e}")
            raise
    
    def save_analysis(self, analysis_data: Dict) -> int:
        """Save a single resume analysis to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO analyses (
                        filename, job_description, match_score, word_count, 
                        skill_count, entity_count, skills, entities, resume_text
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    analysis_data.get('filename'),
                    analysis_data.get('job_description', ''),
                    analysis_data.get('analysis', {}).get('match_score'),
                    analysis_data.get('analysis', {}).get('word_count'),
                    analysis_data.get('analysis', {}).get('skill_count'),
                    analysis_data.get('analysis', {}).get('entity_count'),
                    json.dumps(analysis_data.get('analysis', {}).get('skills', [])),
                    json.dumps(analysis_data.get('analysis', {}).get('entities', [])),
                    analysis_data.get('resume_text', '')
                ))
                
                analysis_id = cursor.lastrowid
                conn.commit()
                logger.info(f"Saved analysis with ID: {analysis_id}")
                return analysis_id
                
        except Exception as e:
            logger.error(f"Error saving analysis: {e}")
            raise
    
    def save_ranking(self, ranking_data: Dict) -> int:
        """Save a candidate ranking to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    INSERT INTO rankings (
                        job_description, total_candidates, ranking_results
                    ) VALUES (?, ?, ?)
                """, (
                    ranking_data.get('job_description'),
                    ranking_data.get('total_candidates'),
                    json.dumps(ranking_data.get('ranked_candidates', []))
                ))
                
                ranking_id = cursor.lastrowid
                conn.commit()
                logger.info(f"Saved ranking with ID: {ranking_id}")
                return ranking_id
                
        except Exception as e:
            logger.error(f"Error saving ranking: {e}")
            raise
    
    def get_recent_analyses(self, limit: int = 10) -> List[Dict]:
        """Get recent analyses from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, filename, job_description, match_score, word_count,
                           skill_count, entity_count, created_at
                    FROM analyses 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting recent analyses: {e}")
            return []
    
    def get_recent_rankings(self, limit: int = 10) -> List[Dict]:
        """Get recent rankings from the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id, job_description, total_candidates, created_at
                    FROM rankings 
                    ORDER BY created_at DESC 
                    LIMIT ?
                """, (limit,))
                
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                
                return [dict(zip(columns, row)) for row in rows]
                
        except Exception as e:
            logger.error(f"Error getting recent rankings: {e}")
            return []
    
    def get_analysis_by_id(self, analysis_id: int) -> Optional[Dict]:
        """Get a specific analysis by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM analyses WHERE id = ?
                """, (analysis_id,))
                
                row = cursor.fetchone()
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    result = dict(zip(columns, row))
                    # Parse JSON fields
                    result['skills'] = json.loads(result['skills']) if result['skills'] else []
                    result['entities'] = json.loads(result['entities']) if result['entities'] else []
                    return result
                
                return None
                
        except Exception as e:
            logger.error(f"Error getting analysis by ID: {e}")
            return None
    
    def get_ranking_by_id(self, ranking_id: int) -> Optional[Dict]:
        """Get a specific ranking by ID."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT * FROM rankings WHERE id = ?
                """, (ranking_id,))
                
                row = cursor.fetchone()
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    result = dict(zip(columns, row))
                    # Parse JSON field
                    result['ranking_results'] = json.loads(result['ranking_results']) if result['ranking_results'] else []
                    return result
                
                return None
                
        except Exception as e:
            logger.error(f"Error getting ranking by ID: {e}")
            return None
    
    def get_stats(self) -> Dict:
        """Get database statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Count analyses
                cursor.execute("SELECT COUNT(*) FROM analyses")
                total_analyses = cursor.fetchone()[0]
                
                # Count rankings
                cursor.execute("SELECT COUNT(*) FROM rankings")
                total_rankings = cursor.fetchone()[0]
                
                # Average match score
                cursor.execute("SELECT AVG(match_score) FROM analyses WHERE match_score IS NOT NULL")
                avg_match_score = cursor.fetchone()[0] or 0
                
                # Most common skills
                cursor.execute("SELECT skills FROM analyses WHERE skills IS NOT NULL")
                all_skills = []
                for row in cursor.fetchall():
                    if row[0]:
                        skills = json.loads(row[0])
                        all_skills.extend(skills)
                
                from collections import Counter
                top_skills = Counter(all_skills).most_common(10)
                
                return {
                    "total_analyses": total_analyses,
                    "total_rankings": total_rankings,
                    "average_match_score": round(avg_match_score, 3) if avg_match_score else 0,
                    "top_skills": top_skills
                }
                
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {
                "total_analyses": 0,
                "total_rankings": 0,
                "average_match_score": 0,
                "top_skills": []
            }

# Initialize database manager
db_manager = DatabaseManager()
