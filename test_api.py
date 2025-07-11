#!/usr/bin/env python3
"""
Test script for AI-Powered Resume Analyzer API
"""

import requests
import json
import os

API_BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test the health endpoint."""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False

def test_root():
    """Test the root endpoint."""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print("✅ Root endpoint working")
            print(f"   Version: {data.get('version', 'N/A')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing root endpoint: {e}")
        return False

def create_sample_resume():
    """Create a sample resume file for testing."""
    sample_resume = """
John Doe
Software Engineer

SUMMARY
Experienced software engineer with 5+ years of experience in Python, JavaScript, and machine learning.
Passionate about building scalable web applications and AI-powered solutions.

EXPERIENCE
Senior Software Engineer | Tech Corp | 2020-2023
- Developed REST APIs using FastAPI and Django
- Implemented machine learning models with TensorFlow and PyTorch
- Led a team of 3 developers in agile environment

Software Engineer | StartupXYZ | 2018-2020
- Built React frontend applications
- Worked with PostgreSQL and MongoDB databases
- Implemented CI/CD pipelines with Docker and Jenkins

EDUCATION
Bachelor of Science in Computer Science | University of Technology | 2018

SKILLS
Python, JavaScript, TypeScript, React, FastAPI, Django, TensorFlow, PyTorch, 
PostgreSQL, MongoDB, Docker, AWS, Git, Machine Learning, Deep Learning, NLP
"""
    
    with open("sample_resume.txt", "w") as f:
        f.write(sample_resume)
    return "sample_resume.txt"

def test_analyze_resume():
    """Test the analyze resume endpoint."""
    print("🔍 Testing analyze resume endpoint...")
    
    resume_file = create_sample_resume()
    
    try:
        with open(resume_file, "rb") as f:
            files = {"file": (resume_file, f, "text/plain")}
            response = requests.post(f"{API_BASE_URL}/analyze_resume/", files=files)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Resume analysis successful")
            print(f"   Skills found: {len(data.get('skills', []))}")
            print(f"   Entities found: {len(data.get('entities', []))}")
            return True
        else:
            print(f"❌ Resume analysis failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing resume analysis: {e}")
        return False
    finally:
        if os.path.exists(resume_file):
            os.remove(resume_file)

def test_match_resume():
    """Test the match resume endpoint."""
    print("🔍 Testing match resume endpoint...")
    
    resume_file = create_sample_resume()
    job_description = """
We are looking for a Senior Python Developer with experience in:
- Python and FastAPI development
- Machine learning and AI
- React for frontend development
- Cloud platforms like AWS
- Database management with PostgreSQL
- Docker containerization

The ideal candidate should have 3+ years of experience and strong problem-solving skills.
"""
    
    try:
        with open(resume_file, "rb") as f:
            files = {"resume": (resume_file, f, "text/plain")}
            data = {"job_description": job_description}
            response = requests.post(f"{API_BASE_URL}/match_resume/", files=files, data=data)
        
        if response.status_code == 200:
            result = response.json()
            analysis = result.get("analysis", {})
            print("✅ Resume matching successful")
            print(f"   Overall score: {analysis.get('overall_score', 0):.3f}")
            print(f"   Skill match: {analysis.get('skill_match_percentage', 0):.1f}%")
            print(f"   Semantic similarity: {analysis.get('semantic_similarity', 0):.3f}")
            return True
        else:
            print(f"❌ Resume matching failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error testing resume matching: {e}")
        return False
    finally:
        if os.path.exists(resume_file):
            os.remove(resume_file)

def main():
    """Run all tests."""
    print("🚀 Starting API tests...\n")
    
    tests = [
        test_health,
        test_root,
        test_analyze_resume,
        test_match_resume
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()  # Empty line for readability
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your API is working correctly.")
    else:
        print("⚠️  Some tests failed. Please check the API implementation.")
    
    return passed == total

if __name__ == "__main__":
    main()
