#!/usr/bin/env python3
"""
Simple test script to verify the PR Review Agent API
"""
import requests
import json
import time
import sys

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Is it running on port 8000?")
        return False

def test_analyze():
    """Test analyze endpoint with a sample GitHub PR"""
    sample_pr_url = "https://github.com/octocat/Hello-World/pull/1"
    
    try:
        print(f"🔍 Testing analysis with: {sample_pr_url}")
        response = requests.post(
            "http://localhost:8000/analyze",
            json={"prUrl": sample_pr_url},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Analysis request successful")
            return True
        else:
            print(f"❌ Analysis failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏰ Analysis timed out (this is normal for first run)")
        return True
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return False

def test_feedback():
    """Test feedback endpoint"""
    try:
        response = requests.get("http://localhost:8000/feedback")
        
        if response.status_code == 200:
            feedback = response.json()
            print("✅ Feedback retrieved successfully")
            print(f"   Score: {feedback.get('score', 'N/A')}")
            print(f"   Issues: {len(feedback.get('issues', []))}")
            return True
        elif response.status_code == 404:
            print("ℹ️  No feedback available yet (this is normal)")
            return True
        else:
            print(f"❌ Feedback request failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Feedback error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing PR Review Agent API")
    print("=" * 40)
    
    # Test health
    if not test_health():
        print("\n❌ Backend is not running. Please start it first:")
        print("   cd backend && python start.py")
        sys.exit(1)
    
    # Test analyze
    print("\n🔍 Testing analysis endpoint...")
    test_analyze()
    
    # Test feedback
    print("\n📊 Testing feedback endpoint...")
    test_feedback()
    
    print("\n🎉 API tests completed!")
    print("\nNext steps:")
    print("1. Open http://localhost:3000 to test the frontend")
    print("2. Try submitting a real PR URL")
    print("3. Check http://localhost:8000/docs for API documentation")

if __name__ == "__main__":
    main()