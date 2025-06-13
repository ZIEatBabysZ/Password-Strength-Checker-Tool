# Makefile for Password Strength Checker Tool
# Compatible with macOS and Linux

.PHONY: help setup test clean install uninstall demo basic enhanced batch

# Default Python command
PYTHON := python3

# Check if Python 3 is available
PYTHON_VERSION := $(shell $(PYTHON) --version 2>/dev/null | grep "Python 3")
ifeq ($(PYTHON_VERSION),)
    PYTHON := python
    PYTHON_VERSION := $(shell $(PYTHON) --version 2>/dev/null | grep "Python 3")
    ifeq ($(PYTHON_VERSION),)
        $(error Python 3 is required but not found. Please install Python 3.)
    endif
endif

# Default target
help:
	@echo "Password Strength Checker Tool - Build System"
	@echo "=============================================="
	@echo ""
	@echo "Available targets:"
	@echo "  help      - Show this help message"
	@echo "  setup     - Install dependencies and setup tool"
	@echo "  test      - Run basic functionality tests"
	@echo "  demo      - Run interactive demo"
	@echo "  clean     - Clean up generated files"
	@echo "  install   - Install tool system-wide (requires sudo)"
	@echo "  uninstall - Remove system-wide installation (requires sudo)"
	@echo ""
	@echo "Usage examples:"
	@echo "  make setup"
	@echo "  make test"
	@echo "  make demo"
	@echo "  ./run.sh enhanced \"MyPassword123!\""
	@echo "  python3 run.py batch test_passwords.txt"
	@echo ""
	@echo "System Information:"
	@echo "  OS: $(shell uname -s) $(shell uname -r)"
	@echo "  Python: $(PYTHON_VERSION)"
	@echo "  Architecture: $(shell uname -m)"

# Setup dependencies and tool
setup:
	@echo "Setting up Password Strength Checker Tool..."
	@echo "Making run.sh executable..."
	@chmod +x run.sh
	@echo "Installing Python dependencies..."
	@$(PYTHON) setup.py
	@echo "Setup complete!"

# Run tests
test:
	@echo "Running functionality tests..."
	@$(PYTHON) password_checker.py -p "Test123!"
	@echo ""
	@$(PYTHON) enhanced_password_checker.py -p "Test123!"

# Run demo
demo:
	@$(PYTHON) demo.py

# Run basic password checker
basic:
	@$(PYTHON) password_checker.py -i

# Run enhanced password checker
enhanced:
	@$(PYTHON) enhanced_password_checker.py -i

# Run batch analysis
batch:
	@$(PYTHON) enhanced_password_checker.py -b test_passwords.txt

# Clean up generated files
clean:
	@echo "Cleaning up..."
	@rm -rf __pycache__/
	@rm -rf *.pyc
	@rm -rf .pytest_cache/
	@rm -rf build/
	@rm -rf dist/
	@rm -rf *.egg-info/
	@echo "Clean complete!"

# Install system-wide (requires sudo)
install:
	@echo "Installing Password Strength Checker Tool system-wide..."
	@if [ "$(shell id -u)" != "0" ]; then \
		echo "Error: Installation requires sudo privileges."; \
		echo "Please run: sudo make install"; \
		exit 1; \
	fi
	@mkdir -p /usr/local/bin/passwordsct
	@cp -r . /usr/local/bin/passwordsct/
	@chmod +x /usr/local/bin/passwordsct/run.sh
	@ln -sf /usr/local/bin/passwordsct/run.sh /usr/local/bin/passwordsct
	@ln -sf /usr/local/bin/passwordsct/run.py /usr/local/bin/passwordsct-gui
	@echo "Installation complete!"
	@echo "You can now use:"
	@echo "  passwordsct [command] [args]  - Command line interface"
	@echo "  passwordsct-gui               - GUI-like interface"

# Uninstall system-wide (requires sudo)
uninstall:
	@echo "Removing Password Strength Checker Tool..."
	@if [ "$(shell id -u)" != "0" ]; then \
		echo "Error: Uninstallation requires sudo privileges."; \
		echo "Please run: sudo make uninstall"; \
		exit 1; \
	fi
	@rm -rf /usr/local/bin/passwordsct
	@rm -f /usr/local/bin/passwordsct
	@rm -f /usr/local/bin/passwordsct-gui
	@echo "Uninstallation complete!"

# Show system information
info:
	@echo "System Information:"
	@echo "==================="
	@echo "OS: $(shell uname -s) $(shell uname -r)"
	@echo "Architecture: $(shell uname -m)"
	@echo "Python: $(PYTHON_VERSION)"
	@echo "Shell: $$SHELL"
	@echo "User: $$USER"
	@echo "Working Directory: $(shell pwd)"
