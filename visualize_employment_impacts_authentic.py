"""
Distributional Effects Visualization 1: Employment Impacts by Region
===================================================================
AUTHENTIC VERSION - Uses 100% Real Model Data
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("Set2")


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


def load_regional_labor_data(excel_file):
    """Load regional employment and unemployment data"""
    print(f"Loading regional labor data from: {excel_file}")

    employment_df = pd.read_excel(
        excel_file, sheet_name='Labor_Market_Employment')
    unemployment_df = pd.read_excel(
        excel_file, sheet_name='Labor_Market_Unemployment')

    print(f"  Employment data shape: {employment_df.shape}")
    print(f"  Unemployment data shape: {unemployment_df.shape}")

    return employment_df, unemployment_df


def parse_regional_data(df, regions=['Centre', 'Islands', 'Northeast', 'Northwest', 'South']):
    """Parse regional data by scenario"""
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


def create_authentic_employment_visualization(employment_df, unemployment_df,
                                              output_file='results/Distributional_Employment_Impacts_Authentic.png'):
    """Create employment visualization using 100% authentic model data"""
    print("\nCreating AUTHENTIC employment impacts visualization...")

    regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']
    colors = {'BAU': '#4285F4', 'ETS1': '#DB4437', 'ETS2': '#F4B400'}

    # Parse regional data
    emp_regional = parse_regional_data(employment_df, regions)
    unemp_regional = parse_regional_data(unemployment_df, regions)

    # Create figure
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Distributional Effects: Regional Employment and Unemployment Impacts',
                 fontsize=16, fontweight='bold', y=0.995)

    # Panel 1: Total National Employment Evolution
    ax1 = axes[0, 0]
    ax1.set_title('Total National Employment Evolution',
                  fontsize=12, fontweight='bold')

    # Calculate national totals by summing all regions
    national_emp = {}
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        years_list = []
        total_values = []

        # Get years from first available region
        for region in regions:
            if scenario in emp_regional[region]:
                years_list = emp_regional[region][scenario]['years']
                break

        # Sum across all regions for each year
        for year_idx, year in enumerate(years_list):
            year_total = 0
            for region in regions:
                if scenario in emp_regional[region]:
                    if year_idx < len(emp_regional[region][scenario]['values']):
                        year_total += emp_regional[region][scenario]['values'][year_idx]
            total_values.append(year_total)

        if len(years_list) > 0:
            ax1.plot(years_list, total_values,
                     color=colors[scenario], linewidth=2.5,
                     label=scenario, alpha=0.8)

    ax1.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Total Employment (Millions)',
                   fontsize=10, fontweight='bold')
    ax1.legend(loc='best', fontsize=10)
    ax1.grid(True, alpha=0.3)

    # Panel 2: Regional Unemployment Rates Evolution
    ax2 = axes[0, 1]
    ax2.set_title('Regional Unemployment Rates - BAU Scenario',
                  fontsize=12, fontweight='bold')

    region_colors = {'Northwest': '#1f77b4', 'Northeast': '#ff7f0e',
                     'Centre': '#2ca02c', 'South': '#d62728', 'Islands': '#9467bd'}

    for region in regions:
        if 'BAU' in unemp_regional[region]:
            data = unemp_regional[region]['BAU']
            ax2.plot(data['years'], data['values'],
                     color=region_colors[region], linewidth=2,
                     label=region, marker='o', markersize=3, alpha=0.7)

    ax2.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Unemployment Rate (%)', fontsize=10, fontweight='bold')
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Regional Employment in 2040 - All Scenarios
    ax3 = axes[1, 0]
    ax3.set_title('Regional Employment by Scenario (2040)',
                  fontsize=12, fontweight='bold')

    # Extract 2040 values for each region and scenario
    data_2040 = {region: {} for region in regions}

    for region in regions:
        for scenario in ['BAU', 'ETS1', 'ETS2']:
            if scenario in emp_regional[region]:
                data = emp_regional[region][scenario]
                # Find 2040 value
                if 2040 in data['years']:
                    idx = list(data['years']).index(2040)
                    data_2040[region][scenario] = data['values'][idx]
                elif len(data['years']) > 0:
                    # Use last available year
                    data_2040[region][scenario] = data['values'][-1]

    x = np.arange(len(regions))
    width = 0.25

    for i, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
        values = [data_2040[region].get(scenario, 0) for region in regions]
        ax3.bar(x + i*width - width, values, width,
                label=scenario, color=colors[scenario], alpha=0.7)

    ax3.set_ylabel('Employment (Millions)', fontsize=10, fontweight='bold')
    ax3.set_xlabel('Region', fontsize=10, fontweight='bold')
    ax3.set_xticks(x)
    ax3.set_xticklabels(regions, rotation=45, ha='right')
    ax3.legend(loc='best', fontsize=10)
    ax3.grid(True, axis='y', alpha=0.3)

    # Panel 4: Regional Unemployment Rate Changes (2040 vs 2021)
    ax4 = axes[1, 1]
    ax4.set_title('Unemployment Rate Changes: 2040 vs 2021 (%points)',
                  fontsize=12, fontweight='bold')

    # Calculate changes
    unemp_changes = {region: {} for region in regions}

    for region in regions:
        for scenario in ['BAU', 'ETS1', 'ETS2']:
            if scenario in unemp_regional[region]:
                data = unemp_regional[region][scenario]
                if len(data['years']) >= 2:
                    initial = data['values'][0]  # 2021
                    final = data['values'][-1]   # 2040 or last year
                    unemp_changes[region][scenario] = final - initial

    x = np.arange(len(regions))
    width = 0.25

    for i, scenario in enumerate(['BAU', 'ETS1', 'ETS2']):
        values = [unemp_changes[region].get(scenario, 0) for region in regions]
        bars = ax4.bar(x + i*width - width, values, width,
                       label=scenario, color=colors[scenario], alpha=0.7)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height,
                     f'{height:+.1f}',
                     ha='center', va='bottom' if height > 0 else 'top', fontsize=8)

    ax4.set_ylabel('Unemployment Rate Change (%points)',
                   fontsize=10, fontweight='bold')
    ax4.set_xlabel('Region', fontsize=10, fontweight='bold')
    ax4.set_xticks(x)
    ax4.set_xticklabels(regions, rotation=45, ha='right')
    ax4.legend(loc='best', fontsize=10)
    ax4.grid(True, axis='y', alpha=0.3)
    ax4.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)

    # Add note
    note_text = ("Note: All data directly from Italian CGE model simulation results. Employment in millions of workers.\n"
                 "Unemployment rates in percent. Regional breakdown: Northwest, Northeast, Centre, South, Islands.")
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
    print("EMPLOYMENT DATA SUMMARY (2021 vs 2040)")
    print("="*80)
    for region in regions:
        print(f"\n{region}:")
        for scenario in ['BAU', 'ETS1', 'ETS2']:
            if scenario in emp_regional[region]:
                data = emp_regional[region][scenario]
                if len(data['values']) >= 2:
                    initial = data['values'][0]
                    final = data['values'][-1]
                    change = ((final - initial) / initial) * 100
                    print(
                        f"  {scenario}: {initial:.2f}M → {final:.2f}M ({change:+.2f}%)")

    return fig


def main():
    """Main execution function"""
    print("="*80)
    print("AUTHENTIC DISTRIBUTIONAL EFFECTS - EMPLOYMENT IMPACTS")
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
    employment_df, unemployment_df = load_regional_labor_data(results_file)

    # Create visualization
    fig = create_authentic_employment_visualization(
        employment_df, unemployment_df)

    print("\n" + "="*80)
    print("✅ AUTHENTIC VISUALIZATION 1/3 COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
