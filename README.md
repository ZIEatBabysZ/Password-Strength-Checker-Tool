# 🔒 Password Strength Checker Tool

A comprehensive Python tool that analyzes password strength using advanced algorithms and provides detailed security assessments.

## ✨ Features

- **Advanced Analysis**: Built-in algorithm + zxcvbn integration
- **Multiple Interfaces**: CLI, GUI, and Web interface
- **Multi-Language Support**: English, Spanish, French
- **Security Checking**: Have I Been Pwned integration
- **Export Options**: JSON, CSV export capabilities
- **Cross-Platform**: Works on Windows, macOS, and Linux

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run interactive launcher
python run.py

# Check a password
python run.py check "MyPassword123!"

# Launch GUI
python run.py gui

# Launch web interface
python run.py web
```

## 📖 Usage

### Command Line
```bash
# Interactive analysis
python enhanced_password_checker.py -i

# Single password
python enhanced_password_checker.py -p "password"

# Batch analysis
python enhanced_password_checker.py -b passwords.txt

# Multi-language
python enhanced_password_checker.py -p "password" -l es
```

### GUI Interface
```bash
python password_checker_gui.py
```

### Web Interface
```bash
python app.py
```
Then open http://localhost:5000

## 🛡️ Security Features

- **Strength Scoring**: 0-100 point comprehensive scoring
- **Pattern Detection**: Sequential chars, dictionary words, common passwords
- **Entropy Calculation**: Mathematical randomness measurement
- **Breach Detection**: Checks against known compromised passwords
- **Attack Time Estimation**: Multiple attack scenario calculations

## 📁 Project Structure

- `enhanced_password_checker.py` - Core analysis engine
- `password_checker_gui.py` - GUI interface
- `app.py` - Web interface
- `run.py` - Cross-platform launcher
- `i18n_manager.py` - Language support
- `hibp_checker.py` - Breach checking

## 📋 Requirements

- Python 3.6+
- colorama
- zxcvbn (optional but recommended)
- requests (for HIBP checking)
- tkinter (for GUI, usually included with Python)
- flask (for web interface)

## 🔧 Installation

```bash
git clone <repository-url>
cd Password-Strength-Checker-Tool
pip install -r requirements.txt
python setup.py  # Setup and test installation
```

## 🌍 Language Support

Supported languages: English (en), Spanish (es), French (fr)

Switch language with `-l` or `--language` parameter:
```bash
python enhanced_password_checker.py -p "password" -l es
```

## 📊 Export Options

Export analysis results:
```bash
# JSON export
python enhanced_password_checker.py -p "password" --export-json results.json

# CSV export (batch mode)
python enhanced_password_checker.py -b passwords.txt --export-csv results.csv
```

## 🚨 Security Notes

- Never store passwords in plain text
- Use unique passwords for each account
- Enable 2FA where possible
- Regularly update passwords
- Use a password manager

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
