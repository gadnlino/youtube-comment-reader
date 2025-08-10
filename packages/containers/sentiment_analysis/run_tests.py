#!/usr/bin/env python3
"""
Test runner for LlmClassifier tests.
"""

import sys
import os
import subprocess

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run the LlmClassifier tests."""
    try:
        # Run pytest on the test file
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/test_llm_classifier.py", 
            "-v"
        ], capture_output=True, text=True)
        
        print("Test Output:")
        print(result.stdout)
        
        if result.stderr:
            print("Test Errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1) 