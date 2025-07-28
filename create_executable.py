#!/usr/bin/env python3
"""
Script to create a standalone executable for the Dispenser QC Analyzer
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed successfully")

def create_executable():
    """Create standalone executable"""
    print("🔨 Creating standalone executable...")
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",                    # Single executable file
        "--windowed",                   # No console window (for GUI)
        "--name=DispenserQCAnalyzer",   # Executable name
        "--add-data=example_data;example_data",  # Include example data
        "--icon=icon.ico",              # Add icon if available
        "qc_check.py"
    ]
    
    # Remove icon if not available
    if not os.path.exists("icon.ico"):
        cmd.remove("--icon=icon.ico")
    
    try:
        subprocess.check_call(cmd)
        print("✅ Executable created successfully!")
        print(f"📁 Location: dist/DispenserQCAnalyzer.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error creating executable: {e}")
        return False
    
    return True

def create_distribution_package():
    """Create a complete distribution package"""
    print("📦 Creating distribution package...")
    
    # Create dist directory structure
    dist_dir = Path("distribution")
    dist_dir.mkdir(exist_ok=True)
    
    # Copy executable
    if os.path.exists("dist/DispenserQCAnalyzer.exe"):
        shutil.copy("dist/DispenserQCAnalyzer.exe", dist_dir)
    
    # Copy example data
    example_dir = dist_dir / "example_data"
    example_dir.mkdir(exist_ok=True)
    if os.path.exists("example_data"):
        for file in os.listdir("example_data"):
            if file.endswith(".csv"):
                shutil.copy(f"example_data/{file}", example_dir)
    
    # Create README for distribution
    readme_content = """# Dispenser QC Analyzer - Standalone Version

## Quick Start

1. **Windows Users**: Double-click `DispenserQCAnalyzer.exe`
2. **Mac/Linux Users**: Run `python qc_check.py`

## Features

- ✅ No installation required
- ✅ All dependencies included
- ✅ Example data included
- ✅ Works on any computer with the same OS

## Usage

1. Run the executable
2. Select your CSV data file
3. Enter standard curve concentrations
4. Enter target concentration
5. Configure chips (optional)
6. Click "Process Data"

## Example Data

The `example_data` folder contains sample files to test the software.

## Support

For issues or questions, please refer to the main GitHub repository.
"""
    
    with open(dist_dir / "README.txt", "w") as f:
        f.write(readme_content)
    
    print("✅ Distribution package created!")
    print(f"📁 Location: {dist_dir}")
    
    return True

def main():
    """Main function"""
    print("🚀 Creating Standalone Executable for Dispenser QC Analyzer")
    print("=" * 60)
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create executable
    if create_executable():
        # Create distribution package
        create_distribution_package()
        
        print("\n🎉 Success! Distribution package created.")
        print("\n📋 Next Steps:")
        print("1. Copy the 'distribution' folder to target computers")
        print("2. Users can run DispenserQCAnalyzer.exe directly")
        print("3. No Python installation required on target computers")
    else:
        print("\n❌ Failed to create executable. Please check the error messages above.")

if __name__ == "__main__":
    main() 