#!/usr/bin/env python3
"""
Quick script to check if the deployed service is running
"""

import requests
import time

def check_deployment(url):
    """Check if the deployment is working"""
    try:
        print(f"Checking deployment at: {url}")
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Deployment is LIVE!")
            print(f"Response: {response.json()}")
            return True
        else:
            print(f"❌ Got status code: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting: {e}")
        return False

def check_health(base_url):
    """Check the health endpoint"""
    try:
        health_url = f"{base_url}/health"
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Health check passed!")
            print(f"Health response: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check error: {e}")
        return False

if __name__ == "__main__":
    # Official Render URL (updated)
    render_url = "https://ai-powered-resume-analyzer-1-i3r9.onrender.com"
    
    print("🚀 Checking deployment status...")
    print("=" * 50)
    
    # Check main endpoint
    if check_deployment(render_url):
        # Check health endpoint
        check_health(render_url)
        
        print("\n🎉 Deployment appears to be working!")
        print(f"Visit: {render_url}")
        print(f"API Docs: {render_url}/docs")
    else:
        print("\n⏳ Deployment might still be in progress...")
        print("Wait a few minutes and try again.")
