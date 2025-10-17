"""
Italian CGE Model: GDP Evolution Visualization
==============================================
Creates publication-quality visualization of Real GDP evolution by scenario
Similar to the reference visualization provided
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from datetime import datetime

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

    # The first row contains scenario names
    # Row 0: ['Scenario', 'BAU', 'ETS1', 'ETS2', 'BAU', 'ETS1', 'ETS2']
    # Row 1: ['Year', nan, nan, nan, nan, nan, nan]
    # Columns: 0=Year, 1-3=GDP_Per_Capita (BAU,ETS1,ETS2), 4-6=Real_GDP_Total (BAU,ETS1,ETS2)

    scenarios_row = gdp_df.iloc[0]  # BAU, ETS1, ETS2, BAU, ETS1, ETS2

    # Find Real_GDP_Total column
    real_gdp_col_start = None
    for i, col_name in enumerate(gdp_df.columns):
        if 'Real_GDP_Total' in str(col_name):
            real_gdp_col_start = i
            break

    if real_gdp_col_start is None:
        print("Error: Could not find Real_GDP_Total columns")
        return pd.DataFrame()

    print(f"  Real GDP columns start at index: {real_gdp_col_start}")

    # Extract the three columns after Real_GDP_Total header
    gdp_data = {}
    for i in range(3):  # BAU, ETS1, ETS2
        col_idx = real_gdp_col_start + i
        if col_idx < len(gdp_df.columns):
            # Get scenario name from row 0
            scenario = str(scenarios_row.iloc[col_idx]).strip()

            if scenario in ['BAU', 'ETS1', 'ETS2']:
                # Extract data starting from row 2 (skip header rows 0 and 1)
                years = gdp_df.iloc[2:, 0].values  # Year column
                values = gdp_df.iloc[2:, col_idx].values

                # Create series with valid data
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
                        f"  Found {scenario} scenario: {len(gdp_data[scenario])} years ({int(valid_years.min())}-{int(valid_years.max())})")

    # Convert to DataFrame  with proper scenario order
    scenario_order = ['BAU', 'ETS1', 'ETS2']
    available_scenarios = [s for s in scenario_order if s in gdp_data]
    gdp_results = pd.DataFrame({s: gdp_data[s] for s in available_scenarios})

    gdp_results.index = gdp_results.index.astype(int)
    gdp_results.index.name = 'Year'

    print(f"  Total years loaded: {len(gdp_results)}")
    print(
        f"  Year range: {gdp_results.index.min()} - {gdp_results.index.max()}")
    print(f"  Scenarios: {list(gdp_results.columns)}")

    return gdp_results


def create_gdp_evolution_visualization(gdp_df, output_file='results/Italian_CGE_GDP_Evolution.png'):
    """
    Create GDP evolution visualization matching the reference style
    """
    print("Creating GDP evolution visualization...")

    # Create figure with two subplots
    year_range = f"{gdp_df.index.min()}-{gdp_df.index.max()}"
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
    fig.suptitle(f'Italian CGE Model: Real GDP Evolution by Scenario ({year_range})',
                 fontsize=16, fontweight='bold', y=0.995)

    # Color scheme
    colors = {'BAU': '#4285F4', 'ETS1': '#DB4437', 'ETS2': '#F4B400'}

    # ===== SUBPLOT 1: GDP Evolution (Absolute Values) =====
    ax1.set_title('', fontsize=12, pad=10)

    # Plot each scenario with smooth lines (no markers)
    for scenario in gdp_df.columns:
        if scenario in colors:
            ax1.plot(gdp_df.index, gdp_df[scenario],
                     color=colors[scenario], linewidth=3,
                     label=scenario, alpha=0.9)

    # Style subplot 1
    ax1.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Real GDP (Billion EUR)', fontsize=11, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
    ax1.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax1.set_xlim(gdp_df.index.min() - 1, gdp_df.index.max() + 1)

    # Set custom x-axis ticks
    ax1.set_xticks([2020, 2025, 2030, 2035, 2040])
    ax1.set_xticklabels([2020, 2025, 2030, 2035, 2040])

    # Add value labels at end point
    last_year = gdp_df.index.max()
    for scenario in gdp_df.columns:
        if scenario in colors and last_year in gdp_df[scenario].dropna().index:
            value = gdp_df.loc[last_year, scenario]
            if pd.notna(value):
                ax1.annotate(f'{int(value)}',
                             xy=(last_year, value),
                             xytext=(5, 0),
                             textcoords='offset points',
                             fontsize=9,
                             fontweight='bold',
                             color=colors[scenario])

    # Set y-axis to start from a reasonable minimum
    y_min = gdp_df.min().min() * 0.95
    y_max = gdp_df.max().max() * 1.05
    ax1.set_ylim(y_min, y_max)

    # ===== SUBPLOT 2: GDP Impact (% Change from BAU) =====
    ax2.set_title(
        'GDP Impact of Policy Scenarios (% Change from BAU)', fontsize=12, pad=10)

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
            ax2.plot(impact.index, impact,
                     color=colors[scenario], linewidth=3,
                     label=f'{scenario} vs BAU', alpha=0.9)

        # Add zero reference line
        ax2.axhline(y=0, color='black', linestyle='--',
                    linewidth=1.5, alpha=0.5)

        # Calculate and display summary statistics in legend box
        if impact_data:
            legend_text = []
            final_year = gdp_df.index.max()
            for scenario, impact in impact_data.items():
                if final_year in impact.index:
                    final_impact = impact.loc[final_year]
                    mean_impact = impact.mean()

                    legend_text.append(
                        f'{scenario}: €{gdp_df.loc[final_year, scenario]:.0f}B ({final_impact:.2f}%)')

            # Add statistics box
            stats_text = f'Summary Statistics ({final_year}):\n' + \
                '\n'.join(legend_text)
            if 'BAU' in gdp_df.columns:
                stats_text += f'\nBAU: €{gdp_df.loc[final_year, "BAU"]:.0f}B'

            ax2.text(0.02, 0.02, stats_text,
                     transform=ax2.transAxes,
                     fontsize=9,
                     verticalalignment='bottom',
                     bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

    # Style subplot 2
    ax2.set_xlabel('Year', fontsize=11, fontweight='bold')
    ax2.set_ylabel('GDP Difference (%)', fontsize=11, fontweight='bold')
    ax2.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
    ax2.grid(True, alpha=0.3, linestyle='--', linewidth=0.5)
    ax2.set_xlim(2020, 2041)

    # Set custom x-axis ticks for subplot 2
    ax2.set_xticks([2020, 2025, 2030, 2035, 2040])
    ax2.set_xticklabels([2020, 2025, 2030, 2035, 2040])

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


def print_gdp_summary(gdp_df):
    """Print summary statistics"""
    print("\n" + "="*80)
    print("GDP EVOLUTION SUMMARY")
    print("="*80)

    for scenario in gdp_df.columns:
        print(f"\n{scenario} Scenario:")
        print(f"  2021: €{gdp_df.loc[2021, scenario]:.1f} billion")

        if 2030 in gdp_df.index and not pd.isna(gdp_df.loc[2030, scenario]):
            print(f"  2030: €{gdp_df.loc[2030, scenario]:.1f} billion")

        if 2040 in gdp_df.index and not pd.isna(gdp_df.loc[2040, scenario]):
            print(f"  2040: €{gdp_df.loc[2040, scenario]:.1f} billion")

        # Get last available year
        last_year = gdp_df.index.max()
        if last_year in gdp_df.index and not pd.isna(gdp_df.loc[last_year, scenario]):
            print(
                f"  {last_year}: €{gdp_df.loc[last_year, scenario]:.1f} billion")

            # Calculate growth from 2021 to last year
            first_year = gdp_df[scenario].first_valid_index()
            if first_year and first_year in gdp_df.index:
                gdp_first = gdp_df.loc[first_year, scenario]
                gdp_last = gdp_df.loc[last_year, scenario]
                years_diff = last_year - first_year

                if years_diff > 0:
                    total_growth = ((gdp_last / gdp_first) - 1) * 100
                    annual_growth = ((gdp_last / gdp_first) **
                                     (1/years_diff) - 1) * 100

                    print(
                        f"  Total Growth ({first_year}-{last_year}): {total_growth:.1f}%")
                    print(f"  Average Annual Growth: {annual_growth:.2f}%")

    # Compare policy scenarios to BAU at last available year
    if 'BAU' in gdp_df.columns:
        last_year = gdp_df.index.max()
        print(f"\n{'='*80}")
        print(f"POLICY IMPACT vs BAU ({last_year})")
        print(f"{'='*80}")

        bau_last = gdp_df.loc[last_year, 'BAU']

        for scenario in ['ETS1', 'ETS2']:
            if scenario in gdp_df.columns and last_year in gdp_df[scenario].dropna().index:
                scenario_last = gdp_df.loc[last_year, scenario]
                diff = scenario_last - bau_last
                diff_pct = (diff / bau_last) * 100

                print(f"{scenario}: €{diff:.1f}B ({diff_pct:+.2f}%)")

    print(f"\n{'='*80}\n")


def main():
    """Main execution function"""
    print("="*80)
    print("ITALIAN CGE MODEL - GDP EVOLUTION VISUALIZATION")
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

    # Print summary
    print_gdp_summary(gdp_df)

    # Create visualization
    fig = create_gdp_evolution_visualization(gdp_df)

    print("\n" + "="*80)
    print("VISUALIZATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
