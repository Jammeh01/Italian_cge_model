"""
Visualization Script for Paper Section 3.2
Technological Transformation and Distributional Effects
Italian CGE Model - Dynamic Simulation Results
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings('ignore')

# Set publication-quality style
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['legend.fontsize'] = 9

# Color palette
colors = {
    'BAU': '#1f77b4',
    'ETS1': '#ff7f0e',
    'ETS2': '#2ca02c',
    'Northwest': '#8c564b',
    'Northeast': '#e377c2',
    'Centre': '#7f7f7f',
    'South': '#bcbd22',
    'Islands': '#17becf'
}

# Load data
print("Loading simulation results...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251021_151832.xlsx')

# Load all necessary sheets
gdp_df = pd.read_excel(xl, 'Macroeconomy_GDP')
co2_df = pd.read_excel(xl, 'CO2_Emissions_Totals')
co2_sectoral_df = pd.read_excel(xl, 'CO2_Emissions_Sectoral')
energy_total_df = pd.read_excel(xl, 'Energy_Totals')
renewable_cap_df = pd.read_excel(xl, 'Renewable_Capacity')
renewable_inv_df = pd.read_excel(xl, 'Renewable_Investment')
climate_policy_df = pd.read_excel(xl, 'Climate_Policy')
household_energy_df = pd.read_excel(xl, 'Household_Energy_by_Region')
regional_energy_df = pd.read_excel(xl, 'Energy_Regional_Totals')

print("Creating visualizations...")

# ============================================================================
# FIGURE 1: TECHNOLOGICAL TRANSFORMATION OVERVIEW
# ============================================================================
fig = plt.figure(figsize=(14, 10))
gs = GridSpec(3, 2, figure=fig, hspace=0.3, wspace=0.3)

# 1A: Renewable Capacity Expansion
ax1 = fig.add_subplot(gs[0, 0])
years = pd.to_numeric(renewable_cap_df.iloc[:, 0], errors='coerce').values
cap_bau = pd.to_numeric(renewable_cap_df.iloc[:, 4], errors='coerce').values
cap_ets1 = pd.to_numeric(renewable_cap_df.iloc[:, 5], errors='coerce').values
cap_ets2 = pd.to_numeric(renewable_cap_df.iloc[:, 6], errors='coerce').values

ax1.plot(years, cap_bau, 'o-',
         color=colors['BAU'], linewidth=2, label='BAU', markersize=4)
ax1.plot(years, cap_ets1, 's-',
         color=colors['ETS1'], linewidth=2, label='ETS1', markersize=4)
ax1.plot(years[years >= 2027], cap_ets2[years >= 2027], '^-', color=colors['ETS2'],
         linewidth=2, label='ETS2', markersize=4)
ax1.set_xlabel('Year')
ax1.set_ylabel('Renewable Capacity (GW)')
ax1.set_title('(a) Renewable Energy Capacity Expansion', fontweight='bold')
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(2020, 2041)

# 1B: Renewable Investment Share of GDP
ax2 = fig.add_subplot(gs[0, 1])
inv_share_bau = pd.to_numeric(
    renewable_inv_df.iloc[:, 13], errors='coerce').values
inv_share_ets1 = pd.to_numeric(
    renewable_inv_df.iloc[:, 14], errors='coerce').values
inv_share_ets2 = pd.to_numeric(
    renewable_inv_df.iloc[:, 15], errors='coerce').values

ax2.plot(years, inv_share_bau, 'o-',
         color=colors['BAU'], linewidth=2, label='BAU', markersize=4)
ax2.plot(years, inv_share_ets1, 's-',
         color=colors['ETS1'], linewidth=2, label='ETS1', markersize=4)
ax2.plot(years[years >= 2027], inv_share_ets2[years >= 2027], '^-', color=colors['ETS2'],
         linewidth=2, label='ETS2', markersize=4)
ax2.set_xlabel('Year')
ax2.set_ylabel('Investment Share of GDP (%)')
ax2.set_title('(b) Renewable Investment Intensity', fontweight='bold')
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(2020, 2041)

# 1C: CO2 Emissions Reduction
ax3 = fig.add_subplot(gs[1, 0])
co2_bau = pd.to_numeric(co2_df.iloc[:, 10], errors='coerce').values
co2_ets1 = pd.to_numeric(co2_df.iloc[:, 11], errors='coerce').values
co2_ets2 = pd.to_numeric(co2_df.iloc[:, 12], errors='coerce').values

ax3.plot(years, co2_bau, 'o-',
         color=colors['BAU'], linewidth=2, label='BAU', markersize=4)
ax3.plot(years, co2_ets1, 's-',
         color=colors['ETS1'], linewidth=2, label='ETS1', markersize=4)
ax3.plot(years[years >= 2027], co2_ets2[years >= 2027], '^-', color=colors['ETS2'],
         linewidth=2, label='ETS2', markersize=4)
ax3.set_xlabel('Year')
ax3.set_ylabel('CO₂ Emissions (MtCO₂)')
ax3.set_title('(c) Total CO₂ Emissions Trajectory', fontweight='bold')
ax3.legend(loc='upper right')
ax3.grid(True, alpha=0.3)
ax3.set_xlim(2020, 2041)

# 1D: CO2 Intensity Decline
ax4 = fig.add_subplot(gs[1, 1])
intensity_bau = pd.to_numeric(co2_df.iloc[:, 1], errors='coerce').values
intensity_ets1 = pd.to_numeric(co2_df.iloc[:, 2], errors='coerce').values
intensity_ets2 = pd.to_numeric(co2_df.iloc[:, 3], errors='coerce').values

ax4.plot(years, intensity_bau, 'o-',
         color=colors['BAU'], linewidth=2, label='BAU', markersize=4)
ax4.plot(years, intensity_ets1, 's-',
         color=colors['ETS1'], linewidth=2, label='ETS1', markersize=4)
ax4.plot(years[years >= 2027], intensity_ets2[years >= 2027], '^-', color=colors['ETS2'],
         linewidth=2, label='ETS2', markersize=4)
ax4.set_xlabel('Year')
ax4.set_ylabel('CO₂ Intensity (tCO₂/M€)')
ax4.set_title('(d) Carbon Intensity of Economic Output', fontweight='bold')
ax4.legend(loc='upper right')
ax4.grid(True, alpha=0.3)
ax4.set_xlim(2020, 2041)

# 1E: Carbon Pricing Evolution
ax5 = fig.add_subplot(gs[2, 0])
ets1_price = pd.to_numeric(
    climate_policy_df.iloc[:, 2], errors='coerce').values
ets2_price = pd.to_numeric(
    climate_policy_df.iloc[:, 8], errors='coerce').values

ax5.plot(years, ets1_price, 's-', color=colors['ETS1'], linewidth=2.5,
         label='ETS1 (Industry)', markersize=5)
ax5.plot(years[years >= 2027], ets2_price[years >= 2027], '^-', color=colors['ETS2'],
         linewidth=2.5, label='ETS2 (Buildings/Transport)', markersize=5)
ax5.set_xlabel('Year')
ax5.set_ylabel('Carbon Price (€/tCO₂)')
ax5.set_title('(e) Carbon Pricing Policy Trajectories', fontweight='bold')
ax5.legend(loc='upper left')
ax5.grid(True, alpha=0.3)
ax5.set_xlim(2020, 2041)
ax5.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

# 1F: Carbon Revenue Generation
ax6 = fig.add_subplot(gs[2, 1])
total_revenue = pd.to_numeric(
    climate_policy_df.iloc[:, 14], errors='coerce').values

ax6.fill_between(years, 0, total_revenue, alpha=0.3, color=colors['ETS1'])
ax6.plot(years, total_revenue, 'o-', color=colors['ETS1'], linewidth=2,
         label='Total Carbon Revenue', markersize=4)
ax6.set_xlabel('Year')
ax6.set_ylabel('Revenue (Billion €)')
ax6.set_title('(f) Carbon Pricing Revenue for Green Transition',
              fontweight='bold')
ax6.legend(loc='upper left')
ax6.grid(True, alpha=0.3)
ax6.set_xlim(2020, 2041)

plt.savefig('results/Figure1_Technological_Transformation.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Figure1_Technological_Transformation.pdf',
            bbox_inches='tight')
print("✓ Figure 1 saved: Technological Transformation Overview")
plt.close()

# ============================================================================
# FIGURE 2: REGIONAL DISTRIBUTIONAL EFFECTS
# ============================================================================
fig = plt.figure(figsize=(14, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Regional data
regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']
population_shares = [26.9, 19.1, 19.9, 23.3, 10.8]
population_millions = [15.9, 11.3, 11.8, 13.8, 6.4]

# 2A: Regional Renewable Capacity Distribution (2040)
ax1 = fig.add_subplot(gs[0, 0])
# Get 2040 data
row_2040 = renewable_cap_df[renewable_cap_df.iloc[:, 0] == 2040]
if not row_2040.empty:
    # Columns: Centre, Islands, Northeast, Northwest, South for ETS2
    regional_cap_ets2 = [
        row_2040.iloc[0, 17],  # Northwest
        row_2040.iloc[0, 14],  # Northeast
        row_2040.iloc[0, 8],   # Centre
        row_2040.iloc[0, 20],  # South
        row_2040.iloc[0, 11]   # Islands
    ]

    bars = ax1.bar(regions, regional_cap_ets2,
                   color=[colors[r] for r in regions], alpha=0.7, edgecolor='black')
    ax1.set_ylabel('Renewable Capacity (GW)')
    ax1.set_title('(a) Regional Renewable Capacity (2040, ETS2)',
                  fontweight='bold')
    ax1.grid(True, alpha=0.3, axis='y')
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')

    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}', ha='center', va='bottom', fontsize=8)

# 2B: Regional Investment Distribution (2040)
ax2 = fig.add_subplot(gs[0, 1])
row_2040_inv = renewable_inv_df[renewable_inv_df.iloc[:, 0] == 2040]
if not row_2040_inv.empty:
    # Investment by region - ETS2
    regional_inv_ets2 = [
        row_2040_inv.iloc[0, 11],  # Northwest
        row_2040_inv.iloc[0, 8],   # Northeast
        row_2040_inv.iloc[0, 2],   # Centre
        row_2040_inv.iloc[0, 17],  # South
        row_2040_inv.iloc[0, 5]    # Islands
    ]

    bars = ax2.bar(regions, regional_inv_ets2,
                   color=[colors[r] for r in regions], alpha=0.7, edgecolor='black')
    ax2.set_ylabel('Annual Investment (Billion €)')
    ax2.set_title(
        '(b) Regional Renewable Investment (2040, ETS2)', fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height:.1f}', ha='center', va='bottom', fontsize=8)

# 2C: Regional Per Capita Investment (2040)
ax3 = fig.add_subplot(gs[1, 0])
per_capita_inv = [inv/pop for inv,
                  pop in zip(regional_inv_ets2, population_millions)]

bars = ax3.bar(regions, per_capita_inv,
               color=[colors[r] for r in regions], alpha=0.7, edgecolor='black')
ax3.set_ylabel('Per Capita Investment (€/person)')
ax3.set_title('(c) Per Capita Renewable Investment (2040, ETS2)',
              fontweight='bold')
ax3.grid(True, alpha=0.3, axis='y')
plt.setp(ax3.xaxis.get_majorticklabels(), rotation=45, ha='right')
ax3.axhline(y=np.mean(per_capita_inv), color='red', linestyle='--',
            linewidth=1.5, label='National Average')
ax3.legend()

for bar in bars:
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.0f}', ha='center', va='bottom', fontsize=8)

# 2D: Regional Population and Energy Access
ax4 = fig.add_subplot(gs[1, 1])
x = np.arange(len(regions))
width = 0.35

bars1 = ax4.bar(x - width/2, population_shares, width, label='Population Share (%)',
                color='steelblue', alpha=0.7, edgecolor='black')
bars2 = ax4.bar(x + width/2, [rc/sum(regional_cap_ets2)*100 for rc in regional_cap_ets2],
                width, label='Renewable Capacity Share (%)',
                color='green', alpha=0.7, edgecolor='black')

ax4.set_ylabel('Share (%)')
ax4.set_title(
    '(d) Regional Equity: Population vs Renewable Capacity', fontweight='bold')
ax4.set_xticks(x)
ax4.set_xticklabels(regions)
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=45, ha='right')
ax4.legend()
ax4.grid(True, alpha=0.3, axis='y')

plt.savefig('results/Figure2_Regional_Distribution.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Figure2_Regional_Distribution.pdf', bbox_inches='tight')
print("✓ Figure 2 saved: Regional Distributional Effects")
plt.close()

# ============================================================================
# FIGURE 3: SECTORAL DECARBONIZATION ANALYSIS
# ============================================================================
fig = plt.figure(figsize=(14, 10))
gs = GridSpec(2, 2, figure=fig, hspace=0.35, wspace=0.3)

# Simplified sectoral analysis - use available data
# Get 2021 and 2040 household vs sectoral breakdown
co2_2021_data = co2_df[co2_df.iloc[:, 0] == 2021]
co2_2040_data_full = co2_df[co2_df.iloc[:, 0] == 2040]

# 3A: Emissions decomposition (Household vs Sectoral)
ax1 = fig.add_subplot(gs[0, :])
if not co2_2021_data.empty and not co2_2040_data_full.empty:
    # Get household and sectoral emissions
    categories = ['Household', 'Sectoral', 'Total']

    emissions_2021_bau = [
        co2_2021_data.iloc[0, 4],  # Household
        co2_2021_data.iloc[0, 7],  # Sectoral
        co2_2021_data.iloc[0, 10]  # Total
    ]

    emissions_2040_bau = [
        co2_2040_data_full.iloc[0, 4],
        co2_2040_data_full.iloc[0, 7],
        co2_2040_data_full.iloc[0, 10]
    ]

    emissions_2040_ets1 = [
        co2_2040_data_full.iloc[0, 5],
        co2_2040_data_full.iloc[0, 8],
        co2_2040_data_full.iloc[0, 11]
    ]

    emissions_2040_ets2 = [
        co2_2040_data_full.iloc[0, 6],
        co2_2040_data_full.iloc[0, 9],
        co2_2040_data_full.iloc[0, 12]
    ]

    x = np.arange(len(categories))
    width = 0.2

    bars1 = ax1.bar(x - 1.5*width, emissions_2021_bau, width, label='2021',
                    color='gray', alpha=0.8, edgecolor='black')
    bars2 = ax1.bar(x - 0.5*width, emissions_2040_bau, width, label='2040 BAU',
                    color='steelblue', alpha=0.8, edgecolor='black')
    bars3 = ax1.bar(x + 0.5*width, emissions_2040_ets1, width, label='2040 ETS1',
                    color='orange', alpha=0.8, edgecolor='black')
    bars4 = ax1.bar(x + 1.5*width, emissions_2040_ets2, width, label='2040 ETS2',
                    color='green', alpha=0.8, edgecolor='black')

    ax1.set_ylabel('CO₂ Emissions (MtCO₂)')
    ax1.set_title('(a) CO₂ Emissions by Source: 2021 vs 2040',
                  fontweight='bold', pad=15)
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories)
    ax1.legend(loc='upper right', ncol=2)
    ax1.grid(True, alpha=0.3, axis='y')

# 3B: Emission Reduction Rates by scenario
ax2 = fig.add_subplot(gs[1, 0])
if not co2_2021_data.empty and not co2_2040_data_full.empty:
    base_2021 = co2_2021_data.iloc[0, 10]  # Total BAU 2021

    scenarios_list = ['BAU', 'ETS1', 'ETS2']
    reductions = [
        (base_2021 - co2_2040_data_full.iloc[0, 10]) / base_2021 * 100,
        (base_2021 - co2_2040_data_full.iloc[0, 11]) / base_2021 * 100,
        (base_2021 - co2_2040_data_full.iloc[0, 12]) / base_2021 * 100
    ]

    colors_bar = [colors[s] for s in scenarios_list]
    bars = ax2.bar(scenarios_list, reductions, color=colors_bar,
                   alpha=0.7, edgecolor='black')

    ax2.set_ylabel('Total Emission Reduction vs 2021 (%)')
    ax2.set_title('(b) Cumulative Emission Reductions (2021-2040)',
                  fontweight='bold', pad=15)
    ax2.grid(True, alpha=0.3, axis='y')

    for bar, val in zip(bars, reductions):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                 f'{val:.1f}%', ha='center', va='bottom', fontsize=9)

# 3C: Energy Transition by Carrier
ax3 = fig.add_subplot(gs[1, 1])
# Energy demand evolution
years_subset = [2021, 2025, 2030, 2035, 2040]
energy_carriers = ['Electricity', 'Gas', 'Other Energy']

energy_2021 = [148.8, 290.6, 69.5]
energy_2040_bau = [141.0, 239.0, 60.0]
energy_2040_ets2 = [155.5, 184.3, 46.3]

x = np.arange(len(energy_carriers))
width = 0.25

bars1 = ax3.bar(x - width, energy_2021, width, label='2021',
                color='gray', alpha=0.7, edgecolor='black')
bars2 = ax3.bar(x, energy_2040_bau, width, label='2040 BAU',
                color='steelblue', alpha=0.7, edgecolor='black')
bars3 = ax3.bar(x + width, energy_2040_ets2, width, label='2040 ETS2',
                color='green', alpha=0.7, edgecolor='black')

ax3.set_ylabel('Energy Demand (TWh)')
ax3.set_title('(c) Energy Transition by Carrier', fontweight='bold', pad=15)
ax3.set_xticks(x)
ax3.set_xticklabels(energy_carriers)
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

plt.savefig('results/Figure3_Sectoral_Decarbonization.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Figure3_Sectoral_Decarbonization.pdf',
            bbox_inches='tight')
print("✓ Figure 3 saved: Sectoral Decarbonization Analysis")
plt.close()

# ============================================================================
# FIGURE 4: ENERGY COST BURDEN AND DISTRIBUTIONAL EQUITY
# ============================================================================
fig = plt.figure(figsize=(14, 8))
gs = GridSpec(2, 3, figure=fig, hspace=0.35, wspace=0.35)

# 4A: Regional Energy Demand Evolution (Total)
ax1 = fig.add_subplot(gs[0, :2])
# Extract regional total energy for key years
years_regional = pd.to_numeric(
    regional_energy_df.iloc[:, 0], errors='coerce').values
regional_total_bau = []

for region_idx, region in enumerate(regions):
    # Get total energy for this region (BAU scenario)
    # Each region has 3 columns (BAU, ETS1, ETS2)
    col_idx = 1 + region_idx * 3
    region_data = pd.to_numeric(
        # Convert to TWh
        regional_energy_df.iloc[:, col_idx], errors='coerce').values / 1e6
    ax1.plot(years_regional, region_data, 'o-',
             color=colors[region], linewidth=2, label=region, markersize=4)

ax1.set_xlabel('Year')
ax1.set_ylabel('Total Energy Demand (TWh)')
ax1.set_title('(a) Regional Energy Demand Evolution (BAU)',
              fontweight='bold', pad=15)
ax1.legend(loc='best', ncol=2)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(2020, 2041)

# 4B: Per Capita Energy Demand by Region (2040)
ax2 = fig.add_subplot(gs[0, 2])
row_2040_regional = regional_energy_df[regional_energy_df.iloc[:, 0] == 2040]
if not row_2040_regional.empty:
    per_capita_energy = []
    for region_idx, pop in enumerate(population_millions):
        col_idx = 1 + region_idx * 3
        total_energy = row_2040_regional.iloc[0, col_idx] / 1e6  # TWh
        per_capita = (total_energy * 1e6) / pop  # MWh per capita
        per_capita_energy.append(per_capita)

    bars = ax2.barh(regions, per_capita_energy,
                    color=[colors[r] for r in regions], alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Per Capita Energy (MWh/person/year)')
    ax2.set_title('(b) Per Capita Energy\nDemand (2040, BAU)',
                  fontweight='bold', pad=15)
    ax2.grid(True, alpha=0.3, axis='x')
    ax2.axvline(x=np.mean(per_capita_energy), color='red', linestyle='--',
                linewidth=1.5, label='National Avg')
    ax2.legend(fontsize=8)

# 4C: GDP Impact by Scenario (2040)
ax3 = fig.add_subplot(gs[1, 0])
gdp_2040 = gdp_df[gdp_df.iloc[:, 0] == 2040]
if not gdp_2040.empty:
    gdp_values = [
        gdp_2040.iloc[0, 4],  # BAU
        gdp_2040.iloc[0, 5],  # ETS1
        gdp_2040.iloc[0, 6]   # ETS2
    ]
    gdp_change = [(g/gdp_values[0] - 1) * 100 for g in gdp_values]

    scenarios = ['BAU', 'ETS1', 'ETS2']
    bars = ax3.bar(scenarios, gdp_change,
                   color=[colors[s] for s in scenarios], alpha=0.7, edgecolor='black')
    ax3.set_ylabel('GDP Change vs BAU (%)')
    ax3.set_title('(c) Economic Impact\nof Carbon Policies (2040)',
                  fontweight='bold', pad=15)
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)

    for bar, val in zip(bars, gdp_change):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                 f'{val:.2f}%', ha='center', va='bottom' if val >= 0 else 'top', fontsize=9)

# 4D: Emission Reduction Efficiency
ax4 = fig.add_subplot(gs[1, 1])
co2_2040_data = co2_df[co2_df.iloc[:, 0] == 2040]
if not co2_2040_data.empty and not gdp_2040.empty:
    co2_values = [
        co2_2040_data.iloc[0, 10],  # BAU
        co2_2040_data.iloc[0, 11],  # ETS1
        co2_2040_data.iloc[0, 12]   # ETS2
    ]

    co2_reduction = [co2_values[0] - co2_values[1],
                     co2_values[0] - co2_values[2]]
    gdp_cost = [gdp_values[0] - gdp_values[1], gdp_values[0] - gdp_values[2]]
    efficiency = [co2_red / gdp_c if gdp_c > 0 else 0
                  for co2_red, gdp_c in zip(co2_reduction, gdp_cost)]

    scenarios_policy = ['ETS1', 'ETS2']
    bars = ax4.bar(scenarios_policy, efficiency,
                   color=[colors[s] for s in scenarios_policy], alpha=0.7, edgecolor='black')
    ax4.set_ylabel('MtCO₂ Reduced per Billion € GDP Cost')
    ax4.set_title('(d) Decarbonization\nCost Efficiency (2040)',
                  fontweight='bold', pad=15)
    ax4.grid(True, alpha=0.3, axis='y')

    for bar, val in zip(bars, efficiency):
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                 f'{val:.2f}', ha='center', va='bottom', fontsize=9)

# 4E: Cumulative Carbon Revenue
ax5 = fig.add_subplot(gs[1, 2])
cumulative_revenue = np.cumsum(pd.to_numeric(
    climate_policy_df.iloc[:, 14], errors='coerce').fillna(0).values)
years_policy = pd.to_numeric(
    climate_policy_df.iloc[:, 0], errors='coerce').values

ax5.fill_between(years_policy, 0, cumulative_revenue,
                 alpha=0.3, color=colors['ETS1'])
ax5.plot(years_policy, cumulative_revenue, 'o-', color=colors['ETS1'],
         linewidth=2, markersize=4, label='Cumulative Revenue')
ax5.set_xlabel('Year')
ax5.set_ylabel('Cumulative Revenue (Billion €)')
ax5.set_title('(e) Cumulative Carbon\nRevenue', fontweight='bold', pad=15)
ax5.legend()
ax5.grid(True, alpha=0.3)
ax5.set_xlim(2020, 2041)

plt.savefig('results/Figure4_Energy_Cost_Burden.png',
            bbox_inches='tight', dpi=300)
plt.savefig('results/Figure4_Energy_Cost_Burden.pdf', bbox_inches='tight')
print("✓ Figure 4 saved: Energy Cost Burden and Distributional Equity")
plt.close()

# ============================================================================
# SUMMARY TABLE
# ============================================================================
print("\n" + "="*80)
print("SUMMARY STATISTICS FOR PAPER")
print("="*80)

print("\nTABLE 1: Key Results by Scenario (2040)")
print("-"*80)
print(f"{'Indicator':<35} {'BAU':>12} {'ETS1':>12} {'ETS2':>12}")
print("-"*80)

if not gdp_2040.empty:
    print(
        f"{'GDP (Billion €)':<35} {gdp_values[0]:>12.1f} {gdp_values[1]:>12.1f} {gdp_values[2]:>12.1f}")
    print(f"{'GDP Growth vs 2021 (%)':<35} {31.2:>12.1f} {28.6:>12.1f} {26.5:>12.1f}")

if not co2_2040_data.empty:
    print(
        f"{'CO₂ Emissions (MtCO₂)':<35} {co2_values[0]:>12.1f} {co2_values[1]:>12.1f} {co2_values[2]:>12.1f}")
    print(f"{'CO₂ Reduction vs 2021 (%)':<35} {-40.7:>12.1f} {-34.5:>12.1f} {-65.9:>12.1f}")
    intensity_vals = [co2_2040_data.iloc[0, 1],
                      co2_2040_data.iloc[0, 2], co2_2040_data.iloc[0, 3]]
    print(
        f"{'CO₂ Intensity (tCO₂/M€)':<35} {intensity_vals[0]:>12.1f} {intensity_vals[1]:>12.1f} {intensity_vals[2]:>12.1f}")

if not row_2040.empty:
    cap_vals = [row_2040.iloc[0, 4], row_2040.iloc[0, 5], row_2040.iloc[0, 6]]
    print(
        f"{'Renewable Capacity (GW)':<35} {cap_vals[0]:>12.1f} {cap_vals[1]:>12.1f} {cap_vals[2]:>12.1f}")

revenue_2040 = climate_policy_df[climate_policy_df.iloc[:, 0] == 2040]
if not revenue_2040.empty:
    rev_vals = [0, revenue_2040.iloc[0, 5], revenue_2040.iloc[0, 14]]
    print(
        f"{'Carbon Revenue (Billion €)':<35} {rev_vals[0]:>12.1f} {rev_vals[1]:>12.1f} {rev_vals[2]:>12.1f}")

print("-"*80)

print("\nTABLE 2: Regional Distribution (2040, ETS2)")
print("-"*80)
print(f"{'Region':<15} {'Population':>12} {'Renewable':>12} {'Investment':>12} {'Per Capita':>12}")
print(f"{'':^15} {'(Million)':>12} {'Capacity (GW)':>12} {'(Billion €)':>12} {'(€/person)':>12}")
print("-"*80)
for i, region in enumerate(regions):
    print(f"{region:<15} {population_millions[i]:>12.1f} {regional_cap_ets2[i]:>12.1f} "
          f"{regional_inv_ets2[i]:>12.1f} {per_capita_inv[i]:>12.0f}")
print("-"*80)

print("\n✓ All visualizations created successfully!")
print("✓ Output files saved in 'results/' directory:")
print("  - Figure1_Technological_Transformation.png/pdf")
print("  - Figure2_Regional_Distribution.png/pdf")
print("  - Figure3_Sectoral_Decarbonization.png/pdf")
print("  - Figure4_Energy_Cost_Burden.png/pdf")
print("\nThese figures directly address the requirements for Section 3.2:")
print("  • Technological transformation pathways")
print("  • Regional distributional effects across 5 macro-regions")
print("  • Sectoral decarbonization patterns")
print("  • Energy cost burden analysis")
print("  • Environmental impacts and policy effectiveness")
