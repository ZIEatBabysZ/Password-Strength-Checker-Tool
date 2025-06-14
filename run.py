#!/usr/bin/env python3
"""
Cross-platform launcher for Password Strength Checker Tool
Usage: python run.py [command] [arguments]
"""

import sys
import platform
import subprocess
import argparse

class PasswordToolLauncher:
    def __init__(self):
        self.python_cmd = self.get_python_command()
    
    def get_python_command(self):
        """Get the appropriate Python command for the current system"""
        for cmd in (["python", "python3"] if platform.system() == "Windows" else ["python3", "python"]):
            try:
                result = subprocess.run([cmd, "--version"], capture_output=True, text=True)
                if result.returncode == 0 and ("Python 3" in result.stdout or platform.system() == "Windows"):
                    return cmd
            except FileNotFoundError:
                continue
        
        print("Error: Python 3 is not installed or not in PATH.")
        sys.exit(1)
    
    def run_command(self, script, args=None):
        """Run a Python script with optional arguments"""
        cmd = [self.python_cmd, script]
        if args:
            cmd.extend(args)
        
        try:
            return subprocess.run(cmd).returncode
        except FileNotFoundError:
            print(f"Error: {script} not found.")
            return 1
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            return 1
    
    def show_help(self):
        """Show help information"""
        print("\nPassword Strength Checker Tool")
        print("Commands:")
        print("  setup      - Install dependencies")
        print("  gui        - Launch GUI interface")
        print("  web        - Launch web interface")
        print("  test       - Run functionality tests")
        print("  check [pw] - Check password strength")
        print("  batch [f]  - Batch analyze from file")
        print("  help       - Show this help")
        print("\nExamples:")
        print("  python run.py gui")
        print('  python run.py check "MyPassword123!"')
        print("  python run.py batch test_passwords.txt")

    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\nPassword Strength Checker Tool")
            print("1. Install dependencies")
            print("2. Launch GUI")
            print("3. Launch web interface")
            print("4. Check password")
            print("5. Test functionality")
            print("6. Batch analyze")
            print("0. Exit")
            
            try:
                choice = input("\nChoice (0-6): ").strip()
            except (EOFError, KeyboardInterrupt):
                break
            
            if choice == "1":
                self.setup()
            elif choice == "2":
                self.gui()
            elif choice == "3":
                self.web()
            elif choice == "4":
                self.interactive_check()
            elif choice == "5":
                self.test()
            elif choice == "6":
                self.batch("test_passwords.txt")
            elif choice == "0":
                break
            else:
                print("Invalid choice.")

    def setup(self):
        """Install dependencies"""
        print("Installing dependencies...")
        subprocess.run([self.python_cmd, "setup.py"])

    def gui(self):
        """Launch GUI interface"""
        print("Launching GUI...")
        self.run_command("password_checker_gui.py")

    def web(self):
        """Launch web interface"""
        print("Launching web interface...")
        self.run_command("app.py")

    def test(self):
        """Run functionality tests"""
        print("Running tests...")
        self.run_command("enhanced_password_checker.py", ["-p", "test123"])

    def check(self, password):
        """Check password strength"""
        if password:
            self.run_command("enhanced_password_checker.py", ["-p", password])
        else:
            self.run_command("enhanced_password_checker.py", ["-i"])

    def batch(self, filename=None):
        """Batch analyze passwords"""
        file = filename or "test_passwords.txt"
        print(f"Analyzing passwords from {file}...")
        self.run_command("enhanced_password_checker.py", ["-b", file])

    def interactive_check(self):
        """Get password input and analyze"""
        try:
            password = input("Enter password to analyze: ").strip()
            if password:
                self.check(password)
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")

def main():
    launcher = PasswordToolLauncher()
    
    if len(sys.argv) == 1:
        launcher.show_menu()
        return
    
    parser = argparse.ArgumentParser(description="Password Strength Checker Tool")
    parser.add_argument("command", nargs="?", help="Command to run")
    parser.add_argument("argument", nargs="?", help="Additional argument")
    
    args = parser.parse_args()
    command = args.command.lower() if args.command else None
    
    if command == "setup":
        launcher.setup()
    elif command == "gui":
        launcher.gui()
    elif command == "web":
        launcher.web()
    elif command == "test":
        launcher.test()
    elif command in ["check", "enhanced", "basic"]:
        launcher.check(args.argument)
    elif command == "batch":
        launcher.batch(args.argument)
    elif command == "help":
        launcher.show_help()
    elif command == "menu":
        launcher.show_menu()
    else:
        print(f"Unknown command: {command}")
        launcher.show_help()

if __name__ == "__main__":
    main()
