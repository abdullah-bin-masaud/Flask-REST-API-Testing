"""
CLI Runner for Flask REST API QA tests.
"""
import pytest
import sys
from pathlib import Path

if __name__ == "__main__":
    tests_dir = Path(__file__).parent / "tests"
    print("=" * 60)
    print("  EXECUTING REST API QUALITY ASSURANCE SUITE")
    print("=" * 60)
    sys.exit(pytest.main(["-v", str(tests_dir)]))
