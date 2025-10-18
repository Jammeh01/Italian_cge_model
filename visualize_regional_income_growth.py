"""
Regional Household Income Growth Visualization: 2021 vs 2040
=============================================================
Separate visualizations for BAU, ETS1, and ETS2 scenarios
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set3")


def find_latest_results_file():
    """Find the most recent Enhanced Dynamic Results file"""
    results_dir = "results"
    if os.path.exists(results_dir):
        excel_files = [f for f in os.listdir(results_dir)
                       if f.startswith("Italian_CGE_Enhanced_Dynamic_Results_") and f.endswith(".xlsx")]
        if excel_files:
            excel_files.sort(reverse=True)
            return os.path.join(results_dir, excel_files[0])
    return None


def load_regional_household_income(excel_file):
    """Load regional household income data"""
    print(f"Loading regional household income data from: {excel_file}")

    hh_income = pd.read_excel(excel_file, sheet_name='Households_Income')
    print(f"  Household income shape: {hh_income.shape}")

    return hh_income


def parse_regional_household_data(df, regions=['Centre', 'Islands', 'Northeast', 'Northwest', 'South']):
    """Parse regional household data by scenario"""
    scenarios_row = df.iloc[0]

    # Structure: {scenario: {region: {'years': [], 'values': []}}}
    regional_data = {scenario: {region: {} for region in regions}
                     for scenario in ['BAU', 'ETS1', 'ETS2']}

    # Get years from first column (starting from row 2)
    years = df.iloc[2:, 0].values

    # Track current region (each region has 3 consecutive columns: BAU, ETS1, ETS2)
    current_region = None
    region_col_count = 0

    for col_idx, col_name in enumerate(df.columns):
        if col_idx == 0:  # Skip Year column
            continue

        scenario = str(scenarios_row.iloc[col_idx]).strip()
        col_name_str = str(col_name)

        # Check if this is the start of a new region (BAU column with region name)
        if scenario == 'BAU':
            for region in regions:
                if region in col_name_str:
                    current_region = region
                    region_col_count = 0
                    break

        # Process data for current region
        if current_region and scenario in ['BAU', 'ETS1', 'ETS2']:
            values = df.iloc[2:, col_idx].values

            valid_mask = pd.notna(values) & pd.notna(years)

            if valid_mask.any():
                regional_data[scenario][current_region] = {
                    'years': years[valid_mask].astype(int),
                    'values': values[valid_mask].astype(float)
                }

        region_col_count += 1

    return regional_data


def create_regional_income_growth_visualization(hh_income,
                                                output_file='results/Regional_Income_Growth_All_Scenarios.png'):
    """Create separate visualizations for regional income growth by scenario"""
    print("\nCreating regional income growth visualizations...")

    regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']
    region_colors = {'Northwest': '#1f77b4', 'Northeast': '#ff7f0e',
                     'Centre': '#2ca02c', 'South': '#d62728', 'Islands': '#9467bd'}

    # Parse regional data
    income_regional = parse_regional_household_data(hh_income, regions)

    # Create figure with 3 separate subplots (one for each scenario)
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle('Regional Household Income Growth: 2021 vs 2040',
                 fontsize=18, fontweight='bold', y=1.02)

    scenarios = ['BAU', 'ETS1', 'ETS2']
    scenario_titles = {
        'BAU': 'Business as Usual (BAU)',
        'ETS1': 'ETS Phase 1 (ETS1)',
        'ETS2': 'ETS Phase 2 (ETS2)'
    }
    scenario_colors = {
        'BAU': '#5DADE2',
        'ETS1': '#E74C3C',
        'ETS2': '#F39C12'
    }

    for ax_idx, scenario in enumerate(scenarios):
        ax = axes[ax_idx]
        ax.set_title(scenario_titles[scenario],
                     fontsize=14, fontweight='bold', pad=10)

        income_2021 = []
        income_2040 = []
        valid_regions = []

        for region in regions:
            if region in income_regional[scenario] and income_regional[scenario][region]:
                data = income_regional[scenario][region]
                if len(data['values']) >= 2:
                    income_2021.append(data['values'][0])
                    income_2040.append(data['values'][-1])
                    valid_regions.append(region)

        if len(valid_regions) > 0:
            x = np.arange(len(valid_regions))
            width = 0.35

            bars1 = ax.bar(x - width/2, income_2021, width, label='2021',
                           color=scenario_colors[scenario], alpha=0.5)
            bars2 = ax.bar(x + width/2, income_2040, width, label='2040',
                           color=scenario_colors[scenario], alpha=0.9)

            ax.set_ylabel('Household Income (Billion EUR)',
                          fontsize=11, fontweight='bold')
            ax.set_xlabel('Region', fontsize=11, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(valid_regions, rotation=45, ha='right')
            ax.legend(loc='upper left', fontsize=10)
            ax.grid(True, axis='y', alpha=0.3)

            # Add growth rate labels
            for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
                if income_2021[i] > 0:
                    growth = (
                        (income_2040[i] - income_2021[i]) / income_2021[i]) * 100
                    y_pos = max(income_2021[i], income_2040[i]) * 1.05
                    ax.text(x[i], y_pos, f'+{growth:.1f}%',
                            ha='center', fontsize=9, fontweight='bold',
                            bbox=dict(boxstyle='round,pad=0.3', facecolor='white',
                                      edgecolor='gray', alpha=0.7))

            # Set consistent y-axis limits across all subplots for comparison
            if len(income_2040) > 0:
                ax.set_ylim(0, max(income_2040) * 1.15)

    # Add note
    note_text = ("Note: All data directly from Italian CGE model simulation results. Income in billion EUR.\n"
                 "Regional breakdown shows actual model outputs for Northwest, Northeast, Centre, South, and Islands.\n"
                 "ETS2 scenario starts from 2027.")
    fig.text(0.5, -0.05, note_text, ha='center', fontsize=10, style='italic')

    plt.tight_layout()

    # Save figure
    os.makedirs('results', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Visualization saved to: {output_file}")

    # Also save as PDF
    pdf_file = output_file.replace('.png', '.pdf')
    plt.savefig(pdf_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ PDF version saved to: {pdf_file}")

    plt.show()

    # Print summary statistics
    print("\n" + "="*80)
    print("REGIONAL HOUSEHOLD INCOME GROWTH SUMMARY (2021 vs 2040)")
    print("="*80)

    for scenario in scenarios:
        print(f"\n{scenario_titles[scenario]}:")
        print("-" * 60)
        for region in regions:
            if region in income_regional[scenario] and income_regional[scenario][region]:
                data = income_regional[scenario][region]
                if len(data['values']) >= 2:
                    inc_initial = data['values'][0]
                    inc_final = data['values'][-1]
                    inc_growth = ((inc_final - inc_initial) /
                                  inc_initial) * 100
                    inc_absolute = inc_final - inc_initial
                    year_start = data['years'][0]
                    year_end = data['years'][-1]
                    print(f"  {region:12s}: €{inc_initial:6.1f}B → €{inc_final:6.1f}B  "
                          f"(+€{inc_absolute:5.1f}B, +{inc_growth:5.2f}%) [{year_start}-{year_end}]")

    return fig


def create_individual_scenario_visualizations(hh_income):
    """Create separate individual files for each scenario"""
    print("\nCreating individual scenario visualizations...")

    regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']
    income_regional = parse_regional_household_data(hh_income, regions)

    scenarios = ['BAU', 'ETS1', 'ETS2']
    scenario_titles = {
        'BAU': 'Business as Usual (BAU)',
        'ETS1': 'ETS Phase 1 (ETS1)',
        'ETS2': 'ETS Phase 2 (ETS2)'
    }
    scenario_colors = {
        'BAU': '#5DADE2',
        'ETS1': '#E74C3C',
        'ETS2': '#F39C12'
    }

    for scenario in scenarios:
        fig, ax = plt.subplots(figsize=(10, 6))
        # Title removed as requested

        income_2021 = []
        income_2040 = []
        valid_regions = []
        year_start = None
        year_end = None

        for region in regions:
            if region in income_regional[scenario] and income_regional[scenario][region]:
                data = income_regional[scenario][region]
                if len(data['values']) >= 2:
                    income_2021.append(data['values'][0])
                    income_2040.append(data['values'][-1])
                    valid_regions.append(region)
                    if year_start is None:
                        year_start = data['years'][0]
                        year_end = data['years'][-1]

        if len(valid_regions) > 0:
            x = np.arange(len(valid_regions))
            width = 0.35

            label_1 = str(year_start) if year_start else '2021'
            label_2 = str(year_end) if year_end else '2040'

            bars1 = ax.bar(x - width/2, income_2021, width, label=label_1,
                           color=scenario_colors[scenario], alpha=0.5)
            bars2 = ax.bar(x + width/2, income_2040, width, label=label_2,
                           color=scenario_colors[scenario], alpha=0.9)

            ax.set_ylabel('Household Income (Billion EUR)',
                          fontsize=12, fontweight='bold')
            ax.set_xlabel('Region', fontsize=12, fontweight='bold')
            ax.set_xticks(x)
            ax.set_xticklabels(valid_regions, rotation=45, ha='right')
            ax.legend(loc='upper left', fontsize=11)
            ax.grid(True, axis='y', alpha=0.3)

            # Add growth rate labels
            for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
                if income_2021[i] > 0:
                    growth = (
                        (income_2040[i] - income_2021[i]) / income_2021[i]) * 100
                    y_pos = max(income_2021[i], income_2040[i]) * 1.05
                    ax.text(x[i], y_pos, f'+{growth:.1f}%',
                            ha='center', fontsize=10, fontweight='bold',
                            bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                                      edgecolor='gray', alpha=0.8))

            if len(income_2040) > 0:
                ax.set_ylim(0, max(income_2040) * 1.15)

        # Note removed as requested

        plt.tight_layout()

        # Save individual scenario figure
        output_file = f'results/Regional_Income_Growth_{scenario}.png'
        plt.savefig(output_file, dpi=300,
                    bbox_inches='tight', facecolor='white')
        print(f"✅ {scenario} visualization saved to: {output_file}")

        # Also save as PDF
        pdf_file = output_file.replace('.png', '.pdf')
        plt.savefig(pdf_file, dpi=300, bbox_inches='tight', facecolor='white')
        print(f"✅ {scenario} PDF saved to: {pdf_file}")

        plt.close()


def main():
    """Main execution function"""
    print("="*80)
    print("REGIONAL HOUSEHOLD INCOME GROWTH VISUALIZATION")
    print("2021 vs 2040 - All Scenarios")
    print("="*80)
    print()

    # Find latest results file
    results_file = find_latest_results_file()

    if not results_file:
        print("Error: No results file found!")
        return

    print(f"Using results file: {os.path.basename(results_file)}")
    print()

    # Load data
    hh_income = load_regional_household_income(results_file)

    # Create combined visualization (all 3 scenarios in one figure)
    fig = create_regional_income_growth_visualization(hh_income)

    # Create individual scenario visualizations
    create_individual_scenario_visualizations(hh_income)

    print("\n" + "="*80)
    print("✅ ALL VISUALIZATIONS COMPLETE")
    print("="*80)
    print("\nGenerated files:")
    print("  1. Regional_Income_Growth_All_Scenarios.png (combined view)")
    print("  2. Regional_Income_Growth_All_Scenarios.pdf (combined view)")
    print("  3. Regional_Income_Growth_BAU.png (individual)")
    print("  4. Regional_Income_Growth_BAU.pdf (individual)")
    print("  5. Regional_Income_Growth_ETS1.png (individual)")
    print("  6. Regional_Income_Growth_ETS1.pdf (individual)")
    print("  7. Regional_Income_Growth_ETS2.png (individual)")
    print("  8. Regional_Income_Growth_ETS2.pdf (individual)")


if __name__ == "__main__":
    main()
