"""
Single Plot: CO2 Emissions by Source - 2021 vs 2040 (Figure 3a)
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
print("Loading CO2 emissions data by source...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251021_151832.xlsx')
sectoral_df = pd.read_excel(xl, 'CO2_Emissions_Sectoral')
households_df = pd.read_excel(xl, 'CO2_Emissions_Households')

# Extract 2021 data (BAU baseline)
row_2021_sectoral = sectoral_df[sectoral_df.iloc[:, 0] == 2021]
row_2021_households = households_df[households_df.iloc[:, 0] == 2021]

# Extract 2040 data (all scenarios)
row_2040_sectoral = sectoral_df[sectoral_df.iloc[:, 0] == 2040]
row_2040_households = households_df[households_df.iloc[:, 0] == 2040]

if not row_2021_sectoral.empty and not row_2040_sectoral.empty:
    # Define emission sources
    sources = ['Agriculture', 'Energy', 'Industry',
               'Services', 'Transport', 'Households']

    # 2021 emissions (BAU - baseline year)
    emissions_2021 = {
        'Agriculture': row_2021_sectoral.iloc[0, 1],  # BAU column
        'Energy': row_2021_sectoral.iloc[0, 4],
        'Industry': row_2021_sectoral.iloc[0, 7],
        'Services': row_2021_sectoral.iloc[0, 10],
        'Transport': row_2021_sectoral.iloc[0, 13],
        'Households': households_df[households_df.iloc[:, 0] == 2021].iloc[0, [1, 4, 7, 10, 13]].sum()
    }

    # 2040 emissions - BAU scenario
    emissions_2040_bau = {
        'Agriculture': row_2040_sectoral.iloc[0, 1],
        'Energy': row_2040_sectoral.iloc[0, 4],
        'Industry': row_2040_sectoral.iloc[0, 7],
        'Services': row_2040_sectoral.iloc[0, 10],
        'Transport': row_2040_sectoral.iloc[0, 13],
        'Households': households_df[households_df.iloc[:, 0] == 2040].iloc[0, [1, 4, 7, 10, 13]].sum()
    }

    # 2040 emissions - ETS1 scenario
    emissions_2040_ets1 = {
        'Agriculture': row_2040_sectoral.iloc[0, 2],
        'Energy': row_2040_sectoral.iloc[0, 5],
        'Industry': row_2040_sectoral.iloc[0, 8],
        'Services': row_2040_sectoral.iloc[0, 11],
        'Transport': row_2040_sectoral.iloc[0, 14],
        'Households': households_df[households_df.iloc[:, 0] == 2040].iloc[0, [2, 5, 8, 11, 14]].sum()
    }

    # 2040 emissions - ETS2 scenario
    emissions_2040_ets2 = {
        'Agriculture': row_2040_sectoral.iloc[0, 3],
        'Energy': row_2040_sectoral.iloc[0, 6],
        'Industry': row_2040_sectoral.iloc[0, 9],
        'Services': row_2040_sectoral.iloc[0, 12],
        'Transport': row_2040_sectoral.iloc[0, 15],
        'Households': households_df[households_df.iloc[:, 0] == 2040].iloc[0, [3, 6, 9, 12, 15]].sum()
    }

    # Convert to arrays
    values_2021 = [emissions_2021[s] for s in sources]
    values_2040_bau = [emissions_2040_bau[s] for s in sources]
    values_2040_ets1 = [emissions_2040_ets1[s] for s in sources]
    values_2040_ets2 = [emissions_2040_ets2[s] for s in sources]

    # Create figure with grouped bar chart
    fig, ax = plt.subplots(figsize=(16, 6))

    x = np.arange(len(sources))
    width = 0.2

    # Create bars
    bars1 = ax.bar(x - 1.5*width, values_2021, width, label='2021 (Baseline)',
                   color='#2C3E50', alpha=0.8, edgecolor='black', linewidth=0.8)
    bars2 = ax.bar(x - 0.5*width, values_2040_bau, width, label='2040 BAU',
                   color='#E74C3C', alpha=0.8, edgecolor='black', linewidth=0.8)
    bars3 = ax.bar(x + 0.5*width, values_2040_ets1, width, label='2040 ETS1 (Industry)',
                   color='#F39C12', alpha=0.8, edgecolor='black', linewidth=0.8)
    bars4 = ax.bar(x + 1.5*width, values_2040_ets2, width, label='2040 ETS2 (Building & Transport)',
                   color='#27AE60', alpha=0.8, edgecolor='black', linewidth=0.8)

    # Formatting
    ax.set_ylabel('CO₂ Emissions (MtCO₂)', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sources, fontsize=11)
    ax.legend(loc='upper right', fontsize=10, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')

    plt.tight_layout()

    # Save
    plt.savefig('results/Single_Plot_CO2_By_Source.png',
                bbox_inches='tight', dpi=300)
    plt.savefig('results/Single_Plot_CO2_By_Source.pdf', bbox_inches='tight')
    print("✓ CO2 emissions by source plot saved!")
    print("  - results/Single_Plot_CO2_By_Source.png")
    print("  - results/Single_Plot_CO2_By_Source.pdf")

    # Print summary
    print("\n" + "="*80)
    print("CO2 EMISSIONS BY SOURCE - 2021 vs 2040")
    print("="*80)
    print(f"{'Source':<15} {'2021':>12} {'2040 BAU':>12} {'2040 ETS1':>12} {'2040 ETS2':>12}")
    print(f"{'':15} {'(MtCO₂)':>12} {'(MtCO₂)':>12} {'(MtCO₂)':>12} {'(MtCO₂)':>12}")
    print("-"*80)
    for i, source in enumerate(sources):
        print(f"{source:<15} {values_2021[i]:>12.2f} {values_2040_bau[i]:>12.2f} "
              f"{values_2040_ets1[i]:>12.2f} {values_2040_ets2[i]:>12.2f}")
    print("-"*80)
    total_2021 = sum(values_2021)
    total_bau = sum(values_2040_bau)
    total_ets1 = sum(values_2040_ets1)
    total_ets2 = sum(values_2040_ets2)
    print(f"{'Total':<15} {total_2021:>12.2f} {total_bau:>12.2f} "
          f"{total_ets1:>12.2f} {total_ets2:>12.2f}")
    print("="*80)

    # Emission changes
    print("\nEMISSION CHANGES (2021 → 2040):")
    print("-"*80)
    print(f"{'Source':<15} {'BAU Change':>15} {'ETS1 Change':>15} {'ETS2 Change':>15}")
    print(f"{'':15} {'(MtCO₂)':>15} {'(MtCO₂)':>15} {'(MtCO₂)':>15}")
    print("-"*80)
    for i, source in enumerate(sources):
        change_bau = values_2040_bau[i] - values_2021[i]
        change_ets1 = values_2040_ets1[i] - values_2021[i]
        change_ets2 = values_2040_ets2[i] - values_2021[i]
        print(
            f"{source:<15} {change_bau:>14.2f} {change_ets1:>15.2f} {change_ets2:>15.2f}")
    print("-"*80)
    total_change_bau = total_bau - total_2021
    total_change_ets1 = total_ets1 - total_2021
    total_change_ets2 = total_ets2 - total_2021
    print(f"{'Total':<15} {total_change_bau:>14.2f} {total_change_ets1:>15.2f} {total_change_ets2:>15.2f}")

    # Percentage changes
    print("\n" + "="*80)
    print("PERCENTAGE CHANGES (2021 → 2040):")
    print("-"*80)
    print(f"{'Source':<15} {'BAU':>15} {'ETS1':>15} {'ETS2':>15}")
    print("-"*80)
    for i, source in enumerate(sources):
        pct_bau = (
            (values_2040_bau[i] - values_2021[i]) / values_2021[i]) * 100
        pct_ets1 = (
            (values_2040_ets1[i] - values_2021[i]) / values_2021[i]) * 100
        pct_ets2 = (
            (values_2040_ets2[i] - values_2021[i]) / values_2021[i]) * 100
        print(f"{source:<15} {pct_bau:>13.1f}% {pct_ets1:>14.1f}% {pct_ets2:>14.1f}%")
    print("-"*80)
    pct_total_bau = ((total_bau - total_2021) / total_2021) * 100
    pct_total_ets1 = ((total_ets1 - total_2021) / total_2021) * 100
    pct_total_ets2 = ((total_ets2 - total_2021) / total_2021) * 100
    print(f"{'Total':<15} {pct_total_bau:>13.1f}% {pct_total_ets1:>14.1f}% {pct_total_ets2:>14.1f}%")
    print("="*80)

    # Sectoral shares
    print("\nSECTORAL EMISSION SHARES:")
    print("-"*80)
    print(f"{'Source':<15} {'2021':>15} {'2040 BAU':>15} {'2040 ETS1':>15} {'2040 ETS2':>15}")
    print("-"*80)
    for i, source in enumerate(sources):
        share_2021 = (values_2021[i] / total_2021) * 100
        share_bau = (values_2040_bau[i] / total_bau) * 100
        share_ets1 = (values_2040_ets1[i] / total_ets1) * 100
        share_ets2 = (values_2040_ets2[i] / total_ets2) * 100
        print(f"{source:<15} {share_2021:>13.1f}% {share_bau:>14.1f}% "
              f"{share_ets1:>14.1f}% {share_ets2:>14.1f}%")
    print("="*80)

    plt.show()

else:
    print("Error: Data not found for 2021 or 2040.")
