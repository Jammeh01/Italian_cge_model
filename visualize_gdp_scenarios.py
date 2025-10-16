"""
GDP Visualization - All Scenarios Comparison
=============================================
Create a clear visualization of GDP across all scenarios
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# Configure matplotlib for better-looking plots
plt.style.use('seaborn-v0_8-darkgrid')
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11
plt.rcParams['lines.linewidth'] = 2.5


def find_latest_results_file():
    """Find the most recent Enhanced Dynamic Results file"""
    results_dir = "results"
    excel_files = [f for f in os.listdir(results_dir)
                   if f.startswith("Italian_CGE_Enhanced_Dynamic_Results_")
                   and f.endswith(".xlsx")]
    if excel_files:
        excel_files.sort(reverse=True)
        return os.path.join(results_dir, excel_files[0])
    return None


def extract_gdp_data(excel_file):
    """Extract GDP data for all scenarios"""
    print(f"Loading data from: {os.path.basename(excel_file)}")

    # Read the Macroeconomy_GDP sheet
    gdp_df = pd.read_excel(
        excel_file, sheet_name='Macroeconomy_GDP', index_col=0)

    # The structure has scenarios in row 0 (after index), years start from row 1
    # Extract Real GDP Total data
    gdp_data = {}

    # Find columns containing Real_GDP_Total
    real_gdp_cols = [
        col for col in gdp_df.columns if 'Real_GDP_Total' in str(col)]

    if real_gdp_cols:
        # Get the column and the next two columns (BAU, ETS1, ETS2)
        col_idx = gdp_df.columns.get_loc(real_gdp_cols[0])

        # Extract data for each scenario
        # Row with "Scenario" contains the scenario names
        scenarios_row = gdp_df.iloc[0]  # First row after column names

        # Get data starting from row 2 (after Scenario and Year rows)
        years = gdp_df.index[2:]  # Skip first two rows (Scenario, Year)

        # Extract BAU
        bau_col = gdp_df.columns[col_idx]
        gdp_data['BAU'] = gdp_df.loc[years, bau_col].astype(float)
        gdp_data['BAU'].index = years

        # Extract ETS1
        if col_idx + 1 < len(gdp_df.columns):
            ets1_col = gdp_df.columns[col_idx + 1]
            ets1_data = gdp_df.loc[years, ets1_col]
            # Remove NaN values
            ets1_data = ets1_data.dropna()
            if len(ets1_data) > 0:
                gdp_data['ETS1'] = ets1_data.astype(float)

        # Extract ETS2
        if col_idx + 2 < len(gdp_df.columns):
            ets2_col = gdp_df.columns[col_idx + 2]
            ets2_data = gdp_df.loc[years, ets2_col]
            # Remove NaN values
            ets2_data = ets2_data.dropna()
            if len(ets2_data) > 0:
                gdp_data['ETS2'] = ets2_data.astype(float)

    return gdp_data


def create_gdp_visualization(gdp_data):
    """Create a professional GDP comparison chart"""

    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10),
                                   gridspec_kw={'height_ratios': [2, 1]})

    # Color scheme
    colors = {
        'BAU': '#2E86AB',      # Blue
        'ETS1': '#A23B72',     # Purple
        'ETS2': '#F18F01'      # Orange
    }

    # Markers
    markers = {
        'BAU': 'o',
        'ETS1': 's',
        'ETS2': '^'
    }

    # Plot 1: GDP Evolution
    for scenario, data in gdp_data.items():
        ax1.plot(data.index, data.values,
                 label=scenario,
                 color=colors[scenario],
                 marker=markers[scenario],
                 markersize=5,
                 markevery=3,  # Show marker every 3rd point
                 linewidth=2.5,
                 alpha=0.9)

    ax1.set_title('Italian CGE Model: Real GDP Evolution by Scenario (2021-2050)',
                  fontsize=16, fontweight='bold', pad=20)
    ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Real GDP (Billion EUR)', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=11, frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3, linestyle='--')

    # Add value annotations at key years
    key_years = [2021, 2030, 2040, 2050]
    for scenario, data in gdp_data.items():
        for year in key_years:
            if year in data.index:
                value = data.loc[year]
                if year == 2050:  # Only annotate the end point
                    ax1.annotate(f'{value:.0f}',
                                 xy=(year, value),
                                 xytext=(5, 5),
                                 textcoords='offset points',
                                 fontsize=9,
                                 color=colors[scenario],
                                 fontweight='bold')

    # Plot 2: GDP Difference from BAU
    bau_data = gdp_data['BAU']

    for scenario in ['ETS1', 'ETS2']:
        if scenario in gdp_data:
            # Calculate difference from BAU (in %)
            diff = ((gdp_data[scenario] - bau_data.loc[gdp_data[scenario].index]) /
                    bau_data.loc[gdp_data[scenario].index]) * 100

            ax2.plot(diff.index, diff.values,
                     label=f'{scenario} vs BAU',
                     color=colors[scenario],
                     marker=markers[scenario],
                     markersize=5,
                     markevery=3,
                     linewidth=2.5,
                     alpha=0.9)

    ax2.axhline(y=0, color='black', linestyle='--', linewidth=1, alpha=0.5)
    ax2.set_title('GDP Impact of Policy Scenarios (% Change from BAU)',
                  fontsize=14, fontweight='bold', pad=15)
    ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax2.set_ylabel('GDP Difference (%)', fontsize=12, fontweight='bold')
    ax2.legend(loc='best', fontsize=11, frameon=True, shadow=True)
    ax2.grid(True, alpha=0.3, linestyle='--')

    # Add a text box with summary statistics
    summary_text = "Summary Statistics (2050):\n"
    for scenario, data in gdp_data.items():
        if 2050 in data.index:
            summary_text += f"{scenario}: €{data.loc[2050]:.1f}B"
            if scenario != 'BAU' and 2050 in bau_data.index:
                pct_diff = (
                    (data.loc[2050] - bau_data.loc[2050]) / bau_data.loc[2050]) * 100
                summary_text += f" ({pct_diff:+.2f}%)"
            summary_text += "\n"

    # Add text box to the plot
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
    ax2.text(0.02, 0.98, summary_text, transform=ax2.transAxes, fontsize=10,
             verticalalignment='top', bbox=props)

    plt.tight_layout()

    return fig


def main():
    """Main execution function"""
    print("="*60)
    print("GDP VISUALIZATION - ALL SCENARIOS")
    print("="*60)

    # Find the latest results file
    excel_file = find_latest_results_file()
    if not excel_file:
        print("Error: No results file found!")
        return

    # Extract GDP data
    print("\nExtracting GDP data...")
    gdp_data = extract_gdp_data(excel_file)

    # Print summary
    print("\nAvailable scenarios:")
    for scenario, data in gdp_data.items():
        print(
            f"  - {scenario}: {len(data)} years ({data.index.min()}-{data.index.max()})")

    # Create visualization
    print("\nCreating visualization...")
    fig = create_gdp_visualization(gdp_data)

    # Save the figure
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(
        output_dir, f"GDP_All_Scenarios_{timestamp}.png")

    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nVisualization saved to: {output_file}")

    # Also save as PDF for high quality
    pdf_file = output_file.replace('.png', '.pdf')
    fig.savefig(pdf_file, bbox_inches='tight', facecolor='white')
    print(f"PDF version saved to: {pdf_file}")

    # Show the plot
    plt.show()

    print("\n" + "="*60)
    print("VISUALIZATION COMPLETE")
    print("="*60)


if __name__ == "__main__":
    main()
