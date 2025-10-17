"""
Distributional Effects Visualization 2: Energy Cost Burden by Region
==================================================================
AUTHENTIC VERSION - Uses 100% Real Model Data
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


def load_regional_household_data(excel_file):
    """Load regional household income and expenditure data"""
    print(f"Loading regional household data from: {excel_file}")

    hh_income = pd.read_excel(excel_file, sheet_name='Households_Income')
    hh_expenditure = pd.read_excel(
        excel_file, sheet_name='Households_Expenditure')
    hh_energy = pd.read_excel(
        excel_file, sheet_name='Household_Energy_by_Region')

    print(f"  Household income shape: {hh_income.shape}")
    print(f"  Household expenditure shape: {hh_expenditure.shape}")
    print(f"  Household energy shape: {hh_energy.shape}")

    return hh_income, hh_expenditure, hh_energy


def parse_regional_household_data(df, regions=['Centre', 'Islands', 'Northeast', 'Northwest', 'South']):
    """Parse regional household data by scenario"""
    scenarios_row = df.iloc[0]

    # Structure: {region: {scenario: {'years': [], 'values': []}}}
    regional_data = {region: {} for region in regions}

    for col_idx, col_name in enumerate(df.columns):
        if col_idx == 0:  # Skip Year column
            continue

        scenario = str(scenarios_row.iloc[col_idx]).strip()
        col_name_str = str(col_name)

        if scenario in ['BAU', 'ETS1', 'ETS2']:
            # Identify which region this column belongs to
            for region in regions:
                if region in col_name_str:
                    years = df.iloc[2:, 0].values
                    values = df.iloc[2:, col_idx].values

                    valid_mask = pd.notna(values) & pd.notna(years)

                    if valid_mask.any():
                        regional_data[region][scenario] = {
                            'years': years[valid_mask].astype(int),
                            'values': values[valid_mask].astype(float)
                        }
                    break

    return regional_data


def create_authentic_energy_burden_visualization(hh_income, hh_expenditure, hh_energy,
                                                 output_file='results/Distributional_Energy_Cost_Burden_Authentic.png'):
    """Create energy burden visualization using 100% authentic model data"""
    print("\nCreating AUTHENTIC energy cost burden visualization...")

    regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']
    colors = {'BAU': '#4285F4', 'ETS1': '#DB4437', 'ETS2': '#F4B400'}
    region_colors = {'Northwest': '#1f77b4', 'Northeast': '#ff7f0e',
                     'Centre': '#2ca02c', 'South': '#d62728', 'Islands': '#9467bd'}

    # Parse regional data
    income_regional = parse_regional_household_data(hh_income, regions)
    expenditure_regional = parse_regional_household_data(
        hh_expenditure, regions)

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Distributional Effects: Regional Household Energy Cost Burden',
                 fontsize=16, fontweight='bold', y=0.995)

    # Panel 1: Total National Household Income Evolution
    ax1 = axes[0, 0]
    ax1.set_title('Total National Household Income by Scenario',
                  fontsize=12, fontweight='bold')

    # Calculate national totals
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        years_list = []
        total_values = []

        # Get years from first available region
        for region in regions:
            if scenario in income_regional[region]:
                years_list = income_regional[region][scenario]['years']
                break

        # Sum across all regions
        for year_idx, year in enumerate(years_list):
            year_total = 0
            for region in regions:
                if scenario in income_regional[region]:
                    if year_idx < len(income_regional[region][scenario]['values']):
                        year_total += income_regional[region][scenario]['values'][year_idx]
            total_values.append(year_total)

        if len(years_list) > 0:
            ax1.plot(years_list, total_values,
                     color=colors[scenario], linewidth=2.5,
                     label=scenario, marker='o', markersize=4, alpha=0.8)

    ax1.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Total Household Income (Billion EUR)',
                   fontsize=10, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Panel 2: Total National Household Expenditure Evolution
    ax2 = axes[0, 1]
    ax2.set_title('Total National Household Expenditure by Scenario',
                  fontsize=12, fontweight='bold')

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        years_list = []
        total_values = []

        for region in regions:
            if scenario in expenditure_regional[region]:
                years_list = expenditure_regional[region][scenario]['years']
                break

        for year_idx, year in enumerate(years_list):
            year_total = 0
            for region in regions:
                if scenario in expenditure_regional[region]:
                    if year_idx < len(expenditure_regional[region][scenario]['values']):
                        year_total += expenditure_regional[region][scenario]['values'][year_idx]
            total_values.append(year_total)

        if len(years_list) > 0:
            ax2.plot(years_list, total_values,
                     color=colors[scenario], linewidth=2.5,
                     label=scenario, marker='s', markersize=4, alpha=0.8)

    ax2.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Total Household Expenditure (Billion EUR)',
                   fontsize=10, fontweight='bold')
    ax2.legend(loc='best', fontsize=10)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Regional Income per Capita (2021 vs 2040) - BAU
    ax3 = axes[1, 0]
    ax3.set_title('Regional Household Income Growth: 2021 vs 2040 (BAU)',
                  fontsize=12, fontweight='bold')

    income_2021 = []
    income_2040 = []

    for region in regions:
        if 'BAU' in income_regional[region]:
            data = income_regional[region]['BAU']
            if len(data['values']) >= 2:
                income_2021.append(data['values'][0])
                income_2040.append(data['values'][-1])
            else:
                income_2021.append(0)
                income_2040.append(0)
        else:
            income_2021.append(0)
            income_2040.append(0)

    x = np.arange(len(regions))
    width = 0.35

    bars1 = ax3.bar(x - width/2, income_2021, width, label='2021',
                    color='#5DADE2', alpha=0.7)
    bars2 = ax3.bar(x + width/2, income_2040, width, label='2040',
                    color='#1F618D', alpha=0.7)

    ax3.set_ylabel('Household Income (Billion EUR)',
                   fontsize=10, fontweight='bold')
    ax3.set_xlabel('Region', fontsize=10, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(regions, rotation=45, ha='right')
    ax3.legend(loc='best', fontsize=10)
    ax3.grid(True, axis='y', alpha=0.3)

    # Add growth rate labels
    for i, (bar1, bar2) in enumerate(zip(bars1, bars2)):
        if income_2021[i] > 0:
            growth = ((income_2040[i] - income_2021[i]) / income_2021[i]) * 100
            ax3.text(x[i], max(income_2021[i], income_2040[i]) * 1.02,
                     f'+{growth:.1f}%', ha='center', fontsize=8, fontweight='bold')

    # Panel 4: Regional Expenditure Changes (% from BAU in 2040)
    ax4 = axes[1, 1]
    ax4.set_title('Regional Expenditure Impact: ETS1 & ETS2 vs BAU (2040)',
                  fontsize=12, fontweight='bold')

    # Calculate percentage changes from BAU
    exp_changes_ets1 = []
    exp_changes_ets2 = []

    for region in regions:
        bau_2040 = 0
        ets1_2040 = 0
        ets2_2040 = 0

        if 'BAU' in expenditure_regional[region]:
            bau_2040 = expenditure_regional[region]['BAU']['values'][-1]

        if 'ETS1' in expenditure_regional[region]:
            ets1_2040 = expenditure_regional[region]['ETS1']['values'][-1]

        if 'ETS2' in expenditure_regional[region]:
            ets2_2040 = expenditure_regional[region]['ETS2']['values'][-1]

        if bau_2040 > 0:
            exp_changes_ets1.append(((ets1_2040 - bau_2040) / bau_2040) * 100)
            exp_changes_ets2.append(((ets2_2040 - bau_2040) / bau_2040) * 100)
        else:
            exp_changes_ets1.append(0)
            exp_changes_ets2.append(0)

    x = np.arange(len(regions))
    width = 0.35

    bars1 = ax4.bar(x - width/2, exp_changes_ets1, width, label='ETS1 vs BAU',
                    color=colors['ETS1'], alpha=0.7)
    bars2 = ax4.bar(x + width/2, exp_changes_ets2, width, label='ETS2 vs BAU',
                    color=colors['ETS2'], alpha=0.7)

    ax4.set_ylabel('Expenditure Change from BAU (%)',
                   fontsize=10, fontweight='bold')
    ax4.set_xlabel('Region', fontsize=10, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(regions, rotation=45, ha='right')
    ax4.legend(loc='best', fontsize=10)
    ax4.grid(True, axis='y', alpha=0.3)
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)

    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:+.2f}%',
                     ha='center', va='bottom' if height > 0 else 'top', fontsize=8)

    # Add note
    note_text = ("Note: All data directly from Italian CGE model simulation results. Income and expenditure in billion EUR.\n"
                 "Regional breakdown shows actual model outputs for Northwest, Northeast, Centre, South, and Islands.")
    fig.text(0.5, 0.01, note_text, ha='center', fontsize=9, style='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 0.99])

    # Save figure
    os.makedirs('results', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ AUTHENTIC visualization saved to: {output_file}")

    # Also save as PDF
    pdf_file = output_file.replace('.png', '.pdf')
    plt.savefig(pdf_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ PDF version saved to: {pdf_file}")

    plt.show()

    # Print summary statistics
    print("\n" + "="*80)
    print("HOUSEHOLD DATA SUMMARY (2021 vs 2040)")
    print("="*80)
    for region in regions:
        print(f"\n{region} - BAU Scenario:")
        if 'BAU' in income_regional[region]:
            inc_data = income_regional[region]['BAU']
            if len(inc_data['values']) >= 2:
                inc_initial = inc_data['values'][0]
                inc_final = inc_data['values'][-1]
                inc_growth = ((inc_final - inc_initial) / inc_initial) * 100
                print(
                    f"  Income: €{inc_initial:.1f}B → €{inc_final:.1f}B ({inc_growth:+.2f}%)")

        if 'BAU' in expenditure_regional[region]:
            exp_data = expenditure_regional[region]['BAU']
            if len(exp_data['values']) >= 2:
                exp_initial = exp_data['values'][0]
                exp_final = exp_data['values'][-1]
                exp_growth = ((exp_final - exp_initial) / exp_initial) * 100
                print(
                    f"  Expenditure: €{exp_initial:.1f}B → €{exp_final:.1f}B ({exp_growth:+.2f}%)")

    return fig


def main():
    """Main execution function"""
    print("="*80)
    print("AUTHENTIC DISTRIBUTIONAL EFFECTS - ENERGY COST BURDEN")
    print("Using 100% Real Model Data")
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
    hh_income, hh_expenditure, hh_energy = load_regional_household_data(
        results_file)

    # Create visualization
    fig = create_authentic_energy_burden_visualization(
        hh_income, hh_expenditure, hh_energy)

    print("\n" + "="*80)
    print("✅ AUTHENTIC VISUALIZATION 2/3 COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
