"""
Single Plot: Per Capita Renewable Investment by Region (2040, ETS1)
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

# Color palette for regions
colors = {
    'Northwest': '#8c564b',
    'Northeast': '#e377c2',
    'Centre': '#7f7f7f',
    'South': '#bcbd22',
    'Islands': '#17becf'
}

# Load data
print("Loading regional renewable investment data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251021_151832.xlsx')
renewable_inv_df = pd.read_excel(xl, 'Renewable_Investment')

# Regional data
regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']
population_millions = [15.9, 11.3, 11.8, 13.8, 6.4]

# Get 2040 data for ETS1 scenario
row_2040_inv = renewable_inv_df[renewable_inv_df.iloc[:, 0] == 2040]

if not row_2040_inv.empty:
    # Extract regional investment (ETS1 columns)
    regional_inv_ets1 = [
        row_2040_inv.iloc[0, 10],  # Northwest ETS1
        row_2040_inv.iloc[0, 7],   # Northeast ETS1
        row_2040_inv.iloc[0, 1],   # Centre ETS1
        row_2040_inv.iloc[0, 16],  # South ETS1
        row_2040_inv.iloc[0, 4]    # Islands ETS1
    ]

    # Calculate per capita investment
    per_capita_inv = [inv * 1000 / pop for inv,
                      pop in zip(regional_inv_ets1, population_millions)]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create horizontal bar chart
    bars = ax.barh(regions, per_capita_inv,
                   color=[colors[r] for r in regions],
                   alpha=0.8, edgecolor='black', linewidth=1.5)

    # Formatting
    ax.set_xlabel('Per Capita Investment (€/person/year)',
                  fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='x', linestyle='--')

    # Calculate national average for console output
    avg_per_capita = sum(regional_inv_ets1) * 1000 / sum(population_millions)

    # Set x-axis limit
    ax.set_xlim(0, max(per_capita_inv) * 1.15)

    plt.tight_layout()

    # Save
    plt.savefig('results/Single_Plot_Per_Capita_Investment_ETS1.png',
                bbox_inches='tight', dpi=300)
    plt.savefig('results/Single_Plot_Per_Capita_Investment_ETS1.pdf',
                bbox_inches='tight')
    print("✓ Per capita renewable investment plot (ETS1) saved!")
    print("  - results/Single_Plot_Per_Capita_Investment_ETS1.png")
    print("  - results/Single_Plot_Per_Capita_Investment_ETS1.pdf")

    # Print summary
    print("\n" + "="*70)
    print("PER CAPITA RENEWABLE INVESTMENT (2040, ETS1)")
    print("="*70)
    print(f"{'Region':<15} {'Population (M)':>15} {'Total Inv. (B€)':>18} {'Per Capita (€)':>18}")
    print("-"*70)
    for i, region in enumerate(regions):
        print(
            f"{region:<15} {population_millions[i]:>15.1f} {regional_inv_ets1[i]:>18.2f} {per_capita_inv[i]:>18,.0f}")
    print("-"*70)
    total_pop = sum(population_millions)
    total_inv = sum(regional_inv_ets1)
    print(f"{'Total Italy':<15} {total_pop:>15.1f} {total_inv:>18.2f} {avg_per_capita:>18,.0f}")
    print("="*70)

    # Rankings
    print("\nRegional Rankings by Per Capita Investment:")
    sorted_regions = sorted(zip(regions, per_capita_inv),
                            key=lambda x: x[1], reverse=True)
    for rank, (region, inv) in enumerate(sorted_regions, 1):
        ratio = inv / avg_per_capita
        print(f"  {rank}. {region}: €{inv:,.0f} ({ratio:.2f}× national average)")

    # Equity analysis
    print("\nEquity Analysis:")
    print(f"{'Region':<15} {'Ratio to National Avg':>25} {'Status':>15}")
    print("-"*70)
    for region, inv in zip(regions, per_capita_inv):
        ratio = inv / avg_per_capita
        status = "Above average" if ratio > 1 else "Below average"
        print(f"{region:<15} {ratio:>25.2f} {status:>15}")

    # Statistical measures
    print("\nStatistical Summary:")
    print(f"  Maximum: €{max(per_capita_inv):,.0f}")
    print(f"  Minimum: €{min(per_capita_inv):,.0f}")
    print(f"  Range: €{max(per_capita_inv) - min(per_capita_inv):,.0f}")
    print(
        f"  Coefficient of Variation: {np.std(per_capita_inv)/np.mean(per_capita_inv)*100:.1f}%")

    # North-South divide
    northern_inv = sum([per_capita_inv[i] * population_millions[i]
                       for i in [0, 1]]) / sum([population_millions[i] for i in [0, 1]])
    southern_inv = sum([per_capita_inv[i] * population_millions[i]
                       for i in [3, 4]]) / sum([population_millions[i] for i in [3, 4]])
    print(f"\nNorth-South Comparison:")
    print(f"  North (Northwest + Northeast): €{northern_inv:,.0f} per capita")
    print(f"  South (South + Islands): €{southern_inv:,.0f} per capita")
    print(f"  South/North ratio: {southern_inv/northern_inv:.2f}")

    # Compare to ETS2
    regional_inv_ets2 = [
        row_2040_inv.iloc[0, 11],  # Northwest ETS2
        row_2040_inv.iloc[0, 8],   # Northeast ETS2
        row_2040_inv.iloc[0, 2],   # Centre ETS2
        row_2040_inv.iloc[0, 17],  # South ETS2
        row_2040_inv.iloc[0, 5]    # Islands ETS2
    ]
    per_capita_ets2 = [inv * 1000 / pop for inv,
                       pop in zip(regional_inv_ets2, population_millions)]

    print("\nComparison: ETS1 vs ETS2 Per Capita Investment (2040):")
    print(f"{'Region':<15} {'ETS1 (€)':>15} {'ETS2 (€)':>15} {'Difference':>15}")
    print("-"*70)
    for i, region in enumerate(regions):
        diff = per_capita_ets2[i] - per_capita_inv[i]
        print(
            f"{region:<15} {per_capita_inv[i]:>15,.0f} {per_capita_ets2[i]:>15,.0f} {diff:>15,.0f}")

    print("="*70)

    plt.show()

else:
    print("Error: 2040 data not found in the renewable investment sheet.")
