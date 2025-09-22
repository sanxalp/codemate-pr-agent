# PR Review Agent - Backend with Flask UI

This directory contains the backend implementation of the PR Review Agent with a new Flask-based web UI.

## Features

- REST API for analyzing pull requests from GitHub, GitLab, and Bitbucket
- Web UI for submitting PR URLs and viewing feedback
- Integration with OpenAI for code review analysis
- Support for multiple git providers

## Requirements

- Python 3.7+
- OpenAI API key
- Git provider tokens (optional but recommended)

## Installation

1. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables by copying `.env.example` to `.env` and filling in your API keys:
   ```
   cp .env.example .env
   ```

## Usage

1. Start the backend server:

   ```
   python start.py
   ```

2. Open your browser and navigate to `http://localhost:8000` to access the web UI

3. Enter a valid PR URL in the form (e.g., https://github.com/facebook/react/pull/12345) and click "Review Pull Request"

4. The analysis will run in the background and the results will be displayed when ready

Note: Using placeholder URLs like "https://github.com/owner/repo/pull/123" will result in error messages since these repositories don't exist.

## API Endpoints

- `POST /analyze` - Submit a PR URL for analysis
- `GET /feedback` - Get the latest analysis feedback
- `GET /health` - Health check endpoint

## Environment Variables

- `OPENAI_API_KEY` - Required for AI analysis
- `GITHUB_TOKEN` - Optional, for GitHub API access
- `GITLAB_TOKEN` - Optional, for GitLab API access
- `BITBUCKET_USERNAME` - Optional, for Bitbucket API access
- `BITBUCKET_APP_PASSWORD` - Optional, for Bitbucket API access

## How It Works

1. The user submits a PR URL through the web UI
2. The backend fetches PR data from the git provider
3. The PR data is analyzed using OpenAI
4. Feedback is generated and stored
5. The frontend polls for feedback and displays it when ready

## Development

The backend is built with:

- Flask for the web UI and API
- FastAPI services for PR analysis (adapted for Flask)
- OpenAI for code review analysis
- Requests for API calls to git providers
