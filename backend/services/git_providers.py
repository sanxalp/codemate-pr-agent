import re
import os
import requests
from abc import ABC, abstractmethod
from typing import Dict, Any
import base64
from urllib.parse import urlparse

from models.feedback import PRData

class GitProvider(ABC):
    """Abstract base class for git providers"""
    
    @abstractmethod
    async def get_pr_data(self, pr_url: str) -> PRData:
        """Get PR data from the provider"""
        pass

class GitHubProvider(GitProvider):
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    async def get_pr_data(self, pr_url: str) -> PRData:
        # Parse GitHub PR URL
        match = re.match(r'https://github\.com/([^/]+)/([^/]+)/pull/(\d+)', pr_url)
        if not match:
            raise ValueError("Invalid GitHub PR URL")
        
        owner, repo, pr_number = match.groups()
        
        # Get PR details
        pr_response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}",
            headers=self.headers
        )
        pr_response.raise_for_status()
        pr_data = pr_response.json()
        
        # Get PR files
        files_response = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files",
            headers=self.headers
        )
        files_response.raise_for_status()
        files_data = files_response.json()
        
        # Get diff
        diff_response = requests.get(
            pr_data["diff_url"],
            headers=self.headers
        )
        diff_response.raise_for_status()
        
        return PRData(
            title=pr_data["title"],
            description=pr_data["body"] or "",
            files_changed=files_data,
            diff=diff_response.text,
            author=pr_data["user"]["login"],
            url=pr_url,
            provider="github"
        )

class GitLabProvider(GitProvider):
    def __init__(self):
        self.token = os.getenv("GITLAB_TOKEN")
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
    
    async def get_pr_data(self, pr_url: str) -> PRData:
        # Parse GitLab MR URL
        match = re.match(r'https://gitlab\.com/([^/]+)/([^/]+)/-/merge_requests/(\d+)', pr_url)
        if not match:
            raise ValueError("Invalid GitLab MR URL")
        
        owner, repo, mr_number = match.groups()
        project_path = f"{owner}/{repo}"
        
        # Get MR details
        mr_response = requests.get(
            f"https://gitlab.com/api/v4/projects/{project_path.replace('/', '%2F')}/merge_requests/{mr_number}",
            headers=self.headers
        )
        mr_response.raise_for_status()
        mr_data = mr_response.json()
        
        # Get MR changes
        changes_response = requests.get(
            f"https://gitlab.com/api/v4/projects/{project_path.replace('/', '%2F')}/merge_requests/{mr_number}/changes",
            headers=self.headers
        )
        changes_response.raise_for_status()
        changes_data = changes_response.json()
        
        # Build diff from changes
        diff_parts = []
        for change in changes_data.get("changes", []):
            diff_parts.append(change.get("diff", ""))
        
        return PRData(
            title=mr_data["title"],
            description=mr_data["description"] or "",
            files_changed=changes_data.get("changes", []),
            diff="\n".join(diff_parts),
            author=mr_data["author"]["username"],
            url=pr_url,
            provider="gitlab"
        )

class BitbucketProvider(GitProvider):
    def __init__(self):
        self.username = os.getenv("BITBUCKET_USERNAME", "dummy_user")
        self.password = os.getenv("BITBUCKET_APP_PASSWORD", "dummy_password")
        auth_string = f"{self.username}:{self.password}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        self.headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Accept": "application/json"
        }
    
    async def get_pr_data(self, pr_url: str) -> PRData:
        # Parse Bitbucket PR URL
        match = re.match(r'https://bitbucket\.org/([^/]+)/([^/]+)/pull-requests/(\d+)', pr_url)
        if not match:
            raise ValueError("Invalid Bitbucket PR URL")
        
        workspace, repo, pr_number = match.groups()
        
        # For demo purposes with dummy credentials, return mock data
        if self.username == "dummy_user":
            return PRData(
                title="Sample Bitbucket PR",
                description="This is a sample PR from Bitbucket (using dummy credentials)",
                files_changed=[
                    {
                        "filename": "src/main.py",
                        "status": "modified",
                        "additions": 10,
                        "deletions": 5
                    }
                ],
                diff="@@ -1,5 +1,10 @@\n def main():\n+    print('Hello World')\n     pass",
                author="sample_user",
                url=pr_url,
                provider="bitbucket"
            )
        
        # Real implementation would make API calls here
        try:
            pr_response = requests.get(
                f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo}/pullrequests/{pr_number}",
                headers=self.headers
            )
            pr_response.raise_for_status()
            pr_data = pr_response.json()
            
            # Get diff
            diff_response = requests.get(
                f"https://api.bitbucket.org/2.0/repositories/{workspace}/{repo}/pullrequests/{pr_number}/diff",
                headers=self.headers
            )
            diff_response.raise_for_status()
            
            return PRData(
                title=pr_data["title"],
                description=pr_data["description"] or "",
                files_changed=[],  # Bitbucket API structure differs
                diff=diff_response.text,
                author=pr_data["author"]["username"],
                url=pr_url,
                provider="bitbucket"
            )
        except Exception:
            # Fallback to dummy data if API fails
            return PRData(
                title="Bitbucket PR (API Error - using dummy data)",
                description="Could not fetch real data, using dummy data",
                files_changed=[],
                diff="Sample diff content",
                author="unknown_user",
                url=pr_url,
                provider="bitbucket"
            )

class GitProviderFactory:
    """Factory class to get the appropriate git provider"""
    
    @staticmethod
    def get_provider(pr_url: str) -> GitProvider:
        if "github.com" in pr_url:
            return GitHubProvider()
        elif "gitlab.com" in pr_url:
            return GitLabProvider()
        elif "bitbucket.org" in pr_url:
            return BitbucketProvider()
        else:
            raise ValueError(f"Unsupported git provider for URL: {pr_url}")