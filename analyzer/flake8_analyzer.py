"""
Flake8 Code Quality Analyzer
"""

import subprocess
import tempfile
import os
from typing import Dict, Any, List
import json


class Flake8Analyzer:
    """Analyzes code quality using Flake8."""
    
    def __init__(self):
        self.name = "flake8"
    
    def analyze(self, changed_files: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze changed files using Flake8.
        
        Args:
            changed_files: List of changed files with their content
            
        Returns:
            Dictionary containing analysis results
        """
        issues = []
        total_errors = 0
        total_warnings = 0
        
        # Process each changed file
        for file in changed_files:
            if file['status'] in ['added', 'modified']:  # Only analyze added/modified files
                filename = file['filename']
                
                # Create temporary file with the content
                with tempfile.NamedTemporaryFile(mode='w', suffix=os.path.splitext(filename)[1], delete=False) as tmp_file:
                    tmp_file.write(file.get('patch', ''))  # Use patch content
                    tmp_filename = tmp_file.name
                
                try:
                    # Run flake8 on the temporary file
                    result = subprocess.run(
                        ['flake8', '--format', '%(row)s:%(col)s:%(code)s:%(text)s', tmp_filename],
                        capture_output=True,
                        text=True,
                        cwd=os.getcwd()
                    )
                    
                    # Parse flake8 output
                    if result.stdout:
                        for line in result.stdout.strip().split('\n'):
                            if line.strip():
                                parts = line.split(':', 3)
                                if len(parts) >= 4:
                                    row, col, code, text = parts[0], parts[1], parts[2], parts[3]
                                    issues.append({
                                        'file': filename,
                                        'line': int(row),
                                        'column': int(col),
                                        'code': code,
                                        'message': text,
                                        'severity': self._get_severity(code)
                                    })
                                    if self._is_error(code):
                                        total_errors += 1
                                    else:
                                        total_warnings += 1
                    
                    # Check for errors in stderr
                    if result.stderr:
                        issues.append({
                            'file': filename,
                            'message': f"Flake8 error: {result.stderr}",
                            'severity': 'error'
                        })
                        
                except FileNotFoundError:
                    issues.append({
                        'file': filename,
                        'message': "Flake8 not installed or not in PATH",
                        'severity': 'error'
                    })
                except Exception as e:
                    issues.append({
                        'file': filename,
                        'message': f"Error running Flake8: {str(e)}",
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
            'issues': issues
        }
    
    def _get_severity(self, code: str) -> str:
        """Determine severity based on Flake8 error code."""
        if code.startswith('E') or code.startswith('F'):
            return 'error'
        elif code.startswith('W') or code.startswith('C'):
            return 'warning'
        else:
            return 'info'
    
    def _is_error(self, code: str) -> bool:
        """Check if the code represents an error (vs warning)."""
        return code.startswith('E') or code.startswith('F')
