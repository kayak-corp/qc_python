import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import stats
import warnings
import argparse
import sys
warnings.filterwarnings('ignore')

class DispenserQCAnalyzerFixedBug:
    def __init__(self):
        self.raw_data = None
        self.standard_concentrations = []
        self.target_concentration = None
        self.standard_curve_data = None
        self.calculated_concentrations = None
        self.qc_results = None
        
    def launch_ui(self):
        """Launch user interface to get inputs"""
        root = tk.Tk()
        root.title("Dispenser QC Analyzer - Multi-Chip Version")
        root.geometry("700x600")
        
        # Create main frame with scrollbar
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # File selection
        tk.Label(scrollable_frame, text="Step 1: Select CSV Data File", font=("Arial", 12, "bold")).pack(pady=10)
        
        file_path = tk.StringVar()
        
        def browse_file():
            filename = filedialog.askopenfilename(
                title="Select CSV file",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if filename:
                file_path.set(filename)
                file_label.config(text=f"Selected: {os.path.basename(filename)}")
        
        tk.Button(scrollable_frame, text="Browse", command=browse_file).pack(pady=5)
        file_label = tk.Label(scrollable_frame, text="No file selected", fg="gray")
        file_label.pack()
        
        # Standard concentrations input
        tk.Label(scrollable_frame, text="\nStep 2: Enter Standard Curve Concentrations", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(scrollable_frame, text="Enter 8 concentrations (comma-separated):").pack()
        
        std_concentrations = tk.StringVar(value="600,300,150,75,37.5,18.75,9.375,4.6875")
        tk.Entry(scrollable_frame, textvariable=std_concentrations, width=50).pack(pady=5)
        
        # Target concentration input
        tk.Label(scrollable_frame, text="\nStep 3: Enter Target Concentration", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(scrollable_frame, text="Expected concentration from dispenser:").pack()
        
        target_conc = tk.StringVar(value="75")
        tk.Entry(scrollable_frame, textvariable=target_conc, width=20).pack(pady=5)
        
        # Chip configuration
        tk.Label(scrollable_frame, text="\nStep 4: Configure Chips", font=("Arial", 12, "bold")).pack(pady=10)
        tk.Label(scrollable_frame, text="Each chip has 8 nozzles. Configure which columns each chip dispenses into:").pack()
        
        # Chip configuration frame
        chip_frame = tk.Frame(scrollable_frame)
        chip_frame.pack(fill=tk.X, pady=5)
        
        # Store chip configurations
        chip_configs = []
        
        def add_chip():
            chip_num = len(chip_configs) + 1
            chip_config = {
                'chip_id': f"Chip_{chip_num}",
                'start_col': tk.StringVar(value="4"),
                'end_col': tk.StringVar(value="24"),
                'frame': None
            }
            chip_configs.append(chip_config)
            create_chip_widget(chip_config)
        
        def remove_chip(chip_config):
            if len(chip_configs) > 1:  # Keep at least one chip
                chip_configs.remove(chip_config)
                chip_config['frame'].destroy()
                # Renumber remaining chips
                for i, config in enumerate(chip_configs):
                    config['chip_id'] = f"Chip_{i+1}"
                    if config['frame']:
                        config['frame'].winfo_children()[0].config(text=config['chip_id'])
        
        def create_chip_widget(chip_config):
            chip_widget_frame = tk.Frame(chip_frame, relief=tk.RAISED, borderwidth=2)
            chip_widget_frame.pack(fill=tk.X, pady=2)
            chip_config['frame'] = chip_widget_frame
            
            chip_header = tk.Frame(chip_widget_frame)
            chip_header.pack(fill=tk.X, padx=5, pady=2)
            
            tk.Label(chip_header, text=chip_config['chip_id'], font=("Arial", 10, "bold")).pack(side=tk.LEFT)
            
            if len(chip_configs) > 1:
                tk.Button(chip_header, text="Remove", command=lambda: remove_chip(chip_config), 
                         bg="red", fg="white", font=("Arial", 8)).pack(side=tk.RIGHT)
            
            chip_content = tk.Frame(chip_widget_frame)
            chip_content.pack(fill=tk.X, padx=10, pady=2)
            
            tk.Label(chip_content, text="Columns:").pack(side=tk.LEFT)
            tk.Entry(chip_content, textvariable=chip_config['start_col'], width=5).pack(side=tk.LEFT, padx=2)
            tk.Label(chip_content, text="to").pack(side=tk.LEFT)
            tk.Entry(chip_content, textvariable=chip_config['end_col'], width=5).pack(side=tk.LEFT, padx=2)
            tk.Label(chip_content, text="(1-24)").pack(side=tk.LEFT, padx=5)
        
        # Add initial chip
        add_chip()
        
        # Add chip button
        tk.Button(scrollable_frame, text="+ Add Another Chip", command=add_chip, 
                 bg="blue", fg="white", font=("Arial", 10)).pack(pady=5)
        
        # Process button
        def process_data():
            try:
                # Get values from UI
                csv_file = file_path.get()
                if not csv_file:
                    messagebox.showerror("Error", "Please select a CSV file")
                    return
                
                # Parse standard concentrations
                std_conc_str = std_concentrations.get()
                self.standard_concentrations = [float(x.strip()) for x in std_conc_str.split(",")]
                
                if len(self.standard_concentrations) != 8:
                    messagebox.showerror("Error", "Please enter exactly 8 standard concentrations")
                    return
                
                # Parse target concentration
                self.target_concentration = float(target_conc.get())
                
                # Parse chip configurations
                self.chip_configurations = []
                for chip_config in chip_configs:
                    try:
                        start_col = int(chip_config['start_col'].get())
                        end_col = int(chip_config['end_col'].get())
                        if start_col < 1 or end_col > 24 or start_col >= end_col:
                            raise ValueError(f"Invalid column range for {chip_config['chip_id']}")
                        self.chip_configurations.append({
                            'chip_id': chip_config['chip_id'],
                            'start_col': start_col - 1,  # Convert to 0-based indexing
                            'end_col': end_col - 1
                        })
                    except ValueError as e:
                        messagebox.showerror("Error", f"Invalid column configuration: {str(e)}")
                        return
                
                # Close UI and process
                root.destroy()
                self.process_qc_analysis(csv_file)
                
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {str(e)}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {str(e)}")
        
        tk.Button(scrollable_frame, text="Process Data", command=process_data, 
                 bg="green", fg="white", font=("Arial", 12, "bold")).pack(pady=20)
        
        # Pack canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        root.mainloop()
    
    def read_csv_manual(self, csv_file):
        """Manual CSV reading for complex files"""
        data = []
        with open(csv_file, 'r', encoding='utf-8') as f:
            for line in f:
                # Split by comma and clean up
                row = [cell.strip().strip('"') for cell in line.split(',')]
                data.append(row)
        
        # Convert to DataFrame
        max_cols = max(len(row) for row in data)
        for row in data:
            while len(row) < max_cols:
                row.append('')
        
        return pd.DataFrame(data)
    
    def load_and_clean_data(self, csv_file):
        """Load and clean the CSV data for Tempest format"""
        try:
            # Read the CSV file manually to handle complex format
            self.raw_data = self.read_csv_manual(csv_file)
            
            print(f"Raw data shape: {self.raw_data.shape}")
            
            # Find the fluorescence data section
            fluorescence_start = None
            for i, row in self.raw_data.iterrows():
                if pd.notna(row[0]) and "Results for Fluorescein" in str(row[0]):
                    fluorescence_start = i + 1
                    break
            
            if fluorescence_start is None:
                raise ValueError("Could not find fluorescence data section")
            
            print(f"Found fluorescence data starting at row {fluorescence_start}")
            
            # Extract fluorescence data (16 rows, 24 columns) - START FROM ROW + 1
            # Row + 0 is the header row, Row + 1 is the actual data
            fluorescence_data = self.raw_data.iloc[fluorescence_start+1:fluorescence_start+17, 1:25].copy()
            
            # Convert to numeric
            for col in fluorescence_data.columns:
                fluorescence_data[col] = pd.to_numeric(fluorescence_data[col], errors='coerce')
            
            self.fluorescence_data = fluorescence_data
            
            # Extract standard curve data from the correct wells
            # STD1-STD8 are in the first 3 columns of every other row (A, C, E, G, I, K, M, O)
            standard_curve_wells = []
            standard_curve_rfu = []
            
            # Map of standard curve wells: A1, A2, A3, C1, C2, C3, E1, E2, E3, etc.
            row_indices = [0, 2, 4, 6, 8, 10, 12, 14]  # A, C, E, G, I, K, M, O
            col_indices = [0, 1, 2]  # Columns 1, 2, 3
            
            for i, row_idx in enumerate(row_indices):
                std_conc = self.standard_concentrations[i]
                for col_idx in col_indices:
                    if row_idx < len(fluorescence_data) and col_idx < len(fluorescence_data.columns):
                        rfu_value = fluorescence_data.iloc[row_idx, col_idx]
                        if pd.notna(rfu_value) and rfu_value > 0:
                            well_id = f"{chr(65+row_idx)}{col_idx+1}"
                            standard_curve_wells.append(well_id)
                            standard_curve_rfu.append(rfu_value)
                            print(f"STD{i+1} well {well_id}: RFU = {rfu_value}, Conc = {std_conc}")
            
            print(f"Found {len(standard_curve_wells)} standard curve wells: {standard_curve_wells}")
            print(f"Standard curve RFU values: {standard_curve_rfu}")
            
            # Create standard curve data using the provided concentrations
            # We need to match concentrations to the wells we found
            if len(standard_curve_rfu) >= 8:
                # Use the first 8 wells (3 wells each for STD1-STD8)
                concentrations = []
                rfu_values = []
                
                for i in range(8):
                    # Get the 3 wells for each standard
                    start_idx = i * 3
                    if start_idx + 2 < len(standard_curve_rfu):
                        # Use median of the 3 wells for each standard (more robust to outliers)
                        median_rfu = np.median(standard_curve_rfu[start_idx:start_idx+3])
                        concentrations.append(self.standard_concentrations[i])
                        rfu_values.append(median_rfu)
                        print(f"STD{i+1} median RFU: {median_rfu}, Concentration: {self.standard_concentrations[i]}")
                
                self.standard_curve_data = pd.DataFrame({
                    'concentration': concentrations,
                    'fluorescence': rfu_values
                })
            else:
                raise ValueError(f"Insufficient standard curve wells found: {len(standard_curve_wells)}")
            
            print(f"Standard curve data: {len(self.standard_curve_data)} points")
            print(f"Standard curve concentrations: {self.standard_curve_data['concentration'].tolist()}")
            print(f"Standard curve RFU values: {self.standard_curve_data['fluorescence'].tolist()}")
            print(f"Fluorescence data shape: {self.fluorescence_data.shape}")
            
            return True
            
        except Exception as e:
            print(f"Error loading data: {str(e)}")
            print("\nTroubleshooting tips:")
            print("1. Check that your CSV file has the correct format")
            print("2. Ensure the file contains 'Results for Fluorescein' section")
            print("3. Verify that standard curve wells (first 3 columns) contain valid data")
            print("4. Check for any special characters or encoding issues")
            return False
    
    def build_standard_curve(self):
        """Perform linear regression to build standard curve"""
        try:
            if len(self.standard_curve_data) < 2:
                raise ValueError("Insufficient standard curve data")
            
            # Check for valid data
            valid_data = self.standard_curve_data.dropna()
            if len(valid_data) < 2:
                raise ValueError("Insufficient valid data after removing NaN values")
            
            # Check for variation in data
            if np.std(valid_data['fluorescence']) == 0:
                raise ValueError("All fluorescence values are the same (no variation)")
            if np.std(valid_data['concentration']) == 0:
                raise ValueError("All concentration values are the same (no variation)")
            
            # Perform linear regression
            x = valid_data['fluorescence'].values
            y = valid_data['concentration'].values
            
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            # Check for reasonable results
            if np.isnan(slope) or np.isnan(intercept):
                raise ValueError("Linear regression produced NaN values")
            
            self.standard_curve_params = {
                'slope': slope,
                'intercept': intercept,
                'r_squared': r_value**2,
                'std_err': std_err
            }
            
            print(f"Standard curve built: y = {slope:.8f}x + {intercept:.8f}")
            print(f"R² = {r_value**2:.4f}")
            
            return True
            
        except Exception as e:
            print(f"Error building standard curve: {str(e)}")
            print("\nTroubleshooting tips:")
            print("1. Check that standard curve data contains numeric values")
            print("2. Ensure there is variation in both concentration and fluorescence values")
            print("3. Verify that the data follows a linear relationship")
            return False
    
    def calculate_concentrations(self):
        """Calculate concentrations for all wells using standard curve"""
        try:
            # Create a copy of fluorescence data for calculations
            self.calculated_concentrations = self.fluorescence_data.copy()
            
            # Apply standard curve to convert fluorescence to concentration
            for row_idx in range(len(self.calculated_concentrations)):
                for col_idx in range(len(self.calculated_concentrations.columns)):
                    fluorescence = self.calculated_concentrations.iloc[row_idx, col_idx]
                    if pd.notna(fluorescence) and fluorescence > 0:
                        # Convert fluorescence to concentration
                        concentration = (fluorescence * self.standard_curve_params['slope'] + 
                                      self.standard_curve_params['intercept'])
                        self.calculated_concentrations.iloc[row_idx, col_idx] = concentration
            
            print("Concentrations calculated for all wells")
            return True
            
        except Exception as e:
            print(f"Error calculating concentrations: {str(e)}")
            return False
    
    def calculate_qc_metrics(self):
        """Calculate %CV and %Accuracy for each chip and nozzle - Multi-chip version"""
        try:
            self.qc_results = []
            
            # Check if we have chip configurations from GUI, otherwise use default
            if not hasattr(self, 'chip_configurations'):
                # Default configuration: single chip covering columns 4-24
                self.chip_configurations = [{
                    'chip_id': 'Chip_1',
                    'start_col': 3,  # 0-based indexing for columns 4-24
                    'end_col': 23
                }]
            
            for chip_config in self.chip_configurations:
                chip_id = chip_config['chip_id']
                start_col = chip_config['start_col']
                end_col = chip_config['end_col']
                
                # Each chip has 8 nozzles (16 rows total, 2 rows per nozzle)
                # For chip columns (4-24): Each nozzle uses 2 consecutive rows
                # Nozzle 1 = Row A & B, Nozzle 2 = Row C & D, etc.
                nozzle_groups = []
                for i in range(0, 16, 2):  # 8 nozzles, 2 rows each
                    nozzle_groups.append({
                        'nozzle_id': f"{chip_id}_Nozzle_{i//2 + 1}",
                        'rows': [i, i + 1]  # Use 2 rows per nozzle (e.g., A & B for Nozzle 1)
                    })
                
                for group in nozzle_groups:
                    # Extract data for this nozzle from the chip's column range
                    nozzle_data = []
                    for row_idx in group['rows']:
                        if row_idx < len(self.calculated_concentrations):
                            # Get data from the chip's assigned columns
                            chip_data = self.calculated_concentrations.iloc[row_idx, start_col:end_col+1].dropna()
                            nozzle_data.extend(chip_data.values)
                    
                    if len(nozzle_data) > 0:
                        # Calculate metrics
                        mean_conc = np.mean(nozzle_data)
                        std_conc = np.std(nozzle_data)
                        
                        # %CV = (std_dev / mean) * 100
                        cv_percent = (std_conc / mean_conc) * 100 if mean_conc != 0 else 0
                        
                        # %Accuracy = ((mean - target) / target) * 100
                        accuracy_percent = ((mean_conc - self.target_concentration) / self.target_concentration) * 100
                        
                        # Debug output
                        col_range = f"columns {start_col+1}-{end_col+1}"
                        print(f"{group['nozzle_id']}: Using {len(nozzle_data)} measurements from {col_range}")
                        print(f"  Mean: {mean_conc:.2f}, Std: {std_conc:.2f}, CV: {cv_percent:.2f}%, Accuracy: {accuracy_percent:.2f}%")
                        
                        self.qc_results.append({
                            'nozzle_id': group['nozzle_id'],
                            'chip_id': chip_id,
                            'mean_concentration': mean_conc,
                            'std_concentration': std_conc,
                            'cv_percent': cv_percent,
                            'accuracy_percent': accuracy_percent,
                            'n_measurements': len(nozzle_data),
                            'column_range': f"{start_col+1}-{end_col+1}"
                        })
            
            print(f"QC metrics calculated for {len(self.qc_results)} nozzles across {len(self.chip_configurations)} chips")
            return True
            
        except Exception as e:
            print(f"Error calculating QC metrics: {str(e)}")
            return False
    
    def generate_plots(self, output_dir):
        """Generate visualization plots"""
        try:
            # Create plots directory
            plots_dir = Path(output_dir) / "plots"
            plots_dir.mkdir(exist_ok=True)
            
            # 1. Standard curve plot
            plt.figure(figsize=(10, 6))
            plt.scatter(self.standard_curve_data['fluorescence'], 
                       self.standard_curve_data['concentration'], 
                       color='blue', s=100, label='Data points')
            
            # Add regression line
            x_range = np.linspace(self.standard_curve_data['fluorescence'].min(), 
                                 self.standard_curve_data['fluorescence'].max(), 100)
            y_pred = x_range * self.standard_curve_params['slope'] + self.standard_curve_params['intercept']
            plt.plot(x_range, y_pred, 'r-', label=f'R² = {self.standard_curve_params["r_squared"]:.4f}')
            
            # Add equation text to the plot
            equation_text = f'y = {self.standard_curve_params["slope"]:.8f}x + {self.standard_curve_params["intercept"]:.8f}'
            plt.text(0.05, 0.95, f'Equation: {equation_text}', 
                    transform=plt.gca().transAxes, fontsize=12, 
                    verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            plt.xlabel('Fluorescence (RFU)')
            plt.ylabel('Concentration')
            plt.title('Standard Curve')
            plt.legend()
            plt.grid(True, alpha=0.3)
            plt.savefig(plots_dir / 'standard_curve.png', dpi=300, bbox_inches='tight')
            plt.close()
            
            # 2. Nozzle performance plots - separate plot for each chip
            if self.qc_results:
                # Group results by chip
                chip_results = {}
                for result in self.qc_results:
                    chip_id = result['chip_id']
                    if chip_id not in chip_results:
                        chip_results[chip_id] = []
                    chip_results[chip_id].append(result)
                
                # Create separate plots for each chip
                for chip_id, chip_data in chip_results.items():
                    nozzle_ids = [r['nozzle_id'].split('_Nozzle_')[1] for r in chip_data]  # Just the nozzle number
                    cv_values = [r['cv_percent'] for r in chip_data]
                    accuracy_values = [r['accuracy_percent'] for r in chip_data]
                    
                    # Calculate chip averages
                    chip_mean_cv = np.mean(cv_values)
                    chip_mean_accuracy = np.mean(accuracy_values)
                    
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                    
                    # CV plot
                    bars1 = ax1.bar(nozzle_ids, cv_values, color='skyblue')
                    ax1.set_ylabel('%CV')
                    ax1.set_title(f'{chip_id} - Nozzle Precision (%CV)')
                    ax1.grid(True, alpha=0.3)
                    
                    # Add value labels on bars
                    for bar, value in zip(bars1, cv_values):
                        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                                f'{value:.1f}%', ha='center', va='bottom')
                    
                    # Add chip average line
                    ax1.axhline(y=chip_mean_cv, color='red', linestyle='--', linewidth=2, label=f'Chip Average: {chip_mean_cv:.1f}%')
                    ax1.legend()
                    
                    # Accuracy plot
                    bars2 = ax2.bar(nozzle_ids, accuracy_values, color='lightcoral')
                    ax2.set_ylabel('%Accuracy')
                    ax2.set_title(f'{chip_id} - Nozzle Accuracy (%Accuracy)')
                    ax2.grid(True, alpha=0.3)
                    
                    # Add value labels on bars
                    for bar, value in zip(bars2, accuracy_values):
                        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                                f'{value:.1f}%', ha='center', va='bottom')
                    
                    # Add chip average line
                    ax2.axhline(y=chip_mean_accuracy, color='red', linestyle='--', linewidth=2, label=f'Chip Average: {chip_mean_accuracy:.1f}%')
                    ax2.legend()
                    
                    plt.tight_layout()
                    # Create filename with chip name
                    chip_filename = chip_id.lower().replace(' ', '_').replace('-', '_')
                    plt.savefig(plots_dir / f'{chip_filename}_nozzle_performance.png', dpi=300, bbox_inches='tight')
                    plt.close()
                
                # Also create a combined plot for all chips (optional)
                if len(chip_results) > 1:
                    all_nozzle_ids = [r['nozzle_id'] for r in self.qc_results]
                    all_cv_values = [r['cv_percent'] for r in self.qc_results]
                    all_accuracy_values = [r['accuracy_percent'] for r in self.qc_results]
                    
                    # Calculate overall averages
                    overall_mean_cv = np.mean(all_cv_values)
                    overall_mean_accuracy = np.mean(all_accuracy_values)
                    
                    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 6))
                    
                    # CV plot
                    bars1 = ax1.bar(all_nozzle_ids, all_cv_values, color='skyblue')
                    ax1.set_ylabel('%CV')
                    ax1.set_title('All Chips - Nozzle Precision (%CV)')
                    ax1.grid(True, alpha=0.3)
                    ax1.tick_params(axis='x', rotation=45)
                    
                    # Add value labels on bars
                    for bar, value in zip(bars1, all_cv_values):
                        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                                f'{value:.1f}%', ha='center', va='bottom')
                    
                    # Add overall average line
                    ax1.axhline(y=overall_mean_cv, color='red', linestyle='--', linewidth=2, label=f'Overall Average: {overall_mean_cv:.1f}%')
                    ax1.legend()
                    
                    # Accuracy plot
                    bars2 = ax2.bar(all_nozzle_ids, all_accuracy_values, color='lightcoral')
                    ax2.set_ylabel('%Accuracy')
                    ax2.set_title('All Chips - Nozzle Accuracy (%Accuracy)')
                    ax2.grid(True, alpha=0.3)
                    ax2.tick_params(axis='x', rotation=45)
                    
                    # Add value labels on bars
                    for bar, value in zip(bars2, all_accuracy_values):
                        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
                                f'{value:.1f}%', ha='center', va='bottom')
                    
                    # Add overall average line
                    ax2.axhline(y=overall_mean_accuracy, color='red', linestyle='--', linewidth=2, label=f'Overall Average: {overall_mean_accuracy:.1f}%')
                    ax2.legend()
                    
                    plt.tight_layout()
                    plt.savefig(plots_dir / 'all_chips_nozzle_performance.png', dpi=300, bbox_inches='tight')
                    plt.close()
            
            print(f"Plots saved to: {plots_dir}")
            return True
            
        except Exception as e:
            print(f"Error generating plots: {str(e)}")
            return False
    
    def generate_output_file(self, input_file):
        """Generate the final output CSV file"""
        try:
            # Create output filename
            input_path = Path(input_file)
            output_file = input_path.parent / f"{input_path.stem}_processed.csv"
            
            # Create output data
            output_data = []
            
            # Add calculated concentrations (include ALL columns for reference)
            for row_idx in range(len(self.calculated_concentrations)):
                row_data = [f"Row_{chr(65 + row_idx)}"]  # A, B, C, etc.
                for col_idx in range(len(self.calculated_concentrations.columns)):
                    val = self.calculated_concentrations.iloc[row_idx, col_idx]
                    if pd.notna(val):
                        row_data.append(f"{val:.6f}")
                    else:
                        row_data.append("")
                output_data.append(row_data)
            
            # Add empty row
            output_data.append([""] * (len(self.calculated_concentrations.columns) + 1))
            
            # Add QC results
            output_data.append(["QC Results", "Chip", "Nozzle", "Mean Conc", "Std Dev", "%CV", "%Accuracy", "N", "Columns"])
            
            # Group results by chip to calculate averages
            chip_results = {}
            for result in self.qc_results:
                chip_id = result['chip_id']
                if chip_id not in chip_results:
                    chip_results[chip_id] = []
                chip_results[chip_id].append(result)
            
            for result in self.qc_results:
                # Parse chip and nozzle from nozzle_id
                nozzle_id = result['nozzle_id']
                if '_Nozzle_' in nozzle_id:
                    chip_part, nozzle_part = nozzle_id.split('_Nozzle_')
                    chip_name = chip_part
                    nozzle_name = f"Nozzle_{nozzle_part}"
                else:
                    chip_name = "N/A"
                    nozzle_name = nozzle_id
                
                output_data.append([
                    "",  # Empty cell for "QC Results" column
                    chip_name,
                    nozzle_name,
                    f"{result['mean_concentration']:.6f}",
                    f"{result['std_concentration']:.6f}",
                    f"{result['cv_percent']:.2f}%",
                    f"{result['accuracy_percent']:.2f}%",
                    result['n_measurements'],
                    f"Cols {result.get('column_range', 'N/A')}"  # Use "Cols" prefix to prevent date conversion
                ])
            
            # Add chip average rows
            for chip_id, chip_data in chip_results.items():
                chip_cv_values = [r['cv_percent'] for r in chip_data]
                chip_accuracy_values = [r['accuracy_percent'] for r in chip_data]
                chip_mean_cv = np.mean(chip_cv_values)
                chip_mean_accuracy = np.mean(chip_accuracy_values)
                chip_total_measurements = sum(r['n_measurements'] for r in chip_data)
                
                output_data.append([
                    "",  # Empty cell for "QC Results" column
                    chip_id,
                    "CHIP_AVERAGE",
                    "",  # No mean concentration for chip average
                    "",  # No std dev for chip average
                    f"{chip_mean_cv:.2f}%",
                    f"{chip_mean_accuracy:.2f}%",
                    chip_total_measurements,
                    f"Cols {chip_data[0].get('column_range', 'N/A')}"  # Use first nozzle's column range
                ])
            
            # Add summary statistics
            output_data.append([""])
            output_data.append(["Summary Statistics"])
            all_cv = [r['cv_percent'] for r in self.qc_results]
            all_accuracy = [r['accuracy_percent'] for r in self.qc_results]
            
            output_data.append(["Average %CV", f"{np.mean(all_cv):.2f}%"])
            output_data.append(["Average %Accuracy", f"{np.mean(all_accuracy):.2f}%"])
            output_data.append(["Standard Curve R²", f"{self.standard_curve_params['r_squared']:.4f}"])
            output_data.append(["Linear Regression Equation", f"y = {self.standard_curve_params['slope']:.8f}x + {self.standard_curve_params['intercept']:.8f}"])
            output_data.append(["Best %CV", f"{min(all_cv):.2f}%"])
            output_data.append(["Worst %CV", f"{max(all_cv):.2f}%"])
            output_data.append(["", ""])
            output_data.append(["Note", "QC calculations exclude standard curve wells (columns 1-3). Each nozzle uses 2 rows (e.g., Nozzle 1 = Row A & B)"])
            
            # Save to CSV
            output_df = pd.DataFrame(output_data)
            output_df.to_csv(output_file, index=False, header=False)
            
            print(f"Output file saved: {output_file}")
            return str(output_file)
            
        except Exception as e:
            print(f"Error generating output file: {str(e)}")
            return None
    
    def process_qc_analysis(self, csv_file, generate_plots=True):
        """Main processing workflow"""
        print("Starting Dispenser QC Analysis (Fixed Bug Version)...")
        print("=" * 50)
        
        # Step 1: Load and clean data
        print("Step 1: Loading and cleaning data...")
        if not self.load_and_clean_data(csv_file):
            print("Failed to load data")
            return False
        
        # Step 2: Build standard curve
        print("Step 2: Building standard curve...")
        if not self.build_standard_curve():
            print("Failed to build standard curve")
            return False
        
        # Step 3: Calculate concentrations
        print("Step 3: Calculating concentrations...")
        if not self.calculate_concentrations():
            print("Failed to calculate concentrations")
            return False
        
        # Step 4: Calculate QC metrics
        print("Step 4: Calculating QC metrics...")
        if not self.calculate_qc_metrics():
            print("Failed to calculate QC metrics")
            return False
        
        # Step 5: Generate output file
        print("Step 5: Generating output file...")
        output_file = self.generate_output_file(csv_file)
        if not output_file:
            print("Failed to generate output file")
            return False
        
        # Step 6: Generate plots (optional)
        if generate_plots:
            print("Step 6: Generating plots...")
            self.generate_plots(Path(csv_file).parent)
        
        # Display summary
        self.display_summary()
        
        return True
    
    def display_summary(self):
        """Display a summary of the results"""
        print("\n" + "=" * 50)
        print("QC ANALYSIS SUMMARY")
        print("=" * 50)
        
        print(f"Standard Curve R²: {self.standard_curve_params['r_squared']:.4f}")
        print(f"Target Concentration: {self.target_concentration}")
        print("\nNozzle Performance:")
        print("-" * 70)
        
        # Group results by chip
        chip_results = {}
        for result in self.qc_results:
            chip_id = result.get('chip_id', 'Unknown')
            if chip_id not in chip_results:
                chip_results[chip_id] = []
            chip_results[chip_id].append(result)
        
        for chip_id, results in chip_results.items():
            print(f"\n{chip_id}:")
            for result in results:
                nozzle_id = result['nozzle_id']
                if '_Nozzle_' in nozzle_id:
                    nozzle_name = nozzle_id.split('_Nozzle_')[1]
                else:
                    nozzle_name = nozzle_id
                
                print(f"  {nozzle_name:8} | "
                      f"CV: {result['cv_percent']:6.2f}% | "
                      f"Accuracy: {result['accuracy_percent']:8.2f}% | "
                      f"N: {result['n_measurements']:3d} | "
                      f"Cols: {result.get('column_range', 'N/A')}")
        
        # Calculate overall statistics
        all_cv = [r['cv_percent'] for r in self.qc_results]
        all_accuracy = [r['accuracy_percent'] for r in self.qc_results]
        
        print("\nOverall Statistics:")
        print(f"Average %CV: {np.mean(all_cv):.2f}%")
        print(f"Average %Accuracy: {np.mean(all_accuracy):.2f}%")
        print(f"Best %CV: {min(all_cv):.2f}%")
        print(f"Worst %CV: {max(all_cv):.2f}%")
        print(f"Linear Regression: y = {self.standard_curve_params['slope']:.8f}x + {self.standard_curve_params['intercept']:.8f}")
        
        # Quality assessment
        print("\nQuality Assessment:")
        if np.mean(all_cv) < 5.0:
            print("✓ Precision: EXCELLENT (Average %CV < 5%)")
        elif np.mean(all_cv) < 10.0:
            print("✓ Precision: GOOD (Average %CV < 10%)")
        else:
            print("⚠ Precision: NEEDS IMPROVEMENT (Average %CV ≥ 10%)")
        
        if abs(np.mean(all_accuracy)) < 10.0:
            print("✓ Accuracy: EXCELLENT (Average %Accuracy < ±10%)")
        elif abs(np.mean(all_accuracy)) < 20.0:
            print("✓ Accuracy: GOOD (Average %Accuracy < ±20%)")
        else:
            print("⚠ Accuracy: NEEDS IMPROVEMENT (Average %Accuracy ≥ ±20%)")
        
        print("\nIMPORTANT: QC calculations exclude standard curve wells (columns 1-3)")

def main():
    """Main function to run the analyzer"""
    parser = argparse.ArgumentParser(description='Dispenser QC Analyzer - Fixed Bug Version')
    parser.add_argument('--file', '-f', help='CSV file to analyze')
    parser.add_argument('--concentrations', '-c', 
                       default='600,300,150,75,37.5,18.75,9.375,4.6875',
                       help='Standard curve concentrations (comma-separated)')
    parser.add_argument('--target', '-t', type=float, default=75.0,
                       help='Target concentration')
    parser.add_argument('--no-plots', action='store_true',
                       help='Skip generating plots')
    
    args = parser.parse_args()
    
    analyzer = DispenserQCAnalyzerFixedBug()
    
    if args.file:
        # Command line mode
        try:
            analyzer.standard_concentrations = [float(x.strip()) for x in args.concentrations.split(",")]
            analyzer.target_concentration = args.target
            
            success = analyzer.process_qc_analysis(args.file, generate_plots=not args.no_plots)
            if success:
                print("\nAnalysis completed successfully!")
            else:
                print("\nAnalysis failed!")
                sys.exit(1)
                
        except Exception as e:
            print(f"Error: {str(e)}")
            sys.exit(1)
    else:
        # GUI mode
        analyzer.launch_ui()

if __name__ == "__main__":
    main() 