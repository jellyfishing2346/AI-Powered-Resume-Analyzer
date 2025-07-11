#!/usr/bin/env python3
"""
Setup script for AI-Powered Resume Analyzer
Installs dependencies and downloads required models
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        # Use pip3 instead of pip for macOS compatibility
        if command.startswith("pip "):
            command = command.replace("pip ", "pip3 ")
        
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    print("🚀 Setting up AI-Powered Resume Analyzer...")
    
    # Install main requirements
    if not run_command("pip install -r requirements.txt", "Installing main dependencies"):
        print("Failed to install main dependencies. Please check your Python environment.")
        return False
    
    # Install optional requirements
    if not run_command("pip install -r requirements-optional.txt", "Installing optional dependencies"):
        print("Warning: Some optional dependencies failed to install. Some features may not work.")
    
    # Download spaCy models
    models_to_download = ["en_core_web_sm", "en_core_web_lg"]
    
    for model in models_to_download:
        if not run_command(f"python -m spacy download {model}", f"Downloading spaCy model: {model}"):
            if model == "en_core_web_sm":
                print("❌ Failed to download required spaCy model. Please install manually:")
                print("python -m spacy download en_core_web_sm")
                return False
            else:
                print(f"⚠️  Failed to download {model}. Will fallback to en_core_web_sm")
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Start the API server: uvicorn main:app --reload")
    print("2. Open http://127.0.0.1:8000/docs for interactive API documentation")
    print("3. Upload resume files and job descriptions to test the API")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
