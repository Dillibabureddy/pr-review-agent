"""
Pylint Code Quality Analyzer
"""

import subprocess
import tempfile
import os
import json
from typing import Dict, Any, List


class PylintAnalyzer:
    """Analyzes code quality using Pylint."""
    
    def __init__(self):
        self.name = "pylint"
    
    def analyze(self, changed_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze changed files using Pylint.
        
        Args:
            changed_files: List of changed files with their content
            
        Returns:
            Dictionary containing analysis results
        """
        issues = []
        total_errors = 0
        total_warnings = 0
        total_infos = 0
        
        # Process each changed file
        for file in changed_files:
            if file['status'] in ['added', 'modified']:  # Only analyze added/modified files
                filename = file['filename']
                
                # Create temporary file with the content
                with tempfile.NamedTemporaryFile(mode='w', suffix=os.path.splitext(filename)[1], delete=False) as tmp_file:
                    tmp_file.write(file.get('patch', ''))  # Use patch content
                    tmp_filename = tmp_file.name
                
                try:
                    # Run pylint on the temporary file with JSON output
                    result = subprocess.run(
                        ['pylint', '--output-format=json', tmp_filename],
                        capture_output=True,
                        text=True,
                        cwd=os.getcwd()
                    )
                    
                    # Parse pylint JSON output
                    if result.stdout:
                        try:
                            pylint_output = json.loads(result.stdout)
                            for item in pylint_output:
                                message = item['message']
                                line = item['line']
                                column = item['column']
                                category = item['category']
                                symbol = item['symbol']
                                
                                issues.append({
                                    'file': filename,
                                    'line': line,
                                    'column': column,
                                    'code': symbol,
                                    'message': message,
                                    'severity': self._get_severity(category)
                                })
                                
                                if category == 'error':
                                    total_errors += 1
                                elif category == 'warning':
                                    total_warnings += 1
                                elif category == 'info':
                                    total_infos += 1
                        except json.JSONDecodeError:
                            # If JSON parsing fails, add the raw output as an issue
                            issues.append({
                                'file': filename,
                                'message': f"Pylint output parsing error: {result.stdout}",
                                'severity': 'error'
                            })
                    
                    # Check for errors in stderr
                    if result.stderr:
                        issues.append({
                            'file': filename,
                            'message': f"Pylint error: {result.stderr}",
                            'severity': 'error'
                        })
                        
                except FileNotFoundError:
                    issues.append({
                        'file': filename,
                        'message': "Pylint not installed or not in PATH",
                        'severity': 'error'
                    })
                except Exception as e:
                    issues.append({
                        'file': filename,
                        'message': f"Error running Pylint: {str(e)}",
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
            'errors': total_errors,
            'warnings': total_warnings,
            'infos': total_infos,
            'issues': issues
        }
    
    def _get_severity(self, category: str) -> str:
        """Determine severity based on Pylint category."""
        if category == 'error':
            return 'error'
        elif category == 'warning':
            return 'warning'
        elif category == 'convention':
            return 'info'
        elif category == 'refactor':
            return 'info'
        elif category == 'info':
            return 'info'
        else:
            return 'info'
