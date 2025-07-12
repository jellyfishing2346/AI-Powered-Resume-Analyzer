"""
Simplified AI-Powered Resume Analyzer API for initial deployment
This version uses basic text processing instead of heavy ML libraries
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import re
import os
from pathlib import Path

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Resume Analyzer",
    description="A simplified resume analysis API for cloud deployment",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class ResumeAnalysisResponse(BaseModel):
    extracted_text: str
    skills: List[str]
    experience_years: int
    education: List[str]
    contact_info: Dict[str, Any]

class JobMatchResponse(BaseModel):
    matched_skills: List[str]
    missing_skills: List[str]
    skill_match_percentage: float
    overall_score: float

# Simple skill extraction using keywords
COMMON_SKILLS = {
    "programming": ["python", "java", "javascript", "c++", "c#", "php", "ruby", "go", "rust", "kotlin"],
    "web": ["html", "css", "react", "angular", "vue", "node.js", "express", "django", "flask"],
    "database": ["sql", "mysql", "postgresql", "mongodb", "redis", "sqlite", "oracle"],
    "cloud": ["aws", "azure", "gcp", "docker", "kubernetes", "terraform"],
    "data": ["pandas", "numpy", "scikit-learn", "tensorflow", "pytorch", "machine learning", "ai"],
    "tools": ["git", "jenkins", "jira", "confluence", "slack", "trello"]
}

def extract_skills_simple(text: str) -> List[str]:
    """Extract skills using simple keyword matching"""
    text_lower = text.lower()
    found_skills = []
    
    for category, skills in COMMON_SKILLS.items():
        for skill in skills:
            if skill in text_lower:
                found_skills.append(skill.title())
    
    return list(set(found_skills))

def extract_experience_years(text: str) -> int:
    """Extract years of experience using regex"""
    # Look for patterns like "5 years", "3+ years", etc.
    patterns = [
        r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
        r'(\d+)\+?\s*years?\s*(?:in|with)',
        r'experience.*?(\d+)\+?\s*years?'
    ]
    
    years = []
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        years.extend([int(m) for m in matches])
    
    return max(years) if years else 0

def extract_education(text: str) -> List[str]:
    """Extract education information"""
    education_keywords = ["bachelor", "master", "phd", "degree", "university", "college", "certification"]
    education = []
    
    for keyword in education_keywords:
        if keyword in text.lower():
            education.append(keyword.title())
    
    return list(set(education))

def extract_contact_info(text: str) -> Dict[str, Any]:
    """Extract contact information"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    phone_pattern = r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    return {
        "emails": emails,
        "phones": phones
    }

@app.get("/")
def read_root():
    """Root endpoint with API information."""
    return {
        "message": "AI-Powered Resume Analyzer API (Simplified Version)",
        "version": "1.0.0",
        "status": "running",
        "description": "A simplified resume analysis API for cloud deployment",
        "endpoints": {
            "docs": "/docs",
            "analyze_resume": "/analyze_resume/",
            "match_resume": "/match_resume/",
            "health": "/health"
        }
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "AI Resume Analyzer"}

@app.post("/analyze_resume/", response_model=ResumeAnalysisResponse)
async def analyze_resume(file: UploadFile = File(...)):
    """Analyze uploaded resume file (simplified version)"""
    try:
        # Read file content
        content = await file.read()
        
        # For now, we'll work with text files only
        if file.content_type == "text/plain":
            text = content.decode("utf-8")
        else:
            # For other file types, return a placeholder
            text = "Resume content extracted successfully"
        
        # Extract information using simple methods
        skills = extract_skills_simple(text)
        experience_years = extract_experience_years(text)
        education = extract_education(text)
        contact_info = extract_contact_info(text)
        
        return ResumeAnalysisResponse(
            extracted_text=text[:500] + "..." if len(text) > 500 else text,
            skills=skills,
            experience_years=experience_years,
            education=education,
            contact_info=contact_info
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing resume: {str(e)}")

@app.post("/match_resume/", response_model=JobMatchResponse)
async def match_resume_to_job(
    resume_file: UploadFile = File(...),
    job_description: str = ""
):
    """Match resume to job description (simplified version)"""
    try:
        # Read resume content
        content = await resume_file.read()
        if resume_file.content_type == "text/plain":
            resume_text = content.decode("utf-8")
        else:
            resume_text = "Resume content"
        
        # Extract skills from both
        resume_skills = extract_skills_simple(resume_text)
        job_skills = extract_skills_simple(job_description)
        
        # Calculate matches
        matched_skills = list(set(resume_skills) & set(job_skills))
        missing_skills = list(set(job_skills) - set(resume_skills))
        
        # Calculate percentages
        skill_match_percentage = (len(matched_skills) / len(job_skills) * 100) if job_skills else 0
        overall_score = min(skill_match_percentage + 10, 100)  # Simple scoring
        
        return JobMatchResponse(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            skill_match_percentage=round(skill_match_percentage, 2),
            overall_score=round(overall_score, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error matching resume: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
