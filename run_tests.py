#!/usr/bin/env python3
"""
Test runner script for ServiceNow Document Template Generator
"""
import sys
import subprocess
from pathlib import Path


def run_tests(test_type="all"):
    """Run tests with specified configuration"""
    
    print(f"🧪 Running {test_type} tests for ServiceNow Document Generator")
    print("=" * 60)
    
    # Add src to Python path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    # Base pytest command
    cmd = ["python", "-m", "pytest"]
    
    if test_type == "unit":
        cmd.extend(["-m", "unit", "-v"])
        print("📋 Running unit tests only")
    elif test_type == "integration":
        cmd.extend(["-m", "integration", "-v"])
        print("🔗 Running integration tests only")
    elif test_type == "web":
        cmd.extend(["-m", "web", "-v"])
        print("🌐 Running web interface tests only")
    elif test_type == "config":
        cmd.extend(["-m", "config", "-v"])
        print("⚙️ Running configuration tests only")
    elif test_type == "coverage":
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term"])
        print("📊 Running tests with coverage report")
    elif test_type == "fast":
        cmd.extend(["-x", "--tb=short"])
        print("⚡ Running fast tests (stop on first failure)")
    elif test_type == "all":
        cmd.extend(["-v", "--tb=short"])
        print("🎯 Running all tests")
    else:
        print(f"❌ Unknown test type: {test_type}")
        print("Available types: unit, integration, web, config, coverage, fast, all")
        return 1
    
    # Run tests
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print(f"\n❌ Tests failed with return code {result.returncode}")
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 130
    except Exception as e:
        print(f"\n💥 Error running tests: {e}")
        return 1


def show_coverage_report():
    """Show coverage report"""
    coverage_file = Path("htmlcov/index.html")
    if coverage_file.exists():
        print(f"\n📊 Coverage report available at: {coverage_file.absolute()}")
        
        # Try to open in browser (optional)
        try:
            import webbrowser
            webbrowser.open(f"file://{coverage_file.absolute()}")
            print("🌐 Opened coverage report in browser")
        except Exception:
            print("💡 Open the file manually in your browser to view the report")
    else:
        print("\n📊 No coverage report found. Run with --coverage to generate one.")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        test_type = sys.argv[1]
    else:
        test_type = "all"
    
    print("🚀 ServiceNow Document Template Generator - Test Suite")
    print("=" * 60)
    
    # Run tests
    exit_code = run_tests(test_type)
    
    # Show coverage report if generated
    if test_type == "coverage":
        show_coverage_report()
    
    # Summary
    if exit_code == 0:
        print("\n🎉 Test suite completed successfully!")
    else:
        print(f"\n💔 Test suite failed (exit code: {exit_code})")
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())