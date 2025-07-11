#!/usr/bin/env python3
"""
Deployment Platform Selector & Configuration Tool
Helps you choose and configure the best deployment platform for your Resume Analyzer
"""

import os
import json
import subprocess
import sys

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def print_info(text):
    print(f"ℹ️  {text}")

def print_success(text):
    print(f"✅ {text}")

def print_warning(text):
    print(f"⚠️  {text}")

def print_error(text):
    print(f"❌ {text}")

def get_user_choice(prompt, options):
    """Get user choice from a list of options."""
    print(f"\n{prompt}")
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (number): "))
            if 1 <= choice <= len(options):
                return choice - 1
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def check_git_status():
    """Check if code is ready for deployment."""
    try:
        # Check if git repo exists
        subprocess.run(["git", "status"], capture_output=True, check=True)
        
        # Check for uncommitted changes
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if result.stdout.strip():
            print_warning("You have uncommitted changes:")
            print(result.stdout)
            commit = input("Do you want to commit these changes? (y/n): ").lower() == 'y'
            if commit:
                message = input("Enter commit message: ") or "Ready for deployment"
                subprocess.run(["git", "add", "."])
                subprocess.run(["git", "commit", "-m", message])
                print_success("Changes committed successfully")
        
        # Check if remote exists
        try:
            subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, check=True)
            print_success("Git repository is ready for deployment")
            return True
        except subprocess.CalledProcessError:
            print_error("No remote origin found. You need to push to GitHub first.")
            return False
            
    except subprocess.CalledProcessError:
        print_error("Not a git repository. You need to initialize git and push to GitHub.")
        return False

def configure_railway():
    """Configure for Railway deployment."""
    print_header("RAILWAY CONFIGURATION")
    
    print_info("Railway is recommended for its simplicity and great AI/ML support.")
    print()
    print("📋 Railway Deployment Steps:")
    print("1. Push your code to GitHub (if not already done)")
    print("2. Go to https://railway.app")
    print("3. Sign up with GitHub")
    print("4. Click 'Deploy from GitHub repo'")
    print("5. Select your AI-Powered-Resume-Analyzer repository")
    print("6. Railway will automatically detect your Dockerfile")
    print()
    print("💡 Tips:")
    print("- Railway provides free PostgreSQL database")
    print("- Automatic SSL certificates")
    print("- Environment variables: Add PORT=8001")
    print("- Cost: ~$5/month for hobby tier")
    
    return True

def configure_render():
    """Configure for Render deployment."""
    print_header("RENDER CONFIGURATION")
    
    # Create render.yaml
    render_config = {
        "services": [
            {
                "type": "web",
                "name": "resume-analyzer",
                "env": "docker",
                "plan": "free",
                "healthCheckPath": "/health",
                "envVars": [
                    {"key": "PORT", "value": "8001"},
                    {"key": "LOG_LEVEL", "value": "INFO"}
                ]
            }
        ],
        "databases": [
            {
                "name": "resume-analyzer-db",
                "plan": "free"
            }
        ]
    }
    
    with open("render.yaml", "w") as f:
        # Write YAML manually since PyYAML might not be installed
        f.write("services:\n")
        f.write("  - type: web\n")
        f.write("    name: resume-analyzer\n")
        f.write("    env: docker\n")
        f.write("    plan: free\n")
        f.write("    healthCheckPath: /health\n")
        f.write("    envVars:\n")
        f.write("      - key: PORT\n")
        f.write("        value: 8001\n")
        f.write("      - key: LOG_LEVEL\n")
        f.write("        value: INFO\n")
        f.write("databases:\n")
        f.write("  - name: resume-analyzer-db\n")
        f.write("    plan: free\n")
    
    print_success("Created render.yaml configuration file")
    print()
    print("📋 Render Deployment Steps:")
    print("1. Push your code to GitHub (including render.yaml)")
    print("2. Go to https://render.com")
    print("3. Sign up with GitHub")
    print("4. Connect your repository")
    print("5. Render will auto-deploy from render.yaml")
    print()
    print("💡 Tips:")
    print("- Free tier available (great for testing)")
    print("- Automatic SSL certificates")
    print("- Cost: Free tier, then $7/month for paid")
    
    return True

def configure_digitalocean():
    """Configure for DigitalOcean App Platform."""
    print_header("DIGITALOCEAN CONFIGURATION")
    
    # Create .do/app.yaml
    os.makedirs(".do", exist_ok=True)
    
    do_config = {
        "name": "resume-analyzer",
        "services": [
            {
                "name": "api",
                "source_dir": "/",
                "dockerfile_path": "Dockerfile",
                "instance_size_slug": "basic-xxs",
                "instance_count": 1,
                "http_port": 8001,
                "health_check": {
                    "http_path": "/health"
                },
                "env_vars": [
                    {"key": "PORT", "value": "8001"},
                    {"key": "LOG_LEVEL", "value": "INFO"}
                ]
            }
        ],
        "databases": [
            {
                "name": "resume-db",
                "engine": "PG",
                "size": "basic-xs"
            }
        ]
    }
    
    with open(".do/app.yaml", "w") as f:
        # Write YAML manually since PyYAML might not be installed
        f.write("name: resume-analyzer\n")
        f.write("services:\n")
        f.write("  - name: api\n")
        f.write("    source_dir: /\n")
        f.write("    dockerfile_path: Dockerfile\n")
        f.write("    instance_size_slug: basic-xxs\n")
        f.write("    instance_count: 1\n")
        f.write("    http_port: 8001\n")
        f.write("    health_check:\n")
        f.write("      http_path: /health\n")
        f.write("    env_vars:\n")
        f.write("      - key: PORT\n")
        f.write("        value: '8001'\n")
        f.write("      - key: LOG_LEVEL\n")
        f.write("        value: INFO\n")
        f.write("databases:\n")
        f.write("  - name: resume-db\n")
        f.write("    engine: PG\n")
        f.write("    size: basic-xs\n")
    
    print_success("Created .do/app.yaml configuration file")
    print()
    print("📋 DigitalOcean Deployment Steps:")
    print("1. Push your code to GitHub (including .do/app.yaml)")
    print("2. Go to https://cloud.digitalocean.com/apps")
    print("3. Create new app from GitHub repo")
    print("4. DigitalOcean will use app.yaml for configuration")
    print()
    print("💡 Tips:")
    print("- No free tier, starts at $5/month")
    print("- Professional grade infrastructure")
    print("- Good for scaling up")
    
    return True

def configure_vercel_split():
    """Configure for split deployment (Vercel + API hosting)."""
    print_header("SPLIT DEPLOYMENT CONFIGURATION")
    
    print_info("Deploy frontend to Vercel, API to Railway/Render")
    
    # Create vercel.json for frontend
    frontend_dir = "frontend"
    if os.path.exists(frontend_dir):
        vercel_config = {
            "builds": [
                {
                    "src": "package.json",
                    "use": "@vercel/static-build",
                    "config": {"distDir": "build"}
                }
            ],
            "routes": [
                {"src": "/(.*)", "dest": "/index.html"}
            ]
        }
        
        with open(f"{frontend_dir}/vercel.json", "w") as f:
            json.dump(vercel_config, f, indent=2)
        
        print_success("Created vercel.json for frontend")
    
    print()
    print("📋 Split Deployment Steps:")
    print("1. Frontend to Vercel:")
    print("   - Push frontend/ folder to separate GitHub repo")
    print("   - Connect to Vercel (free)")
    print("   - Auto-deploy on push")
    print()
    print("2. API to Railway/Render:")
    print("   - Deploy main project to Railway or Render")
    print("   - Update frontend REACT_APP_API_URL to point to API")
    print()
    print("💡 Tips:")
    print("- Best performance (CDN for frontend)")
    print("- Free frontend hosting on Vercel")
    print("- More complex but professional setup")
    
    return True

def main():
    """Main deployment configuration tool."""
    print_header("AI-POWERED RESUME ANALYZER - DEPLOYMENT TOOL")
    
    print("This tool will help you choose and configure the best deployment platform")
    print("for your Resume Analyzer project.")
    
    # Check git status
    if not check_git_status():
        print("\n⚠️  Git setup required before deployment.")
        setup_git = input("Do you want guidance on setting up Git? (y/n): ").lower() == 'y'
        if setup_git:
            print("\n📋 Git Setup Steps:")
            print("1. git init")
            print("2. git add .")
            print("3. git commit -m 'Initial commit'")
            print("4. Create repository on GitHub")
            print("5. git remote add origin <your-github-url>")
            print("6. git push -u origin main")
        return
    
    # Platform selection
    platforms = [
        "Railway (Recommended - Easy & AI-friendly)",
        "Render (Great free tier)",
        "DigitalOcean App Platform (Professional)",
        "Split Deployment (Vercel + API hosting)",
        "Just show me all options"
    ]
    
    choice = get_user_choice("Choose your deployment platform:", platforms)
    
    if choice == 0:  # Railway
        configure_railway()
    elif choice == 1:  # Render
        configure_render()
    elif choice == 2:  # DigitalOcean
        configure_digitalocean()
    elif choice == 3:  # Split
        configure_vercel_split()
    elif choice == 4:  # Show all
        print_header("ALL DEPLOYMENT OPTIONS")
        configure_railway()
        configure_render()
        configure_digitalocean()
        configure_vercel_split()
    
    print_header("DEPLOYMENT SUMMARY")
    print("✅ Configuration files created")
    print("✅ Your project is ready for deployment")
    print()
    print("🚀 Next Steps:")
    print("1. Commit and push any new configuration files to GitHub")
    print("2. Follow the deployment steps for your chosen platform")
    print("3. Set up environment variables in your platform dashboard")
    print("4. Monitor deployment logs for any issues")
    print()
    print("📚 For detailed guides, check DEPLOYMENT_GUIDE.md")
    
    # Offer to commit new files
    if input("\nCommit new configuration files to git? (y/n): ").lower() == 'y':
        try:
            subprocess.run(["git", "add", "."])
            subprocess.run(["git", "commit", "-m", "Add deployment configuration files"])
            print_success("Configuration files committed to git")
        except Exception as e:
            print_error(f"Failed to commit: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDeployment configuration cancelled.")
    except Exception as e:
        print_error(f"An error occurred: {e}")
        sys.exit(1)
