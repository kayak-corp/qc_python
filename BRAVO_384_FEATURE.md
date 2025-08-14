# Bravo 384 Separate Standard Curve File Feature

## Overview

The Bravo 384 liquid dispenser has been enhanced to support a separate standard curve file selection. This feature addresses the unique workflow where the Bravo 384 essentially "stamps" the plate, with 384 nozzles responsible for 1 well each, including where the standard curve normally would be.

## Problem Solved

Previously, the standard curve data was extracted from the first 3 columns of the main data file. However, with Bravo 384, the standard curve wells are also dispensed by the same nozzles, making it necessary to use a separate file for the standard curve data.

## New Functionality

### UI Changes

When "Bravo - 384" is selected as the liquid handler:

1. **Additional File Selection**: A new "Step 1.5" appears in the UI allowing users to select a separate CSV file for standard curve data
2. **Conditional Display**: The standard curve file selection only appears when Bravo 384 is selected and is hidden for other handlers
3. **Validation**: The UI validates that a standard curve file is selected when Bravo 384 is chosen

### File Requirements

The standard curve CSV file must:
- Be in the same format as the main data file
- Contain standard curve data in the first 3 columns only
- Have the "Results for Fluorescein" section
- Follow the same well mapping pattern (A1, A2, A3, C1, C2, C3, etc.)

### Data Processing Changes

1. **Separate Loading**: When Bravo 384 is selected, the standard curve data is loaded from the separate file
2. **Backward Compatibility**: Other handlers continue to use the standard curve data from the main file (first 3 columns)
3. **Error Handling**: Proper error messages guide users if the standard curve file is missing or invalid

## Implementation Details

### New Methods

- `load_standard_curve_from_file(std_curve_file)`: Loads standard curve data from a separate CSV file
- Updated `process_qc_analysis()`: Now accepts an optional `std_curve_file` parameter
- Updated `load_and_clean_data()`: Now accepts an optional `std_curve_file` parameter

### UI Components

- `std_curve_file_frame`: Frame containing the standard curve file selection UI
- `std_curve_file_path`: StringVar storing the selected standard curve file path
- `browse_std_curve_file()`: Function to browse and select the standard curve file
- Updated `update_handler_description()`: Shows/hides standard curve file selection based on handler type

### Data Flow

1. User selects "Bravo - 384" as liquid handler
2. Standard curve file selection UI appears
3. User selects main data file and standard curve file
4. System validates both files are selected
5. Data processing uses separate files for main data and standard curve
6. QC analysis proceeds with the separate standard curve data

## Usage Instructions

1. Launch the Dispenser QC Analyzer
2. Select your main CSV data file (Step 1)
3. Select "Bravo - 384" as the liquid handler (Step 4)
4. A new "Step 1.5" will appear for selecting the standard curve CSV file
5. Select your standard curve CSV file (must contain data in first 3 columns only)
6. Enter standard curve concentrations and target concentration as usual
7. Process the data

## Testing

The implementation includes comprehensive testing via `test_bravo_384.py` which verifies:
- Method existence and signatures
- UI integration
- Data flow integrity
- Backward compatibility

## Backward Compatibility

This feature maintains full backward compatibility:
- All existing handlers (Tempest, Combi, D2, Nano, Bravo - 96) continue to work as before
- The standard curve file selection only appears for Bravo 384
- Existing workflows are unaffected

## Error Handling

The system provides clear error messages for:
- Missing standard curve file when Bravo 384 is selected
- Invalid standard curve file format
- Missing fluorescence data section in standard curve file
- Insufficient standard curve wells found
