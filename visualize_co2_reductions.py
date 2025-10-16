"""
CO2 Emission Reductions Visualization
======================================
Create a visualization showing emission reductions from BAU 2021 baseline
Similar to Panel A style with EU targets
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import datetime

# Configure matplotlib for professional appearance
plt.style.use('seaborn-v0_8-whitegrid')
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


def extract_co2_data(excel_file):
    """Extract CO2 emissions data for all scenarios"""
    print(f"Loading CO2 data from: {os.path.basename(excel_file)}")

    # Read the CO2_Emissions_Totals sheet
    co2_df = pd.read_excel(
        excel_file, sheet_name='CO2_Emissions_Totals', index_col=0)

    co2_data = {}

    # Find columns containing Total_CO2_Emissions
    total_co2_cols = [
        col for col in co2_df.columns if 'Total_CO2_Emissions' in str(col)]

    if total_co2_cols:
        # Get the column and the next two columns (BAU, ETS1, ETS2)
        col_idx = co2_df.columns.get_loc(total_co2_cols[0])

        # Get data starting from row 2 (after Scenario and Year rows)
        years = co2_df.index[2:]  # Skip first two rows

        # Extract BAU
        bau_col = co2_df.columns[col_idx]
        co2_data['BAU'] = co2_df.loc[years, bau_col].astype(float)
        co2_data['BAU'].index = years

        # Extract ETS1
        if col_idx + 1 < len(co2_df.columns):
            ets1_col = co2_df.columns[col_idx + 1]
            ets1_data = co2_df.loc[years, ets1_col]
            ets1_data = ets1_data.dropna()
            if len(ets1_data) > 0:
                co2_data['ETS1'] = ets1_data.astype(float)

        # Extract ETS2
        if col_idx + 2 < len(co2_df.columns):
            ets2_col = co2_df.columns[col_idx + 2]
            ets2_data = co2_df.loc[years, ets2_col]
            ets2_data = ets2_data.dropna()
            if len(ets2_data) > 0:
                co2_data['ETS2'] = ets2_data.astype(float)

    return co2_data


def calculate_emission_reductions(co2_data):
    """Calculate emission reductions as % from each scenario's own 2021 baseline"""

    # For reference image style, calculate reductions relative to each scenario's own baseline
    # But for comparison, we'll use BAU trajectory as reference

    bau_2021 = co2_data['BAU'].loc[2021]

    print(f"\nBAU Baseline (2021): {bau_2021:.2f} Mt CO2")

    # Calculate reductions
    reductions = {}

    # For BAU: show reduction from its 2021 level
    reductions['BAU'] = ((bau_2021 - co2_data['BAU']) / bau_2021) * 100

    # For policy scenarios: show reduction compared to BAU scenario (same year)
    # This shows the ADDITIONAL reduction from policies
    for scenario in ['ETS1', 'ETS2']:
        if scenario in co2_data:
            policy_data = co2_data[scenario]
            # Get BAU values for the same years
            bau_aligned = co2_data['BAU'].loc[policy_data.index]
            # Calculate additional reduction compared to BAU
            reductions[scenario] = (
                (bau_aligned - policy_data) / bau_2021) * 100

    return reductions, bau_2021


def create_emission_reduction_visualization(reductions, baseline, co2_data):
    """Create professional emission reduction chart matching the style"""

    fig, ax = plt.subplots(figsize=(14, 9))

    # Color scheme matching the reference image
    colors = {
        'BAU': '#3498db',           # Blue
        'ETS1': '#9b59b6',          # Purple
        'ETS2': '#e67e22'           # Orange
    }

    # Line styles
    line_styles = {
        'BAU': '-',
        'ETS1': '--',
        'ETS2': '-'
    }

    # Plot each scenario
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in reductions:
            data = reductions[scenario]
            ax.plot(data.index, data.values,
                    label=f'{scenario}' + (' (Industries)' if scenario ==
                                           'ETS1' else ' (+Transport and Buildings)' if scenario == 'ETS2' else ''),
                    color=colors[scenario],
                    linestyle=line_styles[scenario],
                    linewidth=3,
                    alpha=0.9)

            # Add final value annotation
            if 2050 in data.index:
                final_value = data.loc[2050]
                ax.annotate(f'{final_value:.1f}%',
                            xy=(2050, final_value),
                            xytext=(10, 0),
                            textcoords='offset points',
                            fontsize=11,
                            fontweight='bold',
                            color=colors[scenario])

    # Add EU 2030 Target line (-55%)
    ax.axhline(y=55, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7)
    ax.text(2021, 55, 'EU 2030 Target (-55%)',
            fontsize=10, color='#e74c3c', va='bottom', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='#e74c3c'))

    # Add EU 2050 Target line (Net Zero = 100%)
    ax.axhline(y=100, color='#c0392b', linestyle=':', linewidth=2, alpha=0.7)
    ax.text(2021, 100, 'EU 2050 Target (Net Zero)',
            fontsize=10, color='#c0392b', va='bottom', ha='left',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='#c0392b'))

    # Add vertical line at 2030
    ax.axvline(x=2030, color='gray', linestyle=':', linewidth=1.5, alpha=0.5)

    # Formatting
    ax.set_title('Panel A: CO2 Emission Reductions',
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Year', fontsize=13, fontweight='bold')
    ax.set_ylabel('Emission Reduction from BAU 2021 (%)',
                  fontsize=13, fontweight='bold')

    # Set axis limits
    ax.set_xlim(2020, 2050)
    ax.set_ylim(-10, 110)

    # Grid
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # Legend
    ax.legend(loc='upper left', fontsize=11, frameon=True, shadow=True,
              fancybox=True, framealpha=0.95)

    # Add text box with summary
    summary_text = f"Baseline: BAU 2021 = {baseline:.1f} Mt CO2\n\n"
    summary_text += "2050 Emissions:\n"

    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in co2_data and 2050 in co2_data[scenario].index:
            emission = co2_data[scenario].loc[2050]
            reduction = reductions[scenario].loc[2050] if scenario in reductions and 2050 in reductions[scenario].index else 0
            summary_text += f"{scenario}: {emission:.1f} Mt ({reduction:.1f}%)\n"

    props = dict(boxstyle='round', facecolor='wheat', alpha=0.85)
    ax.text(0.98, 0.35, summary_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()

    return fig


def create_detailed_comparison_chart(co2_data, reductions):
    """Create a two-panel figure with absolute emissions and reductions"""

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 12),
                                   gridspec_kw={'height_ratios': [1, 1]})

    # Color scheme
    colors = {
        'BAU': '#3498db',
        'ETS1': '#9b59b6',
        'ETS2': '#e67e22'
    }

    # Panel 1: Absolute CO2 Emissions
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in co2_data:
            data = co2_data[scenario]
            ax1.plot(data.index, data.values,
                     label=f'{scenario}' + (' (Industries)' if scenario ==
                                            'ETS1' else ' (+Transport & Buildings)' if scenario == 'ETS2' else ''),
                     color=colors[scenario],
                     linewidth=3,
                     marker='o' if scenario == 'BAU' else 's' if scenario == 'ETS1' else '^',
                     markersize=5,
                     markevery=5,
                     alpha=0.9)

    ax1.set_title('Panel A: Total CO2 Emissions by Scenario',
                  fontsize=15, fontweight='bold', pad=15)
    ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax1.set_ylabel('CO2 Emissions (Mt CO2)', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='best', fontsize=11, frameon=True, shadow=True)
    ax1.set_xlim(2020, 2050)

    # Panel 2: Emission Reductions (matching the reference image)
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in reductions:
            data = reductions[scenario]
            linestyle = '-' if scenario != 'ETS1' else '--'
            ax2.plot(data.index, data.values,
                     label=f'{scenario}' + (' (Industries)' if scenario ==
                                            'ETS1' else ' (+Transport and Buildings)' if scenario == 'ETS2' else ''),
                     color=colors[scenario],
                     linestyle=linestyle,
                     linewidth=3,
                     alpha=0.9)

            # Add final value annotation
            if 2050 in data.index:
                final_value = data.loc[2050]
                ax2.annotate(f'{final_value:.1f}%',
                             xy=(2050, final_value),
                             xytext=(10, 0),
                             textcoords='offset points',
                             fontsize=11,
                             fontweight='bold',
                             color=colors[scenario])

    # Add EU targets
    ax2.axhline(y=55, color='#e74c3c', linestyle='--', linewidth=2, alpha=0.7,
                label='EU 2030 Target (-55%)')
    ax2.axhline(y=100, color='#c0392b', linestyle=':', linewidth=2, alpha=0.7,
                label='EU 2050 Target (Net Zero)')

    # Vertical line at 2030
    ax2.axvline(x=2030, color='gray', linestyle=':', linewidth=1.5, alpha=0.5)

    ax2.set_title('Panel B: CO2 Emission Reductions from BAU 2021',
                  fontsize=15, fontweight='bold', pad=15)
    ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Emission Reduction from BAU 2021 (%)',
                   fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='upper left', fontsize=10,
               frameon=True, shadow=True, ncol=1)
    ax2.set_xlim(2020, 2050)
    ax2.set_ylim(-5, 105)

    plt.tight_layout()

    return fig


def main():
    """Main execution function"""
    print("="*70)
    print("CO2 EMISSION REDUCTIONS VISUALIZATION")
    print("="*70)

    # Find the latest results file
    excel_file = find_latest_results_file()
    if not excel_file:
        print("Error: No results file found!")
        return

    # Extract CO2 data
    print("\nExtracting CO2 emissions data...")
    co2_data = extract_co2_data(excel_file)

    # Print summary
    print("\nAvailable scenarios:")
    for scenario, data in co2_data.items():
        print(
            f"  - {scenario}: {len(data)} years ({data.index.min()}-{data.index.max()})")
        if 2021 in data.index:
            print(f"    2021: {data.loc[2021]:.2f} Mt CO2")
        if 2050 in data.index:
            print(f"    2050: {data.loc[2050]:.2f} Mt CO2")

    # Calculate emission reductions
    print("\nCalculating emission reductions...")
    reductions, baseline = calculate_emission_reductions(co2_data)

    # Print reduction summary
    print("\nEmission Reductions (% from BAU 2021):")
    for scenario in ['BAU', 'ETS1', 'ETS2']:
        if scenario in reductions:
            print(f"\n{scenario}:")
            for year in [2021, 2030, 2040, 2050]:
                if year in reductions[scenario].index:
                    print(f"  {year}: {reductions[scenario].loc[year]:+.2f}%")

    # Create visualizations
    print("\nCreating visualizations...")

    # Style matching reference image
    fig1 = create_emission_reduction_visualization(
        reductions, baseline, co2_data)

    # Comprehensive two-panel chart
    fig2 = create_detailed_comparison_chart(co2_data, reductions)

    # Save the figures
    output_dir = "results"
    os.makedirs(output_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Save Panel A style (matching reference)
    output_file1 = os.path.join(
        output_dir, f"CO2_Emission_Reductions_PanelA_{timestamp}.png")
    fig1.savefig(output_file1, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nPanel A visualization saved to: {output_file1}")

    pdf_file1 = output_file1.replace('.png', '.pdf')
    fig1.savefig(pdf_file1, bbox_inches='tight', facecolor='white')
    print(f"PDF version saved to: {pdf_file1}")

    # Save two-panel comprehensive chart
    output_file2 = os.path.join(
        output_dir, f"CO2_Comprehensive_Analysis_{timestamp}.png")
    fig2.savefig(output_file2, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"\nComprehensive chart saved to: {output_file2}")

    pdf_file2 = output_file2.replace('.png', '.pdf')
    fig2.savefig(pdf_file2, bbox_inches='tight', facecolor='white')
    print(f"PDF version saved to: {pdf_file2}")

    # Show the plots
    plt.show()

    print("\n" + "="*70)
    print("VISUALIZATION COMPLETE")
    print("="*70)


if __name__ == "__main__":
    main()
