#!/usr/bin/env python3
"""
Test runner for the sentiment analysis Lambda function.

This script runs all tests for the Lambda function and provides
detailed output about test results.
"""

import sys
import subprocess
from pathlib import Path


def run_tests():
    """Run all tests for the sentiment analysis Lambda function."""
    # Add the current directory to Python path
    current_dir = Path(__file__).parent
    sys.path.insert(0, str(current_dir))
    
    print("Running sentiment analysis Lambda function tests...")
    print("=" * 60)

    try:
        # Run pytest with verbose output
        result = subprocess.run([
            sys.executable, '-m', 'pytest',
            'tests/',
            '-v',
            '--tb=short',
            '--color=yes'
        ], cwd=current_dir, capture_output=False)
        
        if result.returncode == 0:
            print("\n" + "=" * 60)
            print("✅ All tests passed successfully!")
            return True
        else:
            print("\n" + "=" * 60)
            print("❌ Some tests failed!")
            return False

    except Exception as e:
        print(f"Error running tests: {e}")
        return False


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
