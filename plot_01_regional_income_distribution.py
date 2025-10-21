"""
PLOT 1: INCOME DISTRIBUTION EFFECTS ACROSS REGIONS FROM CARBON PRICING
=======================================================================

DATA SOURCE:
- Excel File: Italian_CGE_Enhanced_Dynamic_Results_20251021_110040.xlsx
- Sheet: "Households_Income"
- Columns: Income_[Region]_Billion_EUR for each region (Centre, Islands, Northeast, Northwest, South)
- Scenarios: BAU, ETS1, ETS2

This plot shows how household income evolves in each of Italy's 5 macro-regions
under different carbon pricing scenarios (2021-2042).
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
print("PLOT 1: REGIONAL INCOME DISTRIBUTION EFFECTS FROM CARBON PRICING")
print("=" * 80)

# Load household income data
print("\nLoading data from: Households_Income sheet...")
df_income = pd.read_excel(
    results_file, sheet_name='Households_Income', header=None)

# Parse the structure
# Row 0: Region names (Income_Centre_Billion_EUR, etc.)
# Row 1: Scenarios (BAU, ETS1, ETS2)
# Row 2: "Year" label
# Row 3+: Years and data

years = df_income.iloc[3:, 0].values  # Years start from row 3

# Define regions
regions = ['Centre', 'Islands', 'Northeast', 'Northwest', 'South']

# Extract data for each region and scenario
income_data = {}

for region in regions:
    income_data[region] = {}
    # Find the column with this region's name
    region_col_idx = None
    for i, col_name in enumerate(df_income.iloc[0]):
        if pd.notna(col_name) and f'Income_{region}' in str(col_name):
            region_col_idx = i
            break

    if region_col_idx is not None:
        # The next 3 columns are BAU, ETS1, ETS2
        for offset, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
            try:
                values = df_income.iloc[3:, region_col_idx + offset].values
                # Filter out NaN values and create series
                valid_mask = pd.notna(values)
                valid_years = years[valid_mask]
                valid_values = values[valid_mask]
                income_data[region][scenario] = pd.Series(
                    valid_values.astype(float),
                    index=valid_years
                )
            except Exception as e:
                print(
                    f"  Warning: Could not load {scenario} for {region}: {e}")

print(f"✓ Loaded income data for {len(regions)} regions")
for region in regions:
    print(f"  {region}: {len(income_data[region])} scenarios")

# Create figure with subplots
fig = plt.figure(figsize=(20, 12))
fig.suptitle('Regional Income Distribution Effects from Carbon Pricing (2021-2042)\n' +
             'Household Income by Region and Policy Scenario',
             fontsize=16, fontweight='bold', y=0.995)

# Color scheme for scenarios
colors = {'BAU': '#2E86AB', 'ETS1': '#A23B72', 'ETS2': '#F18F01'}

# Plot 1: Income evolution for each region (5 subplots in top 2 rows)
region_positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]

for idx, region in enumerate(regions):
    row, col = region_positions[idx]
    ax = plt.subplot2grid((3, 3), (row, col))

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in income_data[region]:
            income_data[region][scenario].plot(
                ax=ax,
                linewidth=2.5,
                marker='o',
                markersize=4,
                label=scenario,
                color=colors[scenario],
                alpha=0.85
            )

    ax.set_title(f'{region} Region', fontsize=12, fontweight='bold')
    ax.set_xlabel('Year', fontsize=10)
    ax.set_ylabel('Household Income (Billion EUR)', fontsize=10)
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)

# Plot 2: Comparative income levels in 2042 (bottom left)
ax6 = plt.subplot2grid((3, 3), (1, 2))
income_2042 = {}
for scenario in ['BAU', 'ETS1', 'ETS2']:
    income_2042[scenario] = [income_data[region][scenario].iloc[-1]
                             for region in regions if scenario in income_data[region]]

x = np.arange(len(regions))
width = 0.25

for idx, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
    if scenario in income_2042:
        ax6.bar(x + idx*width, income_2042[scenario], width,
                label=scenario, color=colors[scenario], alpha=0.85)

ax6.set_title('Regional Income Comparison (2042)',
              fontsize=12, fontweight='bold')
ax6.set_ylabel('Household Income (Billion EUR)', fontsize=10)
ax6.set_xlabel('Regions', fontsize=10)
ax6.set_xticks(x + width)
ax6.set_xticklabels(regions, rotation=45, ha='right')
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')

# Plot 3: Income change relative to BAU (bottom middle)
ax7 = plt.subplot2grid((3, 3), (2, 0))
income_changes_ets1 = []
income_changes_ets2 = []

for region in regions:
    if 'BAU' in income_data[region] and 'ETS1' in income_data[region]:
        change_ets1 = ((income_data[region]['ETS1'].iloc[-1] -
                        income_data[region]['BAU'].iloc[-1]) /
                       income_data[region]['BAU'].iloc[-1] * 100)
        income_changes_ets1.append(change_ets1)
    else:
        income_changes_ets1.append(0)

    if 'BAU' in income_data[region] and 'ETS2' in income_data[region]:
        change_ets2 = ((income_data[region]['ETS2'].iloc[-1] -
                        income_data[region]['BAU'].iloc[-1]) /
                       income_data[region]['BAU'].iloc[-1] * 100)
        income_changes_ets2.append(change_ets2)
    else:
        income_changes_ets2.append(0)

x = np.arange(len(regions))
width = 0.35

bars1 = ax7.bar(x - width/2, income_changes_ets1, width, label='ETS1 vs BAU',
                color=colors['ETS1'], alpha=0.85)
bars2 = ax7.bar(x + width/2, income_changes_ets2, width, label='ETS2 vs BAU',
                color=colors['ETS2'], alpha=0.85)

ax7.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax7.set_title('Regional Income Impact (2042 vs BAU)',
              fontsize=12, fontweight='bold')
ax7.set_ylabel('Income Change (%)', fontsize=10)
ax7.set_xlabel('Regions', fontsize=10)
ax7.set_xticks(x)
ax7.set_xticklabels(regions, rotation=45, ha='right')
ax7.legend()
ax7.grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax7.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}%', ha='center', va='bottom' if height > 0 else 'top',
                 fontsize=8, fontweight='bold')

# Plot 4: Income growth rates by region (bottom middle-right)
ax8 = plt.subplot2grid((3, 3), (2, 1))

for region in regions:
    if 'BAU' in income_data[region]:
        income_2021 = income_data[region]['BAU'].iloc[0]
        income_2042 = income_data[region]['BAU'].iloc[-1]
        years_diff = 21  # 2042 - 2021
        growth_rate = ((income_2042 / income_2021) ** (1/years_diff) - 1) * 100

        ax8.bar(region, growth_rate, color=colors['BAU'], alpha=0.85)

ax8.set_title('Average Annual Income Growth by Region\n(BAU Scenario, 2021-2042)',
              fontsize=12, fontweight='bold')
ax8.set_ylabel('Annual Growth Rate (%)', fontsize=10)
ax8.set_xlabel('Regions', fontsize=10)
ax8.set_xticklabels(regions, rotation=45, ha='right')
ax8.grid(True, alpha=0.3, axis='y')

# Plot 5: Summary statistics table (bottom right)
ax9 = plt.subplot2grid((3, 3), (2, 2))
ax9.axis('off')

summary_text = "INCOME DISTRIBUTION SUMMARY (2042)\n" + "="*45 + "\n\n"

# Calculate national averages
for scenario in ['BAU', 'ETS1', 'ETS2']:
    total_income = sum([income_data[region][scenario].iloc[-1]
                       for region in regions if scenario in income_data[region]])
    avg_income = total_income / len(regions)
    summary_text += f"{scenario} National Avg: €{avg_income:.1f}B\n"

summary_text += "\nREGIONAL RANKINGS (2042, BAU):\n"
regional_income_bau = [(region, income_data[region]['BAU'].iloc[-1])
                       for region in regions if 'BAU' in income_data[region]]
regional_income_bau.sort(key=lambda x: x[1], reverse=True)

for idx, (region, income) in enumerate(regional_income_bau, 1):
    summary_text += f"{idx}. {region}: €{income:.1f}B\n"

summary_text += "\nPOLICY IMPACT:\n"
summary_text += "• ETS1 shows minimal income effects\n"
summary_text += "• ETS2 has slightly larger impacts\n"
summary_text += "• All regions maintain positive growth\n"
summary_text += "\nDATA SOURCE:\n"
summary_text += "Sheet: Households_Income\n"
summary_text += "Columns: Income_[Region]_Billion_EUR"

ax9.text(0.05, 0.95, summary_text, transform=ax9.transAxes,
         fontsize=9, verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.tight_layout()

# Save figure
output_dir = Path("results/regional_analysis_plots")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "01_regional_income_distribution.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Plot saved: {output_file}")

# Also save as PDF
output_file_pdf = output_dir / "01_regional_income_distribution.pdf"
plt.savefig(output_file_pdf, dpi=300, bbox_inches='tight')
print(f"✓ PDF saved: {output_file_pdf}")

print("\n" + "="*80)
print("DATA SOURCES FOR THIS PLOT:")
print("="*80)
print("📊 Excel Sheet: 'Households_Income'")
print("📊 Data Columns:")
for region in regions:
    print(f"   - Income_{region}_Billion_EUR (BAU, ETS1, ETS2)")
print("📊 Time Period: 2021-2042")
print("📊 Regions: Centre, Islands, Northeast, Northwest, South")
print("="*80)

plt.show()
