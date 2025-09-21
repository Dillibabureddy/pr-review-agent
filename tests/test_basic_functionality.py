"""
Basic functionality tests for PR Review Agent
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__)) + '/..'
sys.path.insert(0, project_root)

from fetcher.github_fetcher import GitHubFetcher
from fetcher.gitlab_fetcher import GitLabFetcher
from fetcher.bitbucket_fetcher import BitbucketFetcher
from analyzer.flake8_analyzer import Flake8Analyzer
from analyzer.pylint_analyzer import PylintAnalyzer
from analyzer.radon_analyzer import RadonAnalyzer
from feedback.feedback_generator import FeedbackGenerator
from main import PRReviewAgent


class TestPRReviewAgent(unittest.TestCase):
    """Test the PR Review Agent components."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.github_fetcher = GitHubFetcher()
        self.gitlab_fetcher = GitLabFetcher()
        self.bitbucket_fetcher = BitbucketFetcher()
        self.flake8_analyzer = Flake8Analyzer()
        self.pylint_analyzer = PylintAnalyzer()
        self.radon_analyzer = RadonAnalyzer()
        self.feedback_generator = FeedbackGenerator()
        self.agent = PRReviewAgent()
    
    def test_agent_initialization(self):
        """Test that the agent initializes correctly."""
        self.assertIsNotNone(self.agent)
        self.assertIn('github', self.agent.fetchers)
        self.assertIn('gitlab', self.agent.fetchers)
        self.assertIn('bitbucket', self.agent.fetchers)
        self.assertIn('flake8', self.agent.analyzers)
        self.assertIn('pylint', self.agent.analyzers)
        self.assertIn('radon', self.agent.analyzers)
    
    def test_feedback_generator_initialization(self):
        """Test that the feedback generator initializes correctly."""
        self.assertIsNotNone(self.feedback_generator)
    
    def test_flake8_analyzer_initialization(self):
        """Test that the flake8 analyzer initializes correctly."""
        self.assertIsNotNone(self.flake8_analyzer)
    
    def test_pylint_analyzer_initialization(self):
        """Test that the pylint analyzer initializes correctly."""
        self.assertIsNotNone(self.pylint_analyzer)
    
    def test_radon_analyzer_initialization(self):
        """Test that the radon analyzer initializes correctly."""
        self.assertIsNotNone(self.radon_analyzer)
    
    def test_github_fetcher_initialization(self):
        """Test that the GitHub fetcher initializes correctly."""
        self.assertIsNotNone(self.github_fetcher)
    
    def test_gitlab_fetcher_initialization(self):
        """Test that the GitLab fetcher initializes correctly."""
        self.assertIsNotNone(self.gitlab_fetcher)
    
    def test_bitbucket_fetcher_initialization(self):
        """Test that the Bitbucket fetcher initializes correctly."""
        self.assertIsNotNone(self.bitbucket_fetcher)


if __name__ == '__main__':
    unittest.main()
