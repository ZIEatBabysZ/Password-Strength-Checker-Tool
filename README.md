# 🔒 Password Strength Checker Tool

A comprehensive Python command-line tool that analyzes password strength using multiple sophisticated algorithms and provides detailed security assessments.

## ✨ Features

### Core Functionality
- **Multiple Analysis Methods**: Built-in algorithm + optional zxcvbn integration
- **Comprehensive Scoring**: 0-100 point scale with detailed breakdowns
- **Color-Coded Output**: Visual strength indicators (Red=Weak, Green=Strong)
- **Multiple Input Methods**: Command-line arguments, interactive mode, batch processing
- **Cross-Platform**: Works on Windows, macOS, and Linux

### Security Analysis
- **Length Assessment**: Optimal length recommendations
- **Character Type Detection**: Uppercase, lowercase, numbers, symbols
- **Pattern Recognition**: Sequential characters, keyboard patterns, repetition
- **Dictionary Word Detection**: Common words and variations
- **Common Password Checking**: Database of 500+ most common passwords
- **Entropy Calculation**: Mathematical randomness measurement
- **Attack Time Estimation**: Multiple attack scenario timeframes

### Advanced Features (with zxcvbn)
- **Machine Learning Analysis**: Advanced pattern recognition
- **Multiple Attack Scenarios**: Online throttled/unthrottled, offline slow/fast
- **Contextual Feedback**: Specific improvement suggestions
- **Sequence Detection**: Advanced pattern matching

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Step 1: Clone or Download
```bash
git clone <repository-url>
cd PasswordSCT
```

### Step 2: Quick Setup (All Platforms)

#### Windows
```cmd
# Option 1: Use the Windows batch file
run.bat setup

# Option 2: Use the cross-platform Python launcher
python run.py setup

# Option 3: Manual setup
pip install -r requirements.txt
```

#### macOS/Linux
```bash
# Option 1: Use the Unix shell script
chmod +x run.sh
./run.sh setup

# Option 2: Use the Makefile (recommended)
make setup

# Option 3: Use the cross-platform Python launcher
python3 run.py setup

# Option 4: Manual setup
pip3 install -r requirements.txt
```

**Required packages:**
- `colorama>=0.4.4` - Cross-platform color output
- `zxcvbn>=4.4.28` - Advanced password analysis (optional but recommended)

## 📖 Usage

### Cross-Platform Quick Start

#### Windows
```cmd
# Interactive menu (double-click run.bat or use command line)
run.bat

# Specific commands
run.bat test
run.bat enhanced "MyPassword123!"
run.bat batch test_passwords.txt
```

#### macOS/Linux
```bash
# Interactive menu
./run.sh

# Using Makefile
make test
make demo

# Specific commands
./run.sh test
./run.sh enhanced "MyPassword123!"
./run.sh batch test_passwords.txt
```

#### All Platforms (Python launcher)
```bash
# Interactive GUI-like menu
python run.py

# Specific commands
python run.py test
python run.py enhanced "MyPassword123!"
python run.py batch test_passwords.txt
```

### Platform-Specific Features

#### Windows Features
- **Double-click support**: Just double-click `run.bat` for interactive menu
- **PowerShell integration**: Use `run.ps1` for PowerShell users
- **Command Prompt support**: Full compatibility with cmd.exe

#### macOS/Linux Features
- **Makefile support**: Use `make` commands for easy operation
- **Shell script**: Native bash script for Unix environments
- **System installation**: `sudo make install` for system-wide access

### System-Wide Installation (Optional)

#### macOS/Linux
```bash
# Install system-wide (requires sudo)
sudo make install

# Now you can use from anywhere:
passwordsct enhanced "MyPassword123!"
passwordsct-gui  # GUI-like interface

# Uninstall if needed
sudo make uninstall
```

#### Windows
```cmd
# Add to PATH manually or use portable mode
# Copy the entire folder to a permanent location
# Add the folder to your PATH environment variable
```

### Direct Python Usage (All Platforms)

#### Basic Version (`password_checker.py`)
```bash
# Windows
python password_checker.py -p "MyPassword123!"

# macOS/Linux
python3 password_checker.py -p "MyPassword123!"
```

#### Enhanced Version (`enhanced_password_checker.py`)
```bash
# Single password analysis
python enhanced_password_checker.py -p "MyPassword123!"

# Interactive mode
python enhanced_password_checker.py -i

# Batch analysis from file
python enhanced_password_checker.py -b passwords.txt

# Force built-in algorithm (skip zxcvbn)
python enhanced_password_checker.py -p "password" --no-zxcvbn

# Help
python enhanced_password_checker.py --help
```

#### Batch Processing
Create a text file with passwords (one per line):
```
passwords.txt:
password123
MySecretPassword!
qwerty123
StrongP@ssw0rd2023!
```

Then run:
```bash
# Windows
run.bat batch passwords.txt

# macOS/Linux
./run.sh batch passwords.txt

# All platforms
python run.py batch passwords.txt
```

## 📊 Sample Output

### Strong Password Example
```
======================================================================
🔒 PASSWORD STRENGTH ANALYSIS 🔒
======================================================================

Analysis Method: zxcvbn + Enhanced Analysis
Password Length: 16 characters

Character Composition:
  • Lowercase letters: ✓
  • Uppercase letters: ✓
  • Numbers: ✓
  • Special characters: ✓

Technical Metrics:
  • Entropy: 95.2 bits
  • Unique characters: 15/16
  • zxcvbn Score: 4/4
  • Guesses needed: 1,234,567,890,123

Overall Assessment:
  • Strength Score: 92/100
  • Strength Level: Very Strong

[██████████████████████████████████████████████████] 92%

🕐 Estimated Crack Time:
  • Online attack (throttled): centuries
  • Online attack (unthrottled): 4 years
  • Offline attack (slow): 4 hours
  • Offline attack (fast): less than a second

🛡️  Security Recommendations:
  • Excellent: This is a very strong password
  • Never reuse passwords across multiple accounts
  • Update passwords regularly, especially for sensitive accounts
  • Store passwords securely using a password manager
```

### Weak Password Example
```
======================================================================
🔒 PASSWORD STRENGTH ANALYSIS 🔒
======================================================================

Analysis Method: zxcvbn + Enhanced Analysis
Password Length: 8 characters

Character Composition:
  • Lowercase letters: ✓
  • Uppercase letters: ✗
  • Numbers: ✓
  • Special characters: ✗

⚠️  Security Issues Detected:
  1. Password is in common passwords list
  2. Contains dictionary word: 'password'

🕐 Estimated Crack Time:
  • Online attack (throttled): 2 minutes
  • Online attack (unthrottled): less than a second
  • Offline attack (slow): less than a second
  • Offline attack (fast): less than a second

Overall Assessment:
  • Strength Score: 15/100
  • Strength Level: Very Weak

[███████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 15%

💡 Improvement Suggestions:
  1. This password is too common - choose a unique one
  2. Add uppercase letters
  3. Add special characters (!@#$%^&*)
  4. Avoid using dictionary words
  5. Use at least 12+ characters for better security

🛡️  Security Recommendations:
  • Critical: This password is easily crackable
  • Use a password manager to generate strong passwords
  • Enable two-factor authentication (2FA) wherever possible
```

## 🔧 Algorithm Details

### Built-in Scoring Algorithm

The tool uses a comprehensive 100-point scoring system:

1. **Length Analysis (0-30 points)**
   - 16+ characters: 30 points
   - 12-15 characters: 25 points
   - 8-11 characters: 20 points
   - 6-7 characters: 15 points
   - 4-5 characters: 10 points
   - <4 characters: 5 points

2. **Character Diversity (0-25 points)**
   - 4 types (upper, lower, numbers, symbols): 25 points
   - 3 types: 20 points
   - 2 types: 15 points
   - 1 type: 10 points

3. **Entropy Assessment (0-25 points)**
   - Based on mathematical entropy calculation
   - Considers character set size and password length

4. **Pattern Penalties (0-25 point deduction)**
   - Common passwords: -7 points each
   - Dictionary words: -7 points each
   - Keyboard patterns: -7 points each
   - Sequential characters: -7 points each
   - Repeated characters: -7 points each

5. **Uniqueness Bonus (0-20 points)**
   - Based on ratio of unique characters to total length

### zxcvbn Integration

When available, the tool also uses the zxcvbn library, which provides:
- Machine learning-based pattern recognition
- Contextual password analysis
- Advanced time-to-crack estimations
- Specific feedback for common weaknesses

## 📁 File Structure

```
PasswordSCT/
├── password_checker.py          # Basic version with built-in algorithm
├── enhanced_password_checker.py # Enhanced version with zxcvbn integration
├── run.py                      # Cross-platform Python launcher (all platforms)
├── run.bat                     # Windows batch file launcher
├── run.ps1                     # Windows PowerShell script
├── run.sh                      # Unix shell script (macOS/Linux)
├── Makefile                    # Build system for macOS/Linux
├── setup.py                    # Setup and dependency installer
├── demo.py                     # Interactive demo
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── LICENSE                     # License file
├── test_passwords.txt          # Sample passwords for testing
├── common_passwords.txt        # Database of common passwords
└── dictionary_words.txt        # Database of dictionary words
```

### Platform-Specific Launchers

#### Windows
- **`run.bat`** - Main Windows launcher (double-click friendly)
- **`run.ps1`** - PowerShell version for advanced users

#### macOS/Linux
- **`run.sh`** - Native bash shell script
- **`Makefile`** - Build system with common targets

#### Cross-Platform
- **`run.py`** - Python-based launcher that works on all platforms

## 🎯 Use Cases

### Personal Security
- Check your existing passwords
- Evaluate potential new passwords
- Learn about password security best practices

### Security Auditing
- Batch analyze organizational passwords
- Identify weak passwords in systems
- Generate security reports

### Educational
- Learn about password entropy and security
- Understand different attack methods
- Explore cryptographic concepts

## 🔒 Security Considerations

### Data Privacy
- **Passwords are NOT stored or transmitted**
- Analysis is performed locally on your machine
- No network connections are made during analysis

### Best Practices
1. **Use unique passwords** for each account
2. **Enable 2FA** wherever possible
3. **Use a password manager** to generate and store strong passwords
4. **Regularly update passwords** for sensitive accounts
5. **Avoid personal information** in passwords

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

### Ideas for Enhancement
- Additional pattern detection algorithms
- Integration with more password analysis libraries
- GUI version of the tool
- Password generation features
- Integration with popular password managers

### Code Contributions
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- **zxcvbn library** by Dropbox for advanced password analysis
- **colorama library** for cross-platform color support
- Security research community for password analysis insights

## 📞 Support

If you encounter any issues or have questions:
1. Check the troubleshooting section below
2. Review the examples in this README
3. Open an issue in the repository

## 🔧 Troubleshooting

### Common Issues

#### "zxcvbn module not found"
```bash
pip install zxcvbn
```

#### "colorama module not found"
```bash
pip install colorama
```

#### Colors not displaying properly on Windows
- Ensure you're using a modern terminal (Windows Terminal, PowerShell, or Command Prompt)
- The tool automatically handles color compatibility

#### Permission denied on Unix systems
```bash
chmod +x password_checker.py
```

### Performance Notes
- Analysis is typically instant for single passwords
- Batch processing depends on file size
- zxcvbn may add slight overhead but provides better analysis

## 🚀 Future Enhancements

- [ ] GUI interface using tkinter or PyQt
- [ ] Password generation with customizable criteria
- [ ] Integration with Have I Been Pwned API
- [ ] Export results to JSON/CSV format
- [ ] Docker containerization
- [ ] Web interface version
- [ ] Multi-language support

---

**Made with ❤️ for better password security**
