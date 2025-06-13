# Quick start script for Password Strength Checker Tool
# Usage: .\run.ps1 [command] [arguments]

param(
    [string]$Command = "",
    [string]$Argument = ""
)

function Show-Help {    Write-Host ""
    Write-Host "Password Strength Checker Tool - Quick Start" -ForegroundColor Cyan
    Write-Host "================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Available commands:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 setup        - Install dependencies and setup tool"
    Write-Host "  .\run.ps1 gui           - Launch GUI interface"
    Write-Host "  .\run.ps1 demo          - Run interactive demo"
    Write-Host "  .\run.ps1 test          - Run basic functionality tests"
    Write-Host "  .\run.ps1 basic [pass]  - Use basic password checker"
    Write-Host "  .\run.ps1 enhanced [pass] - Use enhanced password checker"
    Write-Host "  .\run.ps1 batch [file]  - Batch analyze passwords from file"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Green
    Write-Host "  .\run.ps1 setup"
    Write-Host "  .\run.ps1 gui"
    Write-Host "  .\run.ps1 enhanced `"MyPassword123!`""
    Write-Host "  .\run.ps1 batch test_passwords.txt"
    Write-Host ""
}

function Run-Setup {
    Write-Host "Installing dependencies and setting up tool..." -ForegroundColor Yellow
    python setup.py
}

function Run-Demo {
    Write-Host "Running interactive demo..." -ForegroundColor Yellow
    python demo.py
}

function Run-Test {
    Write-Host "Running basic tests..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Testing basic checker:" -ForegroundColor Cyan
    python password_checker.py -p "Test123!"
    Write-Host ""
    Write-Host "Testing enhanced checker:" -ForegroundColor Cyan
    python enhanced_password_checker.py -p "Test123!"
}

function Run-Basic {
    if ($Argument -eq "") {
        Write-Host "Starting basic password checker in interactive mode..." -ForegroundColor Yellow
        python password_checker.py -i
    } else {
        Write-Host "Analyzing password with basic checker..." -ForegroundColor Yellow
        python password_checker.py -p $Argument
    }
}

function Run-Enhanced {
    if ($Argument -eq "") {
        Write-Host "Starting enhanced password checker in interactive mode..." -ForegroundColor Yellow
        python enhanced_password_checker.py -i
    } else {
        Write-Host "Analyzing password with enhanced checker..." -ForegroundColor Yellow
        python enhanced_password_checker.py -p $Argument
    }
}

function Run-Batch {
    if ($Argument -eq "") {
        Write-Host "Using default test file..." -ForegroundColor Yellow
        python enhanced_password_checker.py -b test_passwords.txt
    } else {
        Write-Host "Analyzing passwords from file: $Argument" -ForegroundColor Yellow
        python enhanced_password_checker.py -b $Argument
    }
}

function Run-GUI {
    Write-Host "Launching GUI interface..." -ForegroundColor Yellow
    python password_checker_gui.py
}

# Main execution
switch ($Command.ToLower()) {
    "" { Show-Help }
    "help" { Show-Help }
    "setup" { Run-Setup }
    "demo" { Run-Demo }
    "test" { Run-Test }
    "basic" { Run-Basic }
    "enhanced" { Run-Enhanced }
    "batch" { Run-Batch }
    "gui" { Run-GUI }
    default { 
        Write-Host "Unknown command: $Command" -ForegroundColor Red
        Show-Help 
    }
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
