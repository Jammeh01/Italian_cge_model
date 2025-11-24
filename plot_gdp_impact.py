"""
Single Plot: GDP Impact of Policy Scenarios (% Change from BAU)
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
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251124_135016.xlsx')
gdp_df = pd.read_excel(xl, 'Macroeconomy_GDP')

# Extract years and filter for 2021-2040
years = pd.to_numeric(gdp_df.iloc[2:, 0], errors='coerce').values
mask = (years >= 2021) & (years <= 2040)
years = years[mask]

# Extract Real GDP data in Billion EUR
gdp_bau = pd.to_numeric(gdp_df.iloc[2:, 1], errors='coerce').values[mask]
gdp_ets1 = pd.to_numeric(gdp_df.iloc[2:, 2], errors='coerce').values[mask]
gdp_ets2 = pd.to_numeric(gdp_df.iloc[2:, 3], errors='coerce').values[mask]

# Define colors
color_ets1 = '#FF8C00'  # Bright Orange (Dark Orange)
color_ets2 = '#2E8B57'  # Vivid medium green (Sea Green)

# Calculate percentage differences from BAU
gdp_ets1_pct = ((gdp_ets1 - gdp_bau) / gdp_bau) * 100
gdp_ets2_pct = ((gdp_ets2 - gdp_bau) / gdp_bau) * 100

# Create figure
fig, ax = plt.subplots(figsize=(14, 6))

# Plot lines
ax.plot(years, gdp_ets1_pct, label='ETS1 vs BAU',
        color=color_ets1, linewidth=2.5)
ax.plot(years, gdp_ets2_pct, label='ETS2 vs BAU',
        color=color_ets2, linewidth=2.5)

# Add horizontal line at zero
ax.axhline(y=0, color='gray', linestyle='--', linewidth=1, alpha=0.5)

# Formatting
ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('GDP Difference (%)', fontsize=13, fontweight='bold')
ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--')

# Set x-axis limits and ticks
ax.set_xlim(2021, 2040)
ax.set_xticks([2021, 2025, 2030, 2035, 2040])

# Add summary statistics box
idx_2040 = np.where(years == 2040)[0][0]
summary_text = (
    f'Summary Statistics (2040):\n'
    f'ETS1: €{gdp_ets1[idx_2040]:.0f}B ({gdp_ets1_pct[idx_2040]:.2f}%)\n'
    f'ETS2: €{gdp_ets2[idx_2040]:.0f}B ({gdp_ets2_pct[idx_2040]:.2f}%)\n'
    f'BAU: €{gdp_bau[idx_2040]:.0f}B'
)
ax.text(0.05, 0.05, summary_text, transform=ax.transAxes,
        fontsize=10, verticalalignment='bottom',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.tight_layout()

# Save
plt.savefig('results/Single_Plot_GDP_Impact.png', bbox_inches='tight', dpi=300)
plt.savefig('results/Single_Plot_GDP_Impact.pdf', bbox_inches='tight')
print("✓ GDP impact plot saved!")
print("  - results/Single_Plot_GDP_Impact.png")
print("  - results/Single_Plot_GDP_Impact.pdf")

# Print summary statistics
print("\n" + "="*80)
print("GDP IMPACT RELATIVE TO BAU (% DIFFERENCE)")
print("="*80)
print(f"{'Year':<8} {'ETS1 (%)':>12} {'ETS2 (%)':>12} {'ETS1 GDP (B€)':>15} {'ETS2 GDP (B€)':>15}")
print("-"*80)

# Print selected years
selected_years = [2021, 2025, 2030, 2035, 2040]
for year in selected_years:
    if year in years:
        idx = np.where(years == year)[0][0]
        print(f"{year:<8} {gdp_ets1_pct[idx]:>12.2f} {gdp_ets2_pct[idx]:>12.2f} "
              f"{gdp_ets1[idx]:>15.1f} {gdp_ets2[idx]:>15.1f}")

print("="*80)

# Additional statistics
print("\nCUMULATIVE GDP IMPACT (2021-2040):")
print("-"*80)
cumulative_loss_ets1 = np.sum(gdp_bau - gdp_ets1)
cumulative_loss_ets2 = np.sum(gdp_bau - gdp_ets2)
print(f"ETS1: €{cumulative_loss_ets1:,.1f}B total GDP loss")
print(f"ETS2: €{cumulative_loss_ets2:,.1f}B total GDP loss")

print("\nMAXIMUM GDP IMPACT:")
print("-"*80)
max_impact_ets1 = np.min(gdp_ets1_pct)
max_impact_ets2 = np.nanmin(gdp_ets2_pct)
year_max_ets1 = years[np.argmin(gdp_ets1_pct)]
year_max_ets2 = years[np.nanargmin(gdp_ets2_pct)]
print(f"ETS1: {max_impact_ets1:.2f}% in {year_max_ets1:.0f}")
print(f"ETS2: {max_impact_ets2:.2f}% in {year_max_ets2:.0f}")
print("="*80)

plt.show()
