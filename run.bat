@echo off
REM Quick start script for Password Strength Checker Tool
REM Usage: run.bat [command] [arguments]

set INTERACTIVE_MODE=0
if "%1"=="" (
    set INTERACTIVE_MODE=1
    goto help_interactive
)
if "%1"=="help" goto help
if "%1"=="setup" goto setup
if "%1"=="demo" goto demo
if "%1"=="test" goto test
if "%1"=="basic" goto basic
if "%1"=="enhanced" goto enhanced
if "%1"=="batch" goto batch_mode
goto help

:help_interactive
echo.
echo Password Strength Checker Tool - Quick Start
echo ================================================
echo.
echo Available commands:
echo   1. Setup tool (install dependencies)
echo   2. Run interactive password checker
echo   3. Test tool functionality
echo   4. Analyze a password you type
echo   5. Batch analyze from file
echo   6. Show command help
echo   0. Exit
echo.
set /p choice="Enter your choice (0-6): "

if "%choice%"=="1" (
    set INTERACTIVE_MODE=1
    goto setup
)
if "%choice%"=="2" (
    set INTERACTIVE_MODE=1
    goto run_interactive
)
if "%choice%"=="3" (
    set INTERACTIVE_MODE=1
    goto test
)
if "%choice%"=="4" (
    set INTERACTIVE_MODE=1
    goto input_password
)
if "%choice%"=="5" (
    set INTERACTIVE_MODE=1
    goto batch_default
)
if "%choice%"=="6" (
    set INTERACTIVE_MODE=1
    goto help
)
if "%choice%"=="0" goto end
echo Invalid choice. Please try again.
echo.
goto help_interactive

:run_interactive
echo Starting enhanced password checker in interactive mode...
python enhanced_password_checker.py -i
goto end

:input_password
echo.
set /p userpass="Enter password to analyze: "
if "%userpass%"=="" (
    echo No password entered.
    goto help_interactive
)
echo Analyzing your password...
python enhanced_password_checker.py -p "%userpass%"
echo.
echo Press any key to return to menu...
pause >nul
goto help_interactive

:batch_default
echo Using default test file...
python enhanced_password_checker.py -b test_passwords.txt
echo.
echo Press any key to return to menu...
pause >nul
goto help_interactive

:help
echo.
echo Password Strength Checker Tool - Quick Start
echo ================================================
echo.
echo Available commands:
echo   run.bat setup        - Install dependencies and setup tool
echo   run.bat demo          - Run interactive demo
echo   run.bat test          - Run basic functionality tests
echo   run.bat basic [pass]  - Use basic password checker
echo   run.bat enhanced [pass] - Use enhanced password checker
echo   run.bat batch [file]  - Batch analyze passwords from file
echo.
echo Examples:
echo   run.bat setup
echo   run.bat enhanced "MyPassword123!"
echo   run.bat batch test_passwords.txt
echo.
if "%INTERACTIVE_MODE%"=="1" (
    echo Press any key to return to menu...
    pause >nul
    goto help_interactive
)
goto end

:setup
echo Installing dependencies and setting up tool...
python setup.py
if "%INTERACTIVE_MODE%"=="1" (
    echo.
    echo Press any key to return to menu...
    pause >nul
    goto help_interactive
)
goto end

:demo
echo Running interactive demo...
python demo.py
if "%INTERACTIVE_MODE%"=="1" (
    echo.
    echo Press any key to return to menu...
    pause >nul
    goto help_interactive
)
goto end

:test
echo Running basic tests...
echo.
echo Testing basic checker:
python password_checker.py -p "Test123!"
echo.
echo Testing enhanced checker:
python enhanced_password_checker.py -p "Test123!"
if "%INTERACTIVE_MODE%"=="1" (
    echo.
    echo Press any key to return to menu...
    pause >nul
    goto help_interactive
)
goto end

:basic
if "%~2"=="" (
    echo Starting basic password checker in interactive mode...
    python password_checker.py -i
) else (
    echo Analyzing password with basic checker...
    python password_checker.py -p "%~2"
)
goto end

:enhanced
if "%~2"=="" (
    echo Starting enhanced password checker in interactive mode...
    python enhanced_password_checker.py -i
) else (
    echo Analyzing password with enhanced checker...
    python enhanced_password_checker.py -p "%~2"
)
goto end

:batch_mode
if "%~2"=="" (
    echo Using default test file...
    python enhanced_password_checker.py -b test_passwords.txt
) else (
    echo Analyzing passwords from file: %~2
    python enhanced_password_checker.py -b "%~2"
)
goto end

:end
echo.
echo Done!
