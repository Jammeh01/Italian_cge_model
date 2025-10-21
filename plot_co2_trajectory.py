"""
Single Plot: Total CO2 Emissions Trajectory (Figure 1c)
Italian CGE Model - Dynamic Simulation Results
"""

import pandas as pd
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

# Color palette
colors = {
    'BAU': '#1f77b4',
    'ETS1': '#ff7f0e',
    'ETS2': '#2ca02c'
}

# Load data
print("Loading CO2 emissions data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251021_151832.xlsx')
co2_df = pd.read_excel(xl, 'CO2_Emissions_Totals')

# Extract data
years = pd.to_numeric(co2_df.iloc[:, 0], errors='coerce').values
co2_bau = pd.to_numeric(co2_df.iloc[:, 10], errors='coerce').values
co2_ets1 = pd.to_numeric(co2_df.iloc[:, 11], errors='coerce').values
co2_ets2 = pd.to_numeric(co2_df.iloc[:, 12], errors='coerce').values

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data - smooth lines with fill for BAU
ax.fill_between(years, 0, co2_bau, alpha=0.15, color=colors['BAU'])
ax.plot(years, co2_bau, '-', color=colors['BAU'], linewidth=2.5,
        label='BAU', alpha=0.9)
ax.plot(years, co2_ets1, '-', color=colors['ETS1'], linewidth=2.5,
        label='ETS1 (Industry)', alpha=0.9)
ax.plot(years[years >= 2027], co2_ets2[years >= 2027], '-', color=colors['ETS2'],
        linewidth=2.5, label='ETS2 (Building & Transport)', alpha=0.9)

# Formatting
ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('CO₂ Emissions (MtCO₂)', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', frameon=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(2020, 2041)
ax.set_xticks([2020, 2025, 2030, 2035, 2040])

# Calculate ylim with valid data only
all_data = list(co2_bau) + list(co2_ets1) + list(co2_ets2)
valid_data = [d for d in all_data if pd.notna(d)]
if valid_data:
    max_val = max(valid_data)
    min_val = min(valid_data)
    ax.set_ylim(0, max_val * 1.1)

# Add annotation for ETS2 start
ax.axvline(x=2027, color='gray', linestyle='--', alpha=0.4, linewidth=1.5)
ax.text(2027, max_val * 1.05, 'ETS2 Starts',
        ha='center', fontsize=9, style='italic', color='gray')

# Add 2030 climate target reference
ax.axhline(y=max_val * 0.45, color='red',
           linestyle=':', alpha=0.5, linewidth=2)
ax.text(2021, max_val * 0.46, '2030 Target (-55%)',
        fontsize=9, style='italic', color='red')

# Add final values
if pd.notna(co2_bau[-1]):
    ax.text(2040.5, co2_bau[-1], f'{co2_bau[-1]:.1f}',
            va='center', fontsize=9, color=colors['BAU'], fontweight='bold')
if pd.notna(co2_ets1[-1]):
    ax.text(2040.5, co2_ets1[-1], f'{co2_ets1[-1]:.1f}',
            va='center', fontsize=9, color=colors['ETS1'], fontweight='bold')
if pd.notna(co2_ets2[-1]):
    ax.text(2040.5, co2_ets2[-1], f'{co2_ets2[-1]:.1f}',
            va='center', fontsize=9, color=colors['ETS2'], fontweight='bold')

plt.tight_layout()

# Save
plt.savefig('results/Single_Plot_CO2_Trajectory.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Single_Plot_CO2_Trajectory.pdf', bbox_inches='tight')
print("✓ CO2 emissions trajectory plot saved!")
print("  - results/Single_Plot_CO2_Trajectory.png")
print("  - results/Single_Plot_CO2_Trajectory.pdf")

# Print summary
print("\n" + "="*70)
print("CO2 EMISSIONS TRAJECTORY SUMMARY")
print("="*70)

# Get 2021 baseline
idx_2021 = 0
co2_2021 = co2_bau[idx_2021]
print(f"2021 Baseline Emissions: {co2_2021:.1f} MtCO₂")

print(f"\n2040 Emissions:")
if pd.notna(co2_bau[-1]):
    reduction_bau = (co2_2021 - co2_bau[-1]) / co2_2021 * 100
    print(f"  BAU:  {co2_bau[-1]:.1f} MtCO₂  ({reduction_bau:+.1f}% vs 2021)")
if pd.notna(co2_ets1[-1]):
    reduction_ets1 = (co2_2021 - co2_ets1[-1]) / co2_2021 * 100
    print(
        f"  ETS1: {co2_ets1[-1]:.1f} MtCO₂  ({reduction_ets1:+.1f}% vs 2021)")
if pd.notna(co2_ets2[-1]):
    reduction_ets2 = (co2_2021 - co2_ets2[-1]) / co2_2021 * 100
    print(
        f"  ETS2: {co2_ets2[-1]:.1f} MtCO₂  ({reduction_ets2:+.1f}% vs 2021)")

print(f"\nEmission Reductions Achieved by ETS2:")
if pd.notna(co2_bau[-1]) and pd.notna(co2_ets2[-1]):
    additional_reduction = co2_bau[-1] - co2_ets2[-1]
    print(f"  Additional reduction vs BAU: {additional_reduction:.1f} MtCO₂")
    print(f"  Total reduction vs 2021: {co2_2021 - co2_ets2[-1]:.1f} MtCO₂")

# Calculate cumulative emissions
cumulative_bau = sum([v for v in co2_bau if pd.notna(v)])
cumulative_ets2 = sum([v for v in co2_ets2 if pd.notna(v)])
print(f"\nCumulative Emissions (2021-2040):")
print(f"  BAU:  {cumulative_bau:.0f} MtCO₂")
print(f"  ETS2: {cumulative_ets2:.0f} MtCO₂")
print(
    f"  Emissions avoided by ETS2: {cumulative_bau - cumulative_ets2:.0f} MtCO₂")
print("="*70)

plt.show()
