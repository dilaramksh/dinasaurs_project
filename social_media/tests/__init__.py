from unittest import TestLoader

# Automatically load all test modules
test_loader = TestLoader()
discover_tests = test_loader.discover(start_dir='.', pattern='test_*.py')