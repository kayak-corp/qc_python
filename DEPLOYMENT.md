# Deployment Guide - Dispenser QC Analyzer

This guide covers the easiest ways to distribute the Dispenser QC Analyzer to other computers.

## 🚀 Method 1: GitHub Repository (Recommended)

### **For Technical Users:**
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/dispenser-qc-analyzer.git
cd dispenser-qc-analyzer

# Install dependencies
pip install -r requirements.txt

# Run (Windows)
run_gui.bat

# Run (Mac/Linux)
python qc_check.py
```

### **For Non-Technical Users:**
1. Go to the GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract to desktop
4. Double-click `run_gui.bat` (Windows) or run `python qc_check.py` (Mac/Linux)

## 📦 Method 2: Standalone Executable

### **Create Executable:**
```bash
# Run the packaging script
python create_executable.py
```

This creates:
- `dist/DispenserQCAnalyzer.exe` - Standalone executable
- `distribution/` folder - Complete package with example data

### **Distribute:**
1. Copy the `distribution` folder to target computers
2. Users double-click `DispenserQCAnalyzer.exe`
3. No Python installation required!

## 🛠️ Method 3: Windows Installer

### **For Windows Users:**
1. Copy the entire project folder to target computer
2. Run `install.bat` as administrator
3. Creates desktop and start menu shortcuts
4. Installs all dependencies automatically

## 📋 Method 4: USB Drive Distribution

### **Create Portable Package:**
1. Copy project folder to USB drive
2. Include `run_gui.bat` and `run_cli.bat`
3. Include `requirements.txt`
4. Include example data

### **On Target Computer:**
1. Insert USB drive
2. Navigate to project folder
3. Run `install.bat` (Windows) or install dependencies manually
4. Run `run_gui.bat` or `python qc_check.py`

## 🖥️ Method 5: Network Deployment

### **Shared Network Drive:**
1. Copy project to network drive
2. Create shortcuts pointing to network location
3. Users access from any computer on network

### **Requirements:**
- All computers need Python installed
- Network drive accessible to all users
- Dependencies installed on each computer

## 📊 Comparison of Methods

| Method | Ease of Use | Setup Time | Dependencies | File Size |
|--------|-------------|------------|--------------|-----------|
| GitHub | ⭐⭐⭐⭐⭐ | 5 min | Python + Git | Small |
| Executable | ⭐⭐⭐⭐⭐ | 0 min | None | Large |
| Installer | ⭐⭐⭐⭐ | 2 min | Python | Small |
| USB Drive | ⭐⭐⭐ | 5 min | Python | Small |
| Network | ⭐⭐⭐ | 10 min | Python + Network | Small |

## 🎯 Recommended Approach by User Type

### **For IT Departments:**
- **Method 1**: GitHub repository with automated deployment scripts
- **Method 2**: Standalone executable for non-technical users

### **For Research Labs:**
- **Method 1**: GitHub repository (version control, updates)
- **Method 3**: Windows installer (easy setup)

### **For Individual Users:**
- **Method 2**: Standalone executable (no setup required)
- **Method 4**: USB drive (portable)

### **For Multiple Organizations:**
- **Method 1**: GitHub repository (centralized updates)
- **Method 2**: Standalone executable (no IT support needed)

## 🔧 Technical Requirements

### **Minimum System Requirements:**
- **OS**: Windows 7+, macOS 10.12+, Linux (Ubuntu 16.04+)
- **RAM**: 4GB
- **Storage**: 100MB free space
- **Python**: 3.7+ (for source distribution)

### **For Executable Distribution:**
- **OS**: Windows 7+ (executable is Windows-specific)
- **RAM**: 4GB
- **Storage**: 200MB free space
- **Python**: Not required

## 📝 Deployment Checklist

### **Before Distribution:**
- [ ] Test on target OS versions
- [ ] Verify all dependencies work
- [ ] Test with example data
- [ ] Create user documentation
- [ ] Test installation process

### **For Each Target Computer:**
- [ ] Install Python (if using source)
- [ ] Install dependencies
- [ ] Test GUI functionality
- [ ] Test CLI functionality
- [ ] Verify example data works
- [ ] Create shortcuts (Windows)

### **Post-Deployment:**
- [ ] User training
- [ ] Support documentation
- [ ] Update procedures
- [ ] Backup procedures

## 🆘 Troubleshooting

### **Common Issues:**

**"Python not found":**
- Install Python from python.org
- Check "Add to PATH" during installation

**"Module not found":**
- Run `pip install -r requirements.txt`
- Check Python version (3.7+ required)

**"GUI not opening":**
- Check tkinter installation
- Try running from command line for error messages

**"Permission denied":**
- Run as administrator (Windows)
- Check file permissions

### **Support Resources:**
- GitHub Issues page
- README.md documentation
- Example data for testing
- Command-line mode for debugging

## 📈 Scaling Considerations

### **For 1-5 Users:**
- GitHub repository or USB drive distribution

### **For 5-20 Users:**
- Network deployment or standalone executables

### **For 20+ Users:**
- Automated deployment scripts
- Centralized update system
- User management system

---

**Note**: Choose the method that best fits your organization's technical capabilities and user requirements. 