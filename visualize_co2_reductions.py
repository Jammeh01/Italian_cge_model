"""
Italian CGE Model: CO2 Emission Reductions Visualization
========================================================
Creates visualization showing CO2 emission reductions from BAU 2021 baseline
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-whitegrid')


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


def load_co2_data(excel_file):
    """Load CO2 emissions data from Enhanced Dynamic Results"""
    print(f"Loading CO2 data from: {excel_file}")

    # Read CO2_Emissions_Totals sheet
    co2_df = pd.read_excel(excel_file, sheet_name='CO2_Emissions_Totals')

    # The structure is similar to GDP data
    scenarios_row = co2_df.iloc[0]

    # Find Total_CO2_Emissions column
    co2_col_start = None
    for i, col_name in enumerate(co2_df.columns):
        if 'Total_CO2_Emissions' in str(col_name):
            co2_col_start = i
            break

    if co2_col_start is None:
        print("Error: Could not find Total_CO2_Emissions columns")
        return pd.DataFrame()

    print(f"  CO2 columns start at index: {co2_col_start}")

    # Extract the three columns for BAU, ETS1, ETS2
    co2_data = {}
    for i in range(3):  # BAU, ETS1, ETS2
        col_idx = co2_col_start + i
        if col_idx < len(co2_df.columns):
            scenario = str(scenarios_row.iloc[col_idx]).strip()

            if scenario in ['BAU', 'ETS1', 'ETS2']:
                years = co2_df.iloc[2:, 0].values
                values = co2_df.iloc[2:, col_idx].values

                valid_mask = pd.notna(values) & pd.notna(years)
                if valid_mask.any():
                    valid_years = years[valid_mask]
                    valid_values = values[valid_mask]

                    co2_data[scenario] = pd.Series(
                        valid_values,
                        index=valid_years,
                        name=scenario
                    )
                    print(
                        f"  Found {scenario} scenario: {len(co2_data[scenario])} years ({int(valid_years.min())}-{int(valid_years.max())})")

    # Convert to DataFrame with proper scenario order
    scenario_order = ['BAU', 'ETS1', 'ETS2']
    available_scenarios = [s for s in scenario_order if s in co2_data]
    co2_results = pd.DataFrame({s: co2_data[s] for s in available_scenarios})

    co2_results.index = co2_results.index.astype(int)
    co2_results.index.name = 'Year'

    print(f"  Total years loaded: {len(co2_results)}")
    print(
        f"  Year range: {co2_results.index.min()} - {co2_results.index.max()}")
    print(f"  Scenarios: {list(co2_results.columns)}")

    return co2_results


def create_co2_reduction_visualization(co2_df, output_file='results/Italian_CGE_CO2_Emission_Reductions_NoTitle.png'):
    """
    Create CO2 emission reductions visualization (% reduction from BAU 2021)
    """
    print("Creating CO2 emission reductions visualization...")

    # Create figure
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))

    # No title - clean visualization

    # Color scheme - matching the reference image
    colors = {
        'BAU': '#4A90E2',      # Blue
        'ETS1': '#9B59B6',     # Purple
        'ETS2': '#E67E22'      # Orange
    }

    line_styles = {
        'BAU': '-',      # Solid
        'ETS1': '--',    # Dashed
        'ETS2': '-'      # Solid
    }

    # Get baseline (BAU 2021)
    if 'BAU' not in co2_df.columns or 2021 not in co2_df.index:
        print("Error: BAU 2021 baseline not found!")
        return None

    baseline_2021 = co2_df.loc[2021, 'BAU']
    print(f"\nBaseline: BAU 2021 = {baseline_2021:.1f} Mt CO2")

    # Calculate emission reductions as percentage from BAU 2021 baseline
    reduction_data = {}

    for scenario in co2_df.columns:
        # Calculate % reduction from 2021 baseline
        reduction_pct = (
            (baseline_2021 - co2_df[scenario]) / baseline_2021) * 100
        reduction_data[scenario] = reduction_pct

        # Get last year value for reporting
        last_year = co2_df[scenario].last_valid_index()
        if last_year:
            final_reduction = reduction_pct.loc[last_year]
            print(f"{scenario}: {final_reduction:.1f}% reduction by {last_year}")

    # Convert to DataFrame
    reduction_df = pd.DataFrame(reduction_data)

    # Plot emission reduction lines
    for scenario in reduction_df.columns:
        if scenario in colors:
            label = scenario
            if scenario == 'ETS1':
                label = 'ETS1 (Industries)'
            elif scenario == 'ETS2':
                label = 'ETS2 (+Transport and Buildings)'

            ax.plot(reduction_df.index, reduction_df[scenario],
                    color=colors[scenario],
                    linestyle=line_styles[scenario],
                    linewidth=2.5,
                    label=label,
                    alpha=0.9)

    # Add 100% reference line (dotted red)
    ax.axhline(y=100, color='red', linestyle=':',
               linewidth=2, alpha=0.7, zorder=1)

    # Add EU 2030 target line (-55%)
    ax.axhline(y=55, color='#E74C3C', linestyle='--', linewidth=1.5,
               alpha=0.6, label='EU 2030 Target (-55%)')

    # Add vertical line at 2030
    ax.axvline(x=2030, color='gray', linestyle='--', linewidth=1, alpha=0.4)

    # Add text box with baseline and final reductions
    last_year = co2_df.index.max()
    info_text = f'Baseline: BAU 2021 = {baseline_2021:.1f} Mt CO2\n'
    info_text += f'{last_year} Emission Reductions:\n'

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in reduction_df.columns and last_year in reduction_df.index:
            final_reduction = reduction_df.loc[last_year, scenario]
            info_text += f'  {scenario}: {final_reduction:.1f}%\n'

    # Place info box in bottom right
    ax.text(0.98, 0.02, info_text,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment='bottom',
            horizontalalignment='right',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.6))

    # Add final year values as text labels
    for scenario in reduction_df.columns:
        if scenario in colors and last_year in reduction_df.index:
            final_value = reduction_df.loc[last_year, scenario]
            if pd.notna(final_value):
                # Position label at end of line
                ax.annotate(f'{final_value:.1f}%',
                            xy=(last_year, final_value),
                            xytext=(10, 0),
                            textcoords='offset points',
                            fontsize=9,
                            fontweight='bold',
                            color=colors[scenario],
                            va='center')

    # Style the plot
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_ylabel('Emission Reduction from BAU 2021 (%)',
                  fontsize=12, fontweight='bold')
    ax.legend(loc='upper left', fontsize=10, frameon=True, shadow=True)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

    # Set axis limits
    ax.set_xlim(2020, last_year + 1)
    ax.set_ylim(-5, 105)

    # Set custom x-axis ticks
    x_ticks = list(range(2020, last_year + 1, 5))
    if last_year not in x_ticks:
        x_ticks.append(last_year)
    ax.set_xticks(x_ticks)

    # Adjust layout
    plt.tight_layout()

    # Save figure
    os.makedirs('results', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nVisualization saved to: {output_file}")

    # Also save as PDF
    pdf_file = output_file.replace('.png', '.pdf')
    plt.savefig(pdf_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"PDF version saved to: {pdf_file}")

    plt.show()

    return fig


def print_co2_summary(co2_df):
    """Print CO2 emissions summary"""
    print("\n" + "="*80)
    print("CO2 EMISSIONS SUMMARY")
    print("="*80)

    baseline_2021 = co2_df.loc[2021,
                               'BAU'] if 2021 in co2_df.index and 'BAU' in co2_df.columns else None

    for scenario in co2_df.columns:
        print(f"\n{scenario} Scenario:")

        # Show key years
        for year in [2021, 2030, 2040]:
            if year in co2_df.index and not pd.isna(co2_df.loc[year, scenario]):
                emissions = co2_df.loc[year, scenario]
                print(f"  {year}: {emissions:.1f} Mt CO2", end='')

                if baseline_2021:
                    reduction = ((baseline_2021 - emissions) /
                                 baseline_2021) * 100
                    print(f" ({reduction:+.1f}% from 2021 baseline)")
                else:
                    print()

        # Show last available year
        last_year = co2_df[scenario].last_valid_index()
        if last_year and last_year not in [2021, 2030, 2040]:
            emissions = co2_df.loc[last_year, scenario]
            print(f"  {last_year}: {emissions:.1f} Mt CO2", end='')

            if baseline_2021:
                reduction = ((baseline_2021 - emissions) / baseline_2021) * 100
                print(f" ({reduction:+.1f}% from 2021 baseline)")
            else:
                print()

    # EU 2030 target comparison
    if 2030 in co2_df.index and baseline_2021:
        print(f"\n{'='*80}")
        print("EU 2030 TARGET COMPARISON (-55% from baseline)")
        print(f"{'='*80}")

        target_2030 = baseline_2021 * 0.45  # 55% reduction

        for scenario in co2_df.columns:
            if scenario in ['BAU', 'ETS1', 'ETS2'] and not pd.isna(co2_df.loc[2030, scenario]):
                emissions_2030 = co2_df.loc[2030, scenario]
                reduction_pct = (
                    (baseline_2021 - emissions_2030) / baseline_2021) * 100
                gap = target_2030 - emissions_2030

                status = "✓ EXCEEDS" if emissions_2030 <= target_2030 else "✗ BELOW"
                print(
                    f"{scenario}: {reduction_pct:.1f}% reduction ({status} target, gap: {gap:+.1f} Mt)")

    print(f"\n{'='*80}\n")


def main():
    """Main execution function"""
    print("="*80)
    print("ITALIAN CGE MODEL - CO2 EMISSION REDUCTIONS VISUALIZATION")
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

    # Load CO2 data
    co2_df = load_co2_data(results_file)

    if co2_df.empty:
        print("Error: No CO2 data loaded!")
        return

    # Print summary
    print_co2_summary(co2_df)

    # Create visualization
    fig = create_co2_reduction_visualization(co2_df)

    print("\n" + "="*80)
    print("VISUALIZATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
