"""
Italian CGE Model: GDP Impact Visualization (Single Panel)
==========================================================
Creates GDP Impact visualization showing % change from BAU
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


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


def load_gdp_data(excel_file):
    """Load GDP data from Enhanced Dynamic Results"""
    print(f"Loading GDP data from: {excel_file}")

    # Read Macroeconomy_GDP sheet without index
    gdp_df = pd.read_excel(excel_file, sheet_name='Macroeconomy_GDP')

    scenarios_row = gdp_df.iloc[0]

    # Find Real_GDP_Total column
    real_gdp_col_start = None
    for i, col_name in enumerate(gdp_df.columns):
        if 'Real_GDP_Total' in str(col_name):
            real_gdp_col_start = i
            break

    if real_gdp_col_start is None:
        print("Error: Could not find Real_GDP_Total columns")
        return pd.DataFrame()

    # Extract the three columns after Real_GDP_Total header
    gdp_data = {}
    for i in range(3):  # BAU, ETS1, ETS2
        col_idx = real_gdp_col_start + i
        if col_idx < len(gdp_df.columns):
            scenario = str(scenarios_row.iloc[col_idx]).strip()

            if scenario in ['BAU', 'ETS1', 'ETS2']:
                years = gdp_df.iloc[2:, 0].values
                values = gdp_df.iloc[2:, col_idx].values

                valid_mask = pd.notna(values) & pd.notna(years)
                if valid_mask.any():
                    valid_years = years[valid_mask]
                    valid_values = values[valid_mask]

                    gdp_data[scenario] = pd.Series(
                        valid_values,
                        index=valid_years,
                        name=scenario
                    )
                    print(
                        f"  Found {scenario} scenario: {len(gdp_data[scenario])} years")

    # Convert to DataFrame with proper scenario order
    scenario_order = ['BAU', 'ETS1', 'ETS2']
    available_scenarios = [s for s in scenario_order if s in gdp_data]
    gdp_results = pd.DataFrame({s: gdp_data[s] for s in available_scenarios})

    gdp_results.index = gdp_results.index.astype(int)
    gdp_results.index.name = 'Year'

    return gdp_results


def create_gdp_impact_visualization(gdp_df, output_file='results/Italian_CGE_GDP_Impact.png'):
    """
    Create GDP impact visualization (% change from BAU) - single panel without title
    """
    print("Creating GDP impact visualization...")

    # Create figure with single subplot
    fig, ax = plt.subplots(1, 1, figsize=(14, 6))

    # Color scheme
    colors = {'BAU': '#4285F4', 'ETS1': '#DB4437', 'ETS2': '#F4B400'}

    # Calculate percentage differences from BAU
    if 'BAU' in gdp_df.columns:
        impact_data = {}

        if 'ETS1' in gdp_df.columns:
            # Calculate % change only for overlapping years
            ets1_years = gdp_df['ETS1'].dropna().index
            bau_years = gdp_df['BAU'].dropna().index
            common_years = ets1_years.intersection(bau_years)

            impact_ets1 = ((gdp_df.loc[common_years, 'ETS1'] - gdp_df.loc[common_years, 'BAU']) /
                           gdp_df.loc[common_years, 'BAU']) * 100
            impact_data['ETS1'] = impact_ets1

        if 'ETS2' in gdp_df.columns:
            # ETS2 starts in 2027
            ets2_years = gdp_df['ETS2'].dropna().index
            bau_years = gdp_df['BAU'].dropna().index
            common_years = ets2_years.intersection(bau_years)

            impact_ets2 = ((gdp_df.loc[common_years, 'ETS2'] - gdp_df.loc[common_years, 'BAU']) /
                           gdp_df.loc[common_years, 'BAU']) * 100
            impact_data['ETS2'] = impact_ets2

        # Plot impact lines with smooth curves (no markers)
        for scenario, impact in impact_data.items():
            ax.plot(impact.index, impact,
                    color=colors[scenario], linewidth=3,
                    label=f'{scenario} vs BAU', alpha=0.9)

        # Add zero reference line
        ax.axhline(y=0, color='black', linestyle='--',
                   linewidth=1.5, alpha=0.5)

        # Calculate and display summary statistics in legend box
        if impact_data:
            legend_text = []
            final_year = gdp_df.index.max()
            for scenario, impact in impact_data.items():
                if final_year in impact.index:
                    final_impact = impact.loc[final_year]

                    legend_text.append(
                        f'{scenario}: €{gdp_df.loc[final_year, scenario]:.0f}B ({final_impact:.2f}%)')

            # Add statistics box
            stats_text = f'Summary Statistics ({final_year}):\n' + \
                '\n'.join(legend_text)
            if 'BAU' in gdp_df.columns:
                stats_text += f'\nBAU: €{gdp_df.loc[final_year, "BAU"]:.0f}B'

            ax.text(0.02, 0.02, stats_text,
                    transform=ax.transAxes,
                    fontsize=9,
                    verticalalignment='bottom',
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Style the plot
    ax.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax.set_ylabel('GDP Difference (%)', fontsize=11, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax.set_xlim(2020, 2041)

    # Set custom x-axis ticks
    ax.set_xticks([2020, 2025, 2030, 2035, 2040])
    ax.set_xticklabels([2020, 2025, 2030, 2035, 2040])

    # Adjust layout
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
    print("ITALIAN CGE MODEL - GDP IMPACT VISUALIZATION (SINGLE PANEL)")
    print("="*80)
    print()

    # Find latest results file
    results_file = find_latest_results_file()

    if not results_file:
        print("Error: No results file found!")
        print("Please run the simulation first: python src/recursive_dynamic_simulation.py")
        return

    print(f"Using results file: {os.path.basename(results_file)}")
    print()

    # Load GDP data
    gdp_df = load_gdp_data(results_file)

    if gdp_df.empty:
        print("Error: No GDP data loaded!")
        return

    # Create visualization
    fig = create_gdp_impact_visualization(gdp_df)

    print("\n" + "="*80)
    print("VISUALIZATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
