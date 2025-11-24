"""
Single Plot: Sectoral Output Change Relative to Baseline (2040)
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
print("Loading sectoral value added data...")
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251124_135016.xlsx')
va_df = pd.read_excel(xl, 'Production_Value_Added')

# Get 2040 data
row_2040 = va_df[va_df.iloc[:, 0] == 2040]

if not row_2040.empty:
    # Extract sectoral value added for 2040
    # Columns: Year=0, then for each sector: BAU, ETS1, ETS2
    # Agriculture: BAU col 1, ETS1 col 2, ETS2 col 3
    # Industry: BAU col 4, ETS1 col 5, ETS2 col 6
    # Energy: BAU col 7, ETS1 col 8, ETS2 col 9
    # Transport: BAU col 10, ETS1 col 11, ETS2 col 12
    # Services: BAU col 13, ETS1 col 14, ETS2 col 15

    sectors = ['Agriculture', 'Industry', 'Energy', 'Transport', 'Services']

    # BAU values (baseline)
    bau_values = {
        'Agriculture': row_2040.iloc[0, 1],
        'Industry': row_2040.iloc[0, 4],
        'Energy': row_2040.iloc[0, 7],
        'Transport': row_2040.iloc[0, 10],
        'Services': row_2040.iloc[0, 13]
    }

    # ETS1 values
    ets1_values = {
        'Agriculture': row_2040.iloc[0, 2],
        'Industry': row_2040.iloc[0, 5],
        'Energy': row_2040.iloc[0, 8],
        'Transport': row_2040.iloc[0, 11],
        'Services': row_2040.iloc[0, 14]
    }

    # ETS2 values
    ets2_values = {
        'Agriculture': row_2040.iloc[0, 3],
        'Industry': row_2040.iloc[0, 6],
        'Energy': row_2040.iloc[0, 9],
        'Transport': row_2040.iloc[0, 12],
        'Services': row_2040.iloc[0, 15]
    }

    # Calculate percentage changes relative to BAU
    ets1_pct_change = [(ets1_values[s] - bau_values[s]) /
                       bau_values[s] * 100 for s in sectors]
    ets2_pct_change = [(ets2_values[s] - bau_values[s]) /
                       bau_values[s] * 100 for s in sectors]

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))

    x = np.arange(len(sectors))
    width = 0.35

    # Colors: Bright Orange for ETS1, Vivid Medium Green for ETS2
    color_ets1 = '#FF8C00'  # Bright Orange (Dark Orange)
    color_ets2 = '#2E8B57'  # Vivid Medium Green (Sea Green)

    # Create bars
    bars1 = ax.bar(x - width/2, ets1_pct_change, width,
                   label='ETS1 (Industry)', color=color_ets1,
                   alpha=0.85, edgecolor='black', linewidth=0.8)
    bars2 = ax.bar(x + width/2, ets2_pct_change, width,
                   label='ETS2 (Buildings & Transport)', color=color_ets2,
                   alpha=0.85, edgecolor='black', linewidth=0.8)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            label_y = height + (1 if height > 0 else -3)
            va = 'bottom' if height > 0 else 'top'
            ax.text(bar.get_x() + bar.get_width()/2., label_y,
                    f'{height:+.1f}%', ha='center', va=va,
                    fontsize=10, fontweight='bold')

    # Formatting
    ax.set_ylabel('Output Change Relative to Baseline (%)',
                  fontsize=13, fontweight='bold')
    ax.set_xlabel('Sector', fontsize=13, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(sectors, fontsize=12)
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.8)
    ax.legend(loc='upper right', fontsize=11, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')

    # Set y-axis limits
    y_max = max(max(ets1_pct_change), max(ets2_pct_change)) * 1.15
    y_min = min(min(ets1_pct_change), min(ets2_pct_change)) * 1.25
    ax.set_ylim(y_min, y_max)

    plt.tight_layout()

    # Save
    plt.savefig('results/Single_Plot_Sectoral_Output_Change.png',
                bbox_inches='tight', dpi=300)
    plt.savefig('results/Single_Plot_Sectoral_Output_Change.pdf',
                bbox_inches='tight')
    print("✓ Sectoral output change plot saved!")
    print("  - results/Single_Plot_Sectoral_Output_Change.png")
    print("  - results/Single_Plot_Sectoral_Output_Change.pdf")

    # Print summary
    print("\n" + "="*80)
    print("SECTORAL OUTPUT CHANGES RELATIVE TO BAU (2040)")
    print("="*80)
    print(f"{'Sector':<15} {'BAU (B€)':>12} {'ETS1 (B€)':>12} {'ETS2 (B€)':>12} {'ETS1 (%)':>10} {'ETS2 (%)':>10}")
    print("-"*80)
    for i, sector in enumerate(sectors):
        print(f"{sector:<15} {bau_values[sector]:>12.2f} {ets1_values[sector]:>12.2f} "
              f"{ets2_values[sector]:>12.2f} {ets1_pct_change[i]:>9.1f} {ets2_pct_change[i]:>9.1f}")
    print("="*80)

    # Additional analysis
    print("\nSECTORAL IMPACT SUMMARY:")
    print("-"*80)
    print("Positive Impact Sectors (ETS1):")
    for i, sector in enumerate(sectors):
        if ets1_pct_change[i] > 0:
            print(f"  - {sector}: +{ets1_pct_change[i]:.1f}%")

    print("\nNegative Impact Sectors (ETS1):")
    for i, sector in enumerate(sectors):
        if ets1_pct_change[i] < 0:
            print(f"  - {sector}: {ets1_pct_change[i]:.1f}%")

    print("\nPositive Impact Sectors (ETS2):")
    for i, sector in enumerate(sectors):
        if ets2_pct_change[i] > 0:
            print(f"  - {sector}: +{ets2_pct_change[i]:.1f}%")

    print("\nNegative Impact Sectors (ETS2):")
    for i, sector in enumerate(sectors):
        if ets2_pct_change[i] < 0:
            print(f"  - {sector}: {ets2_pct_change[i]:.1f}%")

    print("="*80)

    plt.show()

else:
    print("Error: 2040 data not found.")
