#!/usr/bin/env python3
"""
Setup script for Password Strength Checker Tool
Cross-platform setup that works on Windows, macOS, and Linux
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required Python packages"""
    print("\n📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("Please try manually: pip install -r requirements.txt")
        return False
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        return False
    
    return True

def make_scripts_executable():
    """Make shell scripts executable on Unix-like systems"""
    system = platform.system().lower()
    
    if system in ['linux', 'darwin']:  # Linux or macOS
        print("\n🔧 Making scripts executable...")
        scripts = ['run.sh', 'password_checker.py', 'enhanced_password_checker.py', 'run.py']
        
        for script in scripts:
            if os.path.exists(script):
                try:
                    os.chmod(script, 0o755)
                    print(f"✓ Made {script} executable")
                except OSError as e:
                    print(f"⚠️  Could not make {script} executable: {e}")
        
        # Make sure run.sh has correct shebang
        if os.path.exists('run.sh'):
            try:
                with open('run.sh', 'r') as f:
                    content = f.read()
                if not content.startswith('#!/bin/bash'):
                    print("⚠️  run.sh may need #!/bin/bash shebang")
            except Exception:
                pass

def test_installation():
    """Test if the installation works"""
    print("\n🧪 Testing installation...")
    
    try:
        # Test basic import
        import colorama
        print("✓ colorama module available")
    except ImportError:
        print("⚠️  colorama not available - colors may not work")
    
    try:
        import zxcvbn
        print("✓ zxcvbn module available - enhanced analysis enabled")
    except ImportError:
        print("⚠️  zxcvbn not available - only basic analysis will work")
        print("   Install with: pip install zxcvbn")
    
    # Test if scripts can be imported
    try:
        sys.path.insert(0, '.')
        import password_checker
        print("✓ password_checker.py can be imported")
    except ImportError as e:
        print(f"❌ password_checker.py import failed: {e}")
    
    try:
        import enhanced_password_checker
        print("✓ enhanced_password_checker.py can be imported")
    except ImportError as e:
        print(f"❌ enhanced_password_checker.py import failed: {e}")

def show_platform_specific_instructions():
    """Show platform-specific usage instructions"""
    system = platform.system()
    
    print(f"\n🎯 Platform: {system} {platform.release()}")
    print("📋 Usage Instructions:")
    
    if system == "Windows":
        print("\n   Windows Usage:")
        print("   • Double-click run.bat for interactive menu")
        print("   • Command line: run.bat [command] [arguments]")
        print("   • PowerShell: .\\run.ps1 [command] [arguments]")
        print("   • Cross-platform: python run.py [command] [arguments]")
        print("\n   Examples:")
        print("   run.bat test")
        print("   run.bat enhanced \"MyPassword123!\"")
        print("   python run.py batch test_passwords.txt")
    
    elif system in ["Linux", "Darwin"]:  # Darwin is macOS
        os_name = "macOS" if system == "Darwin" else "Linux"
        print(f"\n   {os_name} Usage:")
        print("   • Interactive: ./run.sh")
        print("   • Command line: ./run.sh [command] [arguments]")
        print("   • Makefile: make [target]")
        print("   • Cross-platform: python3 run.py [command] [arguments]")
        print("\n   Examples:")
        print("   ./run.sh setup")
        print("   ./run.sh enhanced \"MyPassword123!\"")
        print("   make test")
        print("   make demo")
        
        if os.geteuid() == 0:  # Running as root
            print("\n   System Installation (optional):")
            print("   sudo make install")
        else:
            print("\n   For system-wide installation:")
            print("   sudo make install")
    
    print("\n   Available Commands:")
    print("   • setup    - Install dependencies")
    print("   • test     - Run functionality tests")
    print("   • demo     - Interactive demo")
    print("   • basic    - Basic password checker")
    print("   • enhanced - Enhanced password checker")
    print("   • batch    - Batch analysis from file")
    print("   • help     - Show help information")

def main():
    """Main setup function"""
    print("[*] Password Strength Checker Tool - Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Make scripts executable on Unix
    make_scripts_executable()
    
    # Test installation
    test_installation()
    
    # Show platform-specific instructions
    show_platform_specific_instructions()
    
    print("\n✅ Setup completed successfully!")
    print("You can now use the Password Strength Checker Tool.")

if __name__ == "__main__":
    main()
