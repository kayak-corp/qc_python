@echo off
echo ========================================
echo    Dispenser QC Analyzer - CLI Mode
echo ========================================
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
python -c "import pandas, numpy, matplotlib, scipy" >nul 2>&1
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

echo.
echo Usage examples:
echo.
echo 1. Run with GUI:
echo    run_gui.bat
echo.
echo 2. Run with command line (example):
echo    python qc_check.py --file "example_data/Tempest(4,5,6)_Test-1.csv" --target 60 --concentrations "600,300,150,75,37.5,18.75,9.375,4.6875"
echo.
echo 3. Run with your own data:
echo    python qc_check.py --file "your_data.csv" --target YOUR_TARGET --concentrations "CONC1,CONC2,CONC3,CONC4,CONC5,CONC6,CONC7,CONC8"
echo.

REM Check if arguments were provided
if "%1"=="" (
    echo No arguments provided. Running with example data...
    echo.
    python qc_check.py --file "example_data/Tempest(4,5,6)_Test-1.csv" --target 60 --concentrations "600,300,150,75,37.5,18.75,9.375,4.6875"
) else (
    echo Running with provided arguments...
    echo.
    python qc_check.py %*
)

if errorlevel 1 (
    echo.
    echo ERROR: Analysis failed
    echo Please check the error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo Analysis completed successfully!
pause 