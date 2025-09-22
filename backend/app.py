#!/usr/bin/env python3
"""
Flask web application for PR Review Agent
"""
import os
import json
import threading
import time
from flask import Flask, request, jsonify, render_template_string
import requests
from dotenv import load_dotenv

# Import our existing services
from services.pr_analyzer import PRAnalyzer
from services.git_providers import GitProviderFactory
from models.feedback import ReviewFeedback, PRData

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Global variables
analyzer = PRAnalyzer()
current_feedback = None
is_processing = False

# HTML template for the improved UI
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PR Review Agent - AI-Powered Code Review</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #6366f1;
            --primary-hover: #4f46e5;
            --success-color: #22c55e;
            --warning-color: #f59e0b;
            --error-color: #ef4444;
            --info-color: #3b82f6;
            --bg-primary: #000000;
            --bg-secondary: #0a0a0a;
            --bg-card: #111111;
            --text-primary: #ffffff;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --border-color: #27272a;
            --border-subtle: #18181b;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3);
            --glow: 0 0 20px rgba(99, 102, 241, 0.3);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            min-height: 100vh;
            color: var(--text-primary);
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }

        .app-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 2rem 0;
            border-bottom: 1px solid var(--border-subtle);
        }

        .header h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
            text-shadow: 0 0 30px rgba(99, 102, 241, 0.5);
        }

        .header p {
            font-size: 1.2rem;
            color: var(--text-secondary);
            font-weight: 300;
        }

        .main-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            box-shadow: var(--shadow-lg);
            overflow: hidden;
            flex: 1;
        }

        .card-header {
            background: linear-gradient(135deg, var(--bg-card), var(--bg-secondary));
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 2rem;
            text-align: center;
        }

        .card-header h2 {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }

        .card-header p {
            color: var(--text-secondary);
        }

        .card-body {
            padding: 2rem;
            background: var(--bg-card);
        }

        .form-section {
            margin-bottom: 2rem;
        }

        .form-group {
            margin-bottom: 1.5rem;
        }

        .form-label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--text-primary);
        }

        .form-input {
            width: 100%;
            padding: 1rem;
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 1rem;
            transition: all 0.3s ease;
            background: var(--bg-secondary);
            color: var(--text-primary);
        }

        .form-input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: var(--glow);
            background: var(--bg-card);
        }

        .form-input::placeholder {
            color: var(--text-muted);
        }

        .btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            padding: 1rem 2rem;
            border: none;
            border-radius: 8px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
            min-height: 48px;
        }

        .btn-primary {
            background: var(--primary-color);
            color: white;
            width: 100%;
        }

        .btn-primary:hover:not(:disabled) {
            background: var(--primary-hover);
            transform: translateY(-1px);
            box-shadow: var(--glow);
        }

        .btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .status-section {
            margin: 2rem 0;
        }

        .status-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            text-align: center;
        }

        .loading {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            color: var(--primary-color);
        }

        .spinner {
            width: 24px;
            height: 24px;
            border: 3px solid var(--border-color);
            border-top: 3px solid var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .feedback-section {
            margin-top: 2rem;
        }

        .feedback-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: var(--shadow-lg);
        }

        .score-header {
            background: linear-gradient(135deg, var(--success-color), #16a34a);
            color: white;
            padding: 2rem;
            text-align: center;
            border-bottom: 1px solid var(--border-color);
        }

        .score-header.warning {
            background: linear-gradient(135deg, var(--warning-color), #d97706);
        }

        .score-header.error {
            background: linear-gradient(135deg, var(--error-color), #dc2626);
        }

        .score-value {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .score-label {
            font-size: 1.1rem;
            opacity: 0.9;
        }

        .feedback-content {
            padding: 2rem;
            background: var(--bg-card);
        }

        .section {
            margin-bottom: 2rem;
        }

        .section-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1rem;
            color: var(--text-primary);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .summary-text {
            background: var(--bg-secondary);
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid var(--primary-color);
            font-size: 1.1rem;
            line-height: 1.7;
            color: var(--text-primary);
        }

        .issues-grid {
            display: grid;
            gap: 1rem;
        }

        .issue-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 1.5rem;
            border-left: 4px solid var(--info-color);
            transition: all 0.3s ease;
        }

        .issue-card:hover {
            box-shadow: var(--shadow);
            transform: translateY(-1px);
            border-color: var(--border-color);
        }

        .issue-card.error {
            border-left-color: var(--error-color);
            background: rgba(239, 68, 68, 0.05);
        }

        .issue-card.warning {
            border-left-color: var(--warning-color);
            background: rgba(245, 158, 11, 0.05);
        }

        .issue-card.info {
            border-left-color: var(--info-color);
            background: rgba(59, 130, 246, 0.05);
        }

        .issue-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.5rem;
        }

        .issue-type {
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.8rem;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            color: white;
        }

        .issue-type.error {
            background: var(--error-color);
        }

        .issue-type.warning {
            background: var(--warning-color);
        }

        .issue-type.info {
            background: var(--info-color);
        }

        .issue-location {
            font-size: 0.9rem;
            color: var(--text-secondary);
            font-family: 'Monaco', 'Menlo', monospace;
        }

        .issue-message {
            margin: 1rem 0;
            font-size: 1rem;
            line-height: 1.6;
        }

        .issue-suggestion {
            background: rgba(255, 255, 255, 0.7);
            padding: 1rem;
            border-radius: 6px;
            font-size: 0.9rem;
            border: 1px solid rgba(0, 0, 0, 0.1);
        }

        .recommendations-list {
            list-style: none;
            display: grid;
            gap: 0.75rem;
        }

        .recommendation-item {
            background: var(--bg-primary);
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid var(--success-color);
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        }

        .recommendation-icon {
            color: var(--success-color);
            margin-top: 0.1rem;
        }

        .error-message {
            background: #fef2f2;
            border: 1px solid #fecaca;
            color: #991b1b;
            padding: 1rem;
            border-radius: 8px;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .stat-card {
            background: var(--bg-primary);
            padding: 1.5rem;
            border-radius: 8px;
            text-align: center;
            border: 1px solid var(--border-color);
        }

        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-color);
        }

        .stat-label {
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }

        @media (max-width: 768px) {
            .app-container {
                padding: 1rem;
            }

            .header h1 {
                font-size: 2rem;
            }

            .card-body {
                padding: 1.5rem;
            }

            .score-value {
                font-size: 2.5rem;
            }
        }
    </style>
</head>
<body>
    <div class="app-container">
        <header class="header">
            <h1><i class="fas fa-robot"></i> PR Review Agent</h1>
            <p>AI-Powered Code Review & Analysis</p>
        </header>

        <div class="main-card">
            <div class="card-header">
                <h2><i class="fas fa-code-branch"></i> Submit Pull Request</h2>
                <p>Enter your PR or MR URL for comprehensive AI analysis</p>
            </div>

            <div class="card-body">
                <form id="prForm" class="form-section">
                    <div class="form-group">
                        <label for="prUrl" class="form-label">
                            <i class="fas fa-link"></i> Pull Request / Merge Request URL
                        </label>
                        <input 
                            type="url" 
                            id="prUrl" 
                            name="prUrl" 
                            class="form-input"
                            placeholder="https://github.com/owner/repo/pull/123"
                            required
                        >
                    </div>
                    <button type="submit" id="submitBtn" class="btn btn-primary">
                        <i class="fas fa-search"></i>
                        <span id="btnText">Analyze Pull Request</span>
                    </button>
                </form>

                <div id="status" class="status-section"></div>
                <div id="feedback" class="feedback-section"></div>
            </div>
        </div>
    </div>

    <script>
        document.getElementById('prForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const prUrl = document.getElementById('prUrl').value;
            const submitBtn = document.getElementById('submitBtn');
            const btnText = document.getElementById('btnText');
            const statusDiv = document.getElementById('status');
            const feedbackDiv = document.getElementById('feedback');
            
            // Update UI for processing state
            submitBtn.disabled = true;
            btnText.textContent = 'Analyzing...';
            statusDiv.innerHTML = `
                <div class="status-card">
                    <div class="loading">
                        <div class="spinner"></div>
                        <div>
                            <strong>Analyzing Pull Request</strong><br>
                            <small>This may take 30-60 seconds...</small>
                        </div>
                    </div>
                </div>
            `;
            feedbackDiv.innerHTML = '';
            
            try {
                // Submit PR for analysis
                const response = await fetch('/analyze', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ prUrl: prUrl })
                });
                
                if (response.ok) {
                    // Poll for feedback
                    const feedback = await pollForFeedback();
                    displayFeedback(feedback);
                    statusDiv.innerHTML = '';
                } else {
                    const error = await response.json();
                    throw new Error(error.error || 'Analysis failed');
                }
            } catch (error) {
                statusDiv.innerHTML = `
                    <div class="status-card">
                        <div class="error-message">
                            <i class="fas fa-exclamation-triangle"></i>
                            <div>
                                <strong>Analysis Failed</strong><br>
                                <small>${error.message}</small>
                            </div>
                        </div>
                    </div>
                `;
            } finally {
                submitBtn.disabled = false;
                btnText.textContent = 'Analyze Pull Request';
            }
        });
        
        async function pollForFeedback() {
            const maxAttempts = 30;
            let attempts = 0;
            
            while (attempts < maxAttempts) {
                try {
                    const response = await fetch('/feedback');
                    if (response.ok) {
                        return await response.json();
                    } else if (response.status === 404) {
                        attempts++;
                        await new Promise(resolve => setTimeout(resolve, 2000));
                        
                        // Update progress
                        const progress = Math.min(90, (attempts / maxAttempts) * 100);
                        document.getElementById('status').innerHTML = `
                            <div class="status-card">
                                <div class="loading">
                                    <div class="spinner"></div>
                                    <div>
                                        <strong>Processing... ${Math.round(progress)}%</strong><br>
                                        <small>Analyzing code quality and generating insights</small>
                                    </div>
                                </div>
                            </div>
                        `;
                    } else {
                        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                    }
                } catch (error) {
                    attempts++;
                    await new Promise(resolve => setTimeout(resolve, 2000));
                }
            }
            
            throw new Error('Analysis timeout - please try again');
        }
        
        function displayFeedback(feedback) {
            const feedbackDiv = document.getElementById('feedback');
            
            // Determine score class
            let scoreClass = 'error';
            if (feedback.score >= 80) scoreClass = '';
            else if (feedback.score >= 60) scoreClass = 'warning';
            
            // Count issues by type
            const issueCounts = {
                error: feedback.issues?.filter(i => i.type === 'error').length || 0,
                warning: feedback.issues?.filter(i => i.type === 'warning').length || 0,
                info: feedback.issues?.filter(i => i.type === 'info').length || 0
            };
            
            let feedbackHtml = `
                <div class="feedback-card">
                    <div class="score-header ${scoreClass}">
                        <div class="score-value">${feedback.score}</div>
                        <div class="score-label">Overall Score</div>
                    </div>
                    
                    <div class="feedback-content">
                        <div class="stats-grid">
                            <div class="stat-card">
                                <div class="stat-value">${issueCounts.error}</div>
                                <div class="stat-label">Errors</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${issueCounts.warning}</div>
                                <div class="stat-label">Warnings</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${issueCounts.info}</div>
                                <div class="stat-label">Info</div>
                            </div>
                            <div class="stat-card">
                                <div class="stat-value">${feedback.recommendations?.length || 0}</div>
                                <div class="stat-label">Recommendations</div>
                            </div>
                        </div>
                        
                        <div class="section">
                            <h3 class="section-title">
                                <i class="fas fa-clipboard-list"></i>
                                Summary
                            </h3>
                            <div class="summary-text">${feedback.summary}</div>
                        </div>
            `;
            
            if (feedback.issues && feedback.issues.length > 0) {
                feedbackHtml += `
                    <div class="section">
                        <h3 class="section-title">
                            <i class="fas fa-bug"></i>
                            Issues Found (${feedback.issues.length})
                        </h3>
                        <div class="issues-grid">
                `;
                
                feedback.issues.forEach(issue => {
                    const icon = issue.type === 'error' ? 'fas fa-times-circle' : 
                                issue.type === 'warning' ? 'fas fa-exclamation-triangle' : 
                                'fas fa-info-circle';
                    
                    feedbackHtml += `
                        <div class="issue-card ${issue.type}">
                            <div class="issue-header">
                                <span class="issue-type ${issue.type}">
                                    <i class="${icon}"></i> ${issue.type}
                                </span>
                                <span class="issue-location">
                                    ${issue.file}${issue.line ? `:${issue.line}` : ''}
                                </span>
                            </div>
                            <div class="issue-message">${issue.message}</div>
                            ${issue.suggestion ? `
                                <div class="issue-suggestion">
                                    <strong><i class="fas fa-lightbulb"></i> Suggestion:</strong> ${issue.suggestion}
                                </div>
                            ` : ''}
                        </div>
                    `;
                });
                
                feedbackHtml += '</div></div>';
            }
            
            if (feedback.recommendations && feedback.recommendations.length > 0) {
                feedbackHtml += `
                    <div class="section">
                        <h3 class="section-title">
                            <i class="fas fa-thumbs-up"></i>
                            Recommendations
                        </h3>
                        <ul class="recommendations-list">
                `;
                
                feedback.recommendations.forEach(rec => {
                    feedbackHtml += `
                        <li class="recommendation-item">
                            <i class="fas fa-check-circle recommendation-icon"></i>
                            <span>${rec}</span>
                        </li>
                    `;
                });
                
                feedbackHtml += '</ul></div>';
            }
            
            feedbackHtml += '</div></div>';
            feedbackDiv.innerHTML = feedbackHtml;
        }
    </script>
</body>
</html>
"""

def process_pr_async(pr_url):
    """Process PR in a separate thread"""
    global current_feedback, is_processing
    
    try:
        # Parse PR URL to determine provider
        provider = GitProviderFactory.get_provider(pr_url)
        
        # Get PR data (this might be async)
        import asyncio
        pr_data = asyncio.run(provider.get_pr_data(pr_url))
        
        # Analyze the PR (this is async)
        feedback = asyncio.run(analyzer.analyze_pr(pr_data))
        
        # Save feedback
        current_feedback = feedback
        
        # Save to history
        save_to_history(pr_url, feedback, pr_data)
        
    except Exception as e:
        current_feedback = {
            "summary": f"Error processing PR: {str(e)}",
            "score": 0,
            "issues": [],
            "recommendations": [],
            "error": True
        }
    finally:
        is_processing = False

def save_to_history(pr_url, feedback, pr_data):
    """Save analysis to history file"""
    try:
        history_file = "analysis_history.json"
        history = []
        
        # Load existing history
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
        
        # Add new entry
        entry = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "pr_url": pr_url,
            "pr_title": getattr(pr_data, 'title', 'Unknown'),
            "author": getattr(pr_data, 'author', 'Unknown'),
            "score": feedback.score if hasattr(feedback, 'score') else feedback.get('score', 0),
            "issues_count": len(feedback.issues) if hasattr(feedback, 'issues') else len(feedback.get('issues', [])),
            "summary": feedback.summary if hasattr(feedback, 'summary') else feedback.get('summary', '')
        }
        
        # Keep only last 50 entries
        history.insert(0, entry)
        history = history[:50]
        
        # Save back to file
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
            
    except Exception as e:
        print(f"Error saving to history: {e}")

@app.route('/')
def index():
    """Serve the main UI page"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze_pr():
    """Analyze a pull request and generate feedback"""
    global is_processing
    
    try:
        data = request.get_json()
        pr_url = data.get('prUrl')
        
        if not pr_url:
            return jsonify({"error": "PR URL is required"}), 400
        
        # Set processing flag
        is_processing = True
        
        # Start processing in a separate thread
        thread = threading.Thread(target=process_pr_async, args=(pr_url,))
        thread.start()
        
        return jsonify({"message": "PR analysis started"})
    except Exception as e:
        is_processing = False
        return jsonify({"error": str(e)}), 500

@app.route('/feedback')
def get_feedback():
    """Get the latest feedback if available"""
    global current_feedback
    
    try:
        if current_feedback:
            # Convert to dict if it's a Pydantic model
            if hasattr(current_feedback, 'model_dump'):
                return jsonify(current_feedback.model_dump())
            elif hasattr(current_feedback, 'dict'):
                return jsonify(current_feedback.dict())
            else:
                return jsonify(current_feedback)
        else:
            return jsonify({"error": "Feedback not ready yet"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"})

@app.route('/history')
def get_history():
    """Get analysis history"""
    try:
        history_file = "analysis_history.json"
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                history = json.load(f)
            return jsonify(history)
        else:
            return jsonify([])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clear-feedback', methods=['POST'])
def clear_feedback():
    """Clear current feedback"""
    global current_feedback
    current_feedback = None
    return jsonify({"message": "Feedback cleared"})

@app.route('/status')
def get_status():
    """Get current processing status"""
    global is_processing
    return jsonify({
        "is_processing": is_processing,
        "has_feedback": current_feedback is not None
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)