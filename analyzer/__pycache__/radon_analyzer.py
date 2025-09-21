"""
Radon Code Complexity Analyzer
"""

import subprocess
import tempfile
import os
import json
from typing import Dict, Any, List


class RadonAnalyzer:
    """Analyzes code complexity using Radon."""
    
    def __init__(self):
        self.name = "radon"
    
    def analyze(self, changed_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze code complexity using Radon.
        
        Args:
            changed_files: List of changed files with their content
            
        Returns:
            Dictionary containing analysis results
        """
        issues = []
        total_complexity_issues = 0
        
        # Process each changed file
        for file in changed_files:
            if file['status'] in ['added', 'modified']:  # Only analyze added/modified files
                filename = file['filename']
                
                # Create temporary file with the content
                with tempfile.NamedTemporaryFile(mode='w', suffix=os.path.splitext(filename)[1], delete=False) as tmp_file:
                    tmp_file.write(file.get('patch', ''))  # Use patch content
                    tmp_filename = tmp_file.name
                
                try:
                    # Run radon cc (cyclomatic complexity) on the temporary file
                    result = subprocess.run(
                        ['radon', 'cc', '--json', '--no-assert', tmp_filename],
                        capture_output=True,
                        text=True,
                        cwd=os.getcwd()
                    )
                    
                    # Parse radon JSON output
                    if result.stdout:
                        try:
                            radon_output = json.loads(result.stdout)
                            
                            # Process each function/class complexity
                            for item in radon_output:
                                if 'complexity' in item:
                                    complexity = item['complexity']
                                    name = item['name']
                                    loc = item['loc']
                                    lloc = item['lloc']
                                    cc = item['cc']
                                    
                                    # Flag high complexity (threshold can be adjusted)
                                    if complexity > 5:  # High complexity threshold
                                        issues.append({
                                            'file': filename,
                                            'line': item.get('start_line', 0),
                                            'message': f"High complexity detected in {name}: {complexity} (CC: {cc})",
                                            'severity': 'warning',
                                            'details': {
                                                'complexity': complexity,
                                                'name': name,
                                                'loc': loc,
                                                'lloc': lloc,
                                                'cc': cc
                                            }
                                        })
                                        total_complexity_issues += 1
                        except json.JSONDecodeError:
                            # If JSON parsing fails, add the raw output as an issue
                            issues.append({
                                'file': filename,
                                'message': f"Radon output parsing error: {result.stdout}",
                                'severity': 'error'
                            })
                    
                    # Check for errors in stderr
                    if result.stderr:
                        issues.append({
                            'file': filename,
                            'message': f"Radon error: {result.stderr}",
                            'severity': 'error'
                        })
                        
                except FileNotFoundError:
                    issues.append({
                        'file': filename,
                        'message': "Radon not installed or not in PATH",
                        'severity': 'error'
                    })
                except Exception as e:
                    issues.append({
                        'file': filename,
                        'message': f"Error running Radon: {str(e)}",
                        'severity': 'error'
                    })
                finally:
                    # Clean up temporary file
                    try:
                        os.unlink(tmp_filename)
                    except:
                        pass
        
        return {
            'total_issues': len(issues),
            'complexity_issues': total_complexity_issues,
            'issues': issues
        }
