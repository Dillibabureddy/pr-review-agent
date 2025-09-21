"""
Bitbucket PR Fetcher
"""

import requests
from typing import Dict, Any
from urllib.parse import urljoin


class BitbucketFetcher:
    """Fetches pull request data from Bitbucket."""
    
    def __init__(self, base_url: str = "https://api.bitbucket.org/2.0"):
        self.base_url = base_url
    
    def fetch_pr(self, repo_owner: str, repo_name: str, pr_number: int, 
                token: str = None, base_url: str = None) -> Dict[str, Any]:
        """
        Fetch pull request data from Bitbucket.
        
        Args:
            repo_owner: Repository owner/organization name
            repo_name: Repository name
            pr_number: Pull request number
            token: Bitbucket personal access token
            base_url: Base URL for Bitbucket API (default: https://api.bitbucket.org/2.0)
            
        Returns:
            Dictionary containing PR data
        """
        if base_url:
            self.base_url = base_url
            
        headers = {
            'User-Agent': 'PR-Review-Agent'
        }
        
        # Bitbucket uses basic auth with token
        if token:
            headers['Authorization'] = f'Bearer {token}'
        
        # Fetch PR details
        pr_url = urljoin(self.base_url, f"/repositories/{repo_owner}/{repo_name}/pullrequests/{pr_number}")
        pr_response = requests.get(pr_url, headers=headers)
        
        if pr_response.status_code != 200:
            raise Exception(f"Failed to fetch PR: {pr_response.status_code} - {pr_response.text}")
        
        pr_data = pr_response.json()
        
        # Fetch changed files
        files_url = urljoin(self.base_url, f"/repositories/{repo_owner}/{repo_name}/pullrequests/{pr_number}/diffstat")
        files_response = requests.get(files_url, headers=headers)
        
        if files_response.status_code != 200:
            raise Exception(f"Failed to fetch PR files: {files_response.status_code} - {files_response.text}")
        
        files_data = files_response.json()
        
        # Process files to extract relevant information
        changed_files = []
        for file in files_data.get('values', []):
            changed_files.append({
                'filename': file['path'],
                'status': file['status'],
                'additions': file.get('added', 0),
                'deletions': file.get('removed', 0),
                'patch': '',  # Bitbucket doesn't provide patch in diffstat
                'raw_url': ''  # Bitbucket doesn't provide raw URLs in this endpoint
            })
        
        return {
            'id': pr_data['id'],
            'title': pr_data['title'],
            'description': pr_data['description'],
            'author': pr_data['author']['username'] if pr_data.get('author') else '',
            'created_at': pr_data['created_on'],
            'updated_at': pr_data['updated_on'],
            'status': pr_data['state'],
            'base_branch': pr_data['destination']['branch']['name'],
            'head_branch': pr_data['source']['branch']['name'],
            'changed_files': changed_files,
            'url': pr_data['links']['html']['href']
        }
