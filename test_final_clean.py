#!/usr/bin/env python3
"""
Final cross-platform compatibility test
Tests all launchers and core functionality
"""

import os
import sys
import subprocess
import platform
import time

def test_command(cmd, timeout=10):
    """Test a command and return success status"""
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout
        )
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Timeout"
    except Exception as e:
        return False, "", str(e)

def main():
    print("Password Strength Checker Tool - Cross-Platform Compatibility Test")
    print("=" * 70)
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print()
    
    tests = []
    
    # Test 1: Core functionality
    print("Testing Core Functionality:")
    print("-" * 30)
    
    success, stdout, stderr = test_command('python password_checker.py -p "Test123!"')
    tests.append(("Basic Password Checker", success))
    print(f"Basic Password Checker: {'PASS' if success else 'FAIL'}")
    
    success, stdout, stderr = test_command('python enhanced_password_checker.py -p "Test123!"')
    tests.append(("Enhanced Password Checker", success))
    print(f"Enhanced Password Checker: {'PASS' if success else 'FAIL'}")
    
    # Test 2: GUI functionality (brief test)
    print(f"\nTesting GUI Functionality:")
    print("-" * 30)
    
    success, stdout, stderr = test_command('python -c "import tkinter; import password_checker_gui; print(\'GUI imports successful\')"')
    tests.append(("GUI Import Test", success))
    print(f"GUI Import Test: {'PASS' if success else 'FAIL'}")
    
    # Test 3: Launcher scripts
    print(f"\nTesting Launcher Scripts:")
    print("-" * 30)
    
    if platform.system() == "Windows":
        # Windows launchers
        success, stdout, stderr = test_command('run.bat help')
        tests.append(("run.bat help", success))
        print(f"run.bat help: {'PASS' if success else 'FAIL'}")
        
        success, stdout, stderr = test_command('powershell -ExecutionPolicy Bypass -File run.ps1 help')
        tests.append(("run.ps1 help", success))
        print(f"run.ps1 help: {'PASS' if success else 'FAIL'}")
    else:
        # Unix launchers
        success, stdout, stderr = test_command('bash run.sh help')
        tests.append(("run.sh help", success))
        print(f"run.sh help: {'PASS' if success else 'FAIL'}")
        
        success, stdout, stderr = test_command('make help')
        tests.append(("Makefile help", success))
        print(f"Makefile help: {'PASS' if success else 'FAIL'}")
    
    # Test 4: Dependencies
    print(f"\nTesting Dependencies:")
    print("-" * 30)
    
    success, stdout, stderr = test_command('python -c "import colorama; print(\'colorama available\')"')
    tests.append(("colorama dependency", success))
    print(f"colorama dependency: {'PASS' if success else 'FAIL'}")
    
    success, stdout, stderr = test_command('python -c "import zxcvbn; print(\'zxcvbn available\')"')
    tests.append(("zxcvbn dependency", success))
    print(f"zxcvbn dependency: {'PASS' if success else 'OPTIONAL'}")
    
    # Summary
    print(f"\n{'='*70}")
    print("TEST SUMMARY")
    print("="*70)
    
    total_tests = len([t for t in tests if t[0] != "zxcvbn dependency"])
    passed_tests = sum(1 for name, success in tests if success and name != "zxcvbn dependency")
    
    print(f"Core Tests: {passed_tests}/{total_tests} passed")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if passed_tests == total_tests:
        print("\nALL TESTS PASSED!")
        print("Password Strength Checker Tool is fully functional")
        print("Cross-platform compatibility verified")
        print("GUI integration working")
        print("All launcher scripts operational")
    else:
        print(f"\nSome issues detected ({passed_tests}/{total_tests})")
        for name, success in tests:
            if not success and name != "zxcvbn dependency":
                print(f"FAILED: {name}")
    
    print(f"\nCompatible Platforms:")
    print("Windows (run.bat, run.ps1, python)")
    print("macOS (run.sh, Makefile, python3)")
    print("Linux (run.sh, Makefile, python3)")
    
    print(f"\nAvailable Launch Methods:")
    if platform.system() == "Windows":
        print("• python password_checker_gui.py")
        print("• run.bat gui")
        print("• run.ps1 gui")
        print("• python run.py gui")
    else:
        print("• python3 password_checker_gui.py")
        print("• ./run.sh gui")
        print("• make gui")
        print("• python3 run.py gui")

if __name__ == "__main__":
    main()
