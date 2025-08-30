import os
import logging
import spacy
import nltk
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Set, Optional
import io
import tempfile
from rapidfuzz import process, fuzz

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Conditional Imports for Optional Libraries ---
try:
    import pdfplumber
except ImportError:
    pdfplumber = None
    logger.warning("pdfplumber not installed. PDF support disabled.")

try:
    import docx
except ImportError:
    docx = None
    logger.warning("python-docx not installed. DOCX support disabled.")

# --- Load spaCy models and NLTK data ---
try:
    nlp = spacy.load("en_core_web_sm")
    logger.info("Loaded spaCy model: en_core_web_sm")
except OSError as e:
    logger.error(f"Could not load spaCy model 'en_core_web_sm': {e}")
    raise RuntimeError("SpaCy model 'en_core_web_sm' not found. Ensure it's downloaded in Dockerfile.")

try:
    nltk.data.find('corpora/stopwords')
    logger.info("NLTK 'stopwords' corpus already downloaded.")
except nltk.downloader.DownloadError:
    logger.info("Downloading NLTK 'stopwords' corpus...")
    nltk.download('stopwords')
    logger.info("NLTK 'stopwords' corpus downloaded.")
except Exception as e:
    logger.error(f"Error checking/downloading NLTK stopwords: {e}")

try:
    nltk.data.find('tokenizers/punkt')
    logger.info("NLTK 'punkt' tokenizer already downloaded.")
except nltk.downloader.DownloadError:
    logger.info("Downloading NLTK 'punkt' tokenizer...")
    nltk.download('punkt')
    logger.info("NLTK 'punkt' tokenizer downloaded.")
except Exception as e:
    logger.error(f"Error checking/downloading NLTK punkt: {e}")

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Resume Analyzer",
    description="A high-performance API for automated resume analysis and candidate ranking using advanced NLP techniques.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Helper Functions ---

def load_skills(filepath: str = "skills.txt") -> set:
    """Loads common skills from a text file."""
    try:
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                return set(line.strip().lower() for line in f if line.strip())
        elif os.path.exists(os.path.join("/app", filepath)):
            with open(os.path.join("/app", filepath), "r") as f:
                return set(line.strip().lower() for line in f if line.strip())
        else:
            logger.warning(f"skills.txt not found at {filepath} or /app/{filepath}. Using empty skill set.")
            return set()
    except Exception as e:
        logger.error(f"Error loading skills from {filepath}: {e}")
        return set()

COMMON_SKILLS = load_skills()

def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file using pdfplumber."""
    if not pdfplumber:
        raise HTTPException(status_code=400, detail="PDF support not available. Please install pdfplumber.")
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(page.extract_text() or '' for page in pdf.pages)
            if not text.strip():
                raise HTTPException(status_code=400, detail="No extractable text found in PDF. Is it a scanned image?")
            return text
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to extract text from PDF file: {str(e)}")

def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file using python-docx."""
    if not docx:
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
        raise # Re-raise HTTPExceptions directly
    except Exception as e:
        logger.error(f"Error processing file {file.filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process the uploaded file: {str(e)}")
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
        logger.error(f"Error extracting entities: {e}", exc_info=True)
        return []

def extract_skills(text: str, skill_set: Set[str] = COMMON_SKILLS) -> Set[str]:
    """Extract skills from text using fuzzy matching and NER."""
    if not text.strip():
        return set()
        
    text_lower = text.lower()
    found = set()
    
    try:
        for skill in skill_set:
            match_result = process.extractOne(skill, [text_lower], scorer=fuzz.partial_ratio)
            if match_result and match_result[1] >= 85:
                found.add(skill)
        
        doc = nlp(text)
        for ent in doc.ents:
            if ent.text.lower() in skill_set:
                found.add(ent.text.lower())
                
    except Exception as e:
        logger.error(f"Error extracting skills: {e}", exc_info=True)
    
    return found

def extract_summary(text: str) -> str:
    """Extracts a simple summary (first few sentences) from the text."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return ' '.join(sentences[:3])

def extract_education(text: str) -> list:
    """Extracts education-related lines from the text."""
    degrees = ["bachelor", "master", "phd", "associate", "b.sc", "m.sc", "b.a", "m.a", "mba", "b.eng", "m.eng", "university", "college", "institute"]
    found = []
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["ORG", "EDU"] and any(deg in ent.text.lower() for deg in degrees):
            found.append(ent.text.strip())
    
    for line in text.splitlines():
        line_lower = line.lower()
        if any(deg in line_lower for deg in degrees) and any(term in line_lower for term in ["university", "college", "institute", "school"]):
            if line.strip() not in found:
                found.append(line.strip())
    return list(set(found))

def extract_experience(text: str) -> list:
    """Extracts experience-related lines from the text."""
    import re
    exp = []
    doc = nlp(text)
    
    for ent in doc.ents:
        if ent.label_ in ["ORG", "DATE", "GPE"]:
            line_match = re.search(r'.*' + re.escape(ent.text) + r'.*', text, re.IGNORECASE)
            if line_match and line_match.group(0).strip() not in exp:
                exp.append(line_match.group(0).strip())

    patterns = [
        r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b \d{4}\s*-\s*(?:present|\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b \d{4})',
        r'\d{4}\s*-\s*(?:present|\d{4})',
        r'\b(?:software engineer|data scientist|project manager|analyst|developer|engineer|manager|specialist)\b.*?\b(?:at|for)\b.*?\b(?:inc|llc|ltd|corp|company)\b',
        r'\b(?:[A-Z][a-z]+(?: [A-Z][a-z]+)*),\s*(?:[A-Z][a-z]+(?: [A-Z][a-z]+)*)\s*(?:\d{4}\s*-\s*(?:present|\d{4}))?'
    ]
    
    for line in text.splitlines():
        for pattern in patterns:
            if re.search(pattern, line, re.IGNORECASE):
                if line.strip() not in exp:
                    exp.append(line.strip())
                    break

    return list(set(exp))

def analyze_resume_vs_job(resume_text: str, job_text: str) -> Dict:
    """Analyze resume against job description and return matching metrics."""
    try:
        resume_skills = extract_skills(resume_text)
        job_skills = extract_skills(job_text)
        
        matched_skills = resume_skills & job_skills
        missing_skills = job_skills - resume_skills
        extra_skills = resume_skills - job_skills
        
        skill_match_percentage = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
        
        semantic_similarity = 0.0 
        
        overall_score = skill_match_percentage / 100 
        
        return {
            "matched_skills": list(matched_skills),
            "missing_skills": list(missing_skills),
            "extra_skills": list(extra_skills),
            "skill_match_percentage": round(skill_match_percentage, 2),
            "semantic_similarity": round(semantic_similarity, 4),
            "overall_score": round(overall_score, 4)
        }
    except Exception as e:
        logger.error(f"Error analyzing resume vs job: {e}", exc_info=True)
        return {
            "matched_skills": [],
            "missing_skills": [],
            "extra_skills": [],
            "skill_match_percentage": 0,
            "semantic_similarity": 0,
            "overall_score": 0
        }

# --- API Endpoints ---

@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "AI-Powered Resume Analyzer API",
        "version": "1.0.0",
        "description": "A high-performance API for automated resume analysis and candidate ranking using advanced NLP techniques.",
        "endpoints": {
            "docs": "/docs",
            "analyze_resume": "/analyze_resume/",
            "match_resume": "/match_resume/",
            "rank_candidates": "/rank_candidates/"
        }
    }

@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "message": "API is running normally"}

@app.post("/analyze_resume/", tags=["Resume Analysis"])
async def analyze_resume(file: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)")):
    """
    Analyze a single resume and extract key information.
    
    - **file**: Upload a resume file (PDF, DOCX, or TXT format)
    
    Returns extracted entities, skills, summary, education, experience, and more.
    """
    logger.info(f"Received file for analysis: {file.filename}")
    try:
        file.file.seek(0) 
        text = extract_text(file)
        
        logger.info(f"Extracted text length: {len(text)}")
        if len(text) < 100:
            logger.info(f"Extracted text preview: {text}")
        else:
            logger.info(f"Extracted text preview: {text[:100]}...")

        if not text.strip():
            logger.warning(f"No text content found in {file.filename} after extraction.")
            raise HTTPException(status_code=400, detail="No text content found in the uploaded file.")
        
        entities = extract_entities(text)
        skills = list(extract_skills(text))
        summary = extract_summary(text)
        education = extract_education(text)
        experience = extract_experience(text)

        logger.info(f"Entities extracted: {len(entities)}")
        logger.info(f"Skills extracted: {len(skills)}")
        logger.info(f"Summary extracted: {summary[:50]}...")
        logger.info(f"Education extracted: {education}")
        logger.info(f"Experience extracted: {experience}")
        
        result = {
            "filename": file.filename,
            "entities": entities,
            "skills": skills,
            "skills_count": len(skills),
            "summary": summary,
            "education": education,
            "experience": experience,
            "text_preview": text[:500] + "..." if len(text) > 500 else text,
            "text_length": len(text)
        }
        
        logger.info(f"Successfully analyzed resume: {file.filename}")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing resume {file.filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to analyze the resume: {str(e)}")

@app.post("/match_resume/", tags=["Resume Analysis"])
async def match_resume(
    resume: UploadFile = File(..., description="Resume file (PDF, DOCX, or TXT)"),
    job_description: str = Form(..., description="Job description text to match against")
):
    """
    Match a resume against a job description and get compatibility analysis.
    
    - **resume**: Upload a resume file (PDF, DOCX, or TXT format)
    - **job_description**: Job description text to analyze compatibility
    
    Returns matching analysis including skills overlap, similarity score, and detailed breakdown.
    """
    logger.info(f"Received resume '{resume.filename}' for matching against job description.")
    try:
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description cannot be empty.")
            
        resume_text = extract_text(resume)
        
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="No text content found in the uploaded resume.")
        
        analysis = analyze_resume_vs_job(resume_text, job_description)
        summary = extract_summary(resume_text)
        education = extract_education(resume_text)
        experience = extract_experience(resume_text)
        
        logger.info(f"Successfully matched resume '{resume.filename}' against job description.")
        return {
            "filename": resume.filename,
            "analysis": analysis,
            "candidate_info": {
                "summary": summary,
                "education": education,
                "experience": experience
            },
            "resume_preview": resume_text[:500] + "..." if len(resume_text) > 500 else resume_text
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error matching resume {resume.filename}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to match resume against job description: {str(e)}")

@app.post("/rank_candidates/", tags=["Candidate Ranking"])
async def rank_candidates(
    resumes: List[UploadFile] = File(..., description="Multiple resume files to rank"),
    job_description: str = Form(..., description="Job description to rank candidates against")
):
    """
    Rank multiple candidates based on their resumes and job description compatibility.
    
    - **resumes**: Upload multiple resume files (PDF, DOCX, or TXT format)
    - **job_description**: Job description text to rank candidates against
    
    Returns a ranked list of candidates with detailed analysis for each.
    """
    logger.info(f"Received {len(resumes)} resumes for ranking against job description.")
    try:
        if not job_description.strip():
            raise HTTPException(status_code=400, detail="Job description cannot be empty.")
            
        if not resumes:
            raise HTTPException(status_code=400, detail="At least one resume file must be provided.")
        
        job_text = job_description
        job_skills = extract_skills(job_text)
        results = []
        
        for file in resumes:
            try:
                file.file.seek(0)
                text = extract_text(file)
                
                if not text.strip():
                    logger.warning(f"Empty content in file: {file.filename}. Skipping.")
                    results.append({
                        "filename": file.filename,
                        "error": "No text content found in the uploaded file.",
                        "overall_score": 0
                    })
                    continue
                
                analysis = analyze_resume_vs_job(text, job_text)
                summary = extract_summary(text)
                education = extract_education(text)
                experience = extract_experience(text)
                
                results.append({
                    "filename": file.filename,
                    "overall_score": analysis["overall_score"],
                    "semantic_similarity": analysis["semantic_similarity"],
                    "skill_match_percentage": analysis["skill_match_percentage"],
                    "matched_skills": analysis["matched_skills"],
                    "missing_skills": analysis["missing_skills"],
                    "extra_skills": analysis["extra_skills"],
                    "candidate_info": {
                        "summary": summary,
                        "education": education,
                        "experience": experience
                    },
                    "preview": text[:200] + "..." if len(text) > 200 else text
                })
                
            except HTTPException as e:
                logger.error(f"HTTPException processing file {file.filename}: {e.detail}")
                results.append({
                    "filename": file.filename,
                    "error": e.detail,
                    "overall_score": 0
                })
                continue
            except Exception as e:
                logger.error(f"Unexpected error processing file {file.filename}: {e}", exc_info=True)
                results.append({
                    "filename": file.filename,
                    "error": str(e),
                    "overall_score": 0
                })
                continue
        
        if not results:
            raise HTTPException(status_code=400, detail="No valid resume content found in any of the uploaded files after processing.")
        
        ranked = sorted(results, key=lambda x: x["overall_score"], reverse=True)
        
        logger.info(f"Ranking process completed for {len(ranked)} candidates.")
        return {
            "job_description_preview": job_text[:200] + "..." if len(job_text) > 200 else job_text,
            "total_candidates": len(ranked),
            "job_required_skills": list(job_skills),
            "ranked_candidates": ranked
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error ranking candidates: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to rank candidates: {str(e)}")