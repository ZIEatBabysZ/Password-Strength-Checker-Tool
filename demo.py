#!/usr/bin/env python3
"""
Demo script showing Password Strength Checker capabilities
"""

import subprocess
import sys
import os

def demo_password_analysis():
    """Demonstrate password analysis with various password types"""
    
    print("[*] Password Strength Checker - Live Demo")
    print("=" * 50)
    
    # Sample passwords with different strength levels
    test_passwords = [
        ("password", "Very weak - common password"),
        ("Password123", "Weak - common pattern"),
        ("MySecureP@ss!", "Medium - better but has dictionary words"),
        ("Tr0ub4dor&3", "Strong - famous xkcd reference"),
        ("correct horse battery staple", "Very Strong - passphrase"),
        ("MyComplexP@ssw0rd2024!#$", "Very Strong - complex password")
    ]
    
    print("\n[TEST] Testing various password strengths:")
    print("-" * 50)
    
    for i, (password, description) in enumerate(test_passwords, 1):
        print(f"\n[Test {i}/6] {description}")
        print(f"Password: '{password}'")
        
        try:
            # Run the enhanced password checker
            result = subprocess.run([
                sys.executable, "enhanced_password_checker.py", "-p", password
            ], capture_output=True, text=True, cwd=os.path.dirname(__file__))
            
            if result.returncode == 0:
                # Extract just the score and strength from the output
                lines = result.stdout.split('\n')
                for line in lines:
                    if "Strength Score:" in line:
                        print(f"Result: {line.strip()}")
                    elif "Strength Level:" in line and "Overall Assessment" not in line:
                        print(f"        {line.strip()}")
                        break
            else:
                print(f"Error analyzing password: {result.stderr}")
                
        except Exception as e:
            print(f"Error running analysis: {e}")
        
        if i < len(test_passwords):
            input("Press Enter to continue...")
    
    print("\n" + "=" * 50)
    print("[SUCCESS] Demo completed!")
    print("\nTry it yourself:")
    print("  python enhanced_password_checker.py -i")
    print("  python enhanced_password_checker.py -b test_passwords.txt")

if __name__ == "__main__":
    demo_password_analysis()
