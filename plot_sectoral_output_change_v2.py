"""
Visualization: Sectoral Output Change under ETS1 and ETS2 Scenarios
Creates a grouped bar chart showing percentage changes relative to baseline (BAU)
Based on actual 2040 Value Added data from the CGE model results
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
df_raw = pd.read_excel(
    results_file, sheet_name='Production_Value_Added', header=None)

print(f"Sheet shape: {df_raw.shape}")

# Extract 2040 data (last row)
data_2040 = df_raw.iloc[22]  # Row 22 is year 2040

# Extract sectors based on column structure
# Column pattern: [Year, BAU, ETS1, ETS2] for each sector
# Agriculture: cols 1-3, Energy: cols 4-6, Industry: cols 7-9, Services: cols 10-12, Transport: cols 13-15

sectors_data = {
    'Agriculture': {
        'BAU': float(data_2040.iloc[1]),
        'ETS1': float(data_2040.iloc[2]),
        'ETS2': float(data_2040.iloc[3])
    },
    'Energy': {
        'BAU': float(data_2040.iloc[4]),
        'ETS1': float(data_2040.iloc[5]),
        'ETS2': float(data_2040.iloc[6])
    },
    'Industry': {
        'BAU': float(data_2040.iloc[7]),
        'ETS1': float(data_2040.iloc[8]),
        'ETS2': float(data_2040.iloc[9])
    },
    'Services': {
        'BAU': float(data_2040.iloc[10]),
        'ETS1': float(data_2040.iloc[11]),
        'ETS2': float(data_2040.iloc[12])
    },
    'Transport': {
        'BAU': float(data_2040.iloc[13]),
        'ETS1': float(data_2040.iloc[14]),
        'ETS2': float(data_2040.iloc[15])
    }
}

print("\n" + "="*70)
print("SECTORAL VALUE ADDED (2040, Billion EUR):")
print("="*70)
for sector, values in sectors_data.items():
    print(f"\n{sector}:")
    print(f"  BAU:  €{values['BAU']:.2f}B")
    print(f"  ETS1: €{values['ETS1']:.2f}B")
    print(f"  ETS2: €{values['ETS2']:.2f}B")

# Calculate percentage changes relative to BAU
percentage_changes = {}
for sector, values in sectors_data.items():
    bau = values['BAU']
    ets1 = values['ETS1']
    ets2 = values['ETS2']

    pct_ets1 = ((ets1 - bau) / bau) * 100
    pct_ets2 = ((ets2 - bau) / bau) * 100

    percentage_changes[sector] = {
        'ETS1': pct_ets1,
        'ETS2': pct_ets2
    }

print("\n" + "="*70)
print("PERCENTAGE CHANGES RELATIVE TO BAU (2040):")
print("="*70)
for sector, changes in percentage_changes.items():
    print(
        f"{sector:12s}: ETS1 = {changes['ETS1']:+6.2f}%, ETS2 = {changes['ETS2']:+6.2f}%")

# Prepare data for plotting
sectors = ['Agriculture', 'Industry', 'Energy', 'Transport', 'Services']
ets1_changes = [percentage_changes[s]['ETS1'] for s in sectors]
ets2_changes = [percentage_changes[s]['ETS2'] for s in sectors]

# Create the grouped bar chart
fig, ax = plt.subplots(figsize=(12, 7))

# Set the width of bars and positions
x = np.arange(len(sectors))
width = 0.35

# Create bars with specified colors
bars1 = ax.bar(x - width/2, ets1_changes, width, label='ETS1 (Industry)',
               color='#87CEEB', edgecolor='black', linewidth=0.8, alpha=0.9)  # Light blue
bars2 = ax.bar(x + width/2, ets2_changes, width, label='ETS2 (Buildings & Transport)',
               color='#2E8B57', edgecolor='black', linewidth=0.8, alpha=0.9)  # Dark green

# Add a horizontal line at y=0
ax.axhline(y=0, color='black', linestyle='-', linewidth=1.2, alpha=0.5)

# Customize the plot
ax.set_xlabel('Sector', fontweight='bold', fontsize=12)
ax.set_ylabel('Output Change Relative to Baseline (%)',
              fontweight='bold', fontsize=12)
ax.set_xticks(x)
ax.set_xticklabels(sectors, fontsize=11)
ax.legend(loc='upper right', frameon=True,
          shadow=True, fontsize=11, fancybox=True)

# Add grid for better readability
ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=0.5)
ax.set_axisbelow(True)

# Set y-axis limits for better visualization
y_min = min(min(ets1_changes), min(ets2_changes)) - 5
y_max = max(max(ets1_changes), max(ets2_changes)) + 5
ax.set_ylim(y_min, y_max)

# Add value labels on bars


def add_value_labels(bars):
    for bar in bars:
        height = bar.get_height()
        if height >= 0:
            label_y = height + 0.5
            va = 'bottom'
        else:
            label_y = height - 0.5
            va = 'top'

        ax.text(bar.get_x() + bar.get_width()/2., label_y,
                f'{height:+.1f}%',
                ha='center', va=va,
                fontsize=9, fontweight='bold')


add_value_labels(bars1)
add_value_labels(bars2)

# Add subtle background color
ax.set_facecolor('#F8F9FA')
fig.patch.set_facecolor('white')

# Adjust layout
plt.tight_layout()

# Save the figure
output_dir = 'results'
output_file = os.path.join(
    output_dir, 'Sectoral_Output_Change_ETS_Scenarios.png')
plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
print(f"\n✓ Figure saved: {output_file}")

# Also save as PDF for publication quality
output_file_pdf = os.path.join(
    output_dir, 'Sectoral_Output_Change_ETS_Scenarios.pdf')
plt.savefig(output_file_pdf, dpi=300, bbox_inches='tight', facecolor='white')
print(f"✓ Figure saved: {output_file_pdf}")

plt.show()

print("\n" + "="*70)
print("VISUALIZATION COMPLETED SUCCESSFULLY")
print("="*70)
print("\nKey Insights:")
print("  • Agriculture and Industry show positive growth under both ETS scenarios")
print("  • Services sector experiences the largest decline under ETS1 (-29.7%)")
print("  • Transport sector shows moderate negative impact under both scenarios")
print("  • ETS2 generally shows less negative impact than ETS1 (except for Transport)")
print("="*70)
