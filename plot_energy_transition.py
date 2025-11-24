"""
Single Plot: Energy Transition by Carrier (Figure 3c)
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
print("Loading energy transition data by carrier...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251124_135016.xlsx')
energy_df = pd.read_excel(xl, 'Energy_Totals')

# Extract years and filter for 2021-2040
years = pd.to_numeric(energy_df.iloc[2:, 0], errors='coerce').values
mask = (years >= 2021) & (years <= 2040)
years = years[mask]

# Extract energy data by carrier for each scenario
# Renewables (column indices: BAU=1, ETS1=2, ETS2=3)
renewables_bau = pd.to_numeric(
    # Convert to TWh
    energy_df.iloc[2:, 1], errors='coerce').values[mask] / 1e9
renewables_ets1 = pd.to_numeric(
    energy_df.iloc[2:, 2], errors='coerce').values[mask] / 1e9
renewables_ets2 = pd.to_numeric(
    energy_df.iloc[2:, 3], errors='coerce').values[mask] / 1e9

# Gas (column indices: BAU=4, ETS1=5, ETS2=6)
gas_bau = pd.to_numeric(
    # Convert to TWh
    energy_df.iloc[2:, 4], errors='coerce').values[mask] / 1e9
gas_ets1 = pd.to_numeric(
    energy_df.iloc[2:, 5], errors='coerce').values[mask] / 1e9
gas_ets2 = pd.to_numeric(
    energy_df.iloc[2:, 6], errors='coerce').values[mask] / 1e9

# Other Energy (column indices: BAU=7, ETS1=8, ETS2=9)
other_bau = pd.to_numeric(
    # Convert to TWh
    energy_df.iloc[2:, 7], errors='coerce').values[mask] / 1e9
other_ets1 = pd.to_numeric(
    energy_df.iloc[2:, 8], errors='coerce').values[mask] / 1e9
other_ets2 = pd.to_numeric(
    energy_df.iloc[2:, 9], errors='coerce').values[mask] / 1e9

# Create figure with subplots for each scenario
fig, axes = plt.subplots(1, 3, figsize=(18, 5), sharey=True)

scenarios = ['BAU', 'ETS1 (Industry)', 'ETS2 (Building & Transport)']
renewables_data = [renewables_bau, renewables_ets1, renewables_ets2]
gas_data = [gas_bau, gas_ets1, gas_ets2]
other_data = [other_bau, other_ets1, other_ets2]

colors = {
    'Renewables': '#2ECC71',   # Green
    'Gas': '#E74C3C',          # Red
    'Other Energy': '#95A5A6'  # Gray
}

for idx, (ax, scenario) in enumerate(zip(axes, scenarios)):
    # Plot stacked area chart
    ax.fill_between(years, 0, renewables_data[idx],
                    color=colors['Renewables'], alpha=0.7, label='Renewables')
    ax.fill_between(years, renewables_data[idx],
                    renewables_data[idx] + gas_data[idx],
                    color=colors['Gas'], alpha=0.7, label='Gas')
    ax.fill_between(years, renewables_data[idx] + gas_data[idx],
                    renewables_data[idx] + gas_data[idx] + other_data[idx],
                    color=colors['Other Energy'], alpha=0.7, label='Other Energy')

    # Add vertical line at 2027 for ETS2 scenarios
    if 'ETS2' in scenario:
        ax.axvline(x=2027, color='black', linestyle='--',
                   linewidth=1.5, alpha=0.5)
        ax.text(2027, ax.get_ylim()[1] * 0.95, 'ETS2 Start',
                rotation=90, verticalalignment='top', fontsize=9, alpha=0.7)

    # Formatting
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    if idx == 0:
        ax.set_ylabel('Energy Consumption (TWh)',
                      fontsize=12, fontweight='bold')
    ax.set_title(scenario, fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(2021, 2040)
    ax.set_xticks([2021, 2025, 2030, 2035, 2040])

    # Add legend only to the last subplot
    if idx == 2:
        ax.legend(loc='upper right', fontsize=10, frameon=True, shadow=True)

plt.tight_layout()

# Save
plt.savefig('results/Single_Plot_Energy_Transition.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Single_Plot_Energy_Transition.pdf', bbox_inches='tight')
print("✓ Energy transition by carrier plot saved!")
print("  - results/Single_Plot_Energy_Transition.png")
print("  - results/Single_Plot_Energy_Transition.pdf")

# Print summary statistics
print("\n" + "="*80)
print("ENERGY CONSUMPTION BY CARRIER - 2021 vs 2040")
print("="*80)

# Get 2021 and 2040 indices
idx_2021 = np.where(years == 2021)[0][0]
idx_2040 = np.where(years == 2040)[0][0]

print(f"\n{'Carrier':<20} {'2021':>12} {'2040 BAU':>12} {'2040 ETS1':>12} {'2040 ETS2':>12}")
print(f"{'':20} {'(TWh)':>12} {'(TWh)':>12} {'(TWh)':>12} {'(TWh)':>12}")
print("-"*80)

carriers = ['Renewables', 'Gas', 'Other Energy']
data_2021 = [
    renewables_bau[idx_2021],
    gas_bau[idx_2021],
    other_bau[idx_2021]
]
data_2040_bau = [
    renewables_bau[idx_2040],
    gas_bau[idx_2040],
    other_bau[idx_2040]
]
data_2040_ets1 = [
    renewables_ets1[idx_2040],
    gas_ets1[idx_2040],
    other_ets1[idx_2040]
]
data_2040_ets2 = [
    renewables_ets2[idx_2040],
    gas_ets2[idx_2040],
    other_ets2[idx_2040]
]

for i, carrier in enumerate(carriers):
    print(f"{carrier:<20} {data_2021[i]:>12.2f} {data_2040_bau[i]:>12.2f} "
          f"{data_2040_ets1[i]:>12.2f} {data_2040_ets2[i]:>12.2f}")

print("-"*80)
total_2021 = sum(data_2021)
total_bau = sum(data_2040_bau)
total_ets1 = sum(data_2040_ets1)
total_ets2 = sum(data_2040_ets2)
print(f"{'Total':<20} {total_2021:>12.2f} {total_bau:>12.2f} "
      f"{total_ets1:>12.2f} {total_ets2:>12.2f}")
print("="*80)

# Percentage changes
print("\nPERCENTAGE CHANGES (2021 → 2040):")
print("-"*80)
print(f"{'Carrier':<20} {'BAU':>15} {'ETS1':>15} {'ETS2':>15}")
print("-"*80)
for i, carrier in enumerate(carriers):
    pct_bau = ((data_2040_bau[i] - data_2021[i]) / data_2021[i]) * 100
    pct_ets1 = ((data_2040_ets1[i] - data_2021[i]) / data_2021[i]) * 100
    pct_ets2 = ((data_2040_ets2[i] - data_2021[i]) / data_2021[i]) * 100
    print(f"{carrier:<20} {pct_bau:>13.1f}% {pct_ets1:>14.1f}% {pct_ets2:>14.1f}%")
print("-"*80)
pct_total_bau = ((total_bau - total_2021) / total_2021) * 100
pct_total_ets1 = ((total_ets1 - total_2021) / total_2021) * 100
pct_total_ets2 = ((total_ets2 - total_2021) / total_2021) * 100
print(f"{'Total':<20} {pct_total_bau:>13.1f}% {pct_total_ets1:>14.1f}% {pct_total_ets2:>14.1f}%")
print("="*80)

# Energy mix shares
print("\nENERGY MIX SHARES:")
print("-"*80)
print(f"{'Carrier':<20} {'2021':>15} {'2040 BAU':>15} {'2040 ETS1':>15} {'2040 ETS2':>15}")
print("-"*80)
for i, carrier in enumerate(carriers):
    share_2021 = (data_2021[i] / total_2021) * 100
    share_bau = (data_2040_bau[i] / total_bau) * 100
    share_ets1 = (data_2040_ets1[i] / total_ets1) * 100
    share_ets2 = (data_2040_ets2[i] / total_ets2) * 100
    print(f"{carrier:<20} {share_2021:>13.1f}% {share_bau:>14.1f}% "
          f"{share_ets1:>14.1f}% {share_ets2:>14.1f}%")
print("="*80)

plt.show()
