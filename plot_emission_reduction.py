"""
Single Plot: Emission Reduction from BAU 2021 Baseline (%)
Italian CGE Model - Dynamic Simulation Results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set publication-quality style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 13
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['xtick.labelsize'] = 11
plt.rcParams['ytick.labelsize'] = 11
plt.rcParams['legend.fontsize'] = 11

# Load data
print("Loading CO2 emissions data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251021_151832.xlsx')
co2_df = pd.read_excel(xl, 'CO2_Emissions_Totals')

# Extract years and filter for 2020-2040
years = pd.to_numeric(co2_df.iloc[2:, 0], errors='coerce').values
mask = (years >= 2020) & (years <= 2040)
years = years[mask]

# Extract Total CO2 Emissions data in MtCO2 (BAU=10, ETS1=11, ETS2=12)
co2_bau = pd.to_numeric(co2_df.iloc[2:, 10], errors='coerce').values[mask]
co2_ets1 = pd.to_numeric(co2_df.iloc[2:, 11], errors='coerce').values[mask]
co2_ets2 = pd.to_numeric(co2_df.iloc[2:, 12], errors='coerce').values[mask]

# Get 2021 baseline value for BAU
idx_2021 = np.where(years == 2021)[0][0]
baseline_2021 = co2_bau[idx_2021]

# Calculate emission reduction percentage from 2021 BAU baseline
reduction_bau = ((baseline_2021 - co2_bau) / baseline_2021) * 100
reduction_ets1 = ((baseline_2021 - co2_ets1) / baseline_2021) * 100
reduction_ets2 = ((baseline_2021 - co2_ets2) / baseline_2021) * 100

# Define colors
color_bau = '#4169E1'   # Medium-dark blue (Royal Blue)
color_ets1 = '#FF8C00'  # Bright Orange (Dark Orange)
color_ets2 = '#2E8B57'  # Vivid medium green (Sea Green)

# Create figure
fig, ax = plt.subplots(figsize=(14, 7))

# Plot lines
ax.plot(years, reduction_bau, label='BAU', color=color_bau, linewidth=2.5)
ax.plot(years, reduction_ets1, label='ETS1 (Industries)', color=color_ets1,
        linewidth=2.5, linestyle='--')
ax.plot(years, reduction_ets2, label='ETS2 (+Transport and Buildings)',
        color=color_ets2, linewidth=2.5)

# Add EU 2030 target line (-55%)
ax.axhline(y=55, color='red', linestyle='--', linewidth=1.5, alpha=0.7,
           label='EU 2030 Target (-55%)')

# Add vertical line at 2030
ax.axvline(x=2030, color='gray', linestyle='-', linewidth=1, alpha=0.3)

# Add horizontal line at 100% for reference
ax.axhline(y=100, color='red', linestyle=':', linewidth=1.5, alpha=0.7)

# Add 2040 values as text labels
idx_2040 = np.where(years == 2040)[0][0]
ax.text(2040.3, reduction_bau[idx_2040], f'{reduction_bau[idx_2040]:.1f}%',
        fontsize=10, fontweight='bold', va='center', color=color_bau)
ax.text(2040.3, reduction_ets1[idx_2040], f'{reduction_ets1[idx_2040]:.1f}%',
        fontsize=10, fontweight='bold', va='center', color=color_ets1)
ax.text(2040.3, reduction_ets2[idx_2040], f'{reduction_ets2[idx_2040]:.1f}%',
        fontsize=10, fontweight='bold', va='center', color=color_ets2)

# Formatting
ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('Emission Reduction from BAU 2021 (%)',
              fontsize=13, fontweight='bold')
ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--')

# Set axis limits
ax.set_xlim(2020, 2040)
ax.set_ylim(0, 110)
ax.set_xticks([2020, 2025, 2030, 2035, 2040])

# Add summary statistics box
summary_text = (
    f'Baseline: BAU 2021 = {baseline_2021:.1f} Mt CO2\n'
    f'2040 Emission Reductions:\n'
    f'BAU: {reduction_bau[idx_2040]:.1f}%\n'
    f'ETS1: {reduction_ets1[idx_2040]:.1f}%\n'
    f'ETS2: {reduction_ets2[idx_2040]:.1f}%'
)
ax.text(0.75, 0.05, summary_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()

# Save
plt.savefig('results/Single_Plot_Emission_Reduction.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Single_Plot_Emission_Reduction.pdf', bbox_inches='tight')
print("✓ Emission reduction plot saved!")
print("  - results/Single_Plot_Emission_Reduction.png")
print("  - results/Single_Plot_Emission_Reduction.pdf")

# Print summary statistics
print("\n" + "="*80)
print("EMISSION REDUCTION FROM BAU 2021 BASELINE")
print("="*80)
print(f"Baseline (2021 BAU): {baseline_2021:.1f} MtCO2")
print("="*80)
print(f"{'Year':<8} {'BAU (%)':>12} {'ETS1 (%)':>12} {'ETS2 (%)':>12} "
      f"{'BAU (Mt)':>12} {'ETS1 (Mt)':>12} {'ETS2 (Mt)':>12}")
print("-"*80)

# Print selected years
selected_years = [2021, 2025, 2030, 2035, 2040]
for year in selected_years:
    if year in years:
        idx = np.where(years == year)[0][0]
        print(f"{year:<8} {reduction_bau[idx]:>12.1f} {reduction_ets1[idx]:>12.1f} "
              f"{reduction_ets2[idx]:>12.1f} {co2_bau[idx]:>12.1f} {co2_ets1[idx]:>12.1f} "
              f"{co2_ets2[idx]:>12.1f}")

print("="*80)

# Check EU 2030 target compliance
idx_2030 = np.where(years == 2030)[0][0]
print("\nEU 2030 TARGET COMPLIANCE (-55%):")
print("-"*80)
print(
    f"BAU:  {reduction_bau[idx_2030]:.1f}% - {'✓ ACHIEVED' if reduction_bau[idx_2030] >= 55 else '✗ NOT ACHIEVED'}")
print(
    f"ETS1: {reduction_ets1[idx_2030]:.1f}% - {'✓ ACHIEVED' if reduction_ets1[idx_2030] >= 55 else '✗ NOT ACHIEVED'}")
print(
    f"ETS2: {reduction_ets2[idx_2030]:.1f}% - {'✓ ACHIEVED' if reduction_ets2[idx_2030] >= 55 else '✗ NOT ACHIEVED'}")

print("\n2040 EMISSION LEVELS:")
print("-"*80)
print(
    f"BAU:  {co2_bau[idx_2040]:.1f} MtCO2 ({reduction_bau[idx_2040]:.1f}% reduction)")
print(
    f"ETS1: {co2_ets1[idx_2040]:.1f} MtCO2 ({reduction_ets1[idx_2040]:.1f}% reduction)")
print(
    f"ETS2: {co2_ets2[idx_2040]:.1f} MtCO2 ({reduction_ets2[idx_2040]:.1f}% reduction)")
print("="*80)

plt.show()
