#!/usr/bin/env python3
"""
Startup script for the PR Review Agent backend
"""
import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

def check_requirements():
    """Check if required environment variables are set"""
    # Load environment variables from .env file
    load_dotenv()
    
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("[ERROR] Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease create a .env file with the required variables.")
        print("See .env.example for reference.")
        return False
    
    return True

def install_requirements():
    """Install Python requirements"""
    print("[INSTALLING] Installing requirements...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("[SUCCESS] Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to install requirements: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("[STARTING] Starting PR Review Agent backend...")
    print("[INFO] Server will be available at: http://localhost:8000")
    print("[INFO] API docs available at: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server\n")
    
    try:
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n[STOPPED] Server stopped")

def main():
    """Main startup function"""
    print("PR Review Agent Backend")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("[ERROR] Please run this script from the backend directory")
        sys.exit(1)
    
    # Check environment variables
    if not check_requirements():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()