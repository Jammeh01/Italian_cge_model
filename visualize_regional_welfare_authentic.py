"""
Distributional Effects Visualization 3: Regional Welfare Changes
==============================================================
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


def load_welfare_data(excel_file):
    """Load GDP and household income data"""
    print(f"Loading welfare data from: {excel_file}")

    gdp_data = pd.read_excel(excel_file, sheet_name='Macroeconomy_GDP')
    hh_income = pd.read_excel(excel_file, sheet_name='Households_Income')

    print(f"  GDP data shape: {gdp_data.shape}")
    print(f"  Household income shape: {hh_income.shape}")

    return gdp_data, hh_income


def parse_regional_household_data(df, regions=['Centre', 'Islands', 'Northeast', 'Northwest', 'South']):
    """Parse regional household income data by scenario"""
    scenarios_row = df.iloc[0]

    regional_data = {region: {} for region in regions}

    for col_idx, col_name in enumerate(df.columns):
        if col_idx == 0:
            continue

        scenario = str(scenarios_row.iloc[col_idx]).strip()
        col_name_str = str(col_name)

        if scenario in ['BAU', 'ETS1', 'ETS2']:
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


def extract_gdp_data(df):
    """Extract Real GDP Total data for all scenarios"""
    scenarios_row = df.iloc[0]

    data = {}

    for col_idx in [4, 5, 6]:  # Real_GDP_Total columns
        scenario = str(scenarios_row.iloc[col_idx]).strip()

        if scenario in ['BAU', 'ETS1', 'ETS2']:
            years = df.iloc[2:, 0].values
            values = df.iloc[2:, col_idx].values

            valid_mask = pd.notna(values) & pd.notna(years)

            if valid_mask.any():
                data[scenario] = {
                    'years': years[valid_mask].astype(int),
                    'values': values[valid_mask].astype(float)
                }

    return data


def create_authentic_welfare_visualization(gdp_data, hh_income_data,
                                           output_file='results/Distributional_Regional_Welfare_Changes_Authentic.png'):
    """Create welfare changes visualization using 100% authentic model data"""
    print("\nCreating AUTHENTIC regional welfare changes visualization...")

    regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']
    colors = {'BAU': '#4285F4', 'ETS1': '#DB4437', 'ETS2': '#F4B400'}
    region_colors = {'Northwest': '#1f77b4', 'Northeast': '#ff7f0e',
                     'Centre': '#2ca02c', 'South': '#d62728', 'Islands': '#9467bd'}

    # Extract data
    gdp = extract_gdp_data(gdp_data)
    income_regional = parse_regional_household_data(hh_income_data, regions)

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Distributional Effects: Regional Welfare Changes from Environmental Policies',
                 fontsize=16, fontweight='bold', y=0.995)

    # Panel 1: National GDP Evolution (Indexed to 2021=100)
    ax1 = axes[0, 0]
    ax1.set_title('National GDP Evolution (Indexed to 2021=100)',
                  fontsize=12, fontweight='bold')

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in gdp:
            years = gdp[scenario]['years']
            values = gdp[scenario]['values']

            # Index to 2021=100
            base_value = values[0]
            indexed_values = (values / base_value) * 100

            ax1.plot(years, indexed_values,
                     color=colors[scenario], linewidth=2.5,
                     label=scenario, marker='o', markersize=4, alpha=0.8)

    ax1.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Real GDP (Index 2021=100)', fontsize=10, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.axhline(y=100, color='black', linestyle='--', linewidth=1, alpha=0.3)

    # Panel 2: Regional Income Evolution - BAU Scenario
    ax2 = axes[0, 1]
    ax2.set_title('Regional Household Income Evolution (BAU)',
                  fontsize=12, fontweight='bold')

    for region in regions:
        if 'BAU' in income_regional[region]:
            data = income_regional[region]['BAU']
            ax2.plot(data['years'], data['values'],
                     color=region_colors[region], linewidth=2,
                     label=region, marker='o', markersize=3, alpha=0.7)

    ax2.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Household Income (Billion EUR)',
                   fontsize=10, fontweight='bold')
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Regional Income Changes from BAU (2040)
    ax3 = axes[1, 0]
    ax3.set_title('Regional Income Changes from BAU (2040, %)',
                  fontsize=12, fontweight='bold')

    income_changes_ets1 = []
    income_changes_ets2 = []

    for region in regions:
        bau_2040 = 0
        ets1_2040 = 0
        ets2_2040 = 0

        if 'BAU' in income_regional[region]:
            bau_2040 = income_regional[region]['BAU']['values'][-1]

        if 'ETS1' in income_regional[region]:
            ets1_2040 = income_regional[region]['ETS1']['values'][-1]

        if 'ETS2' in income_regional[region]:
            ets2_2040 = income_regional[region]['ETS2']['values'][-1]

        if bau_2040 > 0:
            income_changes_ets1.append(
                ((ets1_2040 - bau_2040) / bau_2040) * 100)
            income_changes_ets2.append(
                ((ets2_2040 - bau_2040) / bau_2040) * 100)
        else:
            income_changes_ets1.append(0)
            income_changes_ets2.append(0)

    x = np.arange(len(regions))
    width = 0.35

    bars1 = ax3.bar(x - width/2, income_changes_ets1, width, label='ETS1 vs BAU',
                    color=colors['ETS1'], alpha=0.7)
    bars2 = ax3.bar(x + width/2, income_changes_ets2, width, label='ETS2 vs BAU',
                    color=colors['ETS2'], alpha=0.7)

    ax3.set_ylabel('Income Change from BAU (%)',
                   fontsize=10, fontweight='bold')
    ax3.set_xlabel('Region', fontsize=10, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(regions, rotation=45, ha='right')
    ax3.legend(loc='best', fontsize=10)
    ax3.grid(True, axis='y', alpha=0.3)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:+.2f}%',
                     ha='center', va='bottom' if height > 0 else 'top', fontsize=8)

    # Panel 4: Cumulative Income Gains/Losses (2021-2040, Billion EUR)
    ax4 = axes[1, 1]
    ax4.set_title('Cumulative Regional Income Deviations from BAU (2021-2040)',
                  fontsize=12, fontweight='bold')

    cumulative_ets1 = []
    cumulative_ets2 = []

    for region in regions:
        cum_ets1 = 0
        cum_ets2 = 0

        # Calculate cumulative difference from BAU over entire period
        if 'BAU' in income_regional[region]:
            bau_data = income_regional[region]['BAU']
            bau_years = bau_data['years']
            bau_values = bau_data['values']

            if 'ETS1' in income_regional[region]:
                ets1_data = income_regional[region]['ETS1']
                for i, year in enumerate(ets1_data['years']):
                    if year in bau_years:
                        bau_idx = list(bau_years).index(year)
                        cum_ets1 += (ets1_data['values']
                                     [i] - bau_values[bau_idx])

            if 'ETS2' in income_regional[region]:
                ets2_data = income_regional[region]['ETS2']
                for i, year in enumerate(ets2_data['years']):
                    if year in bau_years and year >= 2027:  # ETS2 starts 2027
                        bau_idx = list(bau_years).index(year)
                        cum_ets2 += (ets2_data['values']
                                     [i] - bau_values[bau_idx])

        cumulative_ets1.append(cum_ets1)
        cumulative_ets2.append(cum_ets2)

    x = np.arange(len(regions))
    width = 0.35

    bars1 = ax4.barh(x - width/2, cumulative_ets1, width, label='ETS1 vs BAU',
                     color=colors['ETS1'], alpha=0.7)
    bars2 = ax4.barh(x + width/2, cumulative_ets2, width, label='ETS2 vs BAU',
                     color=colors['ETS2'], alpha=0.7)

    ax4.set_xlabel('Cumulative Income Deviation (Billion EUR)',
                   fontsize=10, fontweight='bold')
    ax4.set_ylabel('Region', fontsize=10, fontweight='bold')
    ax4.set_yticks(x)
    ax4.set_yticklabels(regions)
    ax4.legend(loc='best', fontsize=10)
    ax4.grid(True, axis='x', alpha=0.3)
    ax4.axvline(x=0, color='black', linestyle='-', linewidth=1, alpha=0.5)

    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            width_val = bar.get_width()
            if abs(width_val) > 0.1:  # Only show if significant
                ax4.text(width_val, bar.get_y() + bar.get_height()/2.,
                         f'{width_val:+.1f}',
                         ha='left' if width_val > 0 else 'right',
                         va='center', fontsize=8)

    # Add note
    note_text = ("Note: All data directly from Italian CGE model simulation results. GDP in billion EUR (constant prices).\n"
                 "Household income by region shows actual model outputs. Negative values indicate welfare losses from carbon pricing.")
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
    print("WELFARE CHANGES SUMMARY (2040 vs BAU)")
    print("="*80)

    print("\nNational GDP (2040):")
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in gdp:
            gdp_2040 = gdp[scenario]['values'][-1]
            print(f"  {scenario}: €{gdp_2040:.1f}B")

    if 'BAU' in gdp and 'ETS1' in gdp:
        gdp_loss_ets1 = ((gdp['ETS1']['values'][-1] - gdp['BAU']
                         ['values'][-1]) / gdp['BAU']['values'][-1]) * 100
        print(f"  ETS1 vs BAU: {gdp_loss_ets1:+.2f}%")

    if 'BAU' in gdp and 'ETS2' in gdp:
        gdp_loss_ets2 = ((gdp['ETS2']['values'][-1] - gdp['BAU']
                         ['values'][-1]) / gdp['BAU']['values'][-1]) * 100
        print(f"  ETS2 vs BAU: {gdp_loss_ets2:+.2f}%")

    print("\nRegional Income Changes (2040 vs BAU):")
    for i, region in enumerate(regions):
        print(f"\n{region}:")
        if income_changes_ets1[i] != 0:
            print(f"  ETS1: {income_changes_ets1[i]:+.2f}%")
        if income_changes_ets2[i] != 0:
            print(f"  ETS2: {income_changes_ets2[i]:+.2f}%")

    return fig


def main():
    """Main execution function"""
    print("="*80)
    print("AUTHENTIC DISTRIBUTIONAL EFFECTS - REGIONAL WELFARE CHANGES")
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
    gdp_data, hh_income_data = load_welfare_data(results_file)

    # Create visualization
    fig = create_authentic_welfare_visualization(gdp_data, hh_income_data)

    print("\n" + "="*80)
    print("✅ AUTHENTIC VISUALIZATION 3/3 COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
