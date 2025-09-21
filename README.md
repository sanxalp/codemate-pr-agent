# PR Review Agent 🤖

An AI-powered pull request review agent that works with GitHub, GitLab, and Bitbucket. Built for hackathons and production use.

![PR Review Agent](https://img.shields.io/badge/AI-Powered-blue) ![Multi-Platform](https://img.shields.io/badge/Multi--Platform-GitHub%20%7C%20GitLab%20%7C%20Bitbucket-green) ![Python](https://img.shields.io/badge/Python-FastAPI-red) ![TypeScript](https://img.shields.io/badge/TypeScript-Next.js-blue)

## ✨ Features

- 🔍 **Multi-Platform Support**: Works with GitHub, GitLab, and Bitbucket
- 🤖 **AI-Powered Analysis**: Uses OpenAI GPT for intelligent code review
- 📊 **Quality Scoring**: Provides 0-100 quality scores for PRs
- 🐛 **Issue Detection**: Identifies errors, warnings, and improvement opportunities
- 💡 **Actionable Suggestions**: Offers specific recommendations for fixes
- 🏗️ **Modular Architecture**: Clean, extensible Python backend
- ⚡ **Real-time Updates**: Polling-based feedback system
- 🎨 **Modern UI**: Beautiful Next.js frontend with Tailwind CSS

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)

```bash
python setup.py
```

This will:

- Check prerequisites (Python, Node.js, pnpm)
- Install all dependencies
- Create environment files
- Generate start scripts

### Option 2: Manual Setup

1. **Backend Setup:**

   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your API keys
   python start.py
   ```

2. **Frontend Setup:**
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```

## 🔑 Environment Variables

Create `backend/.env` with your API keys:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for enhanced functionality)
GITHUB_TOKEN=your_github_token_here
GITLAB_TOKEN=your_gitlab_token_here
BITBUCKET_USERNAME=your_bitbucket_username
BITBUCKET_APP_PASSWORD=your_bitbucket_app_password
```

### Getting API Keys

- **OpenAI**: [Get API Key](https://platform.openai.com/api-keys)
- **GitHub**: [Personal Access Tokens](https://github.com/settings/tokens)
- **GitLab**: [Personal Access Tokens](https://gitlab.com/-/profile/personal_access_tokens)
- **Bitbucket**: [App Passwords](https://bitbucket.org/account/settings/app-passwords/)

## 🏗️ Architecture

```
pr-review-agent/
├── frontend/          # Next.js frontend
│   ├── app/          # App router pages
│   ├── components/   # React components
│   └── ...
├── backend/          # Python FastAPI backend
│   ├── main.py      # FastAPI application
│   ├── models/      # Data models
│   ├── services/    # Business logic
│   └── ...
└── setup.py         # Automated setup script
```

## 🔧 Tech Stack

### Backend

- **FastAPI** - Modern Python web framework
- **OpenAI** - AI-powered code analysis
- **Pydantic** - Data validation
- **Requests** - HTTP client for git APIs

### Frontend

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Radix UI** - Component primitives
- **Lucide React** - Icons

## 📖 Usage

1. **Start both services:**

   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:3000`

2. **Submit a PR for review:**

   - Paste any supported PR/MR URL
   - Wait for AI analysis (30-60 seconds)
   - Review detailed feedback

3. **Supported URL formats:**
   - GitHub: `https://github.com/owner/repo/pull/123`
   - GitLab: `https://gitlab.com/owner/repo/-/merge_requests/123`
   - Bitbucket: `https://bitbucket.org/owner/repo/pull-requests/123`

## 🎯 Hackathon Requirements

✅ **Multi-platform compatibility** - GitHub, GitLab, Bitbucket support  
✅ **Constructive feedback** - AI-generated suggestions and improvements  
✅ **Python backend** - FastAPI with modular structure  
✅ **Code quality analysis** - Structure, standards, and bug detection

### Bonus Features Implemented

✅ **AI-driven feedback** - OpenAI GPT integration  
✅ **Scoring system** - 0-100 quality scores  
✅ **Security analysis** - Identifies potential security issues  
✅ **Performance suggestions** - Optimization recommendations

## 🔍 API Endpoints

### POST /analyze

Analyze a pull request:

```json
{
  "prUrl": "https://github.com/owner/repo/pull/123"
}
```

### GET /feedback

Get analysis results:

```json
{
  "summary": "Overall assessment...",
  "score": 85,
  "issues": [...],
  "recommendations": [...]
}
```

### GET /health

Health check endpoint.

## 🚦 Development

### Backend Development

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development

```bash
cd frontend
pnpm dev
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎉 Hackathon Ready

This project is designed to be hackathon-ready with:

- Quick setup (< 5 minutes)
- Comprehensive documentation
- Working demo with real APIs
- Extensible architecture
- Modern tech stack

Perfect for demonstrating AI-powered developer tools! 🚀
