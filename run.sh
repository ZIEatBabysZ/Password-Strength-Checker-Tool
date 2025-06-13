#!/bin/bash

# Quick start script for Password Strength Checker Tool
# Usage: ./run.sh [command] [arguments]
# Compatible with macOS and Linux

# Set interactive mode flag
INTERACTIVE_MODE=0

# Function to show help
show_help() {
    echo
    echo "Password Strength Checker Tool - Quick Start"
    echo "================================================"
    echo
    echo "Available commands:"
    echo "  ./run.sh setup        - Install dependencies and setup tool"
    echo "  ./run.sh demo          - Run interactive demo"
    echo "  ./run.sh test          - Run basic functionality tests"
    echo "  ./run.sh basic [pass]  - Use basic password checker"
    echo "  ./run.sh enhanced [pass] - Use enhanced password checker"
    echo "  ./run.sh batch [file]  - Batch analyze passwords from file"
    echo
    echo "Examples:"
    echo "  ./run.sh setup"
    echo "  ./run.sh enhanced \"MyPassword123!\""
    echo "  ./run.sh batch test_passwords.txt"
    echo
}

# Function to show interactive menu
show_interactive_menu() {
    while true; do
        echo
        echo "Password Strength Checker Tool - Quick Start"
        echo "================================================"
        echo
        echo "Available commands:"
        echo "  1. Setup tool (install dependencies)"
        echo "  2. Run interactive password checker"
        echo "  3. Test tool functionality"
        echo "  4. Analyze a password you type"
        echo "  5. Batch analyze from file"
        echo "  6. Show command help"
        echo "  0. Exit"
        echo
        read -p "Enter your choice (0-6): " choice
        
        case $choice in
            1)
                INTERACTIVE_MODE=1
                setup_tool
                ;;
            2)
                INTERACTIVE_MODE=1
                run_interactive
                ;;
            3)
                INTERACTIVE_MODE=1
                test_tool
                ;;
            4)
                INTERACTIVE_MODE=1
                input_password
                ;;
            5)
                INTERACTIVE_MODE=1
                batch_default
                ;;
            6)
                INTERACTIVE_MODE=1
                show_help
                if [ "$INTERACTIVE_MODE" -eq 1 ]; then
                    echo "Press Enter to return to menu..."
                    read
                fi
                ;;
            0)
                echo
                echo "Done!"
                exit 0
                ;;
            *)
                echo "Invalid choice. Please try again."
                ;;
        esac
    done
}

# Function to run interactive password checker
run_interactive() {
    echo "Starting enhanced password checker in interactive mode..."
    python3 enhanced_password_checker.py -i
    if [ "$INTERACTIVE_MODE" -eq 1 ]; then
        echo
        echo "Press Enter to return to menu..."
        read
    fi
}

# Function to get user password input
input_password() {
    echo
    read -p "Enter password to analyze: " userpass
    if [ -z "$userpass" ]; then
        echo "No password entered."
        if [ "$INTERACTIVE_MODE" -eq 1 ]; then
            echo "Press Enter to return to menu..."
            read
        fi
        return
    fi
    echo "Analyzing your password..."
    python3 enhanced_password_checker.py -p "$userpass"
    if [ "$INTERACTIVE_MODE" -eq 1 ]; then
        echo
        echo "Press Enter to return to menu..."
        read
    fi
}

# Function to run batch with default file
batch_default() {
    echo "Using default test file..."
    python3 enhanced_password_checker.py -b test_passwords.txt
    if [ "$INTERACTIVE_MODE" -eq 1 ]; then
        echo
        echo "Press Enter to return to menu..."
        read
    fi
}

# Function to setup tool
setup_tool() {
    echo "Installing dependencies and setting up tool..."
    python3 setup.py
    if [ "$INTERACTIVE_MODE" -eq 1 ]; then
        echo
        echo "Press Enter to return to menu..."
        read
    fi
}

# Function to run demo
demo_tool() {
    echo "Running interactive demo..."
    python3 demo.py
    if [ "$INTERACTIVE_MODE" -eq 1 ]; then
        echo
        echo "Press Enter to return to menu..."
        read
    fi
}

# Function to test tool
test_tool() {
    echo "Running basic tests..."
    echo
    echo "Testing basic checker:"
    python3 password_checker.py -p "Test123!"
    echo
    echo "Testing enhanced checker:"
    python3 enhanced_password_checker.py -p "Test123!"
    if [ "$INTERACTIVE_MODE" -eq 1 ]; then
        echo
        echo "Press Enter to return to menu..."
        read
    fi
}

# Function to run basic password checker
basic_checker() {
    if [ -z "$2" ]; then
        echo "Starting basic password checker in interactive mode..."
        python3 password_checker.py -i
    else
        echo "Analyzing password with basic checker..."
        python3 password_checker.py -p "$2"
    fi
}

# Function to run enhanced password checker
enhanced_checker() {
    if [ -z "$2" ]; then
        echo "Starting enhanced password checker in interactive mode..."
        python3 enhanced_password_checker.py -i
    else
        echo "Analyzing password with enhanced checker..."
        python3 enhanced_password_checker.py -p "$2"
    fi
}

# Function to run batch mode
batch_mode() {
    if [ -z "$2" ]; then
        echo "Using default test file..."
        python3 enhanced_password_checker.py -b test_passwords.txt
    else
        echo "Analyzing passwords from file: $2"
        python3 enhanced_password_checker.py -b "$2"
    fi
}

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Main script logic
if [ $# -eq 0 ]; then
    INTERACTIVE_MODE=1
    show_interactive_menu
fi

case "$1" in
    "help")
        show_help
        ;;
    "setup")
        setup_tool
        ;;
    "demo")
        demo_tool
        ;;
    "test")
        test_tool
        ;;
    "basic")
        basic_checker "$@"
        ;;
    "enhanced")
        enhanced_checker "$@"
        ;;
    "batch")
        batch_mode "$@"
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        exit 1
        ;;
esac

echo
echo "Done!"
