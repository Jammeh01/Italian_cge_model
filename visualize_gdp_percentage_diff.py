"""
Visualization of GDP Percentage Difference from BAU
Single graph without title, custom time steps
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from pathlib import Path

# Find the latest results file
results_dir = Path('results')
result_files = list(results_dir.glob(
    'Italian_CGE_Enhanced_Dynamic_Results_*.xlsx'))

if not result_files:
    raise FileNotFoundError(
        "No results file found. Please run the simulation first.")

latest_file = max(result_files, key=os.path.getctime)
print(f"Loading data from: {latest_file.name}\n")

# Load the Macroeconomy_GDP sheet - read raw to understand structure
df_raw = pd.read_excel(latest_file, sheet_name='Macroeconomy_GDP', header=None)

# Excel structure:
# Row 0: Metric names (with NaN for some columns)
# Row 1: "Scenario", then BAU, ..., ETS1, ..., ETS2
# Row 2: "Year"
# Row 3+: Data rows

scenario_row_idx = 1
metric_row_idx = 0
data_start_row = 3

# Get the scenario and metric rows
scenario_row = df_raw.iloc[scenario_row_idx]
metric_row = df_raw.iloc[metric_row_idx]

# Find column indices for each scenario
bau_cols = [i for i, val in enumerate(scenario_row) if val == 'BAU']
ets1_cols = [i for i, val in enumerate(scenario_row) if val == 'ETS1']
ets2_cols = [i for i, val in enumerate(scenario_row) if val == 'ETS2']

# Find the BAU GDP column and calculate its offset
bau_gdp_col = None
bau_gdp_offset = None

for idx, col in enumerate(bau_cols):
    metric_name = str(metric_row.iloc[col]).strip()
    if 'Real_GDP_Total_Billion_EUR' in metric_name or metric_name == 'Real_GDP_Total_Billion_EUR':
        bau_gdp_col = col
        bau_gdp_offset = idx
        break

# Apply same offset to ETS1 and ETS2
ets1_gdp_col = ets1_cols[bau_gdp_offset] if bau_gdp_offset is not None and bau_gdp_offset < len(
    ets1_cols) else None
ets2_gdp_col = ets2_cols[bau_gdp_offset] if bau_gdp_offset is not None and bau_gdp_offset < len(
    ets2_cols) else None

# Find year column
year_col = None
for i, val in enumerate(scenario_row):
    if val == 'Year':
        year_col = i
        break

if year_col is None:
    year_col = 0

# Extract data
years = []
bau_gdp_values = []
ets1_gdp_values = []
ets2_gdp_values = []

for idx in range(data_start_row, len(df_raw)):
    year_val = df_raw.iloc[idx, year_col]

    if pd.isna(year_val):
        break

    try:
        year = int(float(year_val))
        years.append(year)

        if bau_gdp_col is not None:
            bau_val = df_raw.iloc[idx, bau_gdp_col]
            bau_gdp_values.append(
                float(bau_val) if pd.notna(bau_val) else None)

        if ets1_gdp_col is not None:
            ets1_val = df_raw.iloc[idx, ets1_gdp_col]
            ets1_gdp_values.append(
                float(ets1_val) if pd.notna(ets1_val) else None)

        if ets2_gdp_col is not None:
            ets2_val = df_raw.iloc[idx, ets2_gdp_col]
            ets2_gdp_values.append(
                float(ets2_val) if pd.notna(ets2_val) else None)
    except (ValueError, TypeError):
        break

# Create dataframes
bau_data = pd.DataFrame(
    {'Year': years, 'Real_GDP_Total_Billion_EUR': bau_gdp_values})
ets1_data = pd.DataFrame(
    {'Year': years, 'Real_GDP_Total_Billion_EUR': ets1_gdp_values})
ets2_data = pd.DataFrame(
    {'Year': years, 'Real_GDP_Total_Billion_EUR': ets2_gdp_values})

# Remove rows with None values and sort
bau_data = bau_data.dropna().sort_values('Year').reset_index(drop=True)
ets1_data = ets1_data.dropna().sort_values('Year').reset_index(drop=True)
ets2_data = ets2_data.dropna().sort_values('Year').reset_index(drop=True)

print(f"BAU data points: {len(bau_data)}")
print(f"ETS1 data points: {len(ets1_data)}")
print(f"ETS2 data points: {len(ets2_data)}\n")

# Calculate percentage differences from BAU
# Merge datasets on Year
ets1_merged = pd.merge(ets1_data, bau_data, on='Year',
                       suffixes=('_ETS1', '_BAU'))
ets2_merged = pd.merge(ets2_data, bau_data, on='Year',
                       suffixes=('_ETS2', '_BAU'))

ets1_merged['Pct_Diff'] = ((ets1_merged['Real_GDP_Total_Billion_EUR_ETS1'] -
                            ets1_merged['Real_GDP_Total_Billion_EUR_BAU']) /
                           ets1_merged['Real_GDP_Total_Billion_EUR_BAU']) * 100

ets2_merged['Pct_Diff'] = ((ets2_merged['Real_GDP_Total_Billion_EUR_ETS2'] -
                            ets2_merged['Real_GDP_Total_Billion_EUR_BAU']) /
                           ets2_merged['Real_GDP_Total_Billion_EUR_BAU']) * 100

# Create visualization
fig, ax = plt.subplots(figsize=(14, 6))
fig.patch.set_facecolor('#E8E9F0')
ax.set_facecolor('#E8E9F0')

# Plot smooth lines without markers
ax.plot(ets1_merged['Year'], ets1_merged['Pct_Diff'],
        color='#C75146', linewidth=2.5, label='ETS1 vs BAU')
ax.plot(ets2_merged['Year'], ets2_merged['Pct_Diff'],
        color='#E8A13A', linewidth=2.5, label='ETS2 vs BAU')

# Add zero reference line
ax.axhline(y=0, color='#4A4A4A', linestyle='--', linewidth=1.2, alpha=0.6)

# Set custom x-axis ticks
ax.set_xticks([2020, 2025, 2030, 2035, 2040])
ax.set_xlim(2020, 2040)

# Formatting
ax.set_xlabel('Year', fontsize=13, fontweight='normal')
ax.set_ylabel('GDP Difference (%)', fontsize=13, fontweight='normal')
ax.legend(loc='upper left', fontsize=11, framealpha=0.95, edgecolor='gray')
ax.grid(True, alpha=0.25, linestyle='-', linewidth=0.5, color='white')
ax.tick_params(labelsize=11)

# Add summary statistics box
bau_2040 = bau_data[bau_data['Year'] ==
                    2040]['Real_GDP_Total_Billion_EUR'].values[0]
ets1_2040 = ets1_merged[ets1_merged['Year'] ==
                        2040]['Real_GDP_Total_Billion_EUR_ETS1'].values[0]
ets2_2040 = ets2_merged[ets2_merged['Year'] ==
                        2040]['Real_GDP_Total_Billion_EUR_ETS2'].values[0]
ets1_pct_2040 = ets1_merged[ets1_merged['Year'] == 2040]['Pct_Diff'].values[0]
ets2_pct_2040 = ets2_merged[ets2_merged['Year'] == 2040]['Pct_Diff'].values[0]

summary_text = f"Summary Statistics (2040):\n"
summary_text += f"ETS1: €{ets1_2040:.0f}B ({ets1_pct_2040:.2f}%)\n"
summary_text += f"ETS2: €{ets2_2040:.0f}B ({ets2_pct_2040:.2f}%)\n"
summary_text += f"BAU: €{bau_2040:.0f}B"

# Add text box with summary statistics
props = dict(boxstyle='round', facecolor='#D4D4C8',
             alpha=0.9, edgecolor='gray', linewidth=1)
ax.text(0.05, 0.05, summary_text, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', bbox=props, family='monospace')

plt.tight_layout()

# Save figure
output_dir = Path('figures')
output_dir.mkdir(exist_ok=True)

png_path = output_dir / 'GDP_Percentage_Difference.png'
pdf_path = output_dir / 'GDP_Percentage_Difference.pdf'

plt.savefig(png_path, dpi=300, bbox_inches='tight', facecolor='#E8E9F0')
plt.savefig(pdf_path, bbox_inches='tight', facecolor='#E8E9F0')

print(f"✓ Figure saved: {png_path}")
print(f"✓ PDF saved: {pdf_path}")

plt.close()
