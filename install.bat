@echo off
echo ========================================
echo    Dispenser QC Analyzer - Installer
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

echo ✅ Dependencies installed successfully

REM Create desktop shortcut
echo.
echo Creating desktop shortcut...
set SHORTCUT_PATH=%USERPROFILE%\Desktop\Dispenser QC Analyzer.lnk

REM Create shortcut using PowerShell
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_PATH%'); $Shortcut.TargetPath = '%~dp0run_gui.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Dispenser QC Analyzer'; $Shortcut.Save()"

if exist "%SHORTCUT_PATH%" (
    echo ✅ Desktop shortcut created
) else (
    echo ⚠️  Could not create desktop shortcut (requires admin rights)
)

REM Create start menu shortcut
echo Creating start menu shortcut...
set START_MENU_PATH=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Dispenser QC Analyzer.lnk

powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%START_MENU_PATH%'); $Shortcut.TargetPath = '%~dp0run_gui.bat'; $Shortcut.WorkingDirectory = '%~dp0'; $Shortcut.Description = 'Dispenser QC Analyzer'; $Shortcut.Save()"

if exist "%START_MENU_PATH%" (
    echo ✅ Start menu shortcut created
) else (
    echo ⚠️  Could not create start menu shortcut
)

echo.
echo ========================================
echo    Installation Complete!
echo ========================================
echo.
echo You can now run the Dispenser QC Analyzer by:
echo.
echo 1. Double-clicking the desktop shortcut
echo 2. Using the Start Menu
echo 3. Running run_gui.bat from this folder
echo 4. Running python qc_check.py from this folder
echo.
echo The software is ready to use!
echo.
pause 