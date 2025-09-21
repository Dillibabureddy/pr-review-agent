"""
GitHub PR Fetcher
"""

import requests
import json
from typing import Dict, Any, List
from urllib.parse import urljoin


class GitHubFetcher:
    """Fetches pull request data from GitHub."""
    
    def __init__(self, base_url: str = "https://api.github.com"):
        self.base_url = base_url
    
    def fetch_pr(self, repo_owner: str, repo_name: str, pr_number: int, 
                token: str = None, base_url: str = None) -> Dict[str, Any]:
        """
        Fetch pull request data from GitHub.
        
        Args:
            repo_owner: Repository owner/organization name
            repo_name: Repository name
            pr_number: Pull request number
            token: GitHub personal access token
            base_url: Base URL for GitHub API (default: https://api.github.com)
            
        Returns:
            Dictionary containing PR data
        """
        if base_url:
            self.base_url = base_url
            
        headers = {
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'PR-Review-Agent'
        }
        
        if token:
            headers['Authorization'] = f'token {token}'
        
        # Fetch PR details
        pr_url = urljoin(self.base_url, f"/repos/{repo_owner}/{repo_name}/pulls/{pr_number}")
        pr_response = requests.get(pr_url, headers=headers)
        
        if pr_response.status_code != 200:
            raise Exception(f"Failed to fetch PR: {pr_response.status_code} - {pr_response.text}")
        
        pr_data = pr_response.json()
        
        # Fetch changed files
        files_url = urljoin(self.base_url, f"/repos/{repo_owner}/{repo_name}/pulls/{pr_number}/files")
        files_response = requests.get(files_url, headers=headers)
        
        if files_response.status_code != 200:
            raise Exception(f"Failed to fetch PR files: {files_response.status_code} - {files_response.text}")
        
        files_data = files_response.json()
        
        # Process files to extract relevant information
        changed_files = []
        for file in files_data:
            changed_files.append({
                'filename': file['filename'],
                'status': file['status'],
                'additions': file['additions'],
                'deletions': file['deletions'],
                'patch': file.get('patch', ''),
                'raw_url': file.get('raw_url', '')
            })
        
        return {
            'id': pr_data['number'],
            'title': pr_data['title'],
            'description': pr_data['body'],
            'author': pr_data['user']['login'],
            'created_at': pr_data['created_at'],
            'updated_at': pr_data['updated_at'],
            'status': pr_data['state'],
            'base_branch': pr_data['base']['ref'],
            'head_branch': pr_data['head']['ref'],
            'changed_files': changed_files,
            'url': pr_data['html_url']
        }
