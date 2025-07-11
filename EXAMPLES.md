# API Usage Examples

This document provides practical examples of how to use the AI-Powered Resume Analyzer API.

## Prerequisites

Make sure the API server is running:
```bash
uvicorn main:app --reload
```

API Documentation is available at: http://127.0.0.1:8000/docs

## Python Examples

### 1. Analyze a Single Resume

```python
import requests

# Upload and analyze a resume
with open("resume.pdf", "rb") as f:
    files = {"file": ("resume.pdf", f, "application/pdf")}
    response = requests.post("http://127.0.0.1:8000/analyze_resume/", files=files)

if response.status_code == 200:
    data = response.json()
    print(f"Skills found: {data['skills_count']}")
    print(f"Skills: {', '.join(data['skills'])}")
    print(f"Summary: {data['summary']}")
else:
    print(f"Error: {response.status_code}")
```

### 2. Match Resume to Job Description

```python
import requests

job_description = """
We're looking for a Python developer with experience in:
- FastAPI or Django
- Machine Learning (TensorFlow/PyTorch)
- React frontend development
- AWS cloud services
- PostgreSQL databases
"""

with open("candidate_resume.pdf", "rb") as f:
    files = {"resume": ("resume.pdf", f, "application/pdf")}
    data = {"job_description": job_description}
    response = requests.post("http://127.0.0.1:8000/match_resume/", files=files, data=data)

if response.status_code == 200:
    result = response.json()
    analysis = result["analysis"]
    
    print(f"Overall Score: {analysis['overall_score']:.3f}")
    print(f"Skill Match: {analysis['skill_match_percentage']:.1f}%")
    print(f"Matched Skills: {', '.join(analysis['matched_skills'])}")
    print(f"Missing Skills: {', '.join(analysis['missing_skills'])}")
```

### 3. Rank Multiple Candidates

```python
import requests
import os

job_description = """
Senior Full-Stack Developer position requiring:
- 5+ years Python experience
- React/JavaScript frontend skills
- Database design (PostgreSQL/MongoDB)
- Cloud deployment (AWS/Azure)
- Team leadership experience
"""

# Prepare multiple resume files
resume_files = ["resume1.pdf", "resume2.docx", "resume3.txt"]
files = []

for resume_file in resume_files:
    if os.path.exists(resume_file):
        files.append(("resumes", (resume_file, open(resume_file, "rb"))))

data = {"job_description": job_description}
response = requests.post("http://127.0.0.1:8000/rank_candidates/", files=files, data=data)

# Close file handles
for _, (_, file_handle) in files:
    file_handle.close()

if response.status_code == 200:
    result = response.json()
    
    print(f"Total Candidates: {result['total_candidates']}")
    print("\nRanking Results:")
    
    for i, candidate in enumerate(result["ranked_candidates"], 1):
        print(f"\n{i}. {candidate['filename']}")
        print(f"   Overall Score: {candidate['overall_score']:.3f}")
        print(f"   Skill Match: {candidate['skill_match_percentage']:.1f}%")
        print(f"   Top Skills: {', '.join(candidate['matched_skills'][:5])}")
```

## JavaScript/Node.js Examples

### 1. Analyze Resume with FormData

```javascript
const FormData = require('form-data');
const fs = require('fs');
const axios = require('axios');

async function analyzeResume(filePath) {
    const form = new FormData();
    form.append('file', fs.createReadStream(filePath));
    
    try {
        const response = await axios.post('http://127.0.0.1:8000/analyze_resume/', form, {
            headers: form.getHeaders()
        });
        
        console.log('Skills found:', response.data.skills_count);
        console.log('Summary:', response.data.summary);
        return response.data;
    } catch (error) {
        console.error('Error:', error.response?.data || error.message);
    }
}

// Usage
analyzeResume('./resume.pdf');
```

### 2. Match Resume (Frontend JavaScript)

```javascript
async function matchResume(file, jobDescription) {
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);
    
    try {
        const response = await fetch('http://127.0.0.1:8000/match_resume/', {
            method: 'POST',
            body: formData
        });
        
        if (response.ok) {
            const result = await response.json();
            displayResults(result);
        } else {
            console.error('API Error:', response.statusText);
        }
    } catch (error) {
        console.error('Network Error:', error);
    }
}

function displayResults(result) {
    const analysis = result.analysis;
    
    document.getElementById('overall-score').textContent = 
        `${(analysis.overall_score * 100).toFixed(1)}%`;
    document.getElementById('skill-match').textContent = 
        `${analysis.skill_match_percentage.toFixed(1)}%`;
    document.getElementById('matched-skills').textContent = 
        analysis.matched_skills.join(', ');
}
```

## cURL Examples

### 1. Health Check

```bash
curl -X GET "http://127.0.0.1:8000/health"
```

### 2. Analyze Resume

```bash
curl -X POST "http://127.0.0.1:8000/analyze_resume/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@resume.pdf"
```

### 3. Match Resume

```bash
curl -X POST "http://127.0.0.1:8000/match_resume/" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "resume=@resume.pdf" \
  -F "job_description=Looking for Python developer with FastAPI experience"
```

## Error Handling

The API returns structured error responses:

```json
{
  "detail": "Unsupported file format: .xlsx. Supported formats: .pdf, .docx, .doc, .txt"
}
```

Common HTTP status codes:
- `200`: Success
- `400`: Bad Request (invalid input)
- `422`: Validation Error
- `500`: Internal Server Error

## Response Formats

### Analyze Resume Response
```json
{
  "filename": "resume.pdf",
  "entities": [
    {"label": "PERSON", "text": "John Doe", "description": "People, including fictional"},
    {"label": "ORG", "text": "Google", "description": "Companies, agencies, institutions"}
  ],
  "skills": ["python", "machine learning", "fastapi"],
  "skills_count": 3,
  "summary": "Experienced software engineer...",
  "education": ["Bachelor of Science in Computer Science"],
  "experience": ["Senior Software Engineer | 2020-2023"],
  "text_length": 1250
}
```

### Match Resume Response
```json
{
  "filename": "resume.pdf",
  "analysis": {
    "matched_skills": ["python", "fastapi", "machine learning"],
    "missing_skills": ["react", "aws"],
    "extra_skills": ["java", "spring"],
    "skill_match_percentage": 75.0,
    "semantic_similarity": 0.8532,
    "overall_score": 0.8249
  },
  "candidate_info": {
    "summary": "Experienced developer...",
    "education": ["BS Computer Science"],
    "experience": ["5 years at Tech Corp"]
  }
}
```

## Integration Tips

1. **File Size Limits**: The API handles files up to 10MB by default
2. **Concurrent Requests**: The API can handle multiple simultaneous requests
3. **Caching**: Consider caching results for identical resume-job combinations
4. **Batch Processing**: Use the rank_candidates endpoint for efficient batch processing
5. **Error Recovery**: Implement retry logic for network failures

## Performance Optimization

- Use the ranking endpoint for multiple candidates rather than individual matching
- Consider preprocessing large job descriptions to extract key requirements
- Implement client-side file validation before uploading
- Use appropriate file formats (TXT is fastest, PDF requires more processing)

For more detailed API documentation, visit: http://127.0.0.1:8000/docs
