from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import json
import asyncio
from datetime import datetime

from services.pr_analyzer import PRAnalyzer
from services.git_providers import GitProviderFactory
from models.feedback import ReviewFeedback

load_dotenv()

app = FastAPI(title="PR Review Agent", version="1.0.0")

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PRRequest(BaseModel):
    prUrl: str

# Global analyzer instance
analyzer = PRAnalyzer()

@app.post("/analyze")
async def analyze_pr(request: PRRequest):
    """Analyze a pull request and generate feedback"""
    try:
        # Parse PR URL to determine provider
        provider = GitProviderFactory.get_provider(request.prUrl)
        
        # Get PR data
        pr_data = await provider.get_pr_data(request.prUrl)
        
        # Analyze the PR
        feedback = await analyzer.analyze_pr(pr_data)
        
        # Save feedback to file for frontend polling
        with open("feedback.json", "w") as f:
            json.dump(feedback.dict(), f, indent=2)
        
        return {"message": "PR analysis completed", "feedback": feedback}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/feedback")
async def get_feedback():
    """Get the latest feedback if available"""
    try:
        if os.path.exists("feedback.json"):
            with open("feedback.json", "r") as f:
                feedback = json.load(f)
            return feedback
        else:
            raise HTTPException(status_code=404, detail="Feedback not ready yet")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Feedback not ready yet")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)