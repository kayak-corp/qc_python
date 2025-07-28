@echo off
echo ========================================
echo    Building Windows Executable
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    echo.
    pause
    exit /b 1
)

echo ✅ Python found:
python --version

REM Install dependencies
echo.
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    echo Please check your internet connection and try again
    echo.
    pause
    exit /b 1
)

REM Install PyInstaller
echo.
echo Installing PyInstaller...
pip install pyinstaller
if errorlevel 1 (
    echo ERROR: Failed to install PyInstaller
    echo.
    pause
    exit /b 1
)

echo ✅ PyInstaller installed successfully

REM Create Windows executable
echo.
echo Creating Windows executable...
python create_executable.py

if errorlevel 1 (
    echo.
    echo ERROR: Failed to create executable
    echo Please check the error messages above
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Build Complete!
echo ========================================
echo.
echo Your Windows executable is ready:
echo 📁 Location: distribution/DispenserQCAnalyzer.exe
echo.
echo To distribute:
echo 1. Copy the entire 'distribution' folder
echo 2. Users can run DispenserQCAnalyzer.exe directly
echo 3. No Python installation required on target computers
echo.
pause 