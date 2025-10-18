"""
Visualize Real GDP Evolution by Scenario (2021-2040)
Shows GDP evolution across BAU, ETS1, and ETS2 scenarios
with percentage differences from baseline
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Find the most recent results file
results_dir = Path('results')
excel_files = list(results_dir.glob(
    'Italian_CGE_Enhanced_Dynamic_Results_*.xlsx'))

if not excel_files:
    print("No results files found!")
    exit(1)

# Get the most recent file
latest_file = max(excel_files, key=lambda p: p.stat().st_mtime)
print(f"Loading data from: {latest_file.name}")

# Load the Macroeconomy_GDP sheet - read raw to understand structure
df_raw = pd.read_excel(latest_file, sheet_name='Macroeconomy_GDP', header=None)

print("\nRaw structure (first 10 rows, first 10 columns):")
print(df_raw.iloc[:10, :10])

# Based on the structure:
# Row 0: Empty, then metric name headers
# Row 1: "Scenario", then BAU, ..., ETS1, ..., ETS2
# Row 2: "Year", then empty cells
# Row 3+: Year values (2021, 2022, etc.) with corresponding data

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

print(f"\nBAU columns: {bau_cols}")
print(f"ETS1 columns: {ets1_cols}")
print(f"ETS2 columns: {ets2_cols}")

# Print metric names for each scenario's columns
print("\nMetric names by scenario:")
for col in bau_cols:
    print(f"  BAU column {col}: {metric_row.iloc[col]}")
for col in ets1_cols:
    print(f"  ETS1 column {col}: {metric_row.iloc[col]}")
for col in ets2_cols:
    print(f"  ETS2 column {col}: {metric_row.iloc[col]}")

# Find the specific column with Real_GDP_Total_Billion_EUR for each scenario
# Since metric names are NaN for ETS1/ETS2, assume same structure as BAU
bau_gdp_col = None
bau_gdp_offset = None

# First find the BAU GDP column and calculate its offset within BAU columns
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

print(
    f"\nGDP columns - BAU: {bau_gdp_col}, ETS1: {ets1_gdp_col}, ETS2: {ets2_gdp_col}")
print(f"BAU GDP offset within BAU columns: {bau_gdp_offset}")

# Find year column
year_col = None
for i, val in enumerate(scenario_row):
    if val == 'Year':
        year_col = i
        break

if year_col is None:
    year_col = 0  # Default to first column

print(f"Year column: {year_col}")

# Extract data starting from row 3
years = []
bau_gdp_values = []
ets1_gdp_values = []
ets2_gdp_values = []

for idx in range(data_start_row, len(df_raw)):
    year_val = df_raw.iloc[idx, year_col]

    # Stop if we hit NaN or non-numeric year
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

print(
    f"\nExtracted {len(years)} years: {years[:5] if years else 'None'}...{years[-3:] if len(years) > 3 else years}")
print(f"BAU GDP values (first 5): {bau_gdp_values[:5]}")
print(f"ETS1 GDP values (first 5): {ets1_gdp_values[:5]}")
print(f"ETS2 GDP values (first 5): {ets2_gdp_values[:5]}")

# Create dataframes
bau_data = pd.DataFrame(
    {'Year': years, 'Real_GDP_Total_Billion_EUR': bau_gdp_values})
ets1_data = pd.DataFrame(
    {'Year': years, 'Real_GDP_Total_Billion_EUR': ets1_gdp_values})
ets2_data = pd.DataFrame(
    {'Year': years, 'Real_GDP_Total_Billion_EUR': ets2_gdp_values})

# Remove rows with None values
bau_data = bau_data.dropna()
ets1_data = ets1_data.dropna()
ets2_data = ets2_data.dropna()

# Sort by year
bau_data = bau_data.sort_values('Year').reset_index(drop=True)
ets1_data = ets1_data.sort_values('Year').reset_index(drop=True)
ets2_data = ets2_data.sort_values('Year').reset_index(drop=True)

print(f"\nBAU data points: {len(bau_data)}")
print(f"ETS1 data points: {len(ets1_data)}")
print(f"ETS2 data points: {len(ets2_data)}")

# Calculate percentage differences from BAU for overlapping years
# For ETS1 (full period 2021-2040)
merged_ets1 = pd.merge(ets1_data, bau_data, on='Year',
                       suffixes=('_ETS1', '_BAU'))
merged_ets1['GDP_Diff_Pct'] = ((merged_ets1['Real_GDP_Total_Billion_EUR_ETS1'] -
                                merged_ets1['Real_GDP_Total_Billion_EUR_BAU']) /
                               merged_ets1['Real_GDP_Total_Billion_EUR_BAU'] * 100)

# For ETS2 (2027-2040)
merged_ets2 = pd.merge(ets2_data, bau_data, on='Year',
                       suffixes=('_ETS2', '_BAU'))
merged_ets2['GDP_Diff_Pct'] = ((merged_ets2['Real_GDP_Total_Billion_EUR_ETS2'] -
                                merged_ets2['Real_GDP_Total_Billion_EUR_BAU']) /
                               merged_ets2['Real_GDP_Total_Billion_EUR_BAU'] * 100)

# Get 2040 values for summary
bau_2040 = bau_data[bau_data['Year'] ==
                    2040]['Real_GDP_Total_Billion_EUR'].values[0]
ets1_2040 = ets1_data[ets1_data['Year'] ==
                      2040]['Real_GDP_Total_Billion_EUR'].values[0]
ets2_2040 = ets2_data[ets2_data['Year'] ==
                      2040]['Real_GDP_Total_Billion_EUR'].values[0]

ets1_diff_2040 = ((ets1_2040 - bau_2040) / bau_2040 * 100)
ets2_diff_2040 = ((ets2_2040 - bau_2040) / bau_2040 * 100)

# Create figure with two subplots (same layout as attached image)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
fig.patch.set_facecolor('#E8E8F0')
ax1.set_facecolor('#E8E8F0')
ax2.set_facecolor('#E8E8F0')

# ============================================================
# SUBPLOT 1: Real GDP Evolution by Scenario
# ============================================================
ax1.plot(bau_data['Year'], bau_data['Real_GDP_Total_Billion_EUR'],
         linewidth=2.5, label='BAU', color='#4472C4', marker='')
ax1.plot(ets1_data['Year'], ets1_data['Real_GDP_Total_Billion_EUR'],
         linewidth=2.5, label='ETS1', color='#ED7D31', marker='')
ax1.plot(ets2_data['Year'], ets2_data['Real_GDP_Total_Billion_EUR'],
         linewidth=2.5, label='ETS2', color='#FFC000', marker='')

# Add 2040 value labels
ax1.text(2040.3, bau_2040, f'{int(bau_2040)}',
         fontsize=10, fontweight='bold', va='center', color='#4472C4')
ax1.text(2040.3, ets1_2040, f'{int(ets1_2040)}',
         fontsize=10, fontweight='bold', va='center', color='#ED7D31')
ax1.text(2040.3, ets2_2040, f'{int(ets2_2040)}',
         fontsize=10, fontweight='bold', va='center', color='#FFC000')

ax1.set_xlim(2020, 2041)
ax1.set_ylim(1700, 2450)
ax1.set_xlabel('Year', fontsize=11, fontweight='bold')
ax1.set_ylabel('Real GDP (Billion EUR)', fontsize=11, fontweight='bold')
ax1.set_title('Italian CGE Model: Real GDP Evolution by Scenario (2021-2040)',
              fontsize=13, fontweight='bold', pad=15)
ax1.legend(loc='upper left', frameon=True,
           fancybox=True, shadow=True, fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# ============================================================
# SUBPLOT 2: GDP Impact of Policy Scenarios (% Change from BAU)
# ============================================================
ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

ax2.plot(merged_ets1['Year'], merged_ets1['GDP_Diff_Pct'],
         linewidth=2.5, label='ETS1 vs BAU', color='#ED7D31', marker='')
ax2.plot(merged_ets2['Year'], merged_ets2['GDP_Diff_Pct'],
         linewidth=2.5, label='ETS2 vs BAU', color='#FFC000', marker='')

ax2.set_xlim(2020, 2041)
ax2.set_ylim(-4.0, 0.5)
ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
ax2.set_ylabel('GDP Difference (%)', fontsize=11, fontweight='bold')
ax2.set_title('GDP Impact of Policy Scenarios (% Change from BAU)',
              fontsize=13, fontweight='bold', pad=15)
ax2.legend(loc='upper right', frameon=True,
           fancybox=True, shadow=True, fontsize=10)
ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)

# Add summary statistics box
summary_text = f'Summary Statistics (2040):\n'
summary_text += f'ETS1: €{int(ets1_2040)}B ({ets1_diff_2040:.2f}%)\n'
summary_text += f'ETS2: €{int(ets2_2040)}B ({ets2_diff_2040:.2f}%)\n'
summary_text += f'BAU: €{int(bau_2040)}B'

props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax2.text(0.02, 0.05, summary_text, transform=ax2.transAxes, fontsize=9,
         verticalalignment='bottom', bbox=props, family='monospace')

plt.tight_layout()

# Save figure
output_path = 'figures/GDP_Evolution_Scenarios_2021_2040.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#E8E8F0')
print(f"\n✓ Figure saved: {output_path}")

# Also save as PDF
output_pdf = 'figures/GDP_Evolution_Scenarios_2021_2040.pdf'
plt.savefig(output_pdf, bbox_inches='tight', facecolor='#E8E8F0')
print(f"✓ PDF saved: {output_pdf}")

plt.show()

# Print summary statistics
print("\n" + "="*60)
print("REAL GDP EVOLUTION SUMMARY")
print("="*60)
print(
    f"\n2021 Baseline (All Scenarios): €{int(bau_data[bau_data['Year'] == 2021]['Real_GDP_Total_Billion_EUR'].values[0])}B")
print(f"\n2040 GDP by Scenario:")
print(f"  BAU:  €{int(bau_2040)}B")
print(f"  ETS1: €{int(ets1_2040)}B  ({ets1_diff_2040:+.2f}% vs BAU)")
print(f"  ETS2: €{int(ets2_2040)}B  ({ets2_diff_2040:+.2f}% vs BAU)")
print(f"\nAverage Annual Growth (2021-2040):")
gdp_2021 = bau_data[bau_data['Year'] ==
                    2021]['Real_GDP_Total_Billion_EUR'].values[0]
bau_growth = ((bau_2040 / gdp_2021) ** (1/19) - 1) * 100
ets1_growth = ((ets1_2040 / gdp_2021) ** (1/19) - 1) * 100
ets2_growth = ((ets2_2040 / gdp_2021) ** (1/19) - 1) * 100
print(f"  BAU:  {bau_growth:.2f}% per year")
print(f"  ETS1: {ets1_growth:.2f}% per year")
print(f"  ETS2: {ets2_growth:.2f}% per year")
print("="*60)
