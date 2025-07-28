import pandas as pd
import numpy as np

# Simulate the calculated concentrations data
# 16 rows (A-P), 24 columns (1-24)
np.random.seed(42)
data = np.random.rand(16, 24) * 100 + 50  # Random concentrations between 50-150
calculated_concentrations = pd.DataFrame(data)

print("Simulated data shape:", calculated_concentrations.shape)
print("Columns 1-24, Rows A-P")

# Test different chip configurations
test_configs = [
    {
        'chip_id': 'Chip_1',
        'start_col': 3,  # Columns 4-10 (0-based: 3-9)
        'end_col': 9
    },
    {
        'chip_id': 'Chip_2', 
        'start_col': 10,  # Columns 11-17 (0-based: 10-16)
        'end_col': 16
    },
    {
        'chip_id': 'Chip_3',
        'start_col': 17,  # Columns 18-24 (0-based: 17-23)
        'end_col': 23
    }
]

print("\n" + "="*60)
print("TESTING CHIP COLUMN ASSIGNMENTS")
print("="*60)

for chip_config in test_configs:
    chip_id = chip_config['chip_id']
    start_col = chip_config['start_col']
    end_col = chip_config['end_col']
    
    print(f"\n{chip_id}: Columns {start_col+1}-{end_col+1}")
    print("-" * 40)
    
    # Each chip has 8 nozzles (16 rows total, 2 rows per nozzle)
    nozzle_groups = []
    for i in range(0, 16, 2):  # 16 rows, 8 nozzles
        nozzle_groups.append({
            'nozzle_id': f"{chip_id}_Nozzle_{i//2 + 1}",
            'rows': [i, i + 1]
        })
    
    for group in nozzle_groups:
        # Extract data for this nozzle from the chip's column range
        nozzle_data = []
        for row_idx in group['rows']:
            if row_idx < len(calculated_concentrations):
                # Get data from the chip's assigned columns
                chip_data = calculated_concentrations.iloc[row_idx, start_col:end_col+1].dropna()
                nozzle_data.extend(chip_data.values)
        
        if len(nozzle_data) > 0:
            mean_conc = np.mean(nozzle_data)
            std_conc = np.std(nozzle_data)
            cv_percent = (std_conc / mean_conc) * 100 if mean_conc != 0 else 0
            
            print(f"{group['nozzle_id']}: {len(nozzle_data)} measurements")
            print(f"  Mean: {mean_conc:.2f}, Std: {std_conc:.2f}, CV: {cv_percent:.2f}%")
            print(f"  Data range: {min(nozzle_data):.1f} - {max(nozzle_data):.1f}")

print("\n" + "="*60)
print("EXPECTED BEHAVIOR:")
print("="*60)
print("• Chip_1 (cols 4-10): Each nozzle uses 7 columns × 2 rows = 14 measurements")
print("• Chip_2 (cols 11-17): Each nozzle uses 7 columns × 2 rows = 14 measurements") 
print("• Chip_3 (cols 18-24): Each nozzle uses 7 columns × 2 rows = 14 measurements")
print("• Total: 3 chips × 8 nozzles × 14 measurements = 336 total measurements")
print("• Each nozzle only uses its assigned column range") 