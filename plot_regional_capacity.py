"""
Single Plot: Regional Renewable Capacity Distribution (2040, ETS2) - Figure 2a
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
print("Loading regional renewable capacity data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251124_135016.xlsx')
renewable_cap_df = pd.read_excel(xl, 'Renewable_Capacity')

# Regional data
regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']

# Get 2040 data for ETS2 scenario
row_2040 = renewable_cap_df[renewable_cap_df.iloc[:, 0] == 2040]

if not row_2040.empty:
    # Extract regional capacities (ETS2 columns)
    # Centre: col 9, Islands: col 12, Northeast: col 15, Northwest: col 18, South: col 21
    regional_cap_ets2 = [
        row_2040.iloc[0, 18],  # Northwest
        row_2040.iloc[0, 15],  # Northeast
        row_2040.iloc[0, 9],   # Centre
        row_2040.iloc[0, 21],  # South
        row_2040.iloc[0, 12]   # Islands
    ]

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))

    # Create bar chart
    bars = ax.bar(regions, regional_cap_ets2,
                  color=[colors[r] for r in regions],
                  alpha=0.8, edgecolor='black', linewidth=1.5)

    # Formatting
    ax.set_ylabel('Renewable Capacity (GW)', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=0, ha='center')

    # Add percentage of total
    total_capacity = sum(regional_cap_ets2)
    for i, bar in enumerate(bars):
        height = bar.get_height()
        percentage = (regional_cap_ets2[i] / total_capacity) * 100
        ax.text(bar.get_x() + bar.get_width()/2., height * 0.5,
                f'{percentage:.1f}%', ha='center', va='center',
                fontsize=9, color='white', fontweight='bold')

    # Set y-axis limit
    ax.set_ylim(0, max(regional_cap_ets2) * 1.15)

    plt.tight_layout()

    # Save
    plt.savefig('results/Single_Plot_Regional_Capacity.png',
                bbox_inches='tight', dpi=300)
    plt.savefig('results/Single_Plot_Regional_Capacity.pdf',
                bbox_inches='tight')
    print("✓ Regional renewable capacity plot saved!")
    print("  - results/Single_Plot_Regional_Capacity.png")
    print("  - results/Single_Plot_Regional_Capacity.pdf")

    # Print summary
    print("\n" + "="*70)
    print("REGIONAL RENEWABLE CAPACITY DISTRIBUTION (2040, ETS2)")
    print("="*70)
    print(f"{'Region':<15} {'Capacity (GW)':>15} {'Share (%)':>12}")
    print("-"*70)
    for i, region in enumerate(regions):
        share = (regional_cap_ets2[i] / total_capacity) * 100
        print(f"{region:<15} {regional_cap_ets2[i]:>15.1f} {share:>12.1f}")
    print("-"*70)
    print(f"{'Total Italy':<15} {total_capacity:>15.1f} {100.0:>12.1f}")
    print("="*70)

    # Regional rankings
    print("\nRegional Rankings by Capacity:")
    sorted_regions = sorted(zip(regions, regional_cap_ets2),
                            key=lambda x: x[1], reverse=True)
    for rank, (region, capacity) in enumerate(sorted_regions, 1):
        print(f"  {rank}. {region}: {capacity:.1f} GW")

    # Compare to population
    population_shares = {'Northwest': 26.9, 'Northeast': 19.1, 'Centre': 19.9,
                         'South': 23.3, 'Islands': 10.8}
    print("\nCapacity vs Population Comparison:")
    print(f"{'Region':<15} {'Pop. Share (%)':>15} {'Capacity Share (%)':>20} {'Ratio':>10}")
    print("-"*70)
    for region, capacity in zip(regions, regional_cap_ets2):
        cap_share = (capacity / total_capacity) * 100
        pop_share = population_shares[region]
        ratio = cap_share / pop_share
        print(f"{region:<15} {pop_share:>15.1f} {cap_share:>20.1f} {ratio:>10.2f}")
    print("="*70)

    plt.show()

else:
    print("Error: 2040 data not found in the renewable capacity sheet.")
