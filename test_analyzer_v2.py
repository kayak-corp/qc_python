#!/usr/bin/env python3
"""
Test script for the Dispenser QC Analyzer V2
This script demonstrates the analyzer functionality using the provided CSV files.
"""

import pandas as pd
import numpy as np
from dispenser_qc_analyzer_v2 import DispenserQCAnalyzerV2
import os

def test_with_tempest_data():
    """Test the analyzer with the Tempest CSV files"""
    
    # Initialize analyzer
    analyzer = DispenserQCAnalyzerV2()
    
    # Test with first CSV file
    csv_file = "Tempest Chip 1(Plate 1).csv"
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found in current directory")
        return
    
    print("Testing with Tempest Chip 1(Plate 1).csv")
    print("=" * 50)
    
    # Set test parameters
    analyzer.standard_concentrations = [300, 75, 37.5, 18.75, 9.375, 4.6875, 2.34375, 1.171875]
    analyzer.target_concentration = 75.0
    
    # Run analysis
    try:
        analyzer.process_qc_analysis(csv_file)
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {str(e)}")

def analyze_csv_structure():
    """Analyze the structure of the CSV files to understand the data format"""
    
    print("Analyzing CSV file structures...")
    print("=" * 50)
    
    files = ["Tempest Chip 1(Plate 1).csv"]
    
    for file in files:
        if os.path.exists(file):
            print(f"\nFile: {file}")
            print("-" * 30)
            
            try:
                # Read the file
                df = pd.read_csv(file, header=None)
                print(f"Shape: {df.shape}")
                
                # Show first few rows
                print("First 5 rows:")
                print(df.head())
                
                # Show rows around the data section
                print("\nRows 20-25 (around data section):")
                print(df.iloc[20:25])
                
                # Show the standard curve data
                print("\nStandard curve data (rows 0-1):")
                print(df.iloc[0:2, 0:8])
                
                # Show fluorescence data section
                print("\nFluorescence data (rows 23-27):")
                print(df.iloc[23:28, 0:5])
                
            except Exception as e:
                print(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    print("Dispenser QC Analyzer V2 - Test Script")
    print("=" * 50)
    
    # First analyze the CSV structures
    analyze_csv_structure()
    
    # Then test with the data
    print("\n" + "=" * 50)
    print("Running Tests")
    print("=" * 50)
    
    test_with_tempest_data()
    
    print("\nTest script completed!") 