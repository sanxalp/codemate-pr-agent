# PR Review Agent Backend

AI-powered pull request review agent that works with GitHub, GitLab, and Bitbucket.

## Features

- 🔍 Multi-platform support (GitHub, GitLab, Bitbucket)
- 🤖 AI-powered code analysis using OpenAI GPT
- 📊 Code quality scoring (0-100)
- 🐛 Issue detection (errors, warnings, info)
- 💡 Actionable recommendations
- 🏗️ Modular architecture

## Quick Start

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start the server:**

   ```bash
   python start.py
   ```

   Or manually:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

## Environment Variables

Create a `.env` file with the following variables:

```env
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for specific providers)
GITHUB_TOKEN=your_github_token_here
GITLAB_TOKEN=your_gitlab_token_here
BITBUCKET_USERNAME=your_bitbucket_username
BITBUCKET_APP_PASSWORD=your_bitbucket_app_password
```

### Getting API Keys

- **OpenAI**: Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)
- **GitHub**: Create a personal access token at [GitHub Settings](https://github.com/settings/tokens)
- **GitLab**: Create a personal access token at [GitLab Settings](https://gitlab.com/-/profile/personal_access_tokens)
- **Bitbucket**: Create an app password at [Bitbucket Settings](https://bitbucket.org/account/settings/app-passwords/)

## API Endpoints

### POST /analyze

Analyze a pull request and generate feedback.

**Request:**

```json
{
  "prUrl": "https://github.com/owner/repo/pull/123"
}
```

**Response:**

```json
{
  "message": "PR analysis completed",
  "feedback": {
    "summary": "Overall assessment...",
    "score": 85,
    "issues": [...],
    "recommendations": [...]
  }
}
```

### GET /feedback

Get the latest analysis feedback.

**Response:**

```json
{
  "summary": "Overall assessment...",
  "score": 85,
  "issues": [
    {
      "type": "warning",
      "file": "src/main.py",
      "line": 42,
      "message": "Potential issue description",
      "suggestion": "How to fix it"
    }
  ],
  "recommendations": ["Add unit tests", "Improve error handling"]
}
```

### GET /health

Health check endpoint.

## Architecture

```
backend/
├── main.py              # FastAPI application
├── start.py             # Startup script
├── models/
│   └── feedback.py      # Data models
├── services/
│   ├── git_providers.py # Git provider implementations
│   └── pr_analyzer.py   # AI analysis logic
└── requirements.txt     # Dependencies
```

## Supported Platforms

- **GitHub**: `https://github.com/owner/repo/pull/123`
- **GitLab**: `https://gitlab.com/owner/repo/-/merge_requests/123`
- **Bitbucket**: `https://bitbucket.org/owner/repo/pull-requests/123`

## Development

The backend is built with:

- **FastAPI** for the web framework
- **OpenAI** for AI-powered analysis
- **Requests** for API calls to git providers
- **Pydantic** for data validation

## Error Handling

The system includes comprehensive error handling:

- Invalid URLs are rejected with helpful messages
- API failures fall back to basic analysis
- Missing credentials use dummy data for Bitbucket
- Network errors are properly handled and reported

## CORS Configuration

The backend is configured to accept requests from:

- `http://localhost:3000` (Next.js development)
- `http://127.0.0.1:3000`

Update the CORS settings in `main.py` for production deployment.
