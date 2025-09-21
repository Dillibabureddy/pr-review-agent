#!/usr/bin/env python3
"""
Validation script to test that all modules can be imported correctly
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_imports():
    """Test that all modules can be imported"""
    try:
        # Test main module
        from main import PRReviewAgent
        print("✓ main.py imported successfully")
        
        # Test fetchers
        from fetcher.github_fetcher import GitHubFetcher
        from fetcher.gitlab_fetcher import GitLabFetcher
        from fetcher.bitbucket_fetcher import BitbucketFetcher
        print("✓ All fetcher modules imported successfully")
        
        # Test analyzers
        from analyzer.flake8_analyzer import Flake8Analyzer
        from analyzer.pylint_analyzer import PylintAnalyzer
        from analyzer.radon_analyzer import RadonAnalyzer
        print("✓ All analyzer modules imported successfully")
        
        # Test feedback generator
        from feedback.feedback_generator import FeedbackGenerator
        print("✓ feedback_generator.py imported successfully")
        
        # Test that the agent can be instantiated
        agent = PRReviewAgent()
        print("✓ PRReviewAgent instantiated successfully")
        
        print("\n🎉 All modules imported and initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)
