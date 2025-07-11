#!/usr/bin/env python3
"""
Test script for the AI-Powered Resume Analyzer API
Tests basic functionality without optional dependencies that might cause issues.
"""

import sys
import os
sys.path.insert(0, '.')

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import spacy
from sentence_transformers import SentenceTransformer, util as st_util
from rapidfuzz import process, fuzz
import tempfile
import logging
from typing import List, Dict, Set, Optional
from database import db_manager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for optional dependencies
try:
    import pdfplumber
    PDF_SUPPORT = True
    logger.info("pdfplumber available - PDF support enabled")
except ImportError:
    pdfplumber = None
    PDF_SUPPORT = False
    logger.warning("pdfplumber not installed. PDF support disabled.")

try:
    import docx
    DOCX_SUPPORT = True
    logger.info("python-docx available - DOCX support enabled")
except ImportError:
    docx = None
    DOCX_SUPPORT = False
    logger.warning("python-docx not installed. DOCX support disabled.")

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Resume Analyzer (Test)",
    description="A test version of the resume analyzer API with core functionality.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize models
try:
    nlp = spacy.load("en_core_web_lg")
    logger.info("Loaded spaCy model: en_core_web_lg")
except OSError:
    try:
        nlp = spacy.load("en_core_web_sm")
        logger.info("Loaded spaCy model: en_core_web_sm")
    except OSError:
        logger.error("No spaCy model found. Please install with: python -m spacy download en_core_web_sm")
        raise

# Use a transformer model for better semantic similarity
st_model = SentenceTransformer('all-MiniLM-L6-v2')
logger.info("Loaded SentenceTransformer model: all-MiniLM-L6-v2")

# Load skills from skills.txt
def load_skills(filepath: str = "skills.txt") -> set:
    try:
        with open(filepath, "r") as f:
            skills = set(line.strip().lower() for line in f if line.strip())
            logger.info(f"Loaded {len(skills)} skills from {filepath}")
            return skills
    except Exception as e:
        logger.warning(f"Could not load skills from {filepath}: {e}")
        return set()

COMMON_SKILLS = load_skills()

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file using pdfplumber."""
    if not PDF_SUPPORT:
        raise HTTPException(status_code=400, detail="PDF support not available. Please install pdfplumber.")
    try:
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or '' for page in pdf.pages)
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract text from PDF file.")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file using python-docx."""
    if not DOCX_SUPPORT:
        raise HTTPException(status_code=400, detail="DOCX support not available. Please install python-docx.")
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        logger.error(f"Error extracting text from DOCX: {e}")
        raise HTTPException(status_code=400, detail="Failed to extract text from DOCX file.")

def extract_text(file: UploadFile) -> str:
    """Extract text from uploaded file based on file extension."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided.")
    
    suffix = os.path.splitext(file.filename)[1].lower()
    
    # Reset file pointer to beginning
    file.file.seek(0)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        content = file.file.read()
        if not content:
            raise HTTPException(status_code=400, detail="File is empty.")
        tmp.write(content)
        tmp_path = tmp.name
    
    try:
        if suffix == ".pdf":
            return extract_text_from_pdf(tmp_path)
        elif suffix in [".docx", ".doc"]:
            return extract_text_from_docx(tmp_path)
        elif suffix == ".txt":
            with open(tmp_path, "r", encoding="utf-8", errors="ignore") as f:
                return f.read()
        else:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file format: {suffix}. Supported formats: .pdf, .docx, .doc, .txt"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process the uploaded file.")
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

def extract_entities(text: str) -> List[Dict[str, str]]:
    """Extract named entities from text using spaCy NLP."""
    try:
        doc = nlp(text)
        entities = [{"label": ent.label_, "text": ent.text, "description": spacy.explain(ent.label_)} 
                   for ent in doc.ents]
        return entities
    except Exception as e:
        logger.error(f"Error extracting entities: {e}")
        return []

def extract_skills(text: str, skill_set: Set[str] = COMMON_SKILLS) -> Set[str]:
    """Extract skills from text using fuzzy matching and NER."""
    if not text.strip():
        return set()
        
    text_lower = text.lower()
    found = set()
    
    try:
        # Fuzzy match skills using rapidfuzz
        for skill in skill_set:
            # Accept matches with a fuzz ratio >= 85
            match_result = process.extractOne(skill, [text_lower], scorer=fuzz.partial_ratio)
            if match_result and match_result[1] >= 85:
                found.add(skill)
        
        return found
        
    except Exception as e:
        logger.error(f"Error extracting skills: {e}")
        return set()

def calculate_match_score(text1: str, text2: str) -> float:
    """Calculate semantic similarity between two texts using sentence transformers."""
    try:
        embeddings = st_model.encode([text1, text2])
        similarity = st_util.cos_sim(embeddings[0], embeddings[1])
        return float(similarity.item())
    except Exception as e:
        logger.error(f"Error calculating match score: {e}")
        return 0.0

@app.get("/")
async def root():
    """Root endpoint providing API information."""
    return {
        "message": "AI-Powered Resume Analyzer API (Enhanced Version)",
        "version": "1.0.0",
        "status": "operational",
        "features": {
            "pdf_support": PDF_SUPPORT,
            "docx_support": DOCX_SUPPORT,
            "skills_loaded": len(COMMON_SKILLS),
            "models": {
                "spacy": nlp.meta.get("name", "unknown"),
                "sentence_transformer": "all-MiniLM-L6-v2"
            }
        }
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": "2024-01-01T00:00:00Z"}

@app.post("/analyze")
async def analyze_resume(
    file: UploadFile = File(...),
    job_description: str = Form("")
):
    """Analyze a resume file and optionally compare against a job description."""
    try:
        # Extract text from the uploaded file
        resume_text = extract_text(file)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="No text could be extracted from the file.")
        
        # Extract entities and skills
        entities = extract_entities(resume_text)
        skills = list(extract_skills(resume_text))
        
        # Calculate match score if job description provided
        match_score = 0.0
        if job_description.strip():
            match_score = calculate_match_score(resume_text, job_description)
        
        # Basic analysis
        word_count = len(resume_text.split())
        
        result = {
            "success": True,
            "filename": file.filename,
            "analysis": {
                "word_count": word_count,
                "entities": entities,
                "skills": skills,
                "skill_count": len(skills),
                "match_score": round(match_score, 3) if job_description.strip() else None
            },
            "metadata": {
                "processed_at": "2024-01-01T00:00:00Z",
                "file_size": len(resume_text),
                "supported_features": {
                    "entity_extraction": True,
                    "skill_matching": True,
                    "semantic_similarity": True
                }
            }
        }
        
        # Save to database
        try:
            analysis_data = {
                "filename": file.filename,
                "job_description": job_description,
                "analysis": result["analysis"],
                "resume_text": resume_text
            }
            analysis_id = db_manager.save_analysis(analysis_data)
            result["database_id"] = analysis_id
        except Exception as e:
            logger.warning(f"Failed to save analysis to database: {e}")
        
        return JSONResponse(content=result)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing resume: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis.")

@app.post("/rank")
async def rank_candidates(
    files: List[UploadFile] = File(...),
    job_description: str = Form("")
):
    """Rank multiple candidates based on resume analysis and job description matching."""
    try:
        if not files:
            raise HTTPException(status_code=400, detail="No files provided.")
        
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description is required for ranking.")
        
        candidates = []
        
        for file in files:
            try:
                # Extract text from the resume
                resume_text = extract_text(file)
                
                if not resume_text.strip():
                    logger.warning(f"No text extracted from {file.filename}")
                    continue
                
                # Perform analysis
                entities = extract_entities(resume_text)
                skills = list(extract_skills(resume_text))
                match_score = calculate_match_score(resume_text, job_description)
                word_count = len(resume_text.split())
                
                # Create candidate profile
                candidate = {
                    "filename": file.filename,
                    "match_score": round(match_score, 3),
                    "word_count": word_count,
                    "skills": skills,
                    "skill_count": len(skills),
                    "entities": entities,
                    "entity_count": len(entities),
                    "resume_preview": resume_text[:200] + "..." if len(resume_text) > 200 else resume_text,
                    "file_size": len(resume_text)
                }
                
                candidates.append(candidate)
                
            except Exception as e:
                logger.error(f"Error processing {file.filename}: {e}")
                # Continue with other files even if one fails
                continue
        
        if not candidates:
            raise HTTPException(status_code=400, detail="No valid resumes could be processed.")
        
        # Sort candidates by match score (highest first)
        ranked_candidates = sorted(candidates, key=lambda x: x["match_score"], reverse=True)
        
        # Add ranking position
        for i, candidate in enumerate(ranked_candidates):
            candidate["rank"] = i + 1
        
        result = {
            "success": True,
            "job_description": job_description,
            "total_candidates": len(ranked_candidates),
            "ranked_candidates": ranked_candidates,
            "metadata": {
                "processed_at": "2024-01-01T00:00:00Z",
                "ranking_criteria": "semantic_similarity_with_job_description",
                "top_candidate": ranked_candidates[0]["filename"] if ranked_candidates else None,
                "top_score": ranked_candidates[0]["match_score"] if ranked_candidates else None
            }
        }
        
        # Save to database
        try:
            ranking_id = db_manager.save_ranking(result)
            result["database_id"] = ranking_id
        except Exception as e:
            logger.warning(f"Failed to save ranking to database: {e}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ranking candidates: {e}")
        raise HTTPException(status_code=500, detail="Internal server error during candidate ranking.")

@app.post("/test")
async def test_components():
    """Test endpoint to verify all components are working."""
    try:
        # Test spaCy
        test_text = "John Smith is a Python developer with 5 years of experience in machine learning."
        entities = extract_entities(test_text)
        skills = list(extract_skills(test_text))
        
        # Test sentence transformer
        score = calculate_match_score("Python developer", "Software engineer")
        
        return {
            "status": "success",
            "tests": {
                "spacy_entities": len(entities),
                "skill_extraction": len(skills),
                "semantic_similarity": round(score, 3),
                "models_loaded": True
            },
            "sample_results": {
                "entities": entities[:3],  # First 3 entities
                "skills": skills[:5],      # First 5 skills
                "similarity_score": round(score, 3)
            }
        }
        
    except Exception as e:
        logger.error(f"Error in test endpoint: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AI-Powered Resume Analyzer API (Enhanced Version)...")
    print("📖 API Documentation will be available at: http://127.0.0.1:8001/docs")
    print("🔍 Alternative docs at: http://127.0.0.1:8001/redoc")
    uvicorn.run(app, host="127.0.0.1", port=8001, reload=False)
