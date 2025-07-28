@echo off
echo ========================================
echo    Dispenser QC Analyzer
echo ========================================
echo.
echo Starting GUI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking dependencies...
python -c "import pandas, numpy, matplotlib, scipy, tkinter" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install dependencies
        echo Please run: pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
)

REM Run the GUI
echo Starting GUI...
python qc_check.py

REM Check if GUI ran successfully
if errorlevel 1 (
    echo.
    echo ERROR: GUI failed to start
    echo Please check the error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo GUI closed successfully
pause 