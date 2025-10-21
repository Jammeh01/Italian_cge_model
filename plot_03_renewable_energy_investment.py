"""
PLOT 3: RENEWABLE ENERGY INVESTMENT AND CAPACITY ADDITIONS BY REGION
======================================================================

DATA SOURCES:
- Excel File: Italian_CGE_Enhanced_Dynamic_Results_20251021_110040.xlsx
- Sheet 1: "Renewable_Investment" - Annual investment by region
- Sheet 2: "Renewable_Capacity" - Capacity additions and cumulative capacity by region

This plot shows:
1. Annual renewable energy investment by region
2. Cumulative capacity additions over time
3. Regional distribution of renewable capacity
4. Comparison across BAU, ETS1, and ETS2 scenarios

Note: The model tracks aggregate renewable investment. Regional allocation is 
estimated based on regional GDP shares and energy demand patterns.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")

# File path
results_file = "results/Italian_CGE_Enhanced_Dynamic_Results_20251021_110040.xlsx"

print("=" * 80)
print("PLOT 3: RENEWABLE ENERGY INVESTMENT AND CAPACITY ADDITIONS BY REGION")
print("=" * 80)

# Load renewable investment data
print("\n1. Loading renewable investment data by region...")
df_investment = pd.read_excel(
    results_file, sheet_name='Renewable_Investment', header=None)

# Load renewable capacity data
print("2. Loading renewable capacity data...")
df_capacity = pd.read_excel(
    results_file, sheet_name='Renewable_Capacity', header=None)

# Parse years
years = df_investment.iloc[3:, 0].values

# Define regions
regions = ['Centre', 'Islands', 'Northeast', 'Northwest', 'South']

# Extract investment data by region
print("\n3. Extracting investment data by region...")
investment_data = {}

for region in regions:
    investment_data[region] = {}

    # Find column for this region
    region_col_idx = None
    for i, col_name in enumerate(df_investment.iloc[0]):
        if pd.notna(col_name) and f'Investment_{region}' in str(col_name):
            region_col_idx = i
            break

    if region_col_idx is not None:
        # Next 3 columns are BAU, ETS1, ETS2
        for offset, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
            try:
                values = df_investment.iloc[3:, region_col_idx + offset].values
                valid_mask = pd.notna(values)
                valid_years = years[valid_mask]
                valid_values = values[valid_mask]
                investment_data[region][scenario] = pd.Series(
                    valid_values.astype(float),
                    index=valid_years
                )
            except Exception as e:
                pass

print(f"✓ Loaded investment data for {len(regions)} regions")

# Extract capacity data
print("\n4. Extracting capacity data...")
capacity_data = {}

# National annual additions
capacity_data['Annual_Additions_National'] = {}
for i, col_name in enumerate(df_capacity.iloc[0]):
    if pd.notna(col_name) and 'Annual_Capacity_Additions_GW' in str(col_name):
        for offset, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
            try:
                values = df_capacity.iloc[3:, i + offset].values
                valid_mask = pd.notna(values)
                valid_years = years[valid_mask]
                valid_values = values[valid_mask]
                capacity_data['Annual_Additions_National'][scenario] = pd.Series(
                    valid_values.astype(float),
                    index=valid_years
                )
            except:
                pass
        break

# Cumulative national capacity
capacity_data['Cumulative_National'] = {}
for i, col_name in enumerate(df_capacity.iloc[0]):
    if pd.notna(col_name) and 'Cumulative_Renewable_Capacity_GW' in str(col_name):
        for offset, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
            try:
                values = df_capacity.iloc[3:, i + offset].values
                valid_mask = pd.notna(values)
                valid_years = years[valid_mask]
                valid_values = values[valid_mask]
                capacity_data['Cumulative_National'][scenario] = pd.Series(
                    valid_values.astype(float),
                    index=valid_years
                )
            except:
                pass
        break

# Regional capacity
capacity_data['Regional'] = {}
for region in regions:
    capacity_data['Regional'][region] = {}

    region_col_idx = None
    for i, col_name in enumerate(df_capacity.iloc[0]):
        if pd.notna(col_name) and f'Capacity_{region}_GW' in str(col_name):
            region_col_idx = i
            break

    if region_col_idx is not None:
        for offset, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
            try:
                values = df_capacity.iloc[3:, region_col_idx + offset].values
                valid_mask = pd.notna(values)
                valid_years = years[valid_mask]
                valid_values = values[valid_mask]
                capacity_data['Regional'][region][scenario] = pd.Series(
                    valid_values.astype(float),
                    index=valid_years
                )
            except:
                pass

print(f"✓ Loaded capacity data (national and regional)")

# Create visualization
fig = plt.figure(figsize=(20, 14))
fig.suptitle('Renewable Energy Investment and Capacity Additions by Region (2021-2042)\n' +
             'Clean Energy Transition Across Italian Macro-Regions',
             fontsize=16, fontweight='bold', y=0.995)

colors = {'BAU': '#2E86AB', 'ETS1': '#A23B72', 'ETS2': '#F18F01'}

# Plot 1-5: Investment evolution by region
region_positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]

for idx, region in enumerate(regions):
    row, col = region_positions[idx]
    ax = plt.subplot2grid((3, 3), (row, col))

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in investment_data[region]:
            investment_data[region][scenario].plot(
                ax=ax,
                linewidth=2.5,
                marker='o',
                markersize=4,
                label=scenario,
                color=colors[scenario],
                alpha=0.85
            )

    ax.set_title(f'{region} Region Investment', fontsize=12, fontweight='bold')
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Annual Investment (Billion EUR)', fontsize=10)
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)

# Plot 6: Cumulative national capacity
ax6 = plt.subplot2grid((3, 3), (1, 2))

for scenario in ['BAU', 'ETS1', 'ETS2']:
    if scenario in capacity_data['Cumulative_National']:
        capacity_data['Cumulative_National'][scenario].plot(
            ax=ax6,
            linewidth=3,
            marker='s',
            markersize=5,
            label=scenario,
            color=colors[scenario],
            alpha=0.85
        )

ax6.set_title('Cumulative National Renewable Capacity',
              fontsize=12, fontweight='bold')
ax6.set_xlabel('Year', fontsize=10)
ax6.set_ylabel('Cumulative Capacity (GW)', fontsize=10)
ax6.legend(loc='best', framealpha=0.9)
ax6.grid(True, alpha=0.3)
ax6.tick_params(axis='x', rotation=45)

# Plot 7: Regional investment comparison (2042)
ax7 = plt.subplot2grid((3, 3), (2, 0))
investment_2042 = {}
for scenario in ['BAU', 'ETS1', 'ETS2']:
    investment_2042[scenario] = []
    for region in regions:
        if scenario in investment_data[region]:
            last_value = investment_data[region][scenario].dropna(
            ).iloc[-1] if len(investment_data[region][scenario].dropna()) > 0 else 0
            investment_2042[scenario].append(last_value)
        else:
            investment_2042[scenario].append(0)

x = np.arange(len(regions))
width = 0.25

for idx, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
    ax7.bar(x + idx*width, investment_2042[scenario], width,
            label=scenario, color=colors[scenario], alpha=0.85)

ax7.set_title('Regional Investment Comparison (2042)',
              fontsize=12, fontweight='bold')
ax7.set_ylabel('Annual Investment (Billion EUR)', fontsize=10)
ax7.set_xlabel('Regions', fontsize=10)
ax7.set_xticks(x + width)
ax7.set_xticklabels(regions, rotation=45, ha='right')
ax7.legend()
ax7.grid(True, alpha=0.3, axis='y')

# Plot 8: Annual capacity additions (National)
ax8 = plt.subplot2grid((3, 3), (2, 1))

for scenario in ['BAU', 'ETS1', 'ETS2']:
    if scenario in capacity_data['Annual_Additions_National']:
        capacity_data['Annual_Additions_National'][scenario].plot(
            ax=ax8,
            linewidth=2.5,
            marker='D',
            markersize=4,
            label=scenario,
            color=colors[scenario],
            alpha=0.85
        )

ax8.set_title('Annual Capacity Additions (National)',
              fontsize=12, fontweight='bold')
ax8.set_xlabel('Year', fontsize=10)
ax8.set_ylabel('Annual Additions (GW/year)', fontsize=10)
ax8.legend(loc='best', framealpha=0.9)
ax8.grid(True, alpha=0.3)
ax8.tick_params(axis='x', rotation=45)

# Plot 9: Regional capacity distribution (2042, BAU)
ax9 = plt.subplot2grid((3, 3), (2, 2))

# Calculate regional shares for 2042
regional_capacity_2042 = []
regional_capacity_labels = []

for region in regions:
    if 'BAU' in capacity_data['Regional'].get(region, {}):
        cap = capacity_data['Regional'][region]['BAU'].dropna(
        ).iloc[-1] if len(capacity_data['Regional'][region]['BAU'].dropna()) > 0 else 0
        regional_capacity_2042.append(cap)
        regional_capacity_labels.append(f'{region}\n{cap:.1f} GW')
    else:
        regional_capacity_2042.append(0)
        regional_capacity_labels.append(f'{region}\n0 GW')

# Create pie chart
colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
explode = [0.05] * len(regions)

wedges, texts, autotexts = ax9.pie(regional_capacity_2042, labels=regions, autopct='%1.1f%%',
                                   colors=colors_pie, explode=explode, startangle=90,
                                   textprops={'fontsize': 10, 'fontweight': 'bold'})

ax9.set_title('Regional Capacity Distribution (2042, BAU)',
              fontsize=12, fontweight='bold')

# Add legend with actual values
legend_labels = [
    f'{regions[i]}: {regional_capacity_2042[i]:.2f} GW' for i in range(len(regions))]
ax9.legend(legend_labels, loc='upper left',
           bbox_to_anchor=(1, 0, 0.5, 1), fontsize=8)

plt.tight_layout()

# Save figure
output_dir = Path("results/regional_analysis_plots")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "03_renewable_investment_capacity.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Plot saved: {output_file}")

output_file_pdf = output_dir / "03_renewable_investment_capacity.pdf"
plt.savefig(output_file_pdf, dpi=300, bbox_inches='tight')
print(f"✓ PDF saved: {output_file_pdf}")

# Print summary statistics
print("\n" + "="*80)
print("RENEWABLE ENERGY INVESTMENT SUMMARY")
print("="*80)

print("\nCUMULATIVE INVESTMENT (2021-2042):")
for scenario in ['BAU', 'ETS1', 'ETS2']:
    total_investment = 0
    for region in regions:
        if scenario in investment_data[region]:
            total_investment += investment_data[region][scenario].sum()
    print(f"  {scenario}: €{total_investment:.1f} billion")

print("\nCAPACITY GROWTH (2021 → 2042, BAU):")
if 'BAU' in capacity_data['Cumulative_National']:
    cap_2021 = capacity_data['Cumulative_National']['BAU'].iloc[0]
    cap_2042 = capacity_data['Cumulative_National']['BAU'].iloc[-1]
    growth = cap_2042 - cap_2021
    growth_pct = (growth / cap_2021) * 100
    print(f"  2021: {cap_2021:.1f} GW")
    print(f"  2042: {cap_2042:.1f} GW")
    print(f"  Growth: +{growth:.1f} GW (+{growth_pct:.1f}%)")

print("\nLARGEST REGIONAL INVESTORS (2042, ETS2):")
regional_inv_2042 = [(region, investment_data[region]['ETS2'].dropna().iloc[-1])
                     for region in regions if 'ETS2' in investment_data[region] and len(investment_data[region]['ETS2'].dropna()) > 0]
regional_inv_2042.sort(key=lambda x: x[1], reverse=True)
for idx, (region, inv) in enumerate(regional_inv_2042[:3], 1):
    print(f"  {idx}. {region}: €{inv:.2f} billion/year")

print("\n" + "="*80)
print("DATA SOURCES FOR THIS PLOT:")
print("="*80)
print("📊 Excel Sheet 1: 'Renewable_Investment'")
print("   - Renewable_Investment_[Region]_Billion_EUR (BAU, ETS1, ETS2)")
print("📊 Excel Sheet 2: 'Renewable_Capacity'")
print("   - Annual_Capacity_Additions_GW (National)")
print("   - Cumulative_Renewable_Capacity_GW (National)")
print("   - Renewable_Capacity_[Region]_GW (BAU, ETS1, ETS2)")
print("📊 Regions: Centre, Islands, Northeast, Northwest, South")
print("📊 Time Period: 2021-2042")
print("="*80)

plt.show()
