#!/usr/bin/env python3
"""
Debug script for the Dispenser QC Analyzer
This script helps identify issues with standard curve building.
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path

def debug_csv_file(csv_file):
    """Debug a CSV file to identify potential issues"""
    
    print(f"Debugging file: {csv_file}")
    print("=" * 50)
    
    try:
        # Read the CSV file
        df = pd.read_csv(csv_file, header=None)
        print(f"File shape: {df.shape}")
        
        # Check first few rows
        print("\nFirst 10 rows:")
        print(df.head(10))
        
        # Look for standard curve data (first two rows)
        print("\nStandard curve data (rows 0-1):")
        if len(df) >= 2:
            print("Row 0 (concentrations):", df.iloc[0, 1:8].tolist())
            print("Row 1 (RFU values):", df.iloc[1, 1:8].tolist())
            
            # Check if data is numeric
            concentrations = df.iloc[0, 1:8].values
            rfu_values = df.iloc[1, 1:8].values
            
            print("\nData type analysis:")
            print("Concentrations:", [type(x) for x in concentrations])
            print("RFU values:", [type(x) for x in rfu_values])
            
            # Try to convert to numeric
            try:
                concentrations_numeric = pd.to_numeric(concentrations, errors='coerce')
                rfu_values_numeric = pd.to_numeric(rfu_values, errors='coerce')
                
                print("\nNumeric conversion results:")
                print("Concentrations (numeric):", concentrations_numeric.tolist())
                print("RFU values (numeric):", rfu_values_numeric.tolist())
                
                # Check for NaN values
                print("\nNaN check:")
                print("Concentrations with NaN:", np.isnan(concentrations_numeric).sum())
                print("RFU values with NaN:", np.isnan(rfu_values_numeric).sum())
                
                # Check if we have enough valid data points
                valid_concentrations = concentrations_numeric[~np.isnan(concentrations_numeric)]
                valid_rfu = rfu_values_numeric[~np.isnan(rfu_values_numeric)]
                
                print(f"\nValid data points: {len(valid_concentrations)}")
                print(f"Minimum required: 2")
                
                if len(valid_concentrations) < 2:
                    print("❌ ERROR: Insufficient valid data points for standard curve")
                    return False
                else:
                    print("✅ Sufficient data points for standard curve")
                    
                    # Check for zero or negative values
                    if np.any(valid_concentrations <= 0):
                        print("⚠️  WARNING: Some concentrations are zero or negative")
                    
                    if np.any(valid_rfu <= 0):
                        print("⚠️  WARNING: Some RFU values are zero or negative")
                    
                    return True
                    
            except Exception as e:
                print(f"❌ ERROR converting to numeric: {str(e)}")
                return False
        else:
            print("❌ ERROR: File has fewer than 2 rows")
            return False
            
    except Exception as e:
        print(f"❌ ERROR reading file: {str(e)}")
        return False

def test_standard_curve_building(csv_file):
    """Test the standard curve building process"""
    
    print(f"\nTesting standard curve building for: {csv_file}")
    print("=" * 50)
    
    try:
        # Read CSV file
        df = pd.read_csv(csv_file, header=None)
        
        # Extract standard curve data
        concentrations = df.iloc[0, 1:8].values
        rfu_values = df.iloc[1, 1:8].values
        
        # Convert to numeric
        concentrations = pd.to_numeric(concentrations, errors='coerce')
        rfu_values = pd.to_numeric(rfu_values, errors='coerce')
        
        # Create standard curve data
        standard_curve_data = pd.DataFrame({
            'concentration': concentrations,
            'fluorescence': rfu_values
        })
        
        print(f"Standard curve data shape: {standard_curve_data.shape}")
        print("Standard curve data:")
        print(standard_curve_data)
        
        # Check for sufficient data
        if len(standard_curve_data) < 2:
            print("❌ ERROR: Insufficient standard curve data")
            return False
        
        # Check for valid numeric data
        valid_data = standard_curve_data.dropna()
        if len(valid_data) < 2:
            print("❌ ERROR: Insufficient valid data after removing NaN values")
            return False
        
        print(f"Valid data points: {len(valid_data)}")
        
        # Try linear regression
        from scipy import stats
        
        x = valid_data['fluorescence'].values
        y = valid_data['concentration'].values
        
        print(f"X values (fluorescence): {x}")
        print(f"Y values (concentration): {y}")
        
        # Check for constant values
        if np.std(x) == 0:
            print("❌ ERROR: All fluorescence values are the same (no variation)")
            return False
        
        if np.std(y) == 0:
            print("❌ ERROR: All concentration values are the same (no variation)")
            return False
        
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        print(f"✅ Standard curve built successfully!")
        print(f"Slope: {slope:.2e}")
        print(f"Intercept: {intercept:.2e}")
        print(f"R²: {r_value**2:.4f}")
        
        return True
        
    except Exception as e:
        print(f"❌ ERROR building standard curve: {str(e)}")
        return False

def main():
    """Main debug function"""
    
    print("Dispenser QC Analyzer - Debug Tool")
    print("=" * 50)
    
    # Check for CSV files in current directory
    csv_files = list(Path('.').glob('*.csv'))
    
    if not csv_files:
        print("No CSV files found in current directory")
        return
    
    print(f"Found {len(csv_files)} CSV file(s):")
    for file in csv_files:
        print(f"  - {file}")
    
    print("\n" + "=" * 50)
    
    # Debug each CSV file
    for csv_file in csv_files:
        print(f"\n{'='*20} {csv_file} {'='*20}")
        
        # Debug the file structure
        debug_csv_file(csv_file)
        
        # Test standard curve building
        test_standard_curve_building(csv_file)
        
        print("\n" + "-" * 50)

if __name__ == "__main__":
    main() 