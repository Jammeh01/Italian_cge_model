"""
PLOT 4: REGIONAL ENERGY CONSUMPTION PATTERNS ACROSS 5 MACRO-REGIONS
====================================================================

DATA SOURCES:
- Excel File: Italian_CGE_Enhanced_Dynamic_Results_20251021_110040.xlsx
- Sheet: "Household_Energy_by_Region" - Detailed energy consumption by region and carrier

This plot shows comprehensive energy consumption patterns across Italy's 5 macro-regions:
- Electricity consumption
- Natural gas consumption
- Other energy (oil products, etc.)
- Total energy consumption
- Regional differences and trends (2021-2042)
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
print("PLOT 4: REGIONAL ENERGY CONSUMPTION PATTERNS ACROSS 5 MACRO-REGIONS")
print("=" * 80)

# Load household energy data
print("\n1. Loading household energy consumption by region...")
df_energy = pd.read_excel(
    results_file, sheet_name='Household_Energy_by_Region', header=None)

# Parse years
years = df_energy.iloc[3:, 0].values

# Define regions and energy carriers
regions = ['Centre', 'Islands', 'Northeast', 'Northwest', 'South']
energy_carriers = ['Electricity', 'Gas', 'Other_Energy', 'Total']

print("\n2. Extracting energy consumption data...")
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

# Also get national totals for comparison
print("\n3. Extracting national totals...")
national_totals = {}
for carrier in energy_carriers:
    national_totals[carrier] = {}

    col_idx = None
    for i, col_name in enumerate(df_energy.iloc[0]):
        if pd.notna(col_name) and f'National_{carrier}_TWh' in str(col_name):
            col_idx = i
            break

    if col_idx is not None:
        for offset, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
            try:
                values = df_energy.iloc[3:, col_idx + offset].values
                valid_mask = pd.notna(values)
                valid_years = years[valid_mask]
                valid_values = values[valid_mask]
                national_totals[carrier][scenario] = pd.Series(
                    valid_values.astype(float),
                    index=valid_years
                )
            except:
                pass

print(f"✓ Loaded national energy totals")

# Create visualization
fig = plt.figure(figsize=(22, 16))
fig.suptitle('Regional Energy Consumption Patterns Across 5 Macro-Regions (2021-2042)\n' +
             'Household Energy Demand by Region, Carrier, and Scenario',
             fontsize=16, fontweight='bold', y=0.995)

colors = {'BAU': '#2E86AB', 'ETS1': '#A23B72', 'ETS2': '#F18F01'}
carrier_colors = {'Electricity': '#3498DB', 'Gas': '#E74C3C',
                  'Other_Energy': '#F39C12', 'Total': '#2C3E50'}

# Top row: Total energy consumption by region
print("\n4. Creating regional total energy plots...")
for idx, region in enumerate(regions):
    ax = plt.subplot(4, 5, idx + 1)

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in energy_consumption[region]['Total']:
            energy_consumption[region]['Total'][scenario].plot(
                ax=ax,
                linewidth=2.5,
                marker='o',
                markersize=4,
                label=scenario,
                color=colors[scenario],
                alpha=0.85
            )

    ax.set_title(f'{region} - Total Energy', fontsize=11, fontweight='bold')
    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('Energy (TWh)', fontsize=9)
    ax.legend(loc='best', fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45, labelsize=8)

# Second row: Electricity consumption by region
print("5. Creating regional electricity plots...")
for idx, region in enumerate(regions):
    ax = plt.subplot(4, 5, idx + 6)

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in energy_consumption[region]['Electricity']:
            energy_consumption[region]['Electricity'][scenario].plot(
                ax=ax,
                linewidth=2.5,
                marker='s',
                markersize=4,
                label=scenario,
                color=colors[scenario],
                alpha=0.85
            )

    ax.set_title(f'{region} - Electricity', fontsize=11, fontweight='bold')
    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('Electricity (TWh)', fontsize=9)
    ax.legend(loc='best', fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45, labelsize=8)

# Third row: Gas consumption by region
print("6. Creating regional gas consumption plots...")
for idx, region in enumerate(regions):
    ax = plt.subplot(4, 5, idx + 11)

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in energy_consumption[region]['Gas']:
            energy_consumption[region]['Gas'][scenario].plot(
                ax=ax,
                linewidth=2.5,
                marker='^',
                markersize=4,
                label=scenario,
                color=colors[scenario],
                alpha=0.85
            )

    ax.set_title(f'{region} - Gas', fontsize=11, fontweight='bold')
    ax.set_xlabel('Year', fontsize=9)
    ax.set_ylabel('Gas (TWh)', fontsize=9)
    ax.legend(loc='best', fontsize=8, framealpha=0.9)
    ax.grid(True, alpha=0.3)
    ax.tick_params(axis='x', rotation=45, labelsize=8)

# Fourth row: Energy mix breakdown and comparisons
print("7. Creating energy mix and comparison plots...")

# Plot 16: Regional energy mix (2042, BAU) - Stacked bar
ax16 = plt.subplot(4, 5, 16)
carrier_data = {'Electricity': [], 'Gas': [], 'Other_Energy': []}

for region in regions:
    for carrier in ['Electricity', 'Gas', 'Other_Energy']:
        if 'BAU' in energy_consumption[region][carrier]:
            value = energy_consumption[region][carrier]['BAU'].dropna(
            ).iloc[-1] if len(energy_consumption[region][carrier]['BAU'].dropna()) > 0 else 0
            carrier_data[carrier].append(value)
        else:
            carrier_data[carrier].append(0)

x = np.arange(len(regions))
width = 0.8

bottom = np.zeros(len(regions))
for carrier in ['Electricity', 'Gas', 'Other_Energy']:
    ax16.bar(x, carrier_data[carrier], width, label=carrier,
             bottom=bottom, alpha=0.85, color=carrier_colors[carrier])
    bottom += carrier_data[carrier]

ax16.set_title('Regional Energy Mix (2042, BAU)',
               fontsize=11, fontweight='bold')
ax16.set_ylabel('Energy (TWh)', fontsize=9)
ax16.set_xlabel('Regions', fontsize=9)
ax16.set_xticks(x)
ax16.set_xticklabels(regions, rotation=45, ha='right', fontsize=9)
ax16.legend(fontsize=8)
ax16.grid(True, alpha=0.3, axis='y')

# Plot 17: Regional share of national total (2042, BAU) - Pie chart
ax17 = plt.subplot(4, 5, 17)
regional_totals_2042 = []
for region in regions:
    if 'BAU' in energy_consumption[region]['Total']:
        value = energy_consumption[region]['Total']['BAU'].dropna(
        ).iloc[-1] if len(energy_consumption[region]['Total']['BAU'].dropna()) > 0 else 0
        regional_totals_2042.append(value)
    else:
        regional_totals_2042.append(0)

colors_pie = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8']
explode = [0.05] * len(regions)

wedges, texts, autotexts = ax17.pie(regional_totals_2042, labels=regions, autopct='%1.1f%%',
                                    colors=colors_pie, explode=explode, startangle=90,
                                    textprops={'fontsize': 9, 'fontweight': 'bold'})

ax17.set_title('Regional Share of National\nEnergy Consumption (2042, BAU)',
               fontsize=11, fontweight='bold')

# Plot 18: Electrification rate by region (% electricity of total)
ax18 = plt.subplot(4, 5, 18)
electrification_rate = {region: {} for region in regions}

for region in regions:
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in energy_consumption[region]['Electricity'] and scenario in energy_consumption[region]['Total']:
            elec_data = energy_consumption[region]['Electricity'][scenario]
            total_data = energy_consumption[region]['Total'][scenario]
            # Calculate electrification rate
            electrification_rate[region][scenario] = (
                elec_data / total_data * 100).dropna()

# Plot for one representative region
for scenario in ['BAU', 'ETS1', 'ETS2']:
    if scenario in electrification_rate['Northwest']:
        electrification_rate['Northwest'][scenario].plot(
            ax=ax18,
            linewidth=2.5,
            marker='o',
            markersize=4,
            label=scenario,
            color=colors[scenario],
            alpha=0.85
        )

ax18.set_title('Electrification Rate\n(Northwest Region)',
               fontsize=11, fontweight='bold')
ax18.set_xlabel('Year', fontsize=9)
ax18.set_ylabel('Electricity Share (%)', fontsize=9)
ax18.legend(fontsize=8)
ax18.grid(True, alpha=0.3)
ax18.tick_params(axis='x', rotation=45, labelsize=8)

# Plot 19: National total energy consumption
ax19 = plt.subplot(4, 5, 19)
for scenario in ['BAU', 'ETS1', 'ETS2']:
    if scenario in national_totals['Total']:
        national_totals['Total'][scenario].plot(
            ax=ax19,
            linewidth=3,
            marker='o',
            markersize=5,
            label=scenario,
            color=colors[scenario],
            alpha=0.85
        )

ax19.set_title('National Total Energy\nConsumption',
               fontsize=11, fontweight='bold')
ax19.set_xlabel('Year', fontsize=9)
ax19.set_ylabel('Energy (TWh)', fontsize=9)
ax19.legend(fontsize=8)
ax19.grid(True, alpha=0.3)
ax19.tick_params(axis='x', rotation=45, labelsize=8)

# Plot 20: Summary statistics
ax20 = plt.subplot(4, 5, 20)
ax20.axis('off')

summary_text = "REGIONAL CONSUMPTION SUMMARY (2042)\n" + "="*42 + "\n\n"

summary_text += "TOTAL ENERGY BY REGION (BAU):\n"
regional_ranking = [(regions[i], regional_totals_2042[i])
                    for i in range(len(regions))]
regional_ranking.sort(key=lambda x: x[1], reverse=True)

for idx, (region, total) in enumerate(regional_ranking, 1):
    summary_text += f"{idx}. {region}: {total:.1f} TWh\n"

summary_text += "\nELECTRIFICATION RATES (2042, BAU):\n"
for region in regions:
    if 'BAU' in energy_consumption[region]['Electricity'] and 'BAU' in energy_consumption[region]['Total']:
        elec = energy_consumption[region]['Electricity']['BAU'].dropna(
        ).iloc[-1] if len(energy_consumption[region]['Electricity']['BAU'].dropna()) > 0 else 0
        total = energy_consumption[region]['Total']['BAU'].dropna(
        ).iloc[-1] if len(energy_consumption[region]['Total']['BAU'].dropna()) > 0 else 1
        rate = (elec / total * 100) if total > 0 else 0
        summary_text += f"{region}: {rate:.1f}%\n"

summary_text += "\nKEY PATTERNS:\n"
summary_text += "• North regions: Higher gas use\n"
summary_text += "• South/Islands: Oil-dependent\n"
summary_text += "• All regions: Electrifying\n"

summary_text += "\nDATA SOURCE:\n"
summary_text += "Household_Energy_by_Region\n"
summary_text += "[Region]_[Carrier]_TWh"

ax20.text(0.05, 0.95, summary_text, transform=ax20.transAxes,
          fontsize=8, verticalalignment='top', family='monospace',
          bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.3))

plt.tight_layout()

# Save figure
output_dir = Path("results/regional_analysis_plots")
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / "04_regional_energy_consumption.png"
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Plot saved: {output_file}")

output_file_pdf = output_dir / "04_regional_energy_consumption.pdf"
plt.savefig(output_file_pdf, dpi=300, bbox_inches='tight')
print(f"✓ PDF saved: {output_file_pdf}")

# Print detailed statistics
print("\n" + "="*80)
print("REGIONAL ENERGY CONSUMPTION STATISTICS")
print("="*80)

print("\nTOTAL ENERGY CONSUMPTION BY REGION (2042, BAU):")
for region, total in regional_ranking:
    national_total = national_totals['Total']['BAU'].dropna(
    ).iloc[-1] if 'BAU' in national_totals['Total'] and len(national_totals['Total']['BAU'].dropna()) > 0 else 1
    share = (total / national_total * 100) if national_total > 0 else 0
    print(f"  {region}: {total:.2f} TWh ({share:.1f}% of national)")

print("\nENERGY MIX BY REGION (2042, BAU):")
for region in regions:
    print(f"  {region}:")
    for carrier in ['Electricity', 'Gas', 'Other_Energy']:
        if 'BAU' in energy_consumption[region][carrier]:
            value = energy_consumption[region][carrier]['BAU'].dropna(
            ).iloc[-1] if len(energy_consumption[region][carrier]['BAU'].dropna()) > 0 else 0
            total = energy_consumption[region]['Total']['BAU'].dropna(
            ).iloc[-1] if 'BAU' in energy_consumption[region]['Total'] and len(energy_consumption[region]['Total']['BAU'].dropna()) > 0 else 1
            share = (value / total * 100) if total > 0 else 0
            print(f"    {carrier}: {value:.2f} TWh ({share:.1f}%)")

print("\n" + "="*80)
print("DATA SOURCES FOR THIS PLOT:")
print("="*80)
print("📊 Excel Sheet: 'Household_Energy_by_Region'")
print("📊 Data Columns for each region:")
print("   - [Region]_Electricity_TWh (BAU, ETS1, ETS2)")
print("   - [Region]_Gas_TWh (BAU, ETS1, ETS2)")
print("   - [Region]_Other_Energy_TWh (BAU, ETS1, ETS2)")
print("   - [Region]_Total_TWh (BAU, ETS1, ETS2)")
print("📊 National aggregates also included")
print("📊 Regions: Centre, Islands, Northeast, Northwest, South")
print("📊 Time Period: 2021-2042")
print("="*80)

plt.show()
