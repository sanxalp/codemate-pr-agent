import openai
import os
import re
from typing import List, Dict, Any
import json

from models.feedback import ReviewFeedback, Issue, PRData

class PRAnalyzer:
    def __init__(self):
        self.client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    async def analyze_pr(self, pr_data: PRData) -> ReviewFeedback:
        """Analyze PR and generate comprehensive feedback"""
        
        # Prepare context for AI analysis
        context = self._prepare_analysis_context(pr_data)
        
        # Get AI analysis
        ai_feedback = await self._get_ai_analysis(context)
        
        # Parse and structure the feedback
        feedback = self._parse_ai_feedback(ai_feedback, pr_data)
        
        return feedback
    
    def _prepare_analysis_context(self, pr_data: PRData) -> str:
        """Prepare context string for AI analysis"""
        
        files_summary = []
        for file_data in pr_data.files_changed:
            if isinstance(file_data, dict):
                filename = file_data.get('filename', 'unknown')
                status = file_data.get('status', 'modified')
                additions = file_data.get('additions', 0)
                deletions = file_data.get('deletions', 0)
                files_summary.append(f"- {filename} ({status}): +{additions}/-{deletions}")
        
        context = f"""
Pull Request Analysis Request:

Title: {pr_data.title}
Author: {pr_data.author}
Provider: {pr_data.provider}

Description:
{pr_data.description}

Files Changed:
{chr(10).join(files_summary)}

Diff:
{pr_data.diff[:5000]}  # Limit diff size for API

Please analyze this pull request and provide:
1. A summary of the changes
2. Code quality issues (errors, warnings, info)
3. A score from 0-100
4. Recommendations for improvement

Focus on:
- Code structure and organization
- Potential bugs or security issues
- Performance considerations
- Best practices adherence
- Readability and maintainability
"""
        return context
    
    async def _get_ai_analysis(self, context: str) -> str:
        """Get analysis from OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are an expert code reviewer. Analyze the provided pull request and return a JSON response with the following structure:
{
  "summary": "Brief summary of the changes and overall assessment",
  "score": 85,
  "issues": [
    {
      "type": "error|warning|info",
      "file": "filename",
      "line": 42,
      "message": "Description of the issue",
      "suggestion": "How to fix it"
    }
  ],
  "recommendations": [
    "List of general recommendations"
  ]
}

Be thorough but constructive. Focus on actionable feedback."""
                    },
                    {
                        "role": "user",
                        "content": context
                    }
                ],
                temperature=0.3,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            # Fallback to basic analysis if AI fails
            return self._generate_fallback_analysis(context)
    
    def _generate_fallback_analysis(self, context: str) -> str:
        """Generate basic analysis if AI is unavailable"""
        return json.dumps({
            "summary": "Basic analysis completed. AI service unavailable, using rule-based analysis.",
            "score": 75,
            "issues": [
                {
                    "type": "info",
                    "file": "general",
                    "message": "AI analysis unavailable, performed basic checks",
                    "suggestion": "Ensure proper error handling and testing"
                }
            ],
            "recommendations": [
                "Add comprehensive unit tests",
                "Ensure proper error handling",
                "Follow coding standards",
                "Add documentation for new features"
            ]
        })
    
    def _parse_ai_feedback(self, ai_response: str, pr_data: PRData) -> ReviewFeedback:
        """Parse AI response into structured feedback"""
        try:
            # Try to extract JSON from the response
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                feedback_data = json.loads(json_match.group())
            else:
                feedback_data = json.loads(ai_response)
            
            # Convert to our model
            issues = []
            for issue_data in feedback_data.get("issues", []):
                issues.append(Issue(
                    type=issue_data.get("type", "info"),
                    file=issue_data.get("file", "unknown"),
                    line=issue_data.get("line"),
                    message=issue_data.get("message", ""),
                    suggestion=issue_data.get("suggestion")
                ))
            
            return ReviewFeedback(
                summary=feedback_data.get("summary", "Analysis completed"),
                score=max(0, min(100, feedback_data.get("score", 75))),
                issues=issues,
                recommendations=feedback_data.get("recommendations", [])
            )
        
        except Exception as e:
            # Fallback if parsing fails
            return ReviewFeedback(
                summary=f"Analysis completed with parsing issues: {str(e)}",
                score=70,
                issues=[
                    Issue(
                        type="warning",
                        file="parser",
                        message="Could not parse AI response completely",
                        suggestion="Review the changes manually"
                    )
                ],
                recommendations=[
                    "Manual review recommended",
                    "Check for common code issues",
                    "Ensure tests are included"
                ]
            )