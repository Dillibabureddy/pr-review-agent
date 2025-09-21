#!/usr/bin/env python3
"""
PR Review Agent - Multi-server Pull Request Review System
"""

import argparse
import sys
import os
from typing import Dict, Any

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from fetcher.github_fetcher import GitHubFetcher
from fetcher.gitlab_fetcher import GitLabFetcher
from fetcher.bitbucket_fetcher import BitbucketFetcher
from analyzer.flake8_analyzer import Flake8Analyzer
from analyzer.pylint_analyzer import PylintAnalyzer
from analyzer.radon_analyzer import RadonAnalyzer
from feedback.feedback_generator import FeedbackGenerator


class PRReviewAgent:
    """Main PR Review Agent class that orchestrates the review process."""
    
    def __init__(self):
        self.fetchers = {
            'github': GitHubFetcher(),
            'gitlab': GitLabFetcher(),
            'bitbucket': BitbucketFetcher()
        }
        
        self.analyzers = {
            'flake8': Flake8Analyzer(),
            'pylint': PylintAnalyzer(),
            'radon': RadonAnalyzer()
        }
        
        self.feedback_generator = FeedbackGenerator()
    
    def review_pr(self, server_type: str, repo_owner: str, repo_name: str, pr_number: int, 
                  token: str = None, base_url: str = None) -> Dict[str, Any]:
        """
        Main method to review a pull request from any supported git server.
        
        Args:
            server_type: Type of git server ('github', 'gitlab', 'bitbucket')
            repo_owner: Repository owner/organization name
            repo_name: Repository name
            pr_number: Pull request number
            token: Authentication token for the git server
            base_url: Base URL for the git server API (for self-hosted instances)
            
        Returns:
            Dictionary containing review results
        """
        # Validate server type
        if server_type not in self.fetchers:
            raise ValueError(f"Unsupported server type: {server_type}. "
                           f"Supported types: {list(self.fetchers.keys())}")
        
        # Fetch PR data
        print(f"Fetching PR #{pr_number} from {server_type}://{repo_owner}/{repo_name}")
        pr_data = self.fetchers[server_type].fetch_pr(
            repo_owner=repo_owner,
            repo_name=repo_name,
            pr_number=pr_number,
            token=token,
            base_url=base_url
        )
        
        # Analyze code changes
        print("Analyzing code quality...")
        analysis_results = {}
        for analyzer_name, analyzer in self.analyzers.items():
            try:
                analysis_results[analyzer_name] = analyzer.analyze(pr_data['changed_files'])
            except Exception as e:
                print(f"Error analyzing with {analyzer_name}: {str(e)}")
                analysis_results[analyzer_name] = {"error": str(e)}
        
        # Generate feedback
        print("Generating feedback...")
        feedback = self.feedback_generator.generate_feedback(
            pr_data=pr_data,
            analysis_results=analysis_results
        )
        
        # Calculate quality score
        quality_score = self._calculate_quality_score(feedback)
        
        return {
            'pr_info': pr_data,
            'analysis': analysis_results,
            'feedback': feedback,
            'quality_score': quality_score
        }
    
    def _calculate_quality_score(self, feedback: Dict[str, Any]) -> float:
        """
        Calculate a quality score based on feedback severity.
        
        Args:
            feedback: Generated feedback dictionary
            
        Returns:
            Quality score between 0 and 100
        """
        # Simple scoring algorithm - can be enhanced
        total_issues = sum(len(issues) for issues in feedback.get('issues', {}).values())
        severity_weights = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 1
        }
        
        total_weighted_score = 0
        for severity, issues in feedback.get('issues', {}).items():
            weight = severity_weights.get(severity, 1)
            total_weighted_score += len(issues) * weight
        
        # Normalize score to 0-100 scale
        max_possible_score = 100  # Assuming maximum 100 weighted issues
        score = max(0, min(100, max_possible_score - total_weighted_score))
        
        return round(score, 2)


def main():
    """Main entry point for the PR Review Agent."""
    parser = argparse.ArgumentParser(description='Multi-server PR Review Agent')
    parser.add_argument('--server', '-s', required=True, choices=['github', 'gitlab', 'bitbucket'],
                       help='Git server type')
    parser.add_argument('--owner', '-o', required=True, help='Repository owner/organization')
    parser.add_argument('--repo', '-r', required=True, help='Repository name')
    parser.add_argument('--pr', '-p', type=int, required=True, help='Pull request number')
    parser.add_argument('--token', '-t', help='Authentication token')
    parser.add_argument('--base-url', help='Base URL for self-hosted instances')
    
    args = parser.parse_args()
    
    try:
        # Initialize the agent
        agent = PRReviewAgent()
        
        # Perform the review
        result = agent.review_pr(
            server_type=args.server,
            repo_owner=args.owner,
            repo_name=args.repo,
            pr_number=args.pr,
            token=args.token,
            base_url=args.base_url
        )
        
        # Display results
        print("\n" + "="*60)
        print("PULL REQUEST REVIEW RESULTS")
        print("="*60)
        print(f"Repository: {args.owner}/{args.repo}")
        print(f"PR Number: {args.pr}")
        print(f"Server: {args.server.upper()}")
        print(f"Quality Score: {result['quality_score']}/100")
        print("\n" + "-"*40)
        print("FEEDBACK SUMMARY")
        print("-"*40)
        
        for category, issues in result['feedback']['issues'].items():
            print(f"\n{category.upper()} ISSUES ({len(issues)}):")
            for issue in issues[:5]:  # Show first 5 issues
                print(f"  - {issue}")
            if len(issues) > 5:
                print(f"  ... and {len(issues) - 5} more issues")
        
        print("\n" + "-"*40)
        print("RECOMMENDATIONS")
        print("-"*40)
        for rec in result['feedback']['recommendations']:
            print(f"  • {rec}")
            
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"Error during PR review: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
