#!/usr/bin/env python
"""
VALIDATION SCRIPT FOR TOTAL ENERGY DEMAND RESULTS
==================================================
Validates that total energy demand tracking is working correctly
"""

import pandas as pd
import os


def validate_total_energy_results():
    """
    Validate the total energy demand tracking results
    """
    print("="*60)
    print("VALIDATING TOTAL ENERGY DEMAND RESULTS")
    print("="*60)

    # Find the latest results file
    results_dir = "results/dynamic_simulation_2021_2050"
    files = [f for f in os.listdir(results_dir) if f.endswith('.xlsx')]
    latest_file = max(files, key=lambda x: os.path.getctime(
        os.path.join(results_dir, x)))

    excel_path = os.path.join(results_dir, latest_file)
    print(f"Reading results from: {latest_file}")

    # Check available sheets
    excel_file = pd.ExcelFile(excel_path)
    print(f"\nTotal sheets in Excel file: {len(excel_file.sheet_names)}")

    # Validate total energy demand sheets - sectoral
    total_energy_sectoral_sheets = [
        sheet for sheet in excel_file.sheet_names if 'Total_Energy_MWh_' in sheet and 'Household_' not in sheet]
    print(
        f"\nSectoral Total Energy Demand Sheets: {len(total_energy_sectoral_sheets)}")
    for sheet in sorted(total_energy_sectoral_sheets):
        print(f"  - {sheet}")

    # Validate total energy demand sheets - household
    total_energy_household_sheets = [
        sheet for sheet in excel_file.sheet_names if 'Total_Energy_MWh_Household_' in sheet]
    print(
        f"\nHousehold Total Energy Demand Sheets: {len(total_energy_household_sheets)}")
    for sheet in sorted(total_energy_household_sheets):
        print(f"  - {sheet}")

    # Sample data validation - Agriculture total energy demand
    print(f"\n" + "="*60)
    print("SAMPLE DATA VALIDATION - AGRICULTURE TOTAL ENERGY")
    print("="*60)

    if 'Total_Energy_MWh_AGR' in excel_file.sheet_names:
        agr_total = pd.read_excel(
            excel_path, sheet_name='Total_Energy_MWh_AGR', index_col=0)
        print(f"Agriculture Total Energy Demand (MWh):")
        print(f"Shape: {agr_total.shape}")
        print(f"Years: {agr_total.index.min()} to {agr_total.index.max()}")
        print(f"Scenarios: {list(agr_total.columns)}")
        print(f"\nSample data (first 5 years):")
        print(agr_total.head())
        print(f"\nFinal year values:")
        print(agr_total.tail(1))

        # Check if total energy is reasonable (should be larger than individual carriers)
        # Compare with electricity component
        if 'Electricity_MWh_AGR' in excel_file.sheet_names:
            agr_elec = pd.read_excel(
                excel_path, sheet_name='Electricity_MWh_AGR', index_col=0)
            print(f"\nValidation - Total vs Electricity (2021):")
            print(f"Total Energy (AGR): {agr_total.iloc[0]['BAU']:,.0f} MWh")
            print(f"Electricity (AGR): {agr_elec.iloc[0]['BAU']:,.0f} MWh")
            print(
                f"Ratio (Total/Electricity): {agr_total.iloc[0]['BAU'] / agr_elec.iloc[0]['BAU']:.1f}x")

    # Sample data validation - Industry total energy demand
    print(f"\n" + "="*60)
    print("SAMPLE DATA VALIDATION - INDUSTRY TOTAL ENERGY")
    print("="*60)

    if 'Total_Energy_MWh_IND' in excel_file.sheet_names:
        ind_total = pd.read_excel(
            excel_path, sheet_name='Total_Energy_MWh_IND', index_col=0)
        print(f"Industry Total Energy Demand (MWh):")
        print(f"Shape: {ind_total.shape}")
        print(f"Years: {ind_total.index.min()} to {ind_total.index.max()}")
        print(f"Scenarios: {list(ind_total.columns)}")
        print(f"\nSample data (first 5 years):")
        print(ind_total.head())
        print(f"\nFinal year values:")
        print(ind_total.tail(1))

        # Show scenario comparison for final year
        print(f"\nScenario Impact (2050):")
        final_year = ind_total.tail(1)
        for scenario in final_year.columns:
            if pd.notna(final_year[scenario].iloc[0]):
                print(f"  {scenario}: {final_year[scenario].iloc[0]:,.0f} MWh")

    # Sample data validation - Household total energy (NW region)
    print(f"\n" + "="*60)
    print("SAMPLE DATA VALIDATION - HOUSEHOLD TOTAL ENERGY (NW)")
    print("="*60)

    if 'Total_Energy_MWh_Household_NW' in excel_file.sheet_names:
        hh_nw_total = pd.read_excel(
            excel_path, sheet_name='Total_Energy_MWh_Household_NW', index_col=0)
        print(f"Household NW Total Energy Demand (MWh):")
        print(f"Shape: {hh_nw_total.shape}")
        print(f"Years: {hh_nw_total.index.min()} to {hh_nw_total.index.max()}")
        print(f"Scenarios: {list(hh_nw_total.columns)}")
        print(f"\nSample data (first 5 years):")
        print(hh_nw_total.head())
        print(f"\nFinal year values:")
        print(hh_nw_total.tail(1))

    # Cross-validation: Check total energy consistency
    print(f"\n" + "="*60)
    print("CROSS-VALIDATION - TOTAL ENERGY CONSISTENCY")
    print("="*60)

    if all(sheet in excel_file.sheet_names for sheet in ['Total_Energy_MWh_AGR', 'Electricity_MWh_AGR', 'Gas_MWh_AGR', 'Other_Energy_MWh_AGR']):
        # Read all components for Agriculture sector
        agr_total = pd.read_excel(
            excel_path, sheet_name='Total_Energy_MWh_AGR', index_col=0)
        agr_elec = pd.read_excel(
            excel_path, sheet_name='Electricity_MWh_AGR', index_col=0)
        agr_gas = pd.read_excel(
            excel_path, sheet_name='Gas_MWh_AGR', index_col=0)
        agr_other = pd.read_excel(
            excel_path, sheet_name='Other_Energy_MWh_AGR', index_col=0)

        # Calculate sum of components
        agr_calculated_total = agr_elec + agr_gas + agr_other

        # Compare with stored total (BAU scenario, 2021)
        stored_total = agr_total.loc[2021, 'BAU']
        calculated_total = agr_calculated_total.loc[2021, 'BAU']

        print(f"Agriculture 2021 (BAU scenario):")
        print(f"  Electricity: {agr_elec.loc[2021, 'BAU']:,.0f} MWh")
        print(f"  Gas: {agr_gas.loc[2021, 'BAU']:,.0f} MWh")
        print(f"  Other Energy: {agr_other.loc[2021, 'BAU']:,.0f} MWh")
        print(f"  Sum of components: {calculated_total:,.0f} MWh")
        print(f"  Stored total: {stored_total:,.0f} MWh")
        print(
            f"  Difference: {abs(stored_total - calculated_total):,.0f} MWh ({abs(stored_total - calculated_total)/stored_total*100:.2f}%)")

        if abs(stored_total - calculated_total) < 1:  # Allow small rounding differences
            print("  ✅ PASS: Total energy calculation is consistent")
        else:
            print("  ⚠️ WARNING: Total energy calculation may have issues")

    # Summary validation
    print(f"\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    expected_sectors = ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS',
                        'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']
    expected_regions = ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']

    # Check sectoral total energy coverage
    sectoral_total_sectors = [sheet.split(
        '_')[-1] for sheet in total_energy_sectoral_sheets]

    print(
        f"✓ Expected sectors: {len(expected_sectors)} | Found total energy: {len(sectoral_total_sectors)}")

    missing_total = set(expected_sectors) - set(sectoral_total_sectors)
    if missing_total:
        print(f"⚠ Missing total energy sectors: {missing_total}")
    else:
        print(f"✅ All sectors have total energy tracking")

    # Check household regional total energy coverage
    household_total_regions = [sheet.split(
        '_')[-1] for sheet in total_energy_household_sheets]

    print(
        f"✓ Expected regions: {len(expected_regions)} | Found household total energy: {len(household_total_regions)}")

    missing_household_total = set(
        expected_regions) - set(household_total_regions)
    if missing_household_total:
        print(
            f"⚠ Missing household total energy regions: {missing_household_total}")
    else:
        print(f"✅ All regions have household total energy tracking")

    print(f"\n✅ Total energy demand validation completed!")
    print(f"📊 Results file: {latest_file}")
    print(
        f"🏭 Sectoral total energy sheets: {len(total_energy_sectoral_sheets)}")
    print(
        f"🏠 Household total energy sheets: {len(total_energy_household_sheets)}")
    print(
        f"📈 Total new sheets added: {len(total_energy_sectoral_sheets) + len(total_energy_household_sheets)}")


if __name__ == "__main__":
    validate_total_energy_results()
