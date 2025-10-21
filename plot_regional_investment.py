"""
Single Plot: Regional Renewable Investment (2040, ETS2) - Figure 2b
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

# Get 2040 data for ETS2 scenario
row_2040_inv = renewable_inv_df[renewable_inv_df.iloc[:, 0] == 2040]

if not row_2040_inv.empty:
    # Extract regional investment (ETS2 columns)
    regional_inv_ets2 = [
        row_2040_inv.iloc[0, 11],  # Northwest
        row_2040_inv.iloc[0, 8],   # Northeast
        row_2040_inv.iloc[0, 2],   # Centre
        row_2040_inv.iloc[0, 17],  # South
        row_2040_inv.iloc[0, 5]    # Islands
    ]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bar chart
    bars = ax.bar(regions, regional_inv_ets2,
                  color=[colors[r] for r in regions],
                  alpha=0.8, edgecolor='black', linewidth=1.5)

    # Formatting
    ax.set_ylabel('Annual Investment (Billion €)',
                  fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'€{height:.2f}B', ha='center', va='bottom',
                fontsize=10, fontweight='bold')

    # Add percentage of total
    total_investment = sum(regional_inv_ets2)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        percentage = (regional_inv_ets2[i] / total_investment) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height * 0.5,
                f'{percentage:.1f}%', ha='center', va='center',
                fontsize=9, color='white', fontweight='bold')

    # Set y-axis limit
    ax.set_ylim(0, max(regional_inv_ets2) * 1.15)

    plt.tight_layout()

    # Save
    plt.savefig('results/Single_Plot_Regional_Investment.png',
                bbox_inches='tight', dpi=300)
    plt.savefig('results/Single_Plot_Regional_Investment.pdf',
                bbox_inches='tight')
    print("✓ Regional renewable investment plot saved!")
    print("  - results/Single_Plot_Regional_Investment.png")
    print("  - results/Single_Plot_Regional_Investment.pdf")

    # Print summary
    print("\n" + "="*70)
    print("REGIONAL RENEWABLE INVESTMENT (2040, ETS2)")
    print("="*70)
    print(f"{'Region':<15} {'Investment (B€)':>15} {'Share (%)':>12}")
    print("-"*70)
    for i, region in enumerate(regions):
        share = (regional_inv_ets2[i] / total_investment) * 100
        print(f"{region:<15} {regional_inv_ets2[i]:>15.2f} {share:>12.1f}")
    print("-"*70)
    print(f"{'Total Italy':<15} {total_investment:>15.2f} {100.0:>12.1f}")
    print("="*70)

    # Regional rankings
    print("\nRegional Rankings by Investment:")
    sorted_regions = sorted(zip(regions, regional_inv_ets2),
                            key=lambda x: x[1], reverse=True)
    for rank, (region, investment) in enumerate(sorted_regions, 1):
        print(f"  {rank}. {region}: €{investment:.2f} billion")

    # Per capita investment
    per_capita_inv = [inv/pop for inv,
                      pop in zip(regional_inv_ets2, population_millions)]
    print("\nPer Capita Investment (2040):")
    print(f"{'Region':<15} {'Population (M)':>15} {'Per Capita (€/person)':>25}")
    print("-"*70)
    for i, region in enumerate(regions):
        print(
            f"{region:<15} {population_millions[i]:>15.1f} {per_capita_inv[i]:>25.0f}")
    print("-"*70)
    avg_per_capita = total_investment / sum(population_millions)
    print(f"{'National Avg':<15} {sum(population_millions):>15.1f} {avg_per_capita:>25.0f}")

    # Investment intensity (per capita comparison)
    print("\nInvestment Intensity (vs National Average):")
    print(f"{'Region':<15} {'Ratio':>12}")
    print("-"*70)
    for i, region in enumerate(regions):
        ratio = per_capita_inv[i] / avg_per_capita
        print(f"{region:<15} {ratio:>12.2f}")

    # Compare to population shares
    population_shares = {'Northwest': 26.9, 'Northeast': 19.1, 'Centre': 19.9,
                         'South': 23.3, 'Islands': 10.8}
    print("\nInvestment vs Population Comparison:")
    print(f"{'Region':<15} {'Pop. Share (%)':>15} {'Inv. Share (%)':>20} {'Ratio':>10}")
    print("-"*70)
    for region, investment in zip(regions, regional_inv_ets2):
        inv_share = (investment / total_investment) * 100
        pop_share = population_shares[region]
        ratio = inv_share / pop_share
        print(f"{region:<15} {pop_share:>15.1f} {inv_share:>20.1f} {ratio:>10.2f}")

    print("="*70)

    plt.show()

else:
    print("Error: 2040 data not found in the renewable investment sheet.")
