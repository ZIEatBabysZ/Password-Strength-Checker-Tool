#!/usr/bin/env python3
"""
Cross-platform launcher for Password Strength Checker Tool
Works on Windows, macOS, and Linux
Usage: python run.py [command] [arguments]
"""

import os
import sys
import platform
import subprocess
import argparse

class PasswordToolLauncher:
    def __init__(self):
        self.interactive_mode = False
        self.system = platform.system().lower()
        self.python_cmd = self.get_python_command()
    
    def get_python_command(self):
        """Get the appropriate Python command for the current system"""
        if self.system == "windows":
            # Try python first, then python3
            for cmd in ["python", "python3"]:
                try:
                    result = subprocess.run([cmd, "--version"], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        return cmd
                except FileNotFoundError:
                    continue
        else:
            # Unix-like systems (macOS, Linux)
            for cmd in ["python3", "python"]:
                try:
                    result = subprocess.run([cmd, "--version"], 
                                          capture_output=True, text=True)
                    if result.returncode == 0 and "Python 3" in result.stdout:
                        return cmd
                except FileNotFoundError:
                    continue
        
        print("Error: Python 3 is not installed or not in PATH.")
        print("Please install Python 3 and try again.")
        sys.exit(1)
    
    def run_command(self, script, args=None):
        """Run a Python script with optional arguments"""
        cmd = [self.python_cmd, script]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(cmd)
            return result.returncode
        except FileNotFoundError:
            print(f"Error: {script} not found.")
            return 1
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
    
    def show_help(self):
        """Show help information"""
        print()
        print("Password Strength Checker Tool - Cross-Platform Launcher")
        print("=" * 60)
        print()
        print("Available commands:")
        print("  python run.py setup        - Install dependencies and setup tool")
        print("  python run.py gui          - Launch GUI interface")
        print("  python run.py demo         - Run interactive demo")
        print("  python run.py test         - Run basic functionality tests")
        print("  python run.py basic [pass] - Use basic password checker")
        print("  python run.py enhanced [pass] - Use enhanced password checker")
        print("  python run.py batch [file] - Batch analyze passwords from file")
        print()
        print("Examples:")
        print("  python run.py setup")
        print("  python run.py gui")
        print('  python run.py enhanced "MyPassword123!"')
        print("  python run.py batch test_passwords.txt")
        print()
        print(f"System detected: {platform.system()} {platform.release()}")
        print(f"Python command: {self.python_cmd}")
        print()
    
    def show_interactive_menu(self):
        """Show interactive menu for GUI-like usage"""
        while True:
            print()
            print("Password Strength Checker Tool - Cross-Platform")
            print("=" * 50)
            print()
            print("Available commands:")
            print("  1. Setup tool (install dependencies)")
            print("  2. Launch GUI interface")
            print("  3. Run interactive password checker")
            print("  4. Test tool functionality")
            print("  5. Analyze a password you type")
            print("  6. Batch analyze from file")
            print("  7. Show command help")
            print("  0. Exit")
            print()
            
            try:
                choice = input("Enter your choice (0-7): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nExiting...")
                break
            
            if choice == "1":
                self.interactive_mode = True
                self.setup_tool()
            elif choice == "2":
                self.interactive_mode = True
                self.launch_gui()
            elif choice == "3":
                self.interactive_mode = True
                self.run_interactive()
            elif choice == "4":
                self.interactive_mode = True
                self.test_tool()
            elif choice == "5":
                self.interactive_mode = True
                self.input_password()
            elif choice == "6":
                self.interactive_mode = True
                self.batch_default()
            elif choice == "7":
                self.interactive_mode = True
                self.show_help()
                if self.interactive_mode:
                    try:
                        input("Press Enter to return to menu...")
                    except (EOFError, KeyboardInterrupt):
                        break
            elif choice == "0":
                print("\nDone!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def run_interactive(self):
        """Run enhanced password checker in interactive mode"""
        print("Starting enhanced password checker in interactive mode...")
        self.run_command("enhanced_password_checker.py", ["-i"])
        if self.interactive_mode:
            try:
                input("\nPress Enter to return to menu...")
            except (EOFError, KeyboardInterrupt):
                pass
    
    def test_tool(self):
        """Run basic functionality tests"""
        print("Running basic functionality tests...")
        self.run_command("password_checker.py", ["-p", "test123"])
        if self.interactive_mode:
            try:
                input("\nPress Enter to return to menu...")
            except (EOFError, KeyboardInterrupt):
                pass
    
    def input_password(self):
        """Get password input from user and analyze"""
        try:
            password = input("Enter password to analyze: ").strip()
            if not password:
                print("No password entered.")
                return
            print("Analyzing your password...")
            self.run_command("enhanced_password_checker.py", ["-p", password])
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
        if self.interactive_mode:
            try:
                input("\nPress Enter to return to menu...")
            except (EOFError, KeyboardInterrupt):
                pass
    
    def batch_default(self):
        """Run batch mode with default file"""
        print("Using default test file...")
        self.run_command("enhanced_password_checker.py", ["-b", "test_passwords.txt"])
        if self.interactive_mode:
            try:
                input("\nPress Enter to return to menu...")
            except (EOFError, KeyboardInterrupt):
                pass
    
    def setup_tool(self):
        """Setup the tool and install dependencies"""
        print("Installing dependencies and setting up tool...")
        self.run_command("setup.py")
        if self.interactive_mode:
            try:
                input("\nPress Enter to return to menu...")
            except (EOFError, KeyboardInterrupt):
                pass
    
    def demo_tool(self):
        """Run the demo"""
        print("Running interactive demo...")
        self.run_command("demo.py")
        if self.interactive_mode:
            try:
                input("\nPress Enter to return to menu...")
            except (EOFError, KeyboardInterrupt):
                pass
    
    def launch_gui(self):
        """Launch the GUI interface"""
        print("Launching GUI interface...")
        try:
            self.run_command("password_checker_gui.py")
        except Exception as e:
            print(f"Error launching GUI: {e}")
            print("Make sure tkinter is installed (usually comes with Python)")
        if self.interactive_mode:
            try:
                input("\nPress Enter to return to menu...")
            except (EOFError, KeyboardInterrupt):
                pass
    
    def basic_checker(self, password=None):
        """Run basic password checker"""
        if password is None:
            print("Starting basic password checker in interactive mode...")
            self.run_command("password_checker.py", ["-i"])
        else:
            print("Analyzing password with basic checker...")
            self.run_command("password_checker.py", ["-p", password])
    
    def enhanced_checker(self, password=None):
        """Run enhanced password checker"""
        if password is None:
            print("Starting enhanced password checker in interactive mode...")
            self.run_command("enhanced_password_checker.py", ["-i"])
        else:
            print("Analyzing password with enhanced checker...")
            self.run_command("enhanced_password_checker.py", ["-p", password])
    
    def batch_mode(self, filename=None):
        """Run batch mode analysis"""
        if filename is None:
            print("Using default test file...")
            self.run_command("enhanced_password_checker.py", ["-b", "test_passwords.txt"])
        else:
            print(f"Analyzing passwords from file: {filename}")
            self.run_command("enhanced_password_checker.py", ["-b", filename])

def main():
    launcher = PasswordToolLauncher()
    
    # Parse command line arguments
    if len(sys.argv) == 1:
        # No arguments - show interactive menu
        launcher.interactive_mode = True
        launcher.show_interactive_menu()
        return
    
    command = sys.argv[1].lower()
    
    if command == "help":
        launcher.show_help()
    elif command == "setup":
        launcher.setup_tool()
    elif command == "gui":
        launcher.launch_gui()
    elif command == "demo":
        launcher.demo_tool()
    elif command == "test":
        launcher.test_tool()
    elif command == "basic":
        password = sys.argv[2] if len(sys.argv) > 2 else None
        launcher.basic_checker(password)
    elif command == "enhanced":
        password = sys.argv[2] if len(sys.argv) > 2 else None
        launcher.enhanced_checker(password)
    elif command == "batch":
        filename = sys.argv[2] if len(sys.argv) > 2 else None
        launcher.batch_mode(filename)
    else:
        print(f"Unknown command: {command}")
        launcher.show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()