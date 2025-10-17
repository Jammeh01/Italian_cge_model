"""
Distributional Effects Visualization 1: Employment Impacts by Region and Sector
==============================================================================
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


def load_employment_data(excel_file):
    """Load employment and unemployment data"""
    print(f"Loading employment data from: {excel_file}")

    # Load employment data
    employment_df = pd.read_excel(
        excel_file, sheet_name='Labor_Market_Employment')
    unemployment_df = pd.read_excel(
        excel_file, sheet_name='Labor_Market_Unemployment')

    print(f"  Employment sheet columns: {employment_df.columns.tolist()[:5]}")
    print(
        f"  Unemployment sheet columns: {unemployment_df.columns.tolist()[:5]}")

    return employment_df, unemployment_df


def parse_labor_data(df, data_type='employment'):
    """Parse labor market data from Excel sheet"""
    # The structure: Row 0 has scenarios, Row 1 has regions/sectors
    scenarios_row = df.iloc[0]

    # Find BAU, ETS1, ETS2 columns
    data_dict = {}

    for col_idx, col_name in enumerate(df.columns):
        if col_idx == 0:  # Skip first column (Year)
            continue

        scenario = str(scenarios_row.iloc[col_idx]).strip()
        if scenario in ['BAU', 'ETS1', 'ETS2']:
            # Get the region/sector label from column name or second row
            label = str(col_name).replace('Unnamed:', '').strip()

            # Extract years and values
            years = df.iloc[2:, 0].values
            values = df.iloc[2:, col_idx].values

            valid_mask = pd.notna(values) & pd.notna(years)
            if valid_mask.any():
                key = f"{scenario}"
                if key not in data_dict:
                    data_dict[key] = []

                data_dict[key].append({
                    'years': years[valid_mask],
                    'values': values[valid_mask],
                    'label': label
                })

    return data_dict


def create_employment_visualization(employment_df, unemployment_df,
                                    output_file='results/Distributional_Employment_Impacts.png'):
    """Create employment impacts visualization"""
    print("\nCreating employment impacts visualization...")

    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Distributional Effects: Employment and Unemployment by Region',
                 fontsize=16, fontweight='bold', y=0.995)

    # Parse data
    emp_data = parse_labor_data(employment_df, 'employment')
    unemp_data = parse_labor_data(unemployment_df, 'unemployment')

    # Colors for scenarios
    colors = {'BAU': '#4285F4', 'ETS1': '#DB4437', 'ETS2': '#F4B400'}

    # Since we may have limited regional data, let's create aggregate visualizations

    # Panel 1: National Employment Rate Evolution
    ax1 = axes[0, 0]
    ax1.set_title('National Employment Rate by Scenario',
                  fontsize=12, fontweight='bold')

    if emp_data:
        for scenario in ['BAU', 'ETS1', 'ETS2']:
            if scenario in emp_data and len(emp_data[scenario]) > 0:
                # Take first series (typically national/aggregate)
                years = emp_data[scenario][0]['years']
                values = emp_data[scenario][0]['values']
                ax1.plot(years, values, color=colors[scenario], linewidth=2.5,
                         label=scenario, marker='o', markersize=4, alpha=0.8)

    ax1.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Employment Rate (%)', fontsize=10, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel 2: National Unemployment Rate Evolution
    ax2 = axes[0, 1]
    ax2.set_title('National Unemployment Rate by Scenario',
                  fontsize=12, fontweight='bold')

    if unemp_data:
        for scenario in ['BAU', 'ETS1', 'ETS2']:
            if scenario in unemp_data and len(unemp_data[scenario]) > 0:
                years = unemp_data[scenario][0]['years']
                values = unemp_data[scenario][0]['values']
                ax2.plot(years, values, color=colors[scenario], linewidth=2.5,
                         label=scenario, marker='s', markersize=4, alpha=0.8)

    ax2.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax2.set_ylabel('Unemployment Rate (%)', fontsize=10, fontweight='bold')
    ax2.legend(loc='best', fontsize=9)
    ax2.grid(True, alpha=0.3)

    # Panel 3: Employment Impact Comparison (2040)
    ax3 = axes[1, 0]
    ax3.set_title('Employment Rate Comparison (2040)',
                  fontsize=12, fontweight='bold')

    if emp_data:
        emp_2040 = []
        scenarios = []
        for scenario in ['BAU', 'ETS1', 'ETS2']:
            if scenario in emp_data and len(emp_data[scenario]) > 0:
                years = emp_data[scenario][0]['years']
                values = emp_data[scenario][0]['values']
                # Get 2040 value
                idx_2040 = np.where(years.astype(int) == 2040)[0]
                if len(idx_2040) > 0:
                    emp_2040.append(values[idx_2040[0]])
                    scenarios.append(scenario)

        if emp_2040:
            bars = ax3.bar(scenarios, emp_2040, color=[
                           colors[s] for s in scenarios], alpha=0.7, width=0.6)
            ax3.set_ylabel('Employment Rate (%)',
                           fontsize=10, fontweight='bold')
            ax3.grid(True, axis='y', alpha=0.3)

            # Add value labels on bars
            for bar, val in zip(bars, emp_2040):
                height = bar.get_height()
                ax3.text(bar.get_x() + bar.get_width()/2., height,
                         f'{val:.2f}%', ha='center', va='bottom', fontweight='bold')

    # Panel 4: Unemployment Impact Comparison (2040)
    ax4 = axes[1, 1]
    ax4.set_title('Unemployment Rate Comparison (2040)',
                  fontsize=12, fontweight='bold')

    if unemp_data:
        unemp_2040 = []
        scenarios = []
        for scenario in ['BAU', 'ETS1', 'ETS2']:
            if scenario in unemp_data and len(unemp_data[scenario]) > 0:
                years = unemp_data[scenario][0]['years']
                values = unemp_data[scenario][0]['values']
                # Get 2040 value
                idx_2040 = np.where(years.astype(int) == 2040)[0]
                if len(idx_2040) > 0:
                    unemp_2040.append(values[idx_2040[0]])
                    scenarios.append(scenario)

        if unemp_2040:
            bars = ax4.bar(scenarios, unemp_2040, color=[
                           colors[s] for s in scenarios], alpha=0.7, width=0.6)
            ax4.set_ylabel('Unemployment Rate (%)',
                           fontsize=10, fontweight='bold')
            ax4.grid(True, axis='y', alpha=0.3)

            # Add value labels on bars
            for bar, val in zip(bars, unemp_2040):
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                         f'{val:.2f}%', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()

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
    print("DISTRIBUTIONAL EFFECTS - EMPLOYMENT IMPACTS VISUALIZATION")
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
    employment_df, unemployment_df = load_employment_data(results_file)

    # Create visualization
    fig = create_employment_visualization(employment_df, unemployment_df)

    print("\n" + "="*80)
    print("VISUALIZATION 1/3 COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
