"""
Single Plot: Renewable Capacity Expansion (Figure 1a)
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
print("Loading renewable capacity data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251021_151832.xlsx')
renewable_cap_df = pd.read_excel(xl, 'Renewable_Capacity')

# Extract data
years = pd.to_numeric(renewable_cap_df.iloc[:, 0], errors='coerce').values
cap_bau = pd.to_numeric(renewable_cap_df.iloc[:, 4], errors='coerce').values
cap_ets1 = pd.to_numeric(renewable_cap_df.iloc[:, 5], errors='coerce').values
cap_ets2 = pd.to_numeric(renewable_cap_df.iloc[:, 6], errors='coerce').values

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data - smooth lines without markers
ax.plot(years, cap_bau, '-', color=colors['BAU'], linewidth=2.5,
        label='BAU', alpha=0.9)
ax.plot(years, cap_ets1, '-', color=colors['ETS1'], linewidth=2.5,
        label='ETS1 (Industry)', alpha=0.9)
ax.plot(years[years >= 2027], cap_ets2[years >= 2027], '-', color=colors['ETS2'],
        linewidth=2.5, label='ETS2 (Building & Transport)', alpha=0.9)

# Formatting
ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('Renewable Capacity (GW)', fontsize=13, fontweight='bold')
ax.legend(loc='upper left', frameon=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(2020, 2041)
ax.set_xticks([2020, 2025, 2030, 2035, 2040])

# Calculate ylim with valid data only
max_cap = max([c for c in cap_ets2 if pd.notna(c)])
ax.set_ylim(0, max_cap * 1.1)

# Add annotations for key milestones
ax.axvline(x=2027, color='gray', linestyle='--', alpha=0.4, linewidth=1.5)
ax.text(2027, max_cap * 1.05, 'ETS2 Starts',
        ha='center', fontsize=9, style='italic', color='gray')

# Add final values
ax.text(2040.5, cap_bau[-1], f'{cap_bau[-1]:.0f} GW',
        va='center', fontsize=9, color=colors['BAU'], fontweight='bold')
ax.text(2040.5, cap_ets1[-1], f'{cap_ets1[-1]:.0f} GW',
        va='center', fontsize=9, color=colors['ETS1'], fontweight='bold')
ax.text(2040.5, cap_ets2[-1], f'{cap_ets2[-1]:.0f} GW',
        va='center', fontsize=9, color=colors['ETS2'], fontweight='bold')

plt.tight_layout()

# Save
plt.savefig('results/Single_Plot_Renewable_Capacity.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Single_Plot_Renewable_Capacity.pdf', bbox_inches='tight')
print("✓ Renewable capacity expansion plot saved!")
print("  - results/Single_Plot_Renewable_Capacity.png")
print("  - results/Single_Plot_Renewable_Capacity.pdf")

# Print summary
print("\n" + "="*70)
print("RENEWABLE CAPACITY SUMMARY")
print("="*70)
print(f"2021 Starting Capacity: {cap_bau[0]:.1f} GW")
print(f"\n2040 Final Capacity:")
print(
    f"  BAU:  {cap_bau[-1]:.1f} GW  ({(cap_bau[-1]/cap_bau[0]-1)*100:+.1f}%)")
print(
    f"  ETS1: {cap_ets1[-1]:.1f} GW  ({(cap_ets1[-1]/cap_bau[0]-1)*100:+.1f}%)")
print(
    f"  ETS2: {cap_ets2[-1]:.1f} GW  ({(cap_ets2[-1]/cap_bau[0]-1)*100:+.1f}%)")
print("="*70)

plt.show()
