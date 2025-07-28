#!/usr/bin/env python3
"""
Test script to verify correct data extraction from Tempest CSV files
"""

import pandas as pd
import numpy as np

def test_data_extraction():
    """Test the data extraction from the CSV file"""
    
    print("Testing data extraction from Tempest(1,2,3)_Test.csv")
    print("=" * 60)
    
    # Read the CSV file manually
    data = []
    with open("Tempest(1,2,3)_Test.csv", 'r', encoding='utf-8') as f:
        for line in f:
            row = [cell.strip().strip('"') for cell in line.split(',')]
            data.append(row)
    
    # Convert to DataFrame
    max_cols = max(len(row) for row in data)
    for row in data:
        while len(row) < max_cols:
            row.append('')
    
    df = pd.DataFrame(data)
    print(f"Raw data shape: {df.shape}")
    
    # Find the fluorescence data section
    fluorescence_start = None
    for i, row in df.iterrows():
        if pd.notna(row[0]) and "Results for Fluorescein" in str(row[0]):
            fluorescence_start = i + 1
            break
    
    print(f"Found fluorescence data starting at row {fluorescence_start}")
    
    # Extract fluorescence data (16 rows, 24 columns)
    fluorescence_data = df.iloc[fluorescence_start:fluorescence_start+16, 1:25].copy()
    
    # Convert to numeric
    for col in fluorescence_data.columns:
        fluorescence_data[col] = pd.to_numeric(fluorescence_data[col], errors='coerce')
    
    print(f"Fluorescence data shape: {fluorescence_data.shape}")
    
    # Check the first few rows
    print("\nFirst 3 rows of fluorescence data:")
    print(fluorescence_data.head(3))
    
    # Extract standard curve wells
    print("\nStandard curve wells (first 3 columns, every other row):")
    row_indices = [0, 2, 4, 6, 8, 10, 12, 14]  # A, C, E, G, I, K, M, O
    col_indices = [0, 1, 2]  # Columns 1, 2, 3
    
    for i, row_idx in enumerate(row_indices):
        std_num = i + 1
        print(f"\nSTD{std_num} wells:")
        for col_idx in col_indices:
            if row_idx < len(fluorescence_data) and col_idx < len(fluorescence_data.columns):
                rfu_value = fluorescence_data.iloc[row_idx, col_idx]
                well_id = f"{chr(65+row_idx)}{col_idx+1}"
                print(f"  {well_id}: RFU = {rfu_value}")
    
    # Check what the actual values should be
    print("\nExpected values from manual inspection:")
    expected_values = {
        'A1': 2428618, 'A2': 2438349, 'A3': 2370921,
        'C1': 1288572, 'C2': 1267095, 'C3': 1240093,
        'E1': 621981, 'E2': 643548, 'E3': 596619,
        'G1': 326795, 'G2': 325649, 'G3': 330356,
        'I1': 160696, 'I2': 160263, 'I3': 156615,
        'K1': 78086, 'K2': 81071, 'K3': 82020,
        'M1': 38792, 'M2': 41096, 'M3': 39413,
        'O1': 19529, 'O2': 20610, 'O3': 19302
    }
    
    print("Expected vs Actual:")
    for well_id, expected in expected_values.items():
        row_idx = ord(well_id[0]) - ord('A')
        col_idx = int(well_id[1:]) - 1
        if row_idx < len(fluorescence_data) and col_idx < len(fluorescence_data.columns):
            actual = fluorescence_data.iloc[row_idx, col_idx]
            print(f"  {well_id}: Expected {expected}, Actual {actual}")

if __name__ == "__main__":
    test_data_extraction() 