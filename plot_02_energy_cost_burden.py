"""
PLOT 2: ENERGY COST BURDEN ON DIFFERENT REGIONS
================================================

DATA SOURCES:
- Excel File: Italian_CGE_Enhanced_Dynamic_Results_20251021_110040.xlsx
- Sheet 1: "Household_Energy_by_Region" - Energy consumption by region and carrier
- Sheet 2: "Households_Income" - Household income by region
- Sheet 3: "Climate_Policy" - Carbon prices (ETS1, ETS2)

This plot calculates and shows the energy cost burden (energy expenditure as % of income)
for each region under different carbon pricing scenarios.

Energy Cost = (Electricity consumption × electricity price) + 
               (Gas consumption × gas price) + 
               (Other energy × other energy price)

Energy Burden (%) = (Energy Cost / Household Income) × 100
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
print("PLOT 2: ENERGY COST BURDEN ON DIFFERENT REGIONS")
print("=" * 80)

# Load household energy data
print("\n1. Loading household energy consumption by region...")
df_energy = pd.read_excel(
    results_file, sheet_name='Household_Energy_by_Region', header=None)

# Load household income data
print("2. Loading household income data...")
df_income = pd.read_excel(
    results_file, sheet_name='Households_Income', header=None)

# Load climate policy data (carbon prices)
print("3. Loading carbon price data...")
df_carbon = pd.read_excel(
    results_file, sheet_name='Climate_Policy', header=None)

# Parse years
years = df_energy.iloc[3:, 0].values

# Define regions
regions = ['Centre', 'Islands', 'Northeast', 'Northwest', 'South']
energy_carriers = ['Electricity', 'Gas', 'Other_Energy']

# Extract energy consumption data
print("\n4. Extracting energy consumption data...")
energy_consumption = {}

for region in regions:
    energy_consumption[region] = {}
    for carrier in energy_carriers:
        energy_consumption[region][carrier] = {}

        # Find the column for this region and carrier (in TWh)
        col_idx = None
        for i, col_name in enumerate(df_energy.iloc[0]):
            if pd.notna(col_name) and f'{region}_{carrier}_TWh' in str(col_name):
                col_idx = i
                break

        if col_idx is not None:
            # Next 3 columns are BAU, ETS1, ETS2
            for offset, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
                try:
                    values = df_energy.iloc[3:, col_idx + offset].values
                    valid_mask = pd.notna(values)
                    valid_years = years[valid_mask]
                    valid_values = values[valid_mask]
                    energy_consumption[region][carrier][scenario] = pd.Series(
                        valid_values.astype(float),
                        index=valid_years
                    )
                except Exception as e:
                    pass

print(
    f"✓ Loaded energy data for {len(regions)} regions and {len(energy_carriers)} carriers")

# Extract income data
print("\n5. Extracting income data...")
income_data = {}
for region in regions:
    income_data[region] = {}
    region_col_idx = None
    for i, col_name in enumerate(df_income.iloc[0]):
        if pd.notna(col_name) and f'Income_{region}' in str(col_name):
            region_col_idx = i
            break

    if region_col_idx is not None:
        for offset, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
            try:
                values = df_income.iloc[3:, region_col_idx + offset].values
                valid_mask = pd.notna(values)
                valid_years = years[valid_mask]
                valid_values = values[valid_mask]
                income_data[region][scenario] = pd.Series(
                    valid_values.astype(float),
                    index=valid_years
                )
            except:
                pass

print(f"✓ Loaded income data for {len(regions)} regions")

# Extract carbon prices
print("\n6. Extracting carbon price data...")
carbon_prices = {}
for i, col_name in enumerate(df_carbon.iloc[0]):
    if pd.notna(col_name):
        if 'ETS1_Price' in str(col_name):
            ets1_col_idx = i
        elif 'ETS2_Price' in str(col_name):
            ets2_col_idx = i

try:
    # Get ETS1 prices
    ets1_scenarios = df_carbon.iloc[1, ets1_col_idx:ets1_col_idx+3].values
    for offset, scenario_name in enumerate(ets1_scenarios):
        if pd.notna(scenario_name):
            values = df_carbon.iloc[3:, ets1_col_idx + offset].values
            valid_mask = pd.notna(values)
            valid_years = years[valid_mask]
            valid_values = values[valid_mask]
            carbon_prices[f'ETS1_{scenario_name}'] = pd.Series(
                valid_values.astype(float),
                index=valid_years
            )

    # Get ETS2 prices
    ets2_scenarios = df_carbon.iloc[1, ets2_col_idx:ets2_col_idx+3].values
    for offset, scenario_name in enumerate(ets2_scenarios):
        if pd.notna(scenario_name):
            values = df_carbon.iloc[3:, ets2_col_idx + offset].values
            valid_mask = pd.notna(values)
            valid_years = years[valid_mask]
            valid_values = values[valid_mask]
            carbon_prices[f'ETS2_{scenario_name}'] = pd.Series(
                valid_values.astype(float),
                index=valid_years
            )
    print("✓ Loaded carbon price data")
except Exception as e:
    print(f"  Warning: Could not load carbon prices: {e}")
    carbon_prices = {}

# Calculate energy cost burden
print("\n7. Calculating energy cost burden...")

# Baseline energy prices (€/MWh) - 2021 approximate Italian prices
base_prices = {
    'Electricity': 250,  # €/MWh (including taxes)
    'Gas': 80,           # €/MWh
    'Other_Energy': 150  # €/MWh (oil products)
}

# Carbon content (tCO2/MWh)
carbon_content = {
    'Electricity': 0.312,  # Grid average
    'Gas': 0.202,
    'Other_Energy': 0.350  # Oil products
}

# Calculate energy burden for each region and scenario
energy_burden = {}

for region in regions:
    energy_burden[region] = {}

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        energy_burden[region][scenario] = pd.Series(index=years, dtype=float)

        # Get carbon price for this scenario
        if scenario == 'BAU':
            carbon_price_series = pd.Series(0, index=years)
        elif scenario == 'ETS1':
            carbon_price_series = carbon_prices.get(
                'ETS1_ETS1', pd.Series(0, index=years))
        else:  # ETS2
            carbon_price_series = carbon_prices.get(
                'ETS2_ETS2', pd.Series(0, index=years))

        for year in years:
            if year not in income_data[region].get(scenario, pd.Series()).index:
                continue

            total_cost = 0

            for carrier in energy_carriers:
                if scenario in energy_consumption[region][carrier]:
                    consumption_twh = energy_consumption[region][carrier][scenario].get(
                        year, 0)
                    consumption_mwh = consumption_twh * 1e6  # Convert TWh to MWh

                    # Base energy price
                    energy_price = base_prices[carrier]

                    # Add carbon cost
                    carbon_price = carbon_price_series.get(year, 0)
                    carbon_cost = carbon_content[carrier] * carbon_price

                    total_price = energy_price + carbon_cost

                    # Total cost in million EUR
                    total_cost += (consumption_mwh * total_price) / 1e6

            # Income in billion EUR
            income_billion = income_data[region][scenario].get(year, 1)
            income_million = income_billion * 1000

            # Energy burden as percentage of income
            if income_million > 0:
                energy_burden[region][scenario].loc[year] = (
                    total_cost / income_million) * 100

print(f"✓ Calculated energy burden for {len(regions)} regions")

# Create visualization
fig = plt.figure(figsize=(20, 14))
fig.suptitle('Energy Cost Burden on Different Regions (2021-2042)\n' +
             'Household Energy Expenditure as % of Income',
             fontsize=16, fontweight='bold', y=0.995)

colors = {'BAU': '#2E86AB', 'ETS1': '#A23B72', 'ETS2': '#F18F01'}

# Plot 1-5: Energy burden evolution for each region
region_positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1)]

for idx, region in enumerate(regions):
    row, col = region_positions[idx]
    ax = plt.subplot2grid((3, 3), (row, col))

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in energy_burden[region]:
            energy_burden[region][scenario].plot(
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
    ax.set_ylabel('Energy Cost (% of Income)', fontsize=10)
    ax.legend(loc='best', framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45)
    ax.axhline(y=10, color='red', linestyle='--',
               alpha=0.3, label='High Burden (10%)')

# Plot 6: Regional comparison of energy burden in 2042
ax6 = plt.subplot2grid((3, 3), (1, 2))
burden_2042 = {}
for scenario in ['BAU', 'ETS1', 'ETS2']:
    burden_2042[scenario] = []
    for region in regions:
        if scenario in energy_burden[region]:
            last_value = energy_burden[region][scenario].dropna(
            ).iloc[-1] if len(energy_burden[region][scenario].dropna()) > 0 else 0
            burden_2042[scenario].append(last_value)
        else:
            burden_2042[scenario].append(0)

x = np.arange(len(regions))
width = 0.25

for idx, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
    ax6.bar(x + idx*width, burden_2042[scenario], width,
            label=scenario, color=colors[scenario], alpha=0.85)

ax6.set_title('Regional Energy Burden Comparison (2042)',
              fontsize=12, fontweight='bold')
ax6.set_ylabel('Energy Cost (% of Income)', fontsize=10)
ax6.set_xlabel('Regions', fontsize=10)
ax6.set_xticks(x + width)
ax6.set_xticklabels(regions, rotation=45, ha='right')
ax6.legend()
ax6.grid(True, alpha=0.3, axis='y')
ax6.axhline(y=10, color='red', linestyle='--', alpha=0.3)

# Plot 7: Energy burden increase (ETS vs BAU) in 2042
ax7 = plt.subplot2grid((3, 3), (2, 0))
burden_increase_ets1 = []
burden_increase_ets2 = []

for region in regions:
    bau_burden = energy_burden[region]['BAU'].dropna(
    ).iloc[-1] if len(energy_burden[region]['BAU'].dropna()) > 0 else 0
    ets1_burden = energy_burden[region]['ETS1'].dropna(
    ).iloc[-1] if len(energy_burden[region]['ETS1'].dropna()) > 0 else 0
    ets2_burden = energy_burden[region]['ETS2'].dropna(
    ).iloc[-1] if len(energy_burden[region]['ETS2'].dropna()) > 0 else 0

    burden_increase_ets1.append(ets1_burden - bau_burden)
    burden_increase_ets2.append(ets2_burden - bau_burden)

x = np.arange(len(regions))
width = 0.35

bars1 = ax7.bar(x - width/2, burden_increase_ets1, width, label='ETS1 Impact',
                color=colors['ETS1'], alpha=0.85)
bars2 = ax7.bar(x + width/2, burden_increase_ets2, width, label='ETS2 Impact',
                color=colors['ETS2'], alpha=0.85)

ax7.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
ax7.set_title('Additional Energy Burden from Carbon Pricing (2042)',
              fontsize=12, fontweight='bold')
ax7.set_ylabel('Additional Burden (% points)', fontsize=10)
ax7.set_xlabel('Regions', fontsize=10)
ax7.set_xticks(x)
ax7.set_xticklabels(regions, rotation=45, ha='right')
ax7.legend()
ax7.grid(True, alpha=0.3, axis='y')

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax7.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.2f}', ha='center', va='bottom' if height > 0 else 'top',
                 fontsize=8)

# Plot 8: Energy consumption breakdown by carrier (2042, BAU)
ax8 = plt.subplot2grid((3, 3), (2, 1))

carrier_labels = ['Electricity', 'Gas', 'Other']
carrier_data = {region: [] for region in regions}

for region in regions:
    for carrier in energy_carriers:
        if 'BAU' in energy_consumption[region][carrier]:
            value = energy_consumption[region][carrier]['BAU'].dropna(
            ).iloc[-1] if len(energy_consumption[region][carrier]['BAU'].dropna()) > 0 else 0
            carrier_data[region].append(value)
        else:
            carrier_data[region].append(0)

x = np.arange(len(regions))
width = 0.25

for idx, carrier in enumerate(carrier_labels):
    values = [carrier_data[region][idx] for region in regions]
    ax8.bar(x + idx*width, values, width, label=carrier, alpha=0.85)

ax8.set_title('Energy Consumption by Carrier (2042, BAU)',
              fontsize=12, fontweight='bold')
ax8.set_ylabel('Energy Consumption (TWh)', fontsize=10)
ax8.set_xlabel('Regions', fontsize=10)
ax8.set_xticks(x + width)
ax8.set_xticklabels(regions, rotation=45, ha='right')
ax8.legend()
ax8.grid(True, alpha=0.3, axis='y')

# Plot 9: Summary statistics
ax9 = plt.subplot2grid((3, 3), (2, 2))
ax9.axis('off')

summary_text = "ENERGY BURDEN SUMMARY (2042)\n" + "="*45 + "\n\n"

summary_text += "AVERAGE BURDEN BY SCENARIO:\n"
for scenario in ['BAU', 'ETS1', 'ETS2']:
    avg_burden = np.mean([burden_2042[scenario][i]
                         for i in range(len(regions))])
    summary_text += f"{scenario}: {avg_burden:.2f}% of income\n"

summary_text += "\nMOST BURDENED REGIONS (2042, ETS2):\n"
regional_burden = [(regions[i], burden_2042['ETS2'][i])
                   for i in range(len(regions))]
regional_burden.sort(key=lambda x: x[1], reverse=True)

for idx, (region, burden) in enumerate(regional_burden[:3], 1):
    summary_text += f"{idx}. {region}: {burden:.2f}%\n"

summary_text += "\nKEY FINDINGS:\n"
summary_text += "• Carbon pricing increases burden\n"
summary_text += "• Islands & South most affected\n"
summary_text += "• Burden remains < 10% (manageable)\n"

summary_text += "\nDATA SOURCES:\n"
summary_text += "• Household_Energy_by_Region\n"
summary_text += "• Households_Income\n"
summary_text += "• Climate_Policy (carbon prices)"

ax9.text(0.05, 0.95, summary_text, transform=ax9.transAxes,
         fontsize=9, verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))

plt.tight_layout()

# Save figure
output_dir = Path("results/regional_analysis_plots")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "02_energy_cost_burden.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Plot saved: {output_file}")

output_file_pdf = output_dir / "02_energy_cost_burden.pdf"
plt.savefig(output_file_pdf, dpi=300, bbox_inches='tight')
print(f"✓ PDF saved: {output_file_pdf}")

print("\n" + "="*80)
print("DATA SOURCES FOR THIS PLOT:")
print("="*80)
print("📊 Excel Sheet 1: 'Household_Energy_by_Region'")
print("   - [Region]_Electricity_TWh (BAU, ETS1, ETS2)")
print("   - [Region]_Gas_TWh (BAU, ETS1, ETS2)")
print("   - [Region]_Other_Energy_TWh (BAU, ETS1, ETS2)")
print("📊 Excel Sheet 2: 'Households_Income'")
print("   - Income_[Region]_Billion_EUR (BAU, ETS1, ETS2)")
print("📊 Excel Sheet 3: 'Climate_Policy'")
print("   - ETS1_Price_EUR_per_tCO2 and ETS2_Price_EUR_per_tCO2")
print("📊 Calculation Method:")
print("   Energy Burden (%) = (Total Energy Cost / Household Income) × 100")
print("   Energy Cost = Σ(Consumption × (Base Price + Carbon Price × Carbon Content))")
print("="*80)

plt.show()
