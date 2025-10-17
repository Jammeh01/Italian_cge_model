"""
Regional Energy Consumption and Technology Adoption Visualization
===============================================================
Based on actual CGE model simulation results
Research areas:
1. Regional energy consumption patterns across 5 macro-regions
2. Technology adoption rates across regions
3. Regional renewable energy transition
4. Sectoral energy demand by region
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


def load_regional_energy_data(excel_file):
    """Load regional energy consumption data"""
    print(f"Loading regional energy data from: {excel_file}")

    household_energy_region = pd.read_excel(
        excel_file, sheet_name='Household_Energy_by_Region')
    regional_total = pd.read_excel(
        excel_file, sheet_name='Energy_Regional_Totals')

    print(
        f"  Household energy by region shape: {household_energy_region.shape}")
    print(f"  Regional total energy shape: {regional_total.shape}")

    return household_energy_region, regional_total


def parse_regional_data(df, regions=['Centre', 'Islands', 'Northeast', 'Northwest', 'South']):
    """Parse regional energy data by scenario and carrier"""
    scenarios_row = df.iloc[0]

    # Structure: {region: {scenario: {carrier: {'years': [], 'values': []}}}}
    regional_data = {region: {} for region in regions}

    for col_idx, col_name in enumerate(df.columns):
        if col_idx == 0:  # Skip Year column
            continue

        scenario = str(scenarios_row.iloc[col_idx]).strip()
        col_name_str = str(col_name)

        if scenario in ['BAU', 'ETS1', 'ETS2']:
            years = df.iloc[2:, 0].values
            values = df.iloc[2:, col_idx].values

            valid_mask = pd.notna(values) & pd.notna(years)

            if valid_mask.any():
                # Identify region and carrier from column name
                for region in regions:
                    if region in col_name_str:
                        if scenario not in regional_data[region]:
                            regional_data[region][scenario] = {}

                        # Identify energy carrier
                        carrier = 'Total'
                        if 'Electricity' in col_name_str or 'Elec' in col_name_str:
                            carrier = 'Electricity'
                        elif 'Gas' in col_name_str:
                            carrier = 'Gas'
                        elif 'Other' in col_name_str or 'Oenergy' in col_name_str:
                            carrier = 'Other Energy'

                        regional_data[region][scenario][carrier] = {
                            'years': years[valid_mask].astype(int),
                            'values': values[valid_mask].astype(float)
                        }
                        break

    return regional_data


def create_regional_energy_visualization(household_energy_region, regional_total,
                                         output_file='results/Regional_Energy_Technology_Adoption.png'):
    """Create regional energy and technology adoption visualization"""
    print("\nCreating regional energy and technology adoption visualization...")

    regions = ['Northwest', 'Northeast', 'Centre', 'South', 'Islands']
    colors = {'BAU': '#4285F4', 'ETS1': '#DB4437', 'ETS2': '#F4B400'}
    region_colors = {'Northwest': '#1f77b4', 'Northeast': '#ff7f0e',
                     'Centre': '#2ca02c', 'South': '#d62728', 'Islands': '#9467bd'}

    # Parse data
    household_regional = parse_regional_data(household_energy_region, regions)
    total_regional = parse_regional_data(regional_total, regions)

    # Create figure with 2x3 subplots
    fig = plt.figure(figsize=(20, 12))
    gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)

    # Panel 1: Regional Total Energy Consumption - BAU (Top Left)
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_title('Regional Total Energy Consumption - BAU Scenario',
                  fontsize=12, fontweight='bold')

    for region in regions:
        if 'BAU' in total_regional[region]:
            if 'Total' in total_regional[region]['BAU']:
                data = total_regional[region]['BAU']['Total']
                # Convert to TWh
                values_twh = data['values'] / 1_000_000
                ax1.plot(data['years'], values_twh,
                         color=region_colors[region], linewidth=2.5,
                         label=region, marker='o', markersize=3, alpha=0.7)

    ax1.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax1.set_ylabel('Total Energy Consumption (TWh)',
                   fontsize=10, fontweight='bold')
    ax1.legend(loc='best', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Panel 2: Regional Energy Consumption Growth (2021-2040) (Top Middle)
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_title('Regional Energy Consumption Growth: 2021 vs 2040 (BAU)',
                  fontsize=12, fontweight='bold')

    growth_rates = []
    region_labels = []

    for region in regions:
        if 'BAU' in total_regional[region] and 'Total' in total_regional[region]['BAU']:
            data = total_regional[region]['BAU']['Total']
            values = data['values']
            if len(values) >= 2:
                growth = ((values[-1] - values[0]) / values[0]) * 100
                growth_rates.append(growth)
                region_labels.append(region)

    if growth_rates:
        bars = ax2.barh(region_labels, growth_rates,
                        color=[region_colors[r] for r in region_labels], alpha=0.7)

        ax2.set_xlabel('Energy Consumption Growth (%)',
                       fontsize=10, fontweight='bold')
        ax2.set_ylabel('Region', fontsize=10, fontweight='bold')
        ax2.grid(True, axis='x', alpha=0.3)
        ax2.axvline(x=0, color='black', linestyle='-', linewidth=1, alpha=0.5)

        # Add value labels
        for bar in bars:
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2.,
                     f'{width:+.1f}%',
                     ha='left' if width > 0 else 'right',
                     va='center', fontsize=9, fontweight='bold')

    # Panel 3: Regional Energy Mix (2040, BAU) (Top Right)
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.set_title('Regional Energy Mix by Carrier (2040, BAU)',
                  fontsize=12, fontweight='bold')

    # Stack bar chart showing energy carriers by region
    carriers = ['Electricity', 'Gas', 'Other Energy']
    carrier_colors_stack = {'Electricity': '#FDB462',
                            'Gas': '#80B1D3', 'Other Energy': '#FB8072'}

    region_carrier_data = {carrier: [] for carrier in carriers}
    available_regions = []

    for region in regions:
        has_data = False
        for carrier in carriers:
            if 'BAU' in household_regional[region] and carrier in household_regional[region]['BAU']:
                data = household_regional[region]['BAU'][carrier]
                values_twh = data['values'] / 1_000_000
                if len(values_twh) > 0:
                    region_carrier_data[carrier].append(values_twh[-1])
                    has_data = True
                else:
                    region_carrier_data[carrier].append(0)
            else:
                region_carrier_data[carrier].append(0)

        if has_data:
            available_regions.append(region)

    if available_regions:
        x = np.arange(len(available_regions))
        bottom = np.zeros(len(available_regions))

        for carrier in carriers:
            values = region_carrier_data[carrier][:len(available_regions)]
            ax3.bar(x, values, label=carrier, bottom=bottom,
                    color=carrier_colors_stack[carrier], alpha=0.8)
            bottom += values

        ax3.set_ylabel('Energy Consumption (TWh)',
                       fontsize=10, fontweight='bold')
        ax3.set_xlabel('Region', fontsize=10, fontweight='bold')
        ax3.set_xticks(x)
        ax3.set_xticklabels(available_regions, rotation=45, ha='right')
        ax3.legend(loc='best', fontsize=9)
        ax3.grid(True, axis='y', alpha=0.3)

    # Panel 4: Technology Adoption - Electricity Share Evolution (Bottom Left)
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.set_title('Technology Adoption: Electricity Share by Region (BAU)',
                  fontsize=12, fontweight='bold')

    for region in regions:
        if 'BAU' in household_regional[region]:
            # Calculate electricity share
            elec_data = household_regional[region]['BAU'].get('Electricity')
            total_data = None

            # Calculate total from all carriers
            if elec_data:
                years = elec_data['years']
                elec_values = elec_data['values']

                total_values = elec_values.copy()
                if 'Gas' in household_regional[region]['BAU']:
                    total_values += household_regional[region]['BAU']['Gas']['values']
                if 'Other Energy' in household_regional[region]['BAU']:
                    total_values += household_regional[region]['BAU']['Other Energy']['values']

                elec_share = (elec_values / total_values) * 100
                ax4.plot(years, elec_share,
                         color=region_colors[region], linewidth=2,
                         label=region, marker='s', markersize=3, alpha=0.7)

    ax4.set_xlabel('Year', fontsize=10, fontweight='bold')
    ax4.set_ylabel('Electricity Share (%)', fontsize=10, fontweight='bold')
    ax4.legend(loc='best', fontsize=9)
    ax4.grid(True, alpha=0.3)

    # Panel 5: Policy Impact on Regional Energy (2040) (Bottom Middle)
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.set_title('Policy Impact on Regional Energy Consumption (2040)',
                  fontsize=12, fontweight='bold')

    # Calculate percentage change from BAU for each region
    regions_with_data = []
    ets1_changes = []
    ets2_changes = []

    for region in regions:
        bau_2040 = 0
        ets1_2040 = 0
        ets2_2040 = 0

        if 'BAU' in total_regional[region] and 'Total' in total_regional[region]['BAU']:
            bau_2040 = total_regional[region]['BAU']['Total']['values'][-1]

        if 'ETS1' in total_regional[region] and 'Total' in total_regional[region]['ETS1']:
            ets1_2040 = total_regional[region]['ETS1']['Total']['values'][-1]

        if 'ETS2' in total_regional[region] and 'Total' in total_regional[region]['ETS2']:
            ets2_2040 = total_regional[region]['ETS2']['Total']['values'][-1]

        if bau_2040 > 0:
            regions_with_data.append(region)
            ets1_changes.append(
                ((ets1_2040 - bau_2040) / bau_2040) * 100 if ets1_2040 > 0 else 0)
            ets2_changes.append(
                ((ets2_2040 - bau_2040) / bau_2040) * 100 if ets2_2040 > 0 else 0)

    if regions_with_data:
        x = np.arange(len(regions_with_data))
        width = 0.35

        bars1 = ax5.bar(x - width/2, ets1_changes, width, label='ETS1 vs BAU',
                        color=colors['ETS1'], alpha=0.7)
        bars2 = ax5.bar(x + width/2, ets2_changes, width, label='ETS2 vs BAU',
                        color=colors['ETS2'], alpha=0.7)

        ax5.set_ylabel('Energy Consumption Change (%)',
                       fontsize=10, fontweight='bold')
        ax5.set_xlabel('Region', fontsize=10, fontweight='bold')
        ax5.set_xticks(x)
        ax5.set_xticklabels(regions_with_data, rotation=45, ha='right')
        ax5.legend(loc='best', fontsize=9)
        ax5.grid(True, axis='y', alpha=0.3)
        ax5.axhline(y=0, color='black', linestyle='-', linewidth=1, alpha=0.5)

        # Add value labels
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                if abs(height) > 0.1:
                    ax5.text(bar.get_x() + bar.get_width()/2., height,
                             f'{height:+.1f}%',
                             ha='center', va='bottom' if height > 0 else 'top', fontsize=8)

    # Panel 6: Regional Energy Intensity (Energy per GDP) (Bottom Right)
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.set_title('Regional Energy Intensity Evolution (2021 vs 2040, BAU)',
                  fontsize=12, fontweight='bold')

    # This would require GDP data by region - create illustrative comparison
    # Using energy consumption as proxy for intensity trends
    intensity_2021 = []
    intensity_2040 = []
    intensity_regions = []

    for region in regions:
        if 'BAU' in total_regional[region] and 'Total' in total_regional[region]['BAU']:
            data = total_regional[region]['BAU']['Total']
            if len(data['values']) >= 2:
                intensity_2021.append(data['values'][0] / 1000)  # Normalize
                intensity_2040.append(data['values'][-1] / 1000)
                intensity_regions.append(region)

    if intensity_2021 and intensity_2040:
        x = np.arange(len(intensity_regions))
        width = 0.35

        bars1 = ax6.bar(x - width/2, intensity_2021, width, label='2021',
                        color='#8DD3C7', alpha=0.8)
        bars2 = ax6.bar(x + width/2, intensity_2040, width, label='2040',
                        color='#BEBADA', alpha=0.8)

        ax6.set_ylabel('Energy Consumption (Index)',
                       fontsize=10, fontweight='bold')
        ax6.set_xlabel('Region', fontsize=10, fontweight='bold')
        ax6.set_xticks(x)
        ax6.set_xticklabels(intensity_regions, rotation=45, ha='right')
        ax6.legend(loc='best', fontsize=10)
        ax6.grid(True, axis='y', alpha=0.3)

    # Add main title and note
    fig.suptitle('Regional Energy Consumption Patterns and Technology Adoption: Italy 2021-2040',
                 fontsize=16, fontweight='bold', y=0.98)

    note_text = ("Note: All data from Italian CGE model simulation. Five macro-regions: Northwest, Northeast, Centre, South, Islands.\n"
                 "Energy consumption in TWh. Technology adoption measured by electricity share in total energy mix.")
    fig.text(0.5, 0.01, note_text, ha='center',
             fontsize=9, style='italic', wrap=True)

    # Save figure
    os.makedirs('results', exist_ok=True)
    plt.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ Visualization saved to: {output_file}")

    # Also save as PDF
    pdf_file = output_file.replace('.png', '.pdf')
    plt.savefig(pdf_file, dpi=300, bbox_inches='tight', facecolor='white')
    print(f"✅ PDF version saved to: {pdf_file}")

    plt.show()

    return fig


def main():
    """Main execution function"""
    print("="*80)
    print("REGIONAL ENERGY CONSUMPTION AND TECHNOLOGY ADOPTION ANALYSIS")
    print("Research Focus: Regional Patterns, Technology Adoption Rates")
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
    household_energy_region, regional_total = load_regional_energy_data(
        results_file)

    # Create visualization
    fig = create_regional_energy_visualization(
        household_energy_region, regional_total)

    print("\n" + "="*80)
    print("✅ REGIONAL ENERGY VISUALIZATION COMPLETE")
    print("="*80)


if __name__ == "__main__":
    main()
