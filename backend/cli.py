#!/usr/bin/env python3
"""
Command Line Interface for PR Review Agent
"""
import argparse
import asyncio
import json
import sys
from pathlib import Path
from dotenv import load_dotenv
import os

# Import our services
from services.pr_analyzer import PRAnalyzer
from services.git_providers import GitProviderFactory
from models.feedback import ReviewFeedback

# Load environment variables
load_dotenv()

class PRReviewCLI:
    def __init__(self):
        self.analyzer = PRAnalyzer()
    
    async def analyze_pr(self, pr_url, output_format='text', output_file=None):
        """Analyze a PR and output results"""
        try:
            print(f"🔍 Analyzing PR: {pr_url}")
            print("⏳ Fetching PR data...")
            
            # Get provider and PR data
            provider = GitProviderFactory.get_provider(pr_url)
            pr_data = await provider.get_pr_data(pr_url)
            
            print("🤖 Running AI analysis...")
            
            # Analyze the PR
            feedback = await self.analyzer.analyze_pr(pr_data)
            
            # Output results
            if output_format == 'json':
                self._output_json(feedback, output_file)
            else:
                self._output_text(feedback, pr_data, output_file)
                
            return feedback
            
        except Exception as e:
            print(f"❌ Error: {str(e)}", file=sys.stderr)
            sys.exit(1)
    
    def _output_text(self, feedback, pr_data, output_file=None):
        """Output results in human-readable text format"""
        output = []
        
        # Header
        output.append("=" * 80)
        output.append("🤖 PR REVIEW ANALYSIS REPORT")
        output.append("=" * 80)
        output.append("")
        
        # PR Info
        output.append(f"📋 PR Title: {pr_data.title}")
        output.append(f"👤 Author: {pr_data.author}")
        output.append(f"🔗 URL: {pr_data.url}")
        output.append(f"🏢 Provider: {pr_data.provider}")
        output.append("")
        
        # Score
        score_emoji = "🟢" if feedback.score >= 80 else "🟡" if feedback.score >= 60 else "🔴"
        output.append(f"📊 OVERALL SCORE: {score_emoji} {feedback.score}/100")
        output.append("")
        
        # Summary
        output.append("📝 SUMMARY")
        output.append("-" * 40)
        output.append(feedback.summary)
        output.append("")
        
        # Issues
        if feedback.issues:
            output.append(f"🐛 ISSUES FOUND ({len(feedback.issues)})")
            output.append("-" * 40)
            
            for i, issue in enumerate(feedback.issues, 1):
                emoji = "🔴" if issue.type == "error" else "🟡" if issue.type == "warning" else "🔵"
                output.append(f"{i}. {emoji} {issue.type.upper()}")
                output.append(f"   📁 File: {issue.file}")
                if issue.line:
                    output.append(f"   📍 Line: {issue.line}")
                output.append(f"   💬 Message: {issue.message}")
                if issue.suggestion:
                    output.append(f"   💡 Suggestion: {issue.suggestion}")
                output.append("")
        else:
            output.append("✅ No issues found!")
            output.append("")
        
        # Recommendations
        if feedback.recommendations:
            output.append(f"💡 RECOMMENDATIONS ({len(feedback.recommendations)})")
            output.append("-" * 40)
            
            for i, rec in enumerate(feedback.recommendations, 1):
                output.append(f"{i}. ✨ {rec}")
            output.append("")
        
        # Statistics
        error_count = len([i for i in feedback.issues if i.type == "error"])
        warning_count = len([i for i in feedback.issues if i.type == "warning"])
        info_count = len([i for i in feedback.issues if i.type == "info"])
        
        output.append("📈 STATISTICS")
        output.append("-" * 40)
        output.append(f"🔴 Errors: {error_count}")
        output.append(f"🟡 Warnings: {warning_count}")
        output.append(f"🔵 Info: {info_count}")
        output.append(f"📁 Files Changed: {len(pr_data.files_changed)}")
        output.append("")
        
        output.append("=" * 80)
        
        result = "\n".join(output)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(result)
            print(f"📄 Report saved to: {output_file}")
        else:
            print(result)
    
    def _output_json(self, feedback, output_file=None):
        """Output results in JSON format"""
        if hasattr(feedback, 'model_dump'):
            data = feedback.model_dump()
        elif hasattr(feedback, 'dict'):
            data = feedback.dict()
        else:
            data = feedback
        
        json_output = json.dumps(data, indent=2, ensure_ascii=False)
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(json_output)
            print(f"📄 JSON report saved to: {output_file}")
        else:
            print(json_output)
    
    def list_history(self):
        """List analysis history"""
        history_file = "analysis_history.json"
        
        if not os.path.exists(history_file):
            print("📭 No analysis history found.")
            return
        
        try:
            with open(history_file, 'r') as f:
                history = json.load(f)
            
            if not history:
                print("📭 No analysis history found.")
                return
            
            print("📚 ANALYSIS HISTORY")
            print("=" * 80)
            
            for i, entry in enumerate(history[:10], 1):  # Show last 10
                score_emoji = "🟢" if entry['score'] >= 80 else "🟡" if entry['score'] >= 60 else "🔴"
                print(f"{i}. {score_emoji} {entry['score']}/100 - {entry['pr_title']}")
                print(f"   👤 {entry['author']} | 📅 {entry['timestamp']} | 🐛 {entry['issues_count']} issues")
                print(f"   🔗 {entry['pr_url']}")
                print()
                
        except Exception as e:
            print(f"❌ Error reading history: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="PR Review Agent - AI-powered code review",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s https://github.com/owner/repo/pull/123
  %(prog)s https://github.com/owner/repo/pull/123 --format json
  %(prog)s https://github.com/owner/repo/pull/123 --output report.txt
  %(prog)s --history
        """
    )
    
    parser.add_argument('pr_url', nargs='?', help='Pull request URL to analyze')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                       help='Output format (default: text)')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--history', action='store_true',
                       help='Show analysis history')
    
    args = parser.parse_args()
    
    # Check environment
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Error: OPENAI_API_KEY environment variable not set")
        print("Please create a .env file with your OpenAI API key")
        sys.exit(1)
    
    cli = PRReviewCLI()
    
    if args.history:
        cli.list_history()
    elif args.pr_url:
        asyncio.run(cli.analyze_pr(args.pr_url, args.format, args.output))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()