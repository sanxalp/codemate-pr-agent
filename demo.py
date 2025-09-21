#!/usr/bin/env python3
"""
Comprehensive Demo Script for PR Review Agent
Interactive demonstration of all features and capabilities
"""
import json
import time
import sys
import os
import subprocess
import requests
from datetime import datetime

class PRReviewDemo:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.frontend_url = "http://localhost:3000"
        
    def print_header(self, title, char="="):
        """Print a formatted header"""
        print(f"\n{char * 60}")
        print(f"🤖 {title}")
        print(f"{char * 60}")
    
    def print_section(self, title):
        """Print a section header"""
        print(f"\n{'─' * 40}")
        print(f"📋 {title}")
        print(f"{'─' * 40}")
    
    def check_services(self):
        """Check if backend and frontend services are running"""
        print("🔍 Checking service status...")
        
        # Check backend
        try:
            response = requests.get(f"{self.backend_url}/health", timeout=5)
            if response.status_code == 200:
                print("✅ Backend service is running")
                backend_running = True
            else:
                print("❌ Backend service returned error")
                backend_running = False
        except:
            print("❌ Backend service is not running")
            backend_running = False
        
        # Check frontend (just check if port is accessible)
        try:
            response = requests.get(self.frontend_url, timeout=5)
            print("✅ Frontend service is running")
            frontend_running = True
        except:
            print("❌ Frontend service is not running")
            frontend_running = False
        
        return backend_running, frontend_running
    
    def show_architecture(self):
        """Display system architecture"""
        self.print_section("System Architecture")
        
        architecture = """
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   AI Services   │
│   (Next.js)     │◄──►│   (FastAPI)     │◄──►│   (OpenAI)      │
│                 │    │                 │    │                 │
│ • React UI      │    │ • PR Analysis   │    │ • GPT-3.5       │
│ • TypeScript    │    │ • Git APIs      │    │ • Code Review   │
│ • Tailwind CSS  │    │ • Data Models   │    │ • Scoring       │
│ • Form Handling │    │ • CORS Support  │    │ • Suggestions   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        │                        │                        │
        │                        │                        │
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  Git Providers  │    │   Data Storage  │    │   User Input    │
│                 │    │                 │    │                 │
│ • GitHub API    │    │ • JSON Files    │    │ • PR URLs       │
│ • GitLab API    │    │ • Feedback      │    │ • Manual Review │
│ • Bitbucket API │    │ • Temp Storage  │    │ • Configuration │
└─────────────────┘    └─────────────────┘    └─────────────────┘
        """
        print(architecture)
    
    def show_supported_platforms(self):
        """Show supported git platforms with examples"""
        self.print_section("Supported Git Platforms")
        
        platforms = [
            {
                "name": "GitHub",
                "icon": "🐙",
                "format": "https://github.com/owner/repo/pull/123",
                "example": "https://github.com/microsoft/vscode/pull/12345",
                "features": ["Public repos", "Private repos (with token)", "Rich diff data"]
            },
            {
                "name": "GitLab",
                "icon": "🦊", 
                "format": "https://gitlab.com/owner/repo/-/merge_requests/123",
                "example": "https://gitlab.com/gitlab-org/gitlab/-/merge_requests/12345",
                "features": ["GitLab.com", "Self-hosted instances", "Merge request data"]
            },
            {
                "name": "Bitbucket",
                "icon": "🪣",
                "format": "https://bitbucket.org/owner/repo/pull-requests/123", 
                "example": "https://bitbucket.org/atlassian/bitbucket-server/pull-requests/12345",
                "features": ["Atlassian integration", "Pull request analysis", "Team workflows"]
            }
        ]
        
        for platform in platforms:
            print(f"\n{platform['icon']} {platform['name']}")
            print(f"   Format: {platform['format']}")
            print(f"   Example: {platform['example']}")
            print(f"   Features: {', '.join(platform['features'])}")
    
    def show_sample_analysis(self):
        """Show detailed sample AI analysis"""
        self.print_section("Sample AI Analysis Results")
        
        sample_feedback = {
            "summary": "This pull request introduces a new user authentication system with JWT tokens and password hashing. The implementation follows security best practices but has some areas for improvement in error handling and testing coverage.",
            "score": 78,
            "issues": [
                {
                    "type": "error",
                    "file": "src/auth/database.py",
                    "line": 23,
                    "message": "SQL injection vulnerability detected in user query",
                    "suggestion": "Use parameterized queries: cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))"
                },
                {
                    "type": "warning",
                    "file": "src/auth/password.py",
                    "line": 45,
                    "message": "Password validation is too weak",
                    "suggestion": "Implement stronger password requirements: minimum 8 characters, uppercase, lowercase, numbers, and special characters"
                },
                {
                    "type": "warning",
                    "file": "src/api/routes.py",
                    "line": 67,
                    "message": "Missing rate limiting on login endpoint",
                    "suggestion": "Add rate limiting to prevent brute force attacks: @limiter.limit('5 per minute')"
                },
                {
                    "type": "info",
                    "file": "src/models/user.py",
                    "line": 12,
                    "message": "Consider adding type hints for better code documentation",
                    "suggestion": "Add type annotations: def get_user(user_id: int) -> Optional[User]"
                },
                {
                    "type": "info",
                    "file": "src/utils/helpers.py",
                    "line": 89,
                    "message": "Function could be optimized for better performance",
                    "suggestion": "Use list comprehension instead of loop: return [item.id for item in items]"
                }
            ],
            "recommendations": [
                "Add comprehensive unit tests for authentication flow (current coverage: ~40%)",
                "Implement proper logging for security events and failed login attempts",
                "Add API documentation using OpenAPI/Swagger for new endpoints",
                "Consider implementing 2FA for enhanced security",
                "Add input validation middleware for all API endpoints",
                "Implement proper session management and token refresh logic",
                "Add monitoring and alerting for suspicious authentication patterns"
            ]
        }
        
        print(f"📊 Overall Assessment:")
        print(f"   Summary: {sample_feedback['summary']}")
        print(f"   Quality Score: {sample_feedback['score']}/100")
        
        # Color-coded issue display
        issue_colors = {
            "error": "🔴",
            "warning": "🟡", 
            "info": "🔵"
        }
        
        issue_counts = {}
        for issue in sample_feedback['issues']:
            issue_type = issue['type']
            issue_counts[issue_type] = issue_counts.get(issue_type, 0) + 1
        
        print(f"\n🔍 Issues Found:")
        for issue_type, count in issue_counts.items():
            print(f"   {issue_colors[issue_type]} {issue_type.title()}: {count}")
        
        print(f"\n📝 Detailed Issues:")
        for i, issue in enumerate(sample_feedback['issues'], 1):
            icon = issue_colors[issue['type']]
            print(f"\n{i}. {icon} {issue['type'].upper()}: {issue['file']}:{issue.get('line', '?')}")
            print(f"   Problem: {issue['message']}")
            if issue.get('suggestion'):
                print(f"   💡 Solution: {issue['suggestion']}")
        
        print(f"\n🎯 Recommendations ({len(sample_feedback['recommendations'])}):")
        for i, rec in enumerate(sample_feedback['recommendations'], 1):
            print(f"{i}. {rec}")
    
    def show_api_examples(self):
        """Show API usage examples"""
        self.print_section("API Usage Examples")
        
        print("🔗 Backend API Endpoints:")
        print("\n1. Health Check:")
        print("   GET /health")
        print("   Response: {'status': 'healthy', 'timestamp': '2024-01-01T12:00:00'}")
        
        print("\n2. Analyze PR:")
        print("   POST /analyze")
        print("   Body: {'prUrl': 'https://github.com/owner/repo/pull/123'}")
        print("   Response: {'message': 'PR analysis completed', 'feedback': {...}}")
        
        print("\n3. Get Feedback:")
        print("   GET /feedback")
        print("   Response: {'summary': '...', 'score': 85, 'issues': [...], 'recommendations': [...]}")
        
        print("\n📱 Frontend Features:")
        print("• URL validation for GitHub, GitLab, and Bitbucket")
        print("• Real-time analysis progress indicators")
        print("• Interactive feedback display with syntax highlighting")
        print("• Responsive design for desktop and mobile")
        print("• Dark/light theme support")
    
    def show_setup_process(self):
        """Show the complete setup process"""
        self.print_section("Complete Setup Process")
        
        print("🚀 Automated Setup (Recommended):")
        print("   python setup.py")
        print("   ↳ Checks prerequisites (Python, Node.js, pnpm)")
        print("   ↳ Installs backend dependencies (FastAPI, OpenAI, etc.)")
        print("   ↳ Installs frontend dependencies (Next.js, React, etc.)")
        print("   ↳ Creates environment files")
        print("   ↳ Generates start scripts")
        
        print("\n🔧 Manual Setup:")
        print("1. Backend Setup:")
        print("   cd backend")
        print("   pip install -r requirements.txt")
        print("   cp .env.example .env")
        print("   # Edit .env with API keys")
        print("   python start.py")
        
        print("\n2. Frontend Setup:")
        print("   cd frontend")
        print("   pnpm install")
        print("   pnpm dev")
        
        print("\n🔑 Required Environment Variables:")
        env_vars = [
            ("OPENAI_API_KEY", "Required", "Get from https://platform.openai.com/api-keys"),
            ("GITHUB_TOKEN", "Optional", "For private repos: https://github.com/settings/tokens"),
            ("GITLAB_TOKEN", "Optional", "For GitLab access: https://gitlab.com/-/profile/personal_access_tokens"),
            ("BITBUCKET_USERNAME", "Optional", "Your Bitbucket username"),
            ("BITBUCKET_APP_PASSWORD", "Optional", "App password: https://bitbucket.org/account/settings/app-passwords/")
        ]
        
        for var, status, description in env_vars:
            print(f"   {var} ({status}): {description}")
    
    def demonstrate_workflow(self):
        """Show the complete user workflow"""
        self.print_section("User Workflow Demonstration")
        
        workflow_steps = [
            ("1. User visits frontend", "http://localhost:3000"),
            ("2. Enters PR URL", "https://github.com/microsoft/vscode/pull/12345"),
            ("3. Frontend validates URL", "Checks format and provider"),
            ("4. POST request to backend", "/analyze endpoint"),
            ("5. Backend fetches PR data", "Git provider APIs"),
            ("6. AI analysis begins", "OpenAI GPT processing"),
            ("7. Results saved to file", "feedback.json"),
            ("8. Frontend polls for results", "/feedback endpoint"),
            ("9. Display comprehensive feedback", "Issues, score, recommendations"),
            ("10. User reviews suggestions", "Actionable improvements")
        ]
        
        for step, description in workflow_steps:
            print(f"{step}: {description}")
            time.sleep(0.5)  # Simulate processing time
        
        print("\n⏱️ Typical Analysis Time: 30-60 seconds")
        print("🔄 Real-time Updates: Frontend polls every 2 seconds")
    
    def show_tech_stack(self):
        """Display detailed tech stack information"""
        self.print_section("Technology Stack Details")
        
        tech_stack = {
            "Backend": {
                "Framework": "FastAPI (Python)",
                "AI/ML": "OpenAI GPT-3.5-turbo",
                "HTTP Client": "Requests library",
                "Data Validation": "Pydantic models",
                "Environment": "python-dotenv",
                "CORS": "FastAPI CORS middleware"
            },
            "Frontend": {
                "Framework": "Next.js 14 (React)",
                "Language": "TypeScript",
                "Styling": "Tailwind CSS",
                "Components": "Radix UI primitives",
                "Icons": "Lucide React",
                "Forms": "React Hook Form + Zod",
                "HTTP Client": "Fetch API"
            },
            "Infrastructure": {
                "Package Manager": "pnpm (frontend), pip (backend)",
                "Development": "Hot reload, auto-restart",
                "API Documentation": "FastAPI auto-generated docs",
                "Data Storage": "JSON files (temporary)",
                "Deployment": "Docker-ready, cloud-compatible"
            }
        }
        
        for category, technologies in tech_stack.items():
            print(f"\n🔧 {category}:")
            for tech, description in technologies.items():
                print(f"   • {tech}: {description}")
    
    def run_live_demo(self):
        """Run a live demonstration if services are available"""
        self.print_section("Live Demo")
        
        backend_running, frontend_running = self.check_services()
        
        if backend_running:
            print("\n🎯 Testing Backend API...")
            
            # Test health endpoint
            try:
                response = requests.get(f"{self.backend_url}/health")
                print(f"✅ Health Check: {response.json()}")
            except Exception as e:
                print(f"❌ Health Check Failed: {e}")
            
            # Test analyze endpoint with a sample URL
            sample_url = "https://github.com/microsoft/vscode/pull/12345"
            print(f"\n🔍 Testing Analysis with: {sample_url}")
            
            try:
                response = requests.post(
                    f"{self.backend_url}/analyze",
                    json={"prUrl": sample_url},
                    timeout=10
                )
                if response.status_code == 200:
                    print("✅ Analysis request accepted")
                    
                    # Try to get feedback
                    time.sleep(2)
                    feedback_response = requests.get(f"{self.backend_url}/feedback")
                    if feedback_response.status_code == 200:
                        feedback = feedback_response.json()
                        print(f"✅ Feedback received - Score: {feedback.get('score', 'N/A')}")
                    else:
                        print("⏳ Analysis still in progress...")
                else:
                    print(f"❌ Analysis failed: {response.status_code}")
            except Exception as e:
                print(f"❌ Analysis test failed: {e}")
        
        if frontend_running:
            print(f"\n🌐 Frontend is accessible at: {self.frontend_url}")
            print("   • Try submitting a real PR URL for analysis")
            print("   • Experience the full user interface")
        
        if not (backend_running or frontend_running):
            print("\n⚠️  Services not running. To start them:")
            print("   Backend: python backend/start.py")
            print("   Frontend: cd frontend && pnpm dev")
    
    def show_hackathon_features(self):
        """Highlight hackathon-specific features"""
        self.print_section("Hackathon & Competition Ready")
        
        features = [
            ("🚀 Quick Setup", "< 5 minutes with automated script"),
            ("📚 Complete Documentation", "README, API docs, inline comments"),
            ("🎯 Multi-Platform Support", "GitHub, GitLab, Bitbucket compatibility"),
            ("🤖 AI Integration", "OpenAI GPT for intelligent analysis"),
            ("📊 Scoring System", "0-100 quality scores with explanations"),
            ("🔍 Issue Detection", "Errors, warnings, and improvement suggestions"),
            ("💡 Actionable Feedback", "Specific recommendations with code examples"),
            ("🎨 Modern UI", "Professional Next.js frontend"),
            ("🔧 Extensible Architecture", "Easy to add new features"),
            ("📱 Responsive Design", "Works on desktop and mobile"),
            ("🔒 Security Focus", "Identifies security vulnerabilities"),
            ("⚡ Real-time Updates", "Live feedback during analysis")
        ]
        
        for feature, description in features:
            print(f"{feature}: {description}")
        
        print(f"\n🏆 Perfect for demonstrating:")
        demo_scenarios = [
            "AI-powered developer tools",
            "Multi-platform integrations", 
            "Code quality automation",
            "Modern web application architecture",
            "Real-time data processing",
            "User experience design"
        ]
        
        for scenario in demo_scenarios:
            print(f"   • {scenario}")
    
    def interactive_menu(self):
        """Run interactive demo menu"""
        while True:
            self.print_header("PR Review Agent - Interactive Demo")
            
            menu_options = [
                ("1", "🏗️  Show System Architecture"),
                ("2", "🌐 Show Supported Platforms"),
                ("3", "📊 Sample AI Analysis Results"),
                ("4", "🔗 API Usage Examples"),
                ("5", "🚀 Setup Process Guide"),
                ("6", "👤 User Workflow Demo"),
                ("7", "🔧 Technology Stack"),
                ("8", "🎯 Live Demo (if services running)"),
                ("9", "🏆 Hackathon Features"),
                ("0", "❌ Exit Demo")
            ]
            
            print("\nChoose a demo section:")
            for option, description in menu_options:
                print(f"   {option}. {description}")
            
            choice = input("\nEnter your choice (0-9): ").strip()
            
            if choice == "1":
                self.show_architecture()
            elif choice == "2":
                self.show_supported_platforms()
            elif choice == "3":
                self.show_sample_analysis()
            elif choice == "4":
                self.show_api_examples()
            elif choice == "5":
                self.show_setup_process()
            elif choice == "6":
                self.demonstrate_workflow()
            elif choice == "7":
                self.show_tech_stack()
            elif choice == "8":
                self.run_live_demo()
            elif choice == "9":
                self.show_hackathon_features()
            elif choice == "0":
                print("\n👋 Thanks for exploring PR Review Agent!")
                break
            else:
                print("\n❌ Invalid choice. Please try again.")
            
            input("\nPress Enter to continue...")

def main():
    """Main demo function"""
    demo = PRReviewDemo()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        demo.interactive_menu()
    else:
        # Run full demo
        demo.print_header("PR Review Agent - Complete Demo")
        demo.show_architecture()
        demo.show_supported_platforms()
        demo.show_sample_analysis()
        demo.show_setup_process()
        demo.show_tech_stack()
        demo.show_hackathon_features()
        demo.run_live_demo()
        
        print(f"\n🎉 Demo completed!")
        print(f"💡 Run 'python demo.py --interactive' for interactive mode")

if __name__ == "__main__":
    main()