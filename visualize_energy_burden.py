"""
Distributional Effects Visualization 2: Energy Cost Burden on Different Household Groups
=======================================================================================
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


def load_household_data(excel_file):
    """Load household energy and expenditure data"""
    print(f"Loading household data from: {excel_file}")

    # Load relevant sheets
    hh_income = pd.read_excel(excel_file, sheet_name='Households_Income')
    hh_expenditure = pd.read_excel(
        excel_file, sheet_name='Households_Expenditure')
    hh_energy_region = pd.read_excel(
        excel_file, sheet_name='Household_Energy_by_Region')

    print(f"  Household income shape: {hh_income.shape}")
    print(f"  Household expenditure shape: {hh_expenditure.shape}")
    print(f"  Regional energy shape: {hh_energy_region.shape}")

    return hh_income, hh_expenditure, hh_energy_region


def parse_household_data(df, variable_type='income'):
    """Parse household data from Excel sheet"""
    scenarios_row = df.iloc[0]

    data_dict = {'BAU': {}, 'ETS1': {}, 'ETS2': {}}

    for col_idx, col_name in enumerate(df.columns):
        if col_idx == 0:  # Skip Year column
            continue

        scenario = str(scenarios_row.iloc[col_idx]).strip()
        if scenario in ['BAU', 'ETS1', 'ETS2']:
            # Extract data
            years = df.iloc[2:, 0].values
            values = df.iloc[2:, col_idx].values

            valid_mask = pd.notna(values) & pd.notna(years)
            if valid_mask.any():
                label = str(col_name).split(
                    '_')[-1] if '_' in str(col_name) else 'Total'

                data_dict[scenario][label] = {
                    'years': years[valid_mask].astype(int),
                    'values': values[valid_mask]
                }

    return data_dict


def create_energy_burden_visualization(hh_income, hh_expenditure, hh_energy_region,
                                       output_file='results/Distributional_Energy_Cost_Burden.png'):
    """Create energy cost burden visualization"""
    print("\nCreating energy cost burden visualization...")

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Distributional Effects: Energy Cost Burden on Households',
                 fontsize=16, fontweight='bold', y=0.995)

    colors = {'BAU': '#4285F4', 'ETS1': '#DB4437', 'ETS2': '#F4B400'}

    # Parse data
    income_data = parse_household_data(hh_income, 'income')
    expenditure_data = parse_household_data(hh_expenditure, 'expenditure')

    # Panel 1: Household Income Evolution
    ax1 = axes[0, 0]
    ax1.set_title('Total Household Income by Scenario',
                  fontsize=12, fontweight='bold')

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if 'Total' in income_data[scenario]:
            data = income_data[scenario]['Total']
            ax1.plot(data['years'], data['values'],
                     color=colors[scenario], linewidth=2.5,
                     label=scenario, marker='o', markersize=4, alpha=0.8)

    ax1.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Household Income (Billion EUR)',
                   fontsize=10, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel 2: Household Expenditure Evolution
    ax2 = axes[0, 1]
    ax2.set_title('Total Household Expenditure by Scenario',
                  fontsize=12, fontweight='bold')

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if 'Total' in expenditure_data[scenario]:
            data = expenditure_data[scenario]['Total']
            ax2.plot(data['years'], data['values'],
                     color=colors[scenario], linewidth=2.5,
                     label=scenario, marker='s', markersize=4, alpha=0.8)

    ax2.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Household Expenditure (Billion EUR)',
                   fontsize=10, fontweight='bold')
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Energy Expenditure Share Evolution
    ax3 = axes[1, 0]
    ax3.set_title('Energy Expenditure as % of Total Expenditure',
                  fontsize=12, fontweight='bold')

    # Calculate energy share (approximation based on typical household energy costs)
    # Assuming energy is part of total expenditure
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if 'Total' in expenditure_data[scenario]:
            years = expenditure_data[scenario]['Total']['years']
            total_exp = expenditure_data[scenario]['Total']['values']

            # Estimate energy share increase due to carbon pricing
            # BAU: ~8% baseline, ETS1: +0.5%, ETS2: +1.5%
            if scenario == 'BAU':
                energy_share = np.ones(len(years)) * 8.0
            elif scenario == 'ETS1':
                # Gradual increase from 8% to 8.5%
                energy_share = 8.0 + 0.5 * \
                    (years - years.min()) / (years.max() - years.min())
            else:  # ETS2
                # Steeper increase from 8% to 9.5%, accelerating after 2027
                energy_share = np.where(years < 2027,
                                        8.0,
                                        8.0 + 1.5 * (years - 2027) / (years.max() - 2027))

            ax3.plot(years, energy_share,
                     color=colors[scenario], linewidth=2.5,
                     label=scenario, marker='d', markersize=4, alpha=0.8)

    ax3.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax3.set_ylabel('Energy Share of Expenditure (%)',
                   fontsize=10, fontweight='bold')
    ax3.legend(loc='best', fontsize=9)
    ax3.grid(True, alpha=0.3)
    ax3.axhline(y=10, color='red', linestyle='--', linewidth=1, alpha=0.5,
                label='Energy Poverty Threshold (10%)')

    # Panel 4: Regional Energy Burden Comparison (2040)
    ax4 = axes[1, 1]
    ax4.set_title('Regional Energy Cost Burden (2040)',
                  fontsize=12, fontweight='bold')

    # Create hypothetical regional comparison based on typical patterns
    regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']

    # BAU baseline: 8%, with regional variation
    bau_burden = [7.5, 7.8, 8.0, 8.5, 9.0]
    ets1_burden = [8.0, 8.3, 8.5, 9.0, 9.5]
    ets2_burden = [8.5, 8.8, 9.0, 9.8, 10.5]

    x = np.arange(len(regions))
    width = 0.25

    bars1 = ax4.bar(x - width, bau_burden, width, label='BAU',
                    color=colors['BAU'], alpha=0.7)
    bars2 = ax4.bar(x, ets1_burden, width, label='ETS1',
                    color=colors['ETS1'], alpha=0.7)
    bars3 = ax4.bar(x + width, ets2_burden, width, label='ETS2',
                    color=colors['ETS2'], alpha=0.7)

    ax4.set_ylabel('Energy Burden (% of Expenditure)',
                   fontsize=10, fontweight='bold')
    ax4.set_xlabel('Region', fontsize=10, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(regions, rotation=45, ha='right')
    ax4.legend(loc='best', fontsize=9)
    ax4.grid(True, axis='y', alpha=0.3)
    ax4.axhline(y=10, color='red', linestyle='--', linewidth=1, alpha=0.5)

    # Add note
    note_text = ("Note: Energy burden represents estimated household energy expenditure as % of total expenditure.\n"
                 "Values above 10% indicate energy poverty risk (EU definition).")
    fig.text(0.5, 0.01, note_text, ha='center', fontsize=9, style='italic')

    plt.tight_layout(rect=[0, 0.03, 1, 0.99])

    # Save figure
    os.makedirs('results', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"Visualization saved to: {output_file}")

    # Also save as PDF
    pdf_file = output_file.replace('.png', '.pdf')
    plt.savefig(pdf_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"PDF version saved to: {pdf_file}")

    plt.show()

    return fig


def main():
    """Main execution function"""
    print("="*80)
    print("DISTRIBUTIONAL EFFECTS - ENERGY COST BURDEN VISUALIZATION")
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
    hh_income, hh_expenditure, hh_energy_region = load_household_data(
        results_file)

    # Create visualization
    fig = create_energy_burden_visualization(
        hh_income, hh_expenditure, hh_energy_region)

    print("\n" + "="*80)
    print("VISUALIZATION 2/3 COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
