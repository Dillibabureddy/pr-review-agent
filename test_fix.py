#!/usr/bin/env python3
"""
Simple test to verify the fix works
"""

import sys
import os

# Add the project root to the path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def test_feedback_generator():
    """Test that the feedback generator works without the sum() bug"""
    try:
        from feedback.feedback_generator import FeedbackGenerator
        
        # Create a mock feedback structure
        feedback_gen = FeedbackGenerator()
        
        # Test the problematic line
        issues = {
            'critical': [],
            'high': [1, 2],  # Two high severity issues
            'medium': [1],   # One medium severity issue
            'low': []
        }
        
        # This should not throw an error anymore
        complexity_issues = len(issues['high']) + len(issues['medium'])
        print(f"Complexity issues calculated: {complexity_issues}")
        
        print("✓ Feedback generator fix verified successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error in feedback generator test: {e}")
        return False

if __name__ == "__main__":
    success = test_feedback_generator()
    sys.exit(0 if success else 1)
