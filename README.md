# Dispenser QC Analyzer

A Python-based quality control analysis tool for low-volume liquid dispensers using fluorescence-based measurement.

## Overview

This tool automates the quality control (QC) analysis for liquid dispensers by analyzing fluorescence data from plate readers. It calculates two key performance metrics:

- **Precision (%CV)**: How consistent are the volumes dispensed by each nozzle
- **Accuracy (%Accuracy)**: How close is the average dispensed volume to the intended target volume

## Features

### 🔬 Fluorescence-Based Analysis
- Uses fluorescein as a tracer dye
- Converts fluorescence signals to concentration values via standard curve
- Supports 384-well plate analysis

### 📊 Multi-Chip Support
- Analyze multiple chips simultaneously
- Define custom column ranges for each chip
- Per-chip and per-nozzle QC metrics
- Chip average calculations

### 📈 Advanced Visualization
- Standard curve plots with regression equations
- Individual chip performance plots
- Combined multi-chip comparison plots
- Chip average reference lines

### 🖥️ User-Friendly Interface
- GUI mode with Tkinter interface
- Command-line interface for automation
- Interactive chip configuration
- Real-time data validation

## Installation

### Prerequisites
- Python 3.7+
- Required packages (install via pip):

```bash
pip install pandas numpy matplotlib scipy tkinter
```

### Quick Start
1. Clone the repository
2. Run the analyzer:

```bash
# GUI mode
python qc_check.py

# Command line mode
python qc_check.py --file "your_data.csv" --target 60 --concentrations "600,300,150,75,37.5,18.75,9.375,4.6875"
```

## Usage

### GUI Mode
1. Run `python qc_check.py`
2. Select your CSV data file
3. Enter standard curve concentrations (8 values)
4. Enter target concentration
5. Configure chips and column ranges
6. Click "Process Data"

### Command Line Mode
```bash
python qc_check.py --file "data.csv" --target 60 --concentrations "600,300,150,75,37.5,18.75,9.375,4.6875"
```

### Multi-Chip Configuration
- Add multiple chips in the GUI
- Define column ranges for each chip (e.g., Chip 1: columns 4-10, Chip 2: columns 11-20)
- Each chip has 8 nozzles (16 rows total, 2 rows per nozzle)

## Data Format

### Input CSV Requirements
- Raw fluorescence data from plate reader
- Standard curve wells in first 3 columns (every other row)
- Chip data in remaining columns
- Metadata headers at top (automatically skipped)

### Output Files
- `*_processed.csv`: Calculated concentrations and QC metrics
- `plots/standard_curve.png`: Standard curve with regression equation
- `plots/chip_*_nozzle_performance.png`: Individual chip performance plots
- `plots/all_chips_nozzle_performance.png`: Combined multi-chip plot

## QC Metrics

### Precision (%CV)
```
%CV = (Standard Deviation / Mean) × 100
```

### Accuracy (%Accuracy)
```
%Accuracy = ((Mean - Target) / Target) × 100
```

### Quality Assessment
- **EXCELLENT**: %CV < 5%
- **GOOD**: %CV < 10%
- **ACCEPTABLE**: %CV < 15%
- **POOR**: %CV ≥ 15%

## File Structure

```
├── qc_check.py              # Main analyzer script
├── test_multi_chip.py       # Multi-chip plotting test
├── README.md               # This file
├── .gitignore              # Git ignore rules
└── example_data/           # Example data files
    ├── Tempest(4,5,6)_Test-1.csv
    └── Tempest Chip 1(Plate 1).csv
```

## Technical Details

### Standard Curve Calculation
- Uses median of triplicate wells for each standard concentration
- Linear regression: `Concentration = slope × RFU + intercept`
- R² value indicates curve quality

### Nozzle Grouping
- Each nozzle controls 2 consecutive rows
- Nozzle 1 = Rows A & B
- Nozzle 2 = Rows C & D
- etc.

### Data Processing
- Automatically skips metadata headers
- Converts all data to numeric format
- Handles missing or invalid data
- Excludes standard curve wells from QC calculations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues or questions, please open an issue on GitHub or contact the development team.

---

**Note**: This tool is designed for fluorescence-based dispenser QC analysis. Ensure your data format matches the expected structure for optimal results. 