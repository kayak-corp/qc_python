#!/usr/bin/env python3
"""
Test script for the Dispenser QC Analyzer
This script demonstrates the analyzer functionality using the provided CSV files.
"""

import pandas as pd
import numpy as np
from dispenser_qc_analyzer import DispenserQCAnalyzer
import os

def test_with_tempest_data():
    """Test the analyzer with the Tempest CSV files"""
    
    # Initialize analyzer
    analyzer = DispenserQCAnalyzer()
    
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

def test_with_tempest_test_data():
    """Test with the second CSV file"""
    
    # Initialize analyzer
    analyzer = DispenserQCAnalyzer()
    
    # Test with second CSV file
    csv_file = "Tempest(1,2,3)_Test.csv"
    
    if not os.path.exists(csv_file):
        print(f"Error: {csv_file} not found in current directory")
        return
    
    print("\nTesting with Tempest(1,2,3)_Test.csv")
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
    
    files = ["Tempest Chip 1(Plate 1).csv", "Tempest(1,2,3)_Test.csv"]
    
    for file in files:
        if os.path.exists(file):
            print(f"\nFile: {file}")
            print("-" * 30)
            
            try:
                # Read first few lines to understand structure
                df = pd.read_csv(file, header=None)
                print(f"Shape: {df.shape}")
                print(f"First 5 rows:")
                print(df.head())
                
                # Look for numeric data
                numeric_data_found = False
                for i, row in df.iterrows():
                    if i > 20:  # Limit search
                        break
                    numeric_count = 0
                    for val in row:
                        if pd.notna(val) and str(val).replace('.', '').replace('-', '').replace('e', '').replace('E', '').isdigit():
                            numeric_count += 1
                    if numeric_count >= 3:
                        print(f"Potential data section found at row {i}")
                        print(f"Sample values: {row.head().tolist()}")
                        numeric_data_found = True
                        break
                
                if not numeric_data_found:
                    print("No clear numeric data section found")
                    
            except Exception as e:
                print(f"Error reading file: {str(e)}")

if __name__ == "__main__":
    print("Dispenser QC Analyzer - Test Script")
    print("=" * 50)
    
    # First analyze the CSV structures
    analyze_csv_structure()
    
    # Then test with the data
    print("\n" + "=" * 50)
    print("Running Tests")
    print("=" * 50)
    
    test_with_tempest_data()
    test_with_tempest_test_data()
    
    print("\nTest script completed!") 