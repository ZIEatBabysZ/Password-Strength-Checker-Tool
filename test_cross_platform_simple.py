#!/usr/bin/env python3
"""
Cross-platform test script for Password Strength Checker Tool
Tests all launchers and ensures compatibility across Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform

class CrossPlatformTester:
    def __init__(self):
        self.system = platform.system().lower()
        self.test_results = []
        self.test_password = "TestPassword123!"
        
    def log_test(self, test_name, success, details=""):
        """Log test results"""
        status = "[PASS]" if success else "[FAIL]"
        self.test_results.append((test_name, success, details))
        print(f"{status}: {test_name}")
        if details and not success:
            print(f"   Details: {details}")
    
    def run_command(self, command, shell=False, timeout=30):
        """Run a command and return success status and output"""
        try:
            if isinstance(command, str):
                command = command.split() if not shell else command
            
            result = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                timeout=timeout,
                shell=shell
            )
            
            return result.returncode == 0, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return False, "", "Command timed out"
        except FileNotFoundError:
            return False, "", "Command not found"
        except Exception as e:
            return False, "", str(e)
    
    def test_python_scripts(self):
        """Test direct Python script execution"""
        print("\n[PYTHON] Testing Direct Python Script Execution...")
        
        # Test basic password checker
        python_cmd = "python" if self.system == "windows" else "python3"
        success, stdout, stderr = self.run_command([
            python_cmd, "password_checker.py", "-p", self.test_password
        ])
        self.log_test("Basic password checker direct execution", success, stderr)
        
        # Test enhanced password checker
        success, stdout, stderr = self.run_command([
            python_cmd, "enhanced_password_checker.py", "-p", self.test_password
        ])
        self.log_test("Enhanced password checker direct execution", success, stderr)
    
    def test_cross_platform_launcher(self):
        """Test the cross-platform Python launcher"""
        print("\n[LAUNCHER] Testing Cross-Platform Python Launcher...")
        
        python_cmd = "python" if self.system == "windows" else "python3"
        
        # Test help command
        success, stdout, stderr = self.run_command([python_cmd, "run.py", "help"])
        self.log_test("Python launcher help command", success, stderr)
        
        # Test enhanced password analysis
        success, stdout, stderr = self.run_command([
            python_cmd, "run.py", "enhanced", self.test_password
        ])
        self.log_test("Python launcher enhanced analysis", success, stderr)
    
    def test_windows_specific(self):
        """Test Windows-specific launchers"""
        if self.system != "windows":
            return
            
        print("\n[WINDOWS] Testing Windows-Specific Launchers...")
        
        # Test batch file
        success, stdout, stderr = self.run_command([
            "run.bat", "enhanced", self.test_password
        ], shell=True)
        self.log_test("Windows batch file launcher", success, stderr)
    
    def test_dependencies(self):
        """Test that all dependencies are available"""
        print("\n[DEPS] Testing Dependencies...")
        
        python_cmd = "python" if self.system == "windows" else "python3"
        
        # Test colorama
        success, stdout, stderr = self.run_command([
            python_cmd, "-c", "import colorama; print('colorama OK')"
        ])
        self.log_test("colorama module", success, stderr)
        
        # Test zxcvbn
        success, stdout, stderr = self.run_command([
            python_cmd, "-c", "import zxcvbn; print('zxcvbn OK')"
        ])
        self.log_test("zxcvbn module", success, stderr)
    
    def generate_report(self):
        """Generate test report"""
        print("\n" + "="*60)
        print("[*] CROSS-PLATFORM TEST REPORT")
        print("="*60)
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Architecture: {platform.machine()}")
        print()
        
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total} ({passed/total*100:.1f}%)")
        print()
        
        if passed < total:
            print("[FAIL] FAILED TESTS:")
            for test_name, success, details in self.test_results:
                if not success:
                    print(f"   - {test_name}: {details}")
            print()
        
        if passed == total:
            print("[SUCCESS] ALL TESTS PASSED! The Password Strength Checker Tool is working correctly on your platform.")
        else:
            print("[WARNING] Some tests failed. Please check the errors above.")
        
        print("\n[USAGE] Platform-Specific Usage:")
        if self.system == "windows":
            print("   - run.bat [command] [args]")
            print("   - python run.py [command] [args]")
            print("   - powershell -File run.ps1 [command] [args]")
        else:
            print("   - ./run.sh [command] [args]")
            print("   - python3 run.py [command] [args]")
            print("   - make [target]")
        
        return passed == total

def main():
    """Main test function"""
    print("[*] Password Strength Checker Tool - Cross-Platform Test Suite")
    print("="*70)
    
    tester = CrossPlatformTester()
    
    # Run all tests
    tester.test_dependencies()
    tester.test_python_scripts()
    tester.test_cross_platform_launcher()
    tester.test_windows_specific()
    
    # Generate report
    success = tester.generate_report()
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
