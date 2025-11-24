"""
Single Plot: Renewable Investment Intensity (Figure 1b)
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
print("Loading renewable investment data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251124_135016.xlsx')
renewable_inv_df = pd.read_excel(xl, 'Renewable_Investment')

# Extract data
years = pd.to_numeric(renewable_inv_df.iloc[2:, 0], errors='coerce').values
inv_share_bau = pd.to_numeric(
    renewable_inv_df.iloc[2:, 4], errors='coerce').values
inv_share_ets1 = pd.to_numeric(
    renewable_inv_df.iloc[2:, 5], errors='coerce').values
inv_share_ets2 = pd.to_numeric(
    renewable_inv_df.iloc[2:, 6], errors='coerce').values

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data - smooth lines
ax.plot(years, inv_share_bau, '-', color=colors['BAU'], linewidth=2.5,
        label='BAU', alpha=0.9)
ax.plot(years, inv_share_ets1, '-', color=colors['ETS1'], linewidth=2.5,
        label='ETS1 (Industry)', alpha=0.9)
ax.plot(years[years >= 2027], inv_share_ets2[years >= 2027], '-', color=colors['ETS2'],
        linewidth=2.5, label='ETS2 (Building & Transport)', alpha=0.9)

# Formatting
ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('Investment Share of GDP (%)', fontsize=13, fontweight='bold')
ax.legend(loc='upper left', frameon=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(2021, 2041)
ax.set_xticks([2021, 2025, 2030, 2035, 2040])

# Calculate ylim with valid data only
all_data = list(inv_share_bau) + list(inv_share_ets1) + list(inv_share_ets2)
valid_data = [d for d in all_data if pd.notna(d)]
if valid_data:
    max_val = max(valid_data)
    min_val = min(valid_data)
    ax.set_ylim(0, max_val * 1.15)

# Add annotation for ETS2 start
ax.axvline(x=2027, color='gray', linestyle='--', alpha=0.4, linewidth=1.5)
ax.text(2027, max_val * 1.08, 'ETS2 Starts',
        ha='center', fontsize=9, style='italic', color='gray')

# Add final values
if pd.notna(inv_share_bau[-1]):
    ax.text(2040.5, inv_share_bau[-1], f'{inv_share_bau[-1]:.2f}%',
            va='center', fontsize=9, color=colors['BAU'], fontweight='bold')
if pd.notna(inv_share_ets1[-1]):
    ax.text(2040.5, inv_share_ets1[-1], f'{inv_share_ets1[-1]:.2f}%',
            va='center', fontsize=9, color=colors['ETS1'], fontweight='bold')
if pd.notna(inv_share_ets2[-1]):
    ax.text(2040.5, inv_share_ets2[-1], f'{inv_share_ets2[-1]:.2f}%',
            va='center', fontsize=9, color=colors['ETS2'], fontweight='bold')

plt.tight_layout()

# Save
plt.savefig('results/Single_Plot_Investment_Intensity.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Single_Plot_Investment_Intensity.pdf',
            bbox_inches='tight')
print("✓ Renewable investment intensity plot saved!")
print("  - results/Single_Plot_Investment_Intensity.png")
print("  - results/Single_Plot_Investment_Intensity.pdf")

# Print summary
print("\n" + "="*70)
print("RENEWABLE INVESTMENT INTENSITY SUMMARY")
print("="*70)
print(f"2021 Investment Share:")
idx_2021 = 0
if pd.notna(inv_share_bau[idx_2021]):
    print(f"  BAU:  {inv_share_bau[idx_2021]:.2f}% of GDP")

print(f"\n2040 Investment Share:")
if pd.notna(inv_share_bau[-1]):
    print(f"  BAU:  {inv_share_bau[-1]:.2f}% of GDP")
if pd.notna(inv_share_ets1[-1]):
    print(f"  ETS1: {inv_share_ets1[-1]:.2f}% of GDP")
if pd.notna(inv_share_ets2[-1]):
    print(f"  ETS2: {inv_share_ets2[-1]:.2f}% of GDP")

# Calculate cumulative investment
gdp_df = pd.read_excel(xl, 'Macroeconomy_GDP')
gdp_bau = pd.to_numeric(gdp_df.iloc[:, 4], errors='coerce').values
inv_bau = pd.to_numeric(renewable_inv_df.iloc[:, 10], errors='coerce').values
inv_ets2 = pd.to_numeric(renewable_inv_df.iloc[:, 12], errors='coerce').values

cumulative_bau = sum([v for v in inv_bau if pd.notna(v)])
cumulative_ets2 = sum([v for v in inv_ets2 if pd.notna(v)])

print(f"\nCumulative Investment (2021-2040):")
print(f"  BAU:  €{cumulative_bau:.1f} billion")
print(f"  ETS2: €{cumulative_ets2:.1f} billion")
print(
    f"  Additional investment under ETS2: €{cumulative_ets2 - cumulative_bau:.1f} billion")
print("="*70)

plt.show()
