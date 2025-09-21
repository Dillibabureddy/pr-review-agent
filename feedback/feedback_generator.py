"""
Feedback Generator for PR Review Agent
"""

from typing import Dict, Any, List
import re


class FeedbackGenerator:
    """Generates human-readable feedback from analysis results."""
    
    def __init__(self):
        self.severity_mapping = {
            'error': 'critical',
            'warning': 'high',
            'info': 'medium'
        }
    
    def generate_feedback(self, pr_data: Dict[str, Any], 
                         analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive feedback from PR data and analysis results.
        
        Args:
            pr_data: Dictionary containing PR information
            analysis_results: Dictionary containing analysis from all analyzers
            
        Returns:
            Dictionary containing structured feedback
        """
        feedback = {
            'issues': {},
            'recommendations': [],
            'summary': {}
        }
        
        # Categorize issues by severity
        feedback['issues'] = {
            'critical': [],
            'high': [],
            'medium': [],
            'low': []
        }
        
        # Process issues from all analyzers
        for analyzer_name, result in analysis_results.items():
            if 'issues' in result and result['issues']:
                for issue in result['issues']:
                    severity = self._map_severity(issue.get('severity', 'info'))
                    feedback['issues'][severity].append({
                        'analyzer': analyzer_name,
                        'file': issue.get('file', 'unknown'),
                        'line': issue.get('line', 0),
                        'message': issue.get('message', 'Unknown issue'),
                        'code': issue.get('code', 'unknown')
                    })
        
        # Generate recommendations based on issues
        feedback['recommendations'] = self._generate_recommendations(
            pr_data, analysis_results, feedback['issues']
        )
        
        # Generate summary
        feedback['summary'] = self._generate_summary(analysis_results)
        
        return feedback
    
    def _map_severity(self, severity: str) -> str:
        """Map analyzer severity to our standard severity levels."""
        return self.severity_mapping.get(severity.lower(), 'medium')
    
    def _generate_recommendations(self, pr_data: Dict[str, Any], 
                                 analysis_results: Dict[str, Any], 
                                 issues: Dict[str, List[Dict]]) -> List[str]:
        """
        Generate actionable recommendations based on issues found.
        """
        recommendations = []
        
        # General recommendations
        recommendations.append("Ensure all code follows the project's style guidelines")
        recommendations.append("Review all identified issues before merging")
        
        # Specific recommendations based on issues
        total_critical = len(issues['critical'])
        total_high = len(issues['high'])
        total_medium = len(issues['medium'])
        
        if total_critical > 0:
            recommendations.append(f"Fix {total_critical} critical issues before merging")
        
        if total_high > 0:
            recommendations.append(f"Address {total_high} high severity issues")
        
        if total_medium > 0:
            recommendations.append(f"Consider addressing {total_medium} medium severity issues")
        
        # Check for specific patterns
        if self._has_security_issues(analysis_results):
            recommendations.append("Review security implications of code changes")
        
        if self._has_performance_issues(analysis_results):
            recommendations.append("Consider performance optimizations")
        
        # Check for complexity issues
        complexity_issues = len(issues['high']) + len(issues['medium'])
        if complexity_issues > 0:
            recommendations.append("Refactor complex functions to improve readability")
        
        # Check for documentation issues
        if self._has_documentation_issues(analysis_results):
            recommendations.append("Update documentation to reflect code changes")
        
        # Remove duplicates
        recommendations = list(dict.fromkeys(recommendations))  # Preserve order while removing duplicates
        
        return recommendations
    
    def _has_security_issues(self, analysis_results: Dict[str, Any]) -> bool:
        """Check if there are potential security issues."""
        # This is a simplified check - in a real implementation, this would be more sophisticated
        for analyzer_name, result in analysis_results.items():
            if 'issues' in result:
                for issue in result['issues']:
                    message = issue.get('message', '').lower()
                    if any(keyword in message for keyword in ['security', 'vulnerability', 'injection', 'sql']):
                        return True
        return False
    
    def _has_performance_issues(self, analysis_results: Dict[str, Any]) -> bool:
        """Check if there are potential performance issues."""
        # This is a simplified check - in a real implementation, this would be more sophisticated
        for analyzer_name, result in analysis_results.items():
            if 'issues' in result:
                for issue in result['issues']:
                    message = issue.get('message', '').lower()
                    if any(keyword in message for keyword in ['performance', 'slow', 'inefficient', 'memory']):
                        return True
        return False
    
    def _has_documentation_issues(self, analysis_results: Dict[str, Any]) -> bool:
        """Check if there are documentation-related issues."""
        # This is a simplified check - in a real implementation, this would be more sophisticated
        for analyzer_name, result in analysis_results.items():
            if 'issues' in result:
                for issue in result['issues']:
                    message = issue.get('message', '').lower()
                    if any(keyword in message for keyword in ['docstring', 'documentation', 'missing']):
                        return True
        return False
    
    def _generate_summary(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a summary of the analysis."""
        summary = {
            'total_issues': 0,
            'by_severity': {
                'critical': 0,
                'high': 0,
                'medium': 0,
                'low': 0
            },
            'analyzers_used': list(analysis_results.keys())
        }
        
        for analyzer_name, result in analysis_results.items():
            if 'total_issues' in result:
                summary['total_issues'] += result['total_issues']
                summary['by_severity']['critical'] += result.get('errors', 0)
                summary['by_severity']['high'] += result.get('warnings', 0)
                summary['by_severity']['medium'] += result.get('infos', 0)
        
        return summary
