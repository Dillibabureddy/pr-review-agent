"""
GitLab PR Fetcher (Merge Request Fetcher)
"""

import requests
from typing import Dict, Any
from urllib.parse import urljoin


class GitLabFetcher:
    """Fetches merge request data from GitLab."""
    
    def __init__(self, base_url: str = "https://gitlab.com/api/v4"):
        self.base_url = base_url
    
    def fetch_pr(self, repo_owner: str, repo_name: str, pr_number: int, 
                token: str = None, base_url: str = None) -> Dict[str, Any]:
        """
        Fetch merge request data from GitLab.
        
        Args:
            repo_owner: Repository owner/organization name
            repo_name: Repository name
            pr_number: Merge request number
            token: GitLab personal access token
            base_url: Base URL for GitLab API (default: https://gitlab.com/api/v4)
            
        Returns:
            Dictionary containing MR data
        """
        if base_url:
            self.base_url = base_url
            
        headers = {
            'User-Agent': 'PR-Review-Agent'
        }
        
        if token:
            headers['PRIVATE-TOKEN'] = token
        
        # Encode the project path properly (owner/repo)
        project_path = f"{repo_owner}/{repo_name}"
        
        # Fetch MR details
        mr_url = urljoin(self.base_url, f"/projects/{project_path}/merge_requests/{pr_number}")
        mr_response = requests.get(mr_url, headers=headers)
        
        if mr_response.status_code != 200:
            raise Exception(f"Failed to fetch MR: {mr_response.status_code} - {mr_response.text}")
        
        mr_data = mr_response.json()
        
        # Fetch changed files
        files_url = urljoin(self.base_url, f"/projects/{project_path}/merge_requests/{pr_number}/changes")
        files_response = requests.get(files_url, headers=headers)
        
        if files_response.status_code != 200:
            raise Exception(f"Failed to fetch MR files: {files_response.status_code} - {files_response.text}")
        
        files_data = files_response.json()
        
        # Process files to extract relevant information
        changed_files = []
        for file in files_data.get('changes', []):
            changed_files.append({
                'filename': file['new_path'],
                'status': file['status'],
                'additions': file.get('added_lines', 0),
                'deletions': file.get('removed_lines', 0),
                'patch': file.get('diff', ''),
                'raw_url': ''  # GitLab doesn't provide raw URLs in this endpoint
            })
        
        return {
            'id': mr_data['iid'],
            'title': mr_data['title'],
            'description': mr_data['description'],
            'author': mr_data['author']['username'],
            'created_at': mr_data['created_at'],
            'updated_at': mr_data['updated_at'],
            'status': mr_data['state'],
            'base_branch': mr_data['target_branch'],
            'head_branch': mr_data['source_branch'],
            'changed_files': changed_files,
            'url': mr_data['web_url']
        }
