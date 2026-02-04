#!/usr/bin/env python3
"""
Test runner script for GrizzlyDuck tests
"""
import os
import sys
import subprocess
import argparse


def run_tests(test_type='all', verbose=True, coverage=False):
    """Run tests with specified options"""
    
    # Ensure we're in the right directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    os.chdir(project_root)
    
    # Build pytest command
    cmd = ['python', '-m', 'pytest']
    
    if verbose:
        cmd.append('-v')
    
    if coverage:
        cmd.extend(['--cov=src', '--cov-report=html', '--cov-report=term'])
    
    # Select test type
    if test_type == 'unit':
        cmd.extend(['-m', 'unit'])
    elif test_type == 'integration':
        cmd.extend(['-m', 'integration'])
    elif test_type == 'fast':
        cmd.extend(['-m', 'not slow'])
    elif test_type == 'slow':
        cmd.extend(['-m', 'slow'])
    elif test_type == 'statistical':
        cmd.extend(['-m', 'statistical'])
    
    # Add test directory
    cmd.append('tests/')
    
    print(f"Running command: {' '.join(cmd)}")
    print("-" * 60)
    
    try:
        result = subprocess.run(cmd, check=False)
        return result.returncode
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


def main():
    parser = argparse.ArgumentParser(description='Run DuckQuery tests')
    
    parser.add_argument('--type', '-t', 
                       choices=['all', 'unit', 'integration', 'fast', 'slow', 'statistical'],
                       default='all',
                       help='Type of tests to run')
    
    parser.add_argument('--coverage', '-c',
                       action='store_true',
                       help='Run with coverage report')
    
    parser.add_argument('--quiet', '-q',
                       action='store_true',
                       help='Run with minimal output')
    
    parser.add_argument('--install-deps',
                       action='store_true',
                       help='Install test dependencies first')
    
    args = parser.parse_args()
    
    if args.install_deps:
        print("Installing test dependencies...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pytest', 'pytest-cov'], check=True)
    
    verbose = not args.quiet
    
    exit_code = run_tests(
        test_type=args.type,
        verbose=verbose,
        coverage=args.coverage
    )
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
    else:
        print("\n❌ Some tests failed!")
    
    return exit_code


if __name__ == '__main__':
    sys.exit(main())