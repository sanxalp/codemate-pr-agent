#!/usr/bin/env python3
"""
Environment check script for PR Review Agent
"""
import os
from dotenv import load_dotenv

def check_environment():
    """Check if environment is properly configured"""
    load_dotenv()
    
    print("🔍 Environment Configuration Check")
    print("=" * 40)
    
    # Required variables
    required_vars = {
        "OPENAI_API_KEY": "OpenAI API key for AI analysis"
    }
    
    # Optional variables
    optional_vars = {
        "GITHUB_TOKEN": "GitHub personal access token",
        "GITLAB_TOKEN": "GitLab personal access token", 
        "BITBUCKET_USERNAME": "Bitbucket username",
        "BITBUCKET_APP_PASSWORD": "Bitbucket app password"
    }
    
    all_good = True
    
    # Check required variables
    print("\n📋 Required Configuration:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"❌ {var}: Not set - {description}")
            all_good = False
    
    # Check optional variables
    print("\n🔧 Optional Configuration:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = value[:8] + "..." if len(value) > 8 else "***"
            print(f"✅ {var}: {masked_value}")
        else:
            print(f"⚠️  {var}: Not set - {description}")
    
    # Summary
    print("\n" + "=" * 40)
    if all_good:
        print("🎉 Environment is properly configured!")
        print("You can now start the backend server.")
    else:
        print("❌ Environment configuration incomplete.")
        print("Please set the required variables in your .env file.")
        print("See .env.example for reference.")
    
    return all_good

if __name__ == "__main__":
    check_environment()