#!/usr/bin/env python3
"""Compatibility shim for the legacy script location.

The original `test_api_clean.py` was moved to `backend/api/main.py`. This
shim allows running the previous entrypoint name while delegating to the
new module. Running this file will start the FastAPI app using Uvicorn.
"""

import sys
import os

if __name__ == "__main__":
    # Ensure repo root is on path
    sys.path.insert(0, os.path.abspath("."))
    try:
        # Import the app from its new location and run with uvicorn
        from backend.api import main as api_main
        import uvicorn
        uvicorn.run(api_main.app, host="0.0.0.0", port=8001)
    except Exception as e:
        print("Failed to start API from backend/api/main.py:", e)
        raise


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

@app.get("/history/analyses")
async def get_recent_analyses(limit: int = 10):
    """Get recent analysis history."""
    try:
        analyses = db_manager.get_recent_analyses(limit)
        return {
            "success": True,
            "analyses": analyses,
            "count": len(analyses)
        }
    except Exception as e:
        logger.error(f"Error getting analyses: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving analysis history.")

@app.get("/history/rankings")
async def get_recent_rankings(limit: int = 10):
    """Get recent ranking history."""
    try:
        rankings = db_manager.get_recent_rankings(limit)
        return {
            "success": True,
            "rankings": rankings,
            "count": len(rankings)
        }
    except Exception as e:
        logger.error(f"Error getting rankings: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving ranking history.")

@app.get("/stats")
async def get_statistics():
    """Get database statistics and insights."""
    try:
        stats = db_manager.get_stats()
        return {
            "success": True,
            "statistics": stats
        }
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving statistics.")

@app.get("/analysis/{analysis_id}")
async def get_analysis_details(analysis_id: int):
    """Get detailed analysis by ID."""
    try:
        analysis = db_manager.get_analysis_by_id(analysis_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found.")
        return {
            "success": True,
            "analysis": analysis
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting analysis details: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving analysis details.")

@app.get("/ranking/{ranking_id}")
async def get_ranking_details(ranking_id: int):
    """Get detailed ranking by ID."""
    try:
        ranking = db_manager.get_ranking_by_id(ranking_id)
        if not ranking:
            raise HTTPException(status_code=404, detail="Ranking not found.")
        return {
            "success": True,
            "ranking": ranking
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting ranking details: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving ranking details.")

@app.get("/test")
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
