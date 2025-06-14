#!/usr/bin/env python3
"""
Setup script for Password Strength Checker Tool
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 6):
        print("Error: Python 3.6 or higher is required.")
        sys.exit(1)
    print(f"✓ Python {sys.version.split()[0]} detected")

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def test_imports():
    """Test that core modules can be imported"""
    print("🔧 Testing imports...")
    
    try:
        import enhanced_password_checker
        print("✓ Core module imports successfully")
        
        import password_checker_gui
        print("✓ GUI module imports successfully")
        
        import app
        print("✓ Web module imports successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🔒 Password Strength Checker Tool - Setup")
    print("=" * 50)
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Test imports
    if not test_imports():
        print("⚠️  Some modules failed to import. Check dependencies.")
    
    print("\n✅ Setup completed successfully!")
    print("\nQuick start:")
    print("  python run.py")
    print("  python run.py gui")
    print("  python run.py check 'password'")

if __name__ == "__main__":
    main()
