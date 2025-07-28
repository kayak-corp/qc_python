#!/usr/bin/env python3
"""
Test script to demonstrate multi-chip plotting functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qc_check import DispenserQCAnalyzerFixedBug
import pandas as pd
import numpy as np

def test_multi_chip_plots():
    """Test the multi-chip plotting functionality"""
    
    # Create analyzer instance
    analyzer = DispenserQCAnalyzerFixedBug()
    
    # Set up test data
    analyzer.standard_concentrations = [600, 300, 150, 75, 37.5, 18.75, 9.375, 4.6875]
    analyzer.target_concentration = 60
    
    # Simulate QC results for multiple chips
    analyzer.qc_results = [
        # Chip 1 results
        {'nozzle_id': 'Chip_1_Nozzle_1', 'chip_id': 'Chip_1', 'mean_concentration': 68.33, 'std_concentration': 1.35, 'cv_percent': 1.97, 'accuracy_percent': 13.89, 'n_measurements': 21, 'column_range': '4-10'},
        {'nozzle_id': 'Chip_1_Nozzle_2', 'chip_id': 'Chip_1', 'mean_concentration': 63.05, 'std_concentration': 3.51, 'cv_percent': 5.56, 'accuracy_percent': 5.09, 'n_measurements': 21, 'column_range': '4-10'},
        {'nozzle_id': 'Chip_1_Nozzle_3', 'chip_id': 'Chip_1', 'mean_concentration': 66.36, 'std_concentration': 1.36, 'cv_percent': 2.06, 'accuracy_percent': 10.59, 'n_measurements': 21, 'column_range': '4-10'},
        {'nozzle_id': 'Chip_1_Nozzle_4', 'chip_id': 'Chip_1', 'mean_concentration': 67.61, 'std_concentration': 2.43, 'cv_percent': 3.60, 'accuracy_percent': 12.69, 'n_measurements': 21, 'column_range': '4-10'},
        {'nozzle_id': 'Chip_1_Nozzle_5', 'chip_id': 'Chip_1', 'mean_concentration': 64.98, 'std_concentration': 2.86, 'cv_percent': 4.40, 'accuracy_percent': 8.30, 'n_measurements': 21, 'column_range': '4-10'},
        {'nozzle_id': 'Chip_1_Nozzle_6', 'chip_id': 'Chip_1', 'mean_concentration': 65.44, 'std_concentration': 1.15, 'cv_percent': 1.76, 'accuracy_percent': 9.07, 'n_measurements': 21, 'column_range': '4-10'},
        {'nozzle_id': 'Chip_1_Nozzle_7', 'chip_id': 'Chip_1', 'mean_concentration': 66.00, 'std_concentration': 1.97, 'cv_percent': 2.99, 'accuracy_percent': 10.00, 'n_measurements': 21, 'column_range': '4-10'},
        {'nozzle_id': 'Chip_1_Nozzle_8', 'chip_id': 'Chip_1', 'mean_concentration': 67.37, 'std_concentration': 3.31, 'cv_percent': 4.91, 'accuracy_percent': 12.28, 'n_measurements': 21, 'column_range': '4-10'},
        
        # Chip 2 results
        {'nozzle_id': 'Chip_2_Nozzle_1', 'chip_id': 'Chip_2', 'mean_concentration': 66.43, 'std_concentration': 1.26, 'cv_percent': 1.89, 'accuracy_percent': 10.71, 'n_measurements': 21, 'column_range': '11-17'},
        {'nozzle_id': 'Chip_2_Nozzle_2', 'chip_id': 'Chip_2', 'mean_concentration': 62.23, 'std_concentration': 1.76, 'cv_percent': 2.84, 'accuracy_percent': 3.72, 'n_measurements': 21, 'column_range': '11-17'},
        {'nozzle_id': 'Chip_2_Nozzle_3', 'chip_id': 'Chip_2', 'mean_concentration': 67.97, 'std_concentration': 1.64, 'cv_percent': 2.42, 'accuracy_percent': 13.29, 'n_measurements': 21, 'column_range': '11-17'},
        {'nozzle_id': 'Chip_2_Nozzle_4', 'chip_id': 'Chip_2', 'mean_concentration': 64.59, 'std_concentration': 1.58, 'cv_percent': 2.45, 'accuracy_percent': 7.65, 'n_measurements': 21, 'column_range': '11-17'},
        {'nozzle_id': 'Chip_2_Nozzle_5', 'chip_id': 'Chip_2', 'mean_concentration': 63.03, 'std_concentration': 1.52, 'cv_percent': 2.42, 'accuracy_percent': 5.04, 'n_measurements': 21, 'column_range': '11-17'},
        {'nozzle_id': 'Chip_2_Nozzle_6', 'chip_id': 'Chip_2', 'mean_concentration': 64.43, 'std_concentration': 1.92, 'cv_percent': 2.97, 'accuracy_percent': 7.38, 'n_measurements': 21, 'column_range': '11-17'},
        {'nozzle_id': 'Chip_2_Nozzle_7', 'chip_id': 'Chip_2', 'mean_concentration': 66.88, 'std_concentration': 2.38, 'cv_percent': 3.56, 'accuracy_percent': 11.47, 'n_measurements': 21, 'column_range': '11-17'},
        {'nozzle_id': 'Chip_2_Nozzle_8', 'chip_id': 'Chip_2', 'mean_concentration': 67.11, 'std_concentration': 3.53, 'cv_percent': 5.25, 'accuracy_percent': 11.86, 'n_measurements': 21, 'column_range': '11-17'},
        
        # Chip 3 results
        {'nozzle_id': 'Chip_3_Nozzle_1', 'chip_id': 'Chip_3', 'mean_concentration': 67.39, 'std_concentration': 1.82, 'cv_percent': 2.70, 'accuracy_percent': 12.31, 'n_measurements': 21, 'column_range': '18-24'},
        {'nozzle_id': 'Chip_3_Nozzle_2', 'chip_id': 'Chip_3', 'mean_concentration': 65.70, 'std_concentration': 2.40, 'cv_percent': 3.66, 'accuracy_percent': 9.51, 'n_measurements': 21, 'column_range': '18-24'},
        {'nozzle_id': 'Chip_3_Nozzle_3', 'chip_id': 'Chip_3', 'mean_concentration': 66.51, 'std_concentration': 0.95, 'cv_percent': 1.43, 'accuracy_percent': 10.84, 'n_measurements': 21, 'column_range': '18-24'},
        {'nozzle_id': 'Chip_3_Nozzle_4', 'chip_id': 'Chip_3', 'mean_concentration': 68.76, 'std_concentration': 1.74, 'cv_percent': 2.54, 'accuracy_percent': 14.60, 'n_measurements': 21, 'column_range': '18-24'},
        {'nozzle_id': 'Chip_3_Nozzle_5', 'chip_id': 'Chip_3', 'mean_concentration': 65.82, 'std_concentration': 1.55, 'cv_percent': 2.36, 'accuracy_percent': 9.70, 'n_measurements': 21, 'column_range': '18-24'},
        {'nozzle_id': 'Chip_3_Nozzle_6', 'chip_id': 'Chip_3', 'mean_concentration': 65.94, 'std_concentration': 1.46, 'cv_percent': 2.22, 'accuracy_percent': 9.90, 'n_measurements': 21, 'column_range': '18-24'},
        {'nozzle_id': 'Chip_3_Nozzle_7', 'chip_id': 'Chip_3', 'mean_concentration': 67.63, 'std_concentration': 2.41, 'cv_percent': 3.56, 'accuracy_percent': 12.71, 'n_measurements': 21, 'column_range': '18-24'},
        {'nozzle_id': 'Chip_3_Nozzle_8', 'chip_id': 'Chip_3', 'mean_concentration': 69.57, 'std_concentration': 2.63, 'cv_percent': 3.78, 'accuracy_percent': 15.96, 'n_measurements': 21, 'column_range': '18-24'},
    ]
    
    # Mock standard curve data for plotting
    analyzer.standard_curve_data = pd.DataFrame({
        'fluorescence': [2539792, 1338202, 654337, 338513, 164766, 82937, 40810, 20072],
        'concentration': [600, 300, 150, 75, 37.5, 18.75, 9.375, 4.6875]
    })
    
    analyzer.standard_curve_params = {
        'slope': 0.00023472,
        'intercept': -2.55327080,
        'r_squared': 0.9993
    }
    
    print("Testing multi-chip plotting functionality...")
    print(f"Number of QC results: {len(analyzer.qc_results)}")
    print(f"Number of chips: {len(set(r['chip_id'] for r in analyzer.qc_results))}")
    
    # Generate plots
    success = analyzer.generate_plots(".")
    
    if success:
        print("✅ Multi-chip plots generated successfully!")
        print("Generated files:")
        print("  - standard_curve.png")
        print("  - chip_1_nozzle_performance.png")
        print("  - chip_2_nozzle_performance.png") 
        print("  - chip_3_nozzle_performance.png")
        print("  - all_chips_nozzle_performance.png")
    else:
        print("❌ Failed to generate plots")

if __name__ == "__main__":
    test_multi_chip_plots() 