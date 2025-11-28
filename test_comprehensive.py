#!/usr/bin/env python3
"""
Comprehensive test suite for AI-Powered Resume Analyzer
Tests all endpoints, features, and integration points
"""

import requests
import json
import time
import os
from pathlib import Path

API_BASE_URL = "http://localhost:8001"
FRONTEND_URL = "http://localhost:3000"

class ResumeAnalyzerTester:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def test(self, name, test_func):
        """Run a test and record results."""
        print(f"🔍 Testing {name}...")
        try:
            result = test_func()
            if result:
                print(f"  ✅ PASSED: {name}")
                self.passed += 1
                self.results.append({"test": name, "status": "PASSED", "details": ""})
                return True
            else:
                print(f"  ❌ FAILED: {name}")
                self.failed += 1
                self.results.append({"test": name, "status": "FAILED", "details": "Test returned False"})
                return False
        except Exception as e:
            print(f"  ❌ ERROR: {name} - {str(e)}")
            self.failed += 1
            self.results.append({"test": name, "status": "ERROR", "details": str(e)})
            return False
    
    def test_api_health(self):
        """Test API health endpoint."""
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        return response.status_code == 200 and "healthy" in response.json().get("status", "")
    
    def test_api_root(self):
        """Test API root endpoint."""
        response = requests.get(f"{API_BASE_URL}/", timeout=5)
        data = response.json()
        return (response.status_code == 200 and 
                "AI-Powered Resume Analyzer" in data.get("message", "") and
                data.get("status") == "operational")
    
    def test_frontend_accessible(self):
        """Test if frontend is accessible."""
        response = requests.get(FRONTEND_URL, timeout=10)
        return response.status_code == 200 and "<!DOCTYPE html>" in response.text
    
    def test_analyze_text_resume(self):
        """Test analyzing a text resume."""
        if not os.path.exists("sample_resume.txt"):
            return False
        
        with open("sample_resume.txt", "rb") as f:
            files = {"file": f}
            data = {"job_description": "Python developer with Django experience"}
            response = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data, timeout=30)
        
        if response.status_code != 200:
            return False
        
        result = response.json()
        return (result.get("success") and 
                "analysis" in result and
                result["analysis"].get("match_score", 0) > 0)
    
    def test_ranking_multiple_resumes(self):
        """Test ranking multiple resumes."""
        resume_files = ["sample_resume.txt", "sample_resume_2.txt", "sample_resume_3.txt"]
        
        # Check if all files exist
        for filename in resume_files:
            if not os.path.exists(filename):
                return False
        
        files = [("files", open(filename, "rb")) for filename in resume_files]
        data = {"job_description": "Senior Python Developer with Machine Learning experience"}
        
        try:
            response = requests.post(f"{API_BASE_URL}/rank", files=files, data=data, timeout=60)
            
            if response.status_code != 200:
                return False
            
            result = response.json()
            return (result.get("success") and 
                    "ranked_candidates" in result and
                    len(result["ranked_candidates"]) == 3 and
                    result["ranked_candidates"][0].get("rank") == 1)
        finally:
            for _, file_obj in files:
                file_obj.close()
    
    def test_skills_extraction(self):
        """Test that skills are being extracted properly."""
        if not os.path.exists("sample_resume.txt"):
            return False
        
        with open("sample_resume.txt", "rb") as f:
            files = {"file": f}
            data = {"job_description": "Python developer"}
            response = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data, timeout=30)
        
        if response.status_code != 200:
            return False
        
        result = response.json()
        skills = result.get("analysis", {}).get("skills", [])
        
        # Check if common skills are detected
        common_skills = ["python", "javascript", "sql", "git"]
        detected_common = [skill for skill in skills if skill.lower() in common_skills]
        
        return len(skills) > 5 and len(detected_common) > 0
    
    def test_entity_recognition(self):
        """Test named entity recognition."""
        if not os.path.exists("sample_resume.txt"):
            return False
        
        with open("sample_resume.txt", "rb") as f:
            files = {"file": f}
            data = {"job_description": "Software engineer"}
            response = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data, timeout=30)
        
        if response.status_code != 200:
            return False
        
        result = response.json()
        entities = result.get("analysis", {}).get("entities", [])
        
        # Check if entities are detected
        entity_types = [entity.get("label") for entity in entities]
        expected_types = ["PERSON", "ORG", "GPE", "DATE"]
        
        return len(entities) > 5 and any(et in entity_types for et in expected_types)
    
    def test_match_score_calculation(self):
        """Test that match scores are reasonable."""
        if not os.path.exists("sample_resume.txt"):
            return False
        
        # Test with highly relevant job description
        with open("sample_resume.txt", "rb") as f:
            files = {"file": f}
            data = {"job_description": "Python Django developer software engineer machine learning"}
            response = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data, timeout=30)
        
        if response.status_code != 200:
            return False
        
        result1 = response.json()
        score1 = result1.get("analysis", {}).get("match_score", 0)
        
        # Test with irrelevant job description
        with open("sample_resume.txt", "rb") as f:
            files = {"file": f}
            data = {"job_description": "Chef cooking restaurant kitchen management"}
            response = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data, timeout=30)
        
        if response.status_code != 200:
            return False
        
        result2 = response.json()
        score2 = result2.get("analysis", {}).get("match_score", 0)
        
        # Relevant job should have higher score
        return score1 > score2 and 0 <= score1 <= 1 and 0 <= score2 <= 1
    
    def test_database_integration(self):
        """Test that results are saved to database."""
        # Import here to avoid import errors if database module isn't available
        try:
            import sys
            sys.path.append('.')
            from backend.database.operations import db_manager
            
            # Get current count
            stats_before = db_manager.get_stats()
            analyses_before = stats_before.get("total_analyses", 0)
            
            # Perform an analysis
            if not os.path.exists("sample_resume.txt"):
                return False
            
            with open("sample_resume.txt", "rb") as f:
                files = {"file": f}
                data = {"job_description": "Test job description"}
                response = requests.post(f"{API_BASE_URL}/analyze", files=files, data=data, timeout=30)
            
            if response.status_code != 200:
                return False
            
            # Check if count increased
            stats_after = db_manager.get_stats()
            analyses_after = stats_after.get("total_analyses", 0)
            
            return analyses_after > analyses_before
        except Exception:
            return False
    
    def test_file_upload_validation(self):
        """Test file upload validation."""
        # Test with empty file
        response = requests.post(f"{API_BASE_URL}/analyze", 
                               files={"file": ("empty.txt", "", "text/plain")},
                               data={"job_description": "test"}, timeout=10)
        
        # Should return an error for empty file
        return response.status_code != 200
    
    def test_api_error_handling(self):
        """Test API error handling."""
        # Test analyze without file
        response = requests.post(f"{API_BASE_URL}/analyze", 
                               data={"job_description": "test"}, timeout=10)
        return response.status_code == 422  # Validation error
    
    def run_all_tests(self):
        """Run all tests and generate report."""
        print("🚀 Starting Comprehensive Resume Analyzer Test Suite")
        print("=" * 60)
        
        # Core API tests
        self.test("API Health Check", self.test_api_health)
        self.test("API Root Endpoint", self.test_api_root)
        
        # Frontend test
        self.test("Frontend Accessibility", self.test_frontend_accessible)
        
        # Core functionality tests
        self.test("Text Resume Analysis", self.test_analyze_text_resume)
        self.test("Multi-Resume Ranking", self.test_ranking_multiple_resumes)
        
        # Feature tests
        self.test("Skills Extraction", self.test_skills_extraction)
        self.test("Entity Recognition", self.test_entity_recognition)
        self.test("Match Score Calculation", self.test_match_score_calculation)
        
        # Integration tests
        self.test("Database Integration", self.test_database_integration)
        
        # Error handling tests
        self.test("File Upload Validation", self.test_file_upload_validation)
        self.test("API Error Handling", self.test_api_error_handling)
        
        # Generate report
        self.generate_report()
    
    def generate_report(self):
        """Generate test report."""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        total_tests = self.passed + self.failed
        success_rate = (self.passed / total_tests * 100) if total_tests > 0 else 0
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {self.passed} ✅")
        print(f"Failed: {self.failed} ❌")
        print(f"Success Rate: {success_rate:.1f}%")
        
        if self.failed > 0:
            print("\n🔍 FAILED TESTS:")
            for result in self.results:
                if result["status"] in ["FAILED", "ERROR"]:
                    print(f"  ❌ {result['test']}: {result['details']}")
        
        print("\n📄 DETAILED RESULTS:")
        for result in self.results:
            status_emoji = "✅" if result["status"] == "PASSED" else "❌"
            print(f"  {status_emoji} {result['test']}: {result['status']}")
        
        # Save report to file
        report_data = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "total_tests": total_tests,
            "passed": self.passed,
            "failed": self.failed,
            "success_rate": success_rate,
            "detailed_results": self.results
        }
        
        with open("test_report.json", "w") as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\n📝 Full report saved to: test_report.json")
        
        if success_rate >= 80:
            print("\n🎉 Overall Status: EXCELLENT - System is ready for production!")
        elif success_rate >= 60:
            print("\n✅ Overall Status: GOOD - Minor issues to address")
        else:
            print("\n⚠️  Overall Status: NEEDS ATTENTION - Several issues to fix")

def main():
    """Main test runner."""
    print("AI-Powered Resume Analyzer - Comprehensive Test Suite")
    print(f"Testing API at: {API_BASE_URL}")
    print(f"Testing Frontend at: {FRONTEND_URL}")
    print()
    
    # Check if sample files exist
    required_files = ["sample_resume.txt", "sample_resume_2.txt", "sample_resume_3.txt"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print(f"⚠️  Warning: Missing sample files: {missing_files}")
        print("Some tests may fail due to missing sample files.")
    
    tester = ResumeAnalyzerTester()
    tester.run_all_tests()

if __name__ == "__main__":
    main()
