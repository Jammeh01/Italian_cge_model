"""
Single Plot: Carbon Intensity of Economic Output (Figure 1d)
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
print("Loading carbon intensity data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251124_135016.xlsx')
co2_df = pd.read_excel(xl, 'CO2_Emissions_Totals')

# Extract data - CO2_Intensity_tCO2_per_Million_EUR columns
years = pd.to_numeric(co2_df.iloc[2:, 0], errors='coerce').values
intensity_bau = pd.to_numeric(co2_df.iloc[2:, 4], errors='coerce').values
intensity_ets1 = pd.to_numeric(co2_df.iloc[2:, 5], errors='coerce').values
intensity_ets2 = pd.to_numeric(co2_df.iloc[2:, 6], errors='coerce').values

# Create figure
fig, ax = plt.subplots(figsize=(10, 6))

# Plot data - smooth lines
ax.plot(years, intensity_bau, '-', color=colors['BAU'], linewidth=2.5,
        label='BAU', alpha=0.9)
ax.plot(years, intensity_ets1, '-', color=colors['ETS1'], linewidth=2.5,
        label='ETS1 (Industry)', alpha=0.9)
ax.plot(years[years >= 2027], intensity_ets2[years >= 2027], '-', color=colors['ETS2'],
        linewidth=2.5, label='ETS2 (Building & Transport)', alpha=0.9)

# Formatting
ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('CO₂ Intensity (tCO₂/M€)', fontsize=13, fontweight='bold')
ax.legend(loc='upper right', frameon=True, shadow=True)
ax.grid(True, alpha=0.3, linestyle='--')
ax.set_xlim(2021, 2041)
ax.set_xticks([2021, 2025, 2030, 2035, 2040])

# Calculate ylim with valid data only
all_data = list(intensity_bau) + list(intensity_ets1) + list(intensity_ets2)
valid_data = [d for d in all_data if pd.notna(d)]
if valid_data:
    max_val = max(valid_data)
    min_val = min(valid_data)
    ax.set_ylim(0, max_val * 1.1)

# Add annotation for ETS2 start
ax.axvline(x=2027, color='gray', linestyle='--', alpha=0.4, linewidth=1.5)
ax.text(2027, max_val * 1.05, 'ETS2 Starts',
        ha='center', fontsize=9, style='italic', color='gray')

# Add final values
if pd.notna(intensity_bau[-1]):
    ax.text(2040.5, intensity_bau[-1], f'{intensity_bau[-1]:.1f}',
            va='center', fontsize=9, color=colors['BAU'], fontweight='bold')
if pd.notna(intensity_ets1[-1]):
    ax.text(2040.5, intensity_ets1[-1], f'{intensity_ets1[-1]:.1f}',
            va='center', fontsize=9, color=colors['ETS1'], fontweight='bold')
if pd.notna(intensity_ets2[-1]):
    ax.text(2040.5, intensity_ets2[-1], f'{intensity_ets2[-1]:.1f}',
            va='center', fontsize=9, color=colors['ETS2'], fontweight='bold')

plt.tight_layout()

# Save
plt.savefig('results/Single_Plot_Carbon_Intensity.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Single_Plot_Carbon_Intensity.pdf', bbox_inches='tight')
print("✓ Carbon intensity plot saved!")
print("  - results/Single_Plot_Carbon_Intensity.png")
print("  - results/Single_Plot_Carbon_Intensity.pdf")

# Print summary
print("\n" + "="*70)
print("CARBON INTENSITY OF ECONOMIC OUTPUT SUMMARY")
print("="*70)

# Get 2021 baseline
idx_2021 = 0
intensity_2021 = intensity_bau[idx_2021]
if pd.notna(intensity_2021):
    print(f"2021 Baseline Intensity: {intensity_2021:.1f} tCO₂/M€")

print(f"\n2040 Carbon Intensity:")
if pd.notna(intensity_bau[-1]):
    reduction_bau = (intensity_2021 - intensity_bau[-1]) / \
        intensity_2021 * 100 if pd.notna(intensity_2021) else 0
    print(
        f"  BAU:  {intensity_bau[-1]:.1f} tCO₂/M€  ({reduction_bau:+.1f}% vs 2021)")
if pd.notna(intensity_ets1[-1]):
    reduction_ets1 = (
        intensity_2021 - intensity_ets1[-1]) / intensity_2021 * 100 if pd.notna(intensity_2021) else 0
    print(
        f"  ETS1: {intensity_ets1[-1]:.1f} tCO₂/M€  ({reduction_ets1:+.1f}% vs 2021)")
if pd.notna(intensity_ets2[-1]):
    reduction_ets2 = (
        intensity_2021 - intensity_ets2[-1]) / intensity_2021 * 100 if pd.notna(intensity_2021) else 0
    print(
        f"  ETS2: {intensity_ets2[-1]:.1f} tCO₂/M€  ({reduction_ets2:+.1f}% vs 2021)")

print(f"\nDecarbonization Rate (Annual Average):")
years_span = 2040 - 2021
if pd.notna(intensity_2021) and pd.notna(intensity_bau[-1]):
    rate_bau = ((intensity_bau[-1] / intensity_2021)
                ** (1/years_span) - 1) * 100
    print(f"  BAU:  {rate_bau:.2f}% per year")
if pd.notna(intensity_2021) and pd.notna(intensity_ets1[-1]):
    rate_ets1 = ((intensity_ets1[-1] / intensity_2021)
                 ** (1/years_span) - 1) * 100
    print(f"  ETS1: {rate_ets1:.2f}% per year")
if pd.notna(intensity_2021) and pd.notna(intensity_ets2[-1]):
    rate_ets2 = ((intensity_ets2[-1] / intensity_2021)
                 ** (1/years_span) - 1) * 100
    print(f"  ETS2: {rate_ets2:.2f}% per year")

print(f"\nIntensity Improvement vs BAU (2040):")
if pd.notna(intensity_bau[-1]) and pd.notna(intensity_ets1[-1]):
    improvement_ets1 = (
        intensity_bau[-1] - intensity_ets1[-1]) / intensity_bau[-1] * 100
    print(f"  ETS1: {improvement_ets1:.1f}% lower intensity")
if pd.notna(intensity_bau[-1]) and pd.notna(intensity_ets2[-1]):
    improvement_ets2 = (
        intensity_bau[-1] - intensity_ets2[-1]) / intensity_bau[-1] * 100
    print(f"  ETS2: {improvement_ets2:.1f}% lower intensity")

print("="*70)

plt.show()
