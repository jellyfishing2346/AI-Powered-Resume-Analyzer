#!/usr/bin/env python3
"""
Simple test client for the AI-Powered Resume Analyzer API
"""

import requests
import json
import sys
import os
from pathlib import Path

API_BASE_URL = "http://127.0.0.1:8000"

def test_api_health():
    """Test if the API is running and healthy."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False

def get_api_info():
    """Get API information and capabilities."""
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def test_components():
    """Test API components."""
    try:
        response = requests.post(f"{API_BASE_URL}/test", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return {"error": str(e)}

def analyze_resume(file_path, job_description=""):
    """Analyze a resume file."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    try:
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {'job_description': job_description}
            response = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data, timeout=30)
            
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API returned status {response.status_code}: {response.text}"}
    except Exception as e:
        return {"error": str(e)}

def main():
    print("🧪 AI-Powered Resume Analyzer - Test Client")
    print("=" * 50)
    
    # Test API health
    print("1. Testing API health...")
    if test_api_health():
        print("✅ API is running and healthy")
    else:
        print("❌ API is not responding. Please start the API server first.")
        print("   Run: python3 test_api_clean.py")
        return
    
    # Get API info
    print("\n2. Getting API information...")
    api_info = get_api_info()
    if api_info:
        print("✅ API Information:")
        print(json.dumps(api_info, indent=2))
    else:
        print("❌ Could not get API information")
    
    # Test components
    print("\n3. Testing API components...")
    component_test = test_components()
    if component_test and component_test.get("status") == "success":
        print("✅ Component test successful:")
        print(f"   - spaCy entities extracted: {component_test['tests']['spacy_entities']}")
        print(f"   - Skills found: {component_test['tests']['skill_extraction']}")
        print(f"   - Semantic similarity score: {component_test['tests']['semantic_similarity']}")
    else:
        print("❌ Component test failed:")
        print(json.dumps(component_test, indent=2))
    
    # Test resume analysis
    print("\n4. Testing resume analysis...")
    sample_resume = "sample_resume.txt"
    
    if os.path.exists(sample_resume):
        job_desc = """We are looking for a Python developer with experience in machine learning, 
                     AWS, and Django. Knowledge of Docker and Kubernetes is a plus. 
                     Experience with React and REST APIs is preferred."""
        
        print(f"   Analyzing: {sample_resume}")
        result = analyze_resume(sample_resume, job_desc)
        
        if result.get("success"):
            analysis = result["analysis"]
            print("✅ Resume analysis successful:")
            print(f"   - File: {result['filename']}")
            print(f"   - Word count: {analysis['word_count']}")
            print(f"   - Skills found: {analysis['skill_count']}")
            print(f"   - Entities extracted: {len(analysis['entities'])}")
            print(f"   - Job match score: {analysis['match_score']}")
            print(f"   - Top skills: {', '.join(analysis['skills'][:10])}")
        else:
            print("❌ Resume analysis failed:")
            print(json.dumps(result, indent=2))
    else:
        print(f"   Sample resume not found: {sample_resume}")
        print("   You can create your own resume file and test with:")
        print(f"   python3 test_client.py <path_to_resume>")
    
    print("\n🎉 Testing completed!")
    print("\n📖 For interactive testing, visit: http://127.0.0.1:8000/docs")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Custom file testing
        file_path = sys.argv[1]
        job_desc = sys.argv[2] if len(sys.argv) > 2 else ""
        
        print(f"Testing custom resume: {file_path}")
        if not test_api_health():
            print("❌ API is not running. Start with: python3 test_api_clean.py")
            sys.exit(1)
        
        result = analyze_resume(file_path, job_desc)
        print(json.dumps(result, indent=2))
    else:
        main()
