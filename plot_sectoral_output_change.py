"""
Visualization: Sectoral Output Change under ETS1 and ETS2 Scenarios
Creates a grouped bar chart showing percentage changes relative to baseline (BAU)
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Set publication-quality style
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.size'] = 11
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 14

# File path
results_file = 'results/Italian_CGE_Enhanced_Dynamic_Results_20251019_212648.xlsx'

print("Loading sectoral value-added data...")
# Read Production Value Added sheet
df_raw = pd.read_excel(results_file, sheet_name='Production_Value_Added', header=None)

# Display structure to understand the data
print(f"Sheet shape: {df_raw.shape}")
print("\nFirst few rows:")
print(df_raw.head(4))

# Extract column headers (row 0)
headers = df_raw.iloc[0].tolist()
print(f"\nColumn headers: {headers}")

# Extract scenario labels (row 1)
scenarios = df_raw.iloc[1].tolist()
print(f"\nScenario row: {scenarios}")

# Parse the data structure
# Looking for sectors: Agriculture, Industry, Energy (Elec+Gas+Other), Transport, Services
sectors_mapping = {
    'Agriculture': [],
    'Industry': [],
    'Electricity': [],
    'Gas': [],
    'Other_Energy': [],
    'Road_Transport': [],
    'Rail_Transport': [],
    'Air_Transport': [],
    'Water_Transport': [],
    'Other_Transport': [],
    'Services': []
}

# Find column indices for each sector
for i, header in enumerate(headers):
    if header and 'Agriculture' in str(header):
        sectors_mapping['Agriculture'].append(i)
    elif header and 'Industry' in str(header):
        sectors_mapping['Industry'].append(i)
    elif header and 'Electricity' in str(header):
        sectors_mapping['Electricity'].append(i)
    elif header and 'Gas' in str(header) and 'Other' not in str(header):
        sectors_mapping['Gas'].append(i)
    elif header and 'Other_Energy' in str(header):
        sectors_mapping['Other_Energy'].append(i)
    elif header and 'Road' in str(header):
        sectors_mapping['Road_Transport'].append(i)
    elif header and 'Rail' in str(header):
        sectors_mapping['Rail_Transport'].append(i)
    elif header and 'Air' in str(header):
        sectors_mapping['Air_Transport'].append(i)
    elif header and 'Water' in str(header):
        sectors_mapping['Water_Transport'].append(i)
    elif header and 'Other_Transport' in str(header):
        sectors_mapping['Other_Transport'].append(i)
    elif header and 'Services' in str(header):
        sectors_mapping['Services'].append(i)

print("\nSector column mapping:")
for sector, cols in sectors_mapping.items():
    print(f"  {sector}: columns {cols}")

# Extract 2040 data (last data row)
year_2040_row = df_raw.iloc[-1]  # Last row should be 2040

print(f"\n2040 data row index: {len(df_raw)-1}")

# Function to extract BAU, ETS1, ETS2 values for a sector
def extract_scenario_values(col_indices, row_data):
    """Extract BAU, ETS1, ETS2 values from column group"""
    if not col_indices:
        return None, None, None
    
    col_start = col_indices[0]
    # Pattern: [BAU, spacer, spacer, ETS1, spacer, spacer, ETS2]
    # But we need to check actual scenario labels
    
    # Try to find BAU, ETS1, ETS2 in the next few columns
    bau_val = None
    ets1_val = None
    ets2_val = None
    
    # Check columns starting from col_start
    for offset in range(7):  # Check up to 7 columns ahead
        if col_start + offset < len(scenarios):
            scenario_label = scenarios[col_start + offset]
            value = row_data.iloc[col_start + offset] if col_start + offset < len(row_data) else None
            
            if scenario_label == 'BAU' and bau_val is None:
                bau_val = value
            elif scenario_label == 'ETS1' and ets1_val is None:
                ets1_val = value
            elif scenario_label == 'ETS2' and ets2_val is None:
                ets2_val = value
    
    return bau_val, ets1_val, ets2_val

# Extract 2040 values for each sector
results_2040 = {}
for sector, cols in sectors_mapping.items():
    if cols:
        bau, ets1, ets2 = extract_scenario_values(cols, year_2040_row)
        results_2040[sector] = {
            'BAU': bau,
            'ETS1': ets1,
            'ETS2': ets2
        }
        print(f"\n{sector} 2040 values:")
        print(f"  BAU: {bau}")
        print(f"  ETS1: {ets1}")
        print(f"  ETS2: {ets2}")

# Aggregate sectors as requested
aggregated_data = {
    'Agriculture': results_2040.get('Agriculture', {}),
    'Industry': results_2040.get('Industry', {}),
    'Energy': {},
    'Transport': {},
    'Services': results_2040.get('Services', {})
}

# Aggregate Energy sector (Electricity + Gas + Other Energy)
energy_bau = sum([float(results_2040[s]['BAU']) for s in ['Electricity', 'Gas', 'Other_Energy'] 
                  if s in results_2040 and results_2040[s]['BAU'] is not None and str(results_2040[s]['BAU']) != 'nan'])
energy_ets1 = sum([float(results_2040[s]['ETS1']) for s in ['Electricity', 'Gas', 'Other_Energy'] 
                   if s in results_2040 and results_2040[s]['ETS1'] is not None and str(results_2040[s]['ETS1']) != 'nan'])
energy_ets2 = sum([float(results_2040[s]['ETS2']) for s in ['Electricity', 'Gas', 'Other_Energy'] 
                   if s in results_2040 and results_2040[s]['ETS2'] is not None and str(results_2040[s]['ETS2']) != 'nan'])
aggregated_data['Energy'] = {'BAU': energy_bau, 'ETS1': energy_ets1, 'ETS2': energy_ets2}

# Aggregate Transport sector (all transport subsectors)
transport_sectors = ['Road_Transport', 'Rail_Transport', 'Air_Transport', 'Water_Transport', 'Other_Transport']
transport_bau = sum([float(results_2040[s]['BAU']) for s in transport_sectors 
                     if s in results_2040 and results_2040[s]['BAU'] is not None and str(results_2040[s]['BAU']) != 'nan'])
transport_ets1 = sum([float(results_2040[s]['ETS1']) for s in transport_sectors 
                      if s in results_2040 and results_2040[s]['ETS1'] is not None and str(results_2040[s]['ETS1']) != 'nan'])
transport_ets2 = sum([float(results_2040[s]['ETS2']) for s in transport_sectors 
                      if s in results_2040 and results_2040[s]['ETS2'] is not None and str(results_2040[s]['ETS2']) != 'nan'])
aggregated_data['Transport'] = {'BAU': transport_bau, 'ETS1': transport_ets1, 'ETS2': transport_ets2}

print("\n" + "="*70)
print("AGGREGATED SECTOR DATA (2040):")
print("="*70)
for sector, values in aggregated_data.items():
    print(f"\n{sector}:")
    print(f"  BAU: {values.get('BAU', 'N/A')}")
    print(f"  ETS1: {values.get('ETS1', 'N/A')}")
    print(f"  ETS2: {values.get('ETS2', 'N/A')}")

# Calculate percentage changes relative to BAU
percentage_changes = {}
for sector, values in aggregated_data.items():
    bau = float(values['BAU']) if values.get('BAU') is not None else 0
    ets1 = float(values['ETS1']) if values.get('ETS1') is not None else 0
    ets2 = float(values['ETS2']) if values.get('ETS2') is not None else 0
    
    if bau > 0:
        pct_ets1 = ((ets1 - bau) / bau) * 100
        pct_ets2 = ((ets2 - bau) / bau) * 100
    else:
        pct_ets1 = 0
        pct_ets2 = 0
    
    percentage_changes[sector] = {
        'ETS1': pct_ets1,
        'ETS2': pct_ets2
    }

print("\n" + "="*70)
print("PERCENTAGE CHANGES RELATIVE TO BAU (2040):")
print("="*70)
for sector, changes in percentage_changes.items():
    print(f"{sector:12s}: ETS1 = {changes['ETS1']:6.2f}%, ETS2 = {changes['ETS2']:6.2f}%")

# Prepare data for plotting
sectors = ['Agriculture', 'Industry', 'Energy', 'Transport', 'Services']
ets1_changes = [percentage_changes[s]['ETS1'] for s in sectors]
ets2_changes = [percentage_changes[s]['ETS2'] for s in sectors]

# Create the grouped bar chart
fig, ax = plt.subplots(figsize=(12, 7))

# Set the width of bars and positions
x = np.arange(len(sectors))
width = 0.35

# Create bars
bars1 = ax.bar(x - width/2, ets1_changes, width, label='ETS1 (Industry)', 
               color='#5DADE2', edgecolor='black', linewidth=0.8)
bars2 = ax.bar(x + width/2, ets2_changes, width, label='ETS2 (Buildings & Transport)', 
               color='#27AE60', edgecolor='black', linewidth=0.8)

# Add a horizontal line at y=0
ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8, alpha=0.3)

# Customize the plot
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Output Change Relative to Baseline (%)', fontweight='bold', fontsize=12)
ax.set_title('Sectoral Output Change under ETS1 and ETS2 Scenarios\n(Relative to Baseline, 2040)', 
             fontweight='bold', fontsize=14, pad=20)
ax.set_xticks(x)
ax.set_xticklabels(sectors, fontsize=11)
ax.legend(loc='upper right', frameon=True, shadow=True, fontsize=10)

# Add grid for better readability
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
ax.set_axisbelow(True)

# Add value labels on bars
def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        label_y = height + 0.1 if height >= 0 else height - 0.3
        ax.text(bar.get_x() + bar.get_width()/2., label_y,
                f'{height:.1f}%',
                ha='center', va='bottom' if height >= 0 else 'top', 
                fontsize=9, fontweight='bold')

add_value_labels(bars1)
add_value_labels(bars2)

# Adjust layout
plt.tight_layout()

# Save the figure
output_dir = 'results'
output_file = os.path.join(output_dir, 'Sectoral_Output_Change_ETS_Scenarios.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\n✓ Figure saved: {output_file}")

# Also save as PDF for publication quality
output_file_pdf = os.path.join(output_dir, 'Sectoral_Output_Change_ETS_Scenarios.pdf')
plt.savefig(output_file_pdf, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Figure saved: {output_file_pdf}")

plt.show()

print("\n" + "="*70)
print("VISUALIZATION COMPLETED SUCCESSFULLY")
print("="*70)
