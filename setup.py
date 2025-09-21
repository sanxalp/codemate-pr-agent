#!/usr/bin/env python3
"""
Complete setup script for PR Review Agent
Sets up both frontend and backend
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, cwd=None, shell=False):
    """Run a command and return success status"""
    try:
        if shell:
            result = subprocess.run(command, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, cwd=cwd, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_prerequisites():
    """Check if required tools are installed"""
    print("🔍 Checking prerequisites...")
    
    # Check Python
    try:
        python_version = subprocess.check_output([sys.executable, "--version"], text=True).strip()
        print(f"✅ {python_version}")
    except:
        print("❌ Python not found")
        return False
    
    # Check Node.js
    success, output = run_command(["node", "--version"])
    if success:
        print(f"✅ Node.js {output.strip()}")
    else:
        print("❌ Node.js not found. Please install Node.js 18+ from https://nodejs.org/")
        return False
    
    # Check pnpm
    success, output = run_command(["pnpm", "--version"])
    if success:
        print(f"✅ pnpm {output.strip()}")
    else:
        print("❌ pnpm not found. Installing pnpm...")
        success, _ = run_command(["npm", "install", "-g", "pnpm"])
        if not success:
            print("❌ Failed to install pnpm")
            return False
        print("✅ pnpm installed")
    
    return True

def setup_backend():
    """Set up the Python backend"""
    print("\n🐍 Setting up Python backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    # Install Python dependencies
    print("📦 Installing Python dependencies...")
    success, output = run_command([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], cwd=backend_dir)
    if not success:
        print(f"❌ Failed to install Python dependencies: {output}")
        return False
    print("✅ Python dependencies installed")
    
    # Create .env file if it doesn't exist
    env_file = backend_dir / ".env"
    env_example = backend_dir / ".env.example"
    
    if not env_file.exists() and env_example.exists():
        shutil.copy(env_example, env_file)
        print("📝 Created .env file from template")
        print("⚠️  Please edit backend/.env with your API keys before running the backend")
    
    return True

def setup_frontend():
    """Set up the Next.js frontend"""
    print("\n⚛️  Setting up Next.js frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Frontend directory not found")
        return False
    
    # Install Node.js dependencies
    print("📦 Installing Node.js dependencies...")
    success, output = run_command(["pnpm", "install"], cwd=frontend_dir)
    if not success:
        print(f"❌ Failed to install Node.js dependencies: {output}")
        return False
    print("✅ Node.js dependencies installed")
    
    return True

def create_start_scripts():
    """Create convenient start scripts"""
    print("\n📜 Creating start scripts...")
    
    # Backend start script (cross-platform)
    backend_script = """#!/bin/bash
cd backend
python start.py
"""
    
    backend_script_win = """@echo off
cd backend
python start.py
"""
    
    # Frontend start script (cross-platform)
    frontend_script = """#!/bin/bash
cd frontend
pnpm dev
"""
    
    frontend_script_win = """@echo off
cd frontend
pnpm dev
"""
    
    # Write scripts
    with open("start-backend.sh", "w") as f:
        f.write(backend_script)
    os.chmod("start-backend.sh", 0o755)
    
    with open("start-backend.bat", "w") as f:
        f.write(backend_script_win)
    
    with open("start-frontend.sh", "w") as f:
        f.write(frontend_script)
    os.chmod("start-frontend.sh", 0o755)
    
    with open("start-frontend.bat", "w") as f:
        f.write(frontend_script_win)
    
    print("✅ Start scripts created")

def main():
    """Main setup function"""
    print("🚀 PR Review Agent Setup")
    print("=" * 40)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites check failed")
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("\n❌ Backend setup failed")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("\n❌ Frontend setup failed")
        sys.exit(1)
    
    # Create start scripts
    create_start_scripts()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit backend/.env with your API keys:")
    print("   - OPENAI_API_KEY (required)")
    print("   - GITHUB_TOKEN (optional)")
    print("   - GITLAB_TOKEN (optional)")
    print("   - BITBUCKET credentials (optional)")
    print("\n2. Start the backend:")
    print("   ./start-backend.sh  (Linux/Mac)")
    print("   start-backend.bat   (Windows)")
    print("\n3. Start the frontend (in another terminal):")
    print("   ./start-frontend.sh  (Linux/Mac)")
    print("   start-frontend.bat   (Windows)")
    print("\n4. Open http://localhost:3000 in your browser")
    print("\n🔗 Backend API docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main()