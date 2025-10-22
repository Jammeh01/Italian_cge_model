"""
Single Plot: Real GDP Evolution and Impact by Scenario (2021-2040)
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
print("Loading GDP data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251021_151832.xlsx')
gdp_df = pd.read_excel(xl, 'Macroeconomy_GDP')

# Extract years and filter for 2020-2040
years = pd.to_numeric(gdp_df.iloc[2:, 0], errors='coerce').values
mask = (years >= 2020) & (years <= 2040)
years = years[mask]

# Extract Real GDP data in Billion EUR (BAU=4, ETS1=5, ETS2=6)
gdp_bau = pd.to_numeric(gdp_df.iloc[2:, 4], errors='coerce').values[mask]
gdp_ets1 = pd.to_numeric(gdp_df.iloc[2:, 5], errors='coerce').values[mask]
gdp_ets2 = pd.to_numeric(gdp_df.iloc[2:, 6], errors='coerce').values[mask]

# Define colors
color_bau = '#4169E1'   # Medium-dark blue (Royal Blue)
color_ets1 = '#FF8C00'  # Bright Orange (Dark Orange)
color_ets2 = '#2E8B57'  # Vivid medium green (Sea Green)

# Create figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# ============================================================================
# Top Panel: Real GDP Evolution
# ============================================================================
ax1.plot(years, gdp_bau, label='BAU', color=color_bau, linewidth=2.5)
ax1.plot(years, gdp_ets1, label='ETS1', color=color_ets1, linewidth=2.5)
ax1.plot(years, gdp_ets2, label='ETS2', color=color_ets2, linewidth=2.5)

# Add 2040 values as text labels
idx_2040 = np.where(years == 2040)[0][0]
ax1.text(2040, gdp_bau[idx_2040], f'{gdp_bau[idx_2040]:.0f}',
         fontsize=10, fontweight='bold', ha='left', va='bottom', color=color_bau)
ax1.text(2040, gdp_ets1[idx_2040], f'{gdp_ets1[idx_2040]:.0f}',
         fontsize=10, fontweight='bold', ha='left', va='top', color=color_ets1)
ax1.text(2040, gdp_ets2[idx_2040], f'{gdp_ets2[idx_2040]:.0f}',
         fontsize=10, fontweight='bold', ha='left', va='bottom', color=color_ets2)

ax1.set_ylabel('Real GDP (Billion EUR)', fontsize=13, fontweight='bold')
ax1.set_title('Italian CGE Model: Real GDP Evolution by Scenario (2021-2040)',
              fontsize=14, fontweight='bold', pad=15)
ax1.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)
ax1.grid(True, alpha=0.3, linestyle='--')

# ============================================================================
# Bottom Panel: GDP Impact (% Change from BAU)
# ============================================================================
# Calculate percentage differences from BAU
gdp_ets1_pct = ((gdp_ets1 - gdp_bau) / gdp_bau) * 100
gdp_ets2_pct = ((gdp_ets2 - gdp_bau) / gdp_bau) * 100

ax2.plot(years, gdp_ets1_pct, label='ETS1 vs BAU',
         color=color_ets1, linewidth=2.5)
ax2.plot(years, gdp_ets2_pct, label='ETS2 vs BAU',
         color=color_ets2, linewidth=2.5)
ax2.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

ax2.set_xlabel('Year', fontsize=13, fontweight='bold')
ax2.set_ylabel('GDP Difference (%)', fontsize=13, fontweight='bold')
ax2.set_title('GDP Impact of Policy Scenarios (% Change from BAU)',
              fontsize=14, fontweight='bold', pad=15)
ax2.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)
ax2.grid(True, alpha=0.3, linestyle='--')

# Add summary statistics box
idx_2040 = np.where(years == 2040)[0][0]
summary_text = (
    f'Summary Statistics (2040):\n'
    f'ETS1: €{gdp_ets1[idx_2040]:.0f}B ({gdp_ets1_pct[idx_2040]:.2f}%)\n'
    f'ETS2: €{gdp_ets2[idx_2040]:.0f}B ({gdp_ets2_pct[idx_2040]:.2f}%)\n'
    f'BAU: €{gdp_bau[idx_2040]:.0f}B'
)
ax2.text(0.05, 0.05, summary_text, transform=ax2.transAxes,
         fontsize=9, verticalalignment='bottom', bbox=dict(boxstyle='round',
                                                           facecolor='wheat', alpha=0.5))

# Set x-axis limits and ticks
ax2.set_xlim(2020, 2040)
ax2.set_xticks([2020, 2022.5, 2025, 2027.5, 2030, 2032.5, 2035, 2037.5, 2040])

plt.tight_layout()

# Save
plt.savefig('results/Single_Plot_GDP_Evolution.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Single_Plot_GDP_Evolution.pdf', bbox_inches='tight')
print("✓ GDP evolution and impact plot saved!")
print("  - results/Single_Plot_GDP_Evolution.png")
print("  - results/Single_Plot_GDP_Evolution.pdf")

# Print summary statistics
print("\n" + "="*80)
print("REAL GDP EVOLUTION (2021-2040)")
print("="*80)
print(f"{'Year':<8} {'BAU (B€)':>12} {'ETS1 (B€)':>12} {'ETS2 (B€)':>12} "
      f"{'ETS1 (%)':>10} {'ETS2 (%)':>10}")
print("-"*80)

# Print selected years
selected_years = [2021, 2025, 2030, 2035, 2040]
for year in selected_years:
    if year in years:
        idx = np.where(years == year)[0][0]
        pct1 = ((gdp_ets1[idx] - gdp_bau[idx]) / gdp_bau[idx]) * 100
        pct2 = ((gdp_ets2[idx] - gdp_bau[idx]) / gdp_bau[idx]) * 100
        print(f"{year:<8} {gdp_bau[idx]:>12.1f} {gdp_ets1[idx]:>12.1f} {gdp_ets2[idx]:>12.1f} "
              f"{pct1:>9.2f} {pct2:>9.2f}")

print("="*80)

# Growth rates
idx_2021 = np.where(years == 2021)[0][0]
idx_2040 = np.where(years == 2040)[0][0]

growth_bau = ((gdp_bau[idx_2040] - gdp_bau[idx_2021]) /
              gdp_bau[idx_2021]) * 100
growth_ets1 = ((gdp_ets1[idx_2040] - gdp_ets1[idx_2021]
                ) / gdp_ets1[idx_2021]) * 100
growth_ets2 = ((gdp_ets2[idx_2040] - gdp_ets2[idx_2021]
                ) / gdp_ets2[idx_2021]) * 100

print("\nGDP GROWTH (2021-2040):")
print("-"*80)
print(f"BAU:  {growth_bau:>6.2f}%")
print(f"ETS1: {growth_ets1:>6.2f}%")
print(f"ETS2: {growth_ets2:>6.2f}%")

print("\n2040 GDP IMPACT RELATIVE TO BAU:")
print("-"*80)
gdp_loss_ets1 = gdp_bau[idx_2040] - gdp_ets1[idx_2040]
gdp_loss_ets2 = gdp_bau[idx_2040] - gdp_ets2[idx_2040]
print(f"ETS1: €{gdp_loss_ets1:>6.1f}B ({gdp_ets1_pct[idx_2040]:>5.2f}%)")
print(f"ETS2: €{gdp_loss_ets2:>6.1f}B ({gdp_ets2_pct[idx_2040]:>5.2f}%)")
print("="*80)

plt.show()
