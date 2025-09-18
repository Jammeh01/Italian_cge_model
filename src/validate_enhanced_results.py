#!/usr/bin/env python
"""
VALIDATION SCRIPT FOR ENHANCED ENERGY DEMAND RESULTS
====================================================
Validates that sectoral and regional energy demand tracking is working correctly
"""

import pandas as pd
import os


def validate_enhanced_results():
    """
    Validate the enhanced energy demand tracking results
    """
    print("="*60)
    print("VALIDATING ENHANCED ENERGY DEMAND RESULTS")
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

    # Validate sectoral electricity demand sheets
    sectoral_elec_sheets = [
        sheet for sheet in excel_file.sheet_names if 'Electricity_MWh_' in sheet and 'Industry_' not in sheet and 'Household_' not in sheet]
    print(f"\nSectoral Electricity Demand Sheets: {len(sectoral_elec_sheets)}")
    for sheet in sorted(sectoral_elec_sheets):
        print(f"  - {sheet}")

    # Validate sectoral gas demand sheets
    sectoral_gas_sheets = [
        sheet for sheet in excel_file.sheet_names if 'Gas_MWh_' in sheet and 'Industry_' not in sheet and 'Household_' not in sheet]
    print(f"\nSectoral Gas Demand Sheets: {len(sectoral_gas_sheets)}")
    for sheet in sorted(sectoral_gas_sheets):
        print(f"  - {sheet}")

    # Validate other energy demand sheets
    other_energy_sheets = [
        sheet for sheet in excel_file.sheet_names if 'Other_Energy_MWh_' in sheet]
    print(f"\nOther Energy Demand Sheets: {len(other_energy_sheets)}")
    for sheet in sorted(other_energy_sheets):
        print(f"  - {sheet}")

    # Validate household regional sheets
    household_sheets = [
        sheet for sheet in excel_file.sheet_names if 'Household_' in sheet]
    print(f"\nHousehold Regional Sheets: {len(household_sheets)}")
    for sheet in sorted(household_sheets):
        print(f"  - {sheet}")

    # Sample data validation - Agriculture electricity demand
    print(f"\n" + "="*60)
    print("SAMPLE DATA VALIDATION - AGRICULTURE ELECTRICITY DEMAND")
    print("="*60)

    if 'Electricity_MWh_AGR' in excel_file.sheet_names:
        agr_elec = pd.read_excel(
            excel_path, sheet_name='Electricity_MWh_AGR', index_col=0)
        print(f"Agriculture Electricity Demand (MWh):")
        print(f"Shape: {agr_elec.shape}")
        print(f"Years: {agr_elec.index.min()} to {agr_elec.index.max()}")
        print(f"Scenarios: {list(agr_elec.columns)}")
        print(f"\nSample data (first 5 years):")
        print(agr_elec.head())
        print(f"\nFinal year values:")
        print(agr_elec.tail(1))

    # Sample data validation - Industry gas demand
    print(f"\n" + "="*60)
    print("SAMPLE DATA VALIDATION - INDUSTRY GAS DEMAND")
    print("="*60)

    if 'Gas_MWh_IND' in excel_file.sheet_names:
        ind_gas = pd.read_excel(
            excel_path, sheet_name='Gas_MWh_IND', index_col=0)
        print(f"Industry Gas Demand (MWh):")
        print(f"Shape: {ind_gas.shape}")
        print(f"Years: {ind_gas.index.min()} to {ind_gas.index.max()}")
        print(f"Scenarios: {list(ind_gas.columns)}")
        print(f"\nSample data (first 5 years):")
        print(ind_gas.head())
        print(f"\nFinal year values:")
        print(ind_gas.tail(1))

    # Sample data validation - Other energy for renewables
    print(f"\n" + "="*60)
    print("SAMPLE DATA VALIDATION - OTHER ENERGY SECTOR")
    print("="*60)

    if 'Other_Energy_MWh_OENERGY' in excel_file.sheet_names:
        oe_other = pd.read_excel(
            excel_path, sheet_name='Other_Energy_MWh_OENERGY', index_col=0)
        print(f"Other Energy Sector - Other Energy Demand (MWh):")
        print(f"Shape: {oe_other.shape}")
        print(f"Years: {oe_other.index.min()} to {oe_other.index.max()}")
        print(f"Scenarios: {list(oe_other.columns)}")
        print(f"\nSample data (first 5 years):")
        print(oe_other.head())
        print(f"\nFinal year values:")
        print(oe_other.tail(1))

    # Summary validation
    print(f"\n" + "="*60)
    print("VALIDATION SUMMARY")
    print("="*60)

    expected_sectors = ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS',
                        'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']
    expected_regions = ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']

    # Check sectoral coverage
    sectoral_elec_sectors = [sheet.split('_')[-1]
                             for sheet in sectoral_elec_sheets]
    sectoral_gas_sectors = [sheet.split('_')[-1]
                            for sheet in sectoral_gas_sheets]
    other_energy_sectors = [sheet.split('_')[-1]
                            for sheet in other_energy_sheets]

    print(f"✓ Expected sectors: {len(expected_sectors)} | Found electricity: {len(sectoral_elec_sectors)} | Found gas: {len(sectoral_gas_sectors)} | Found other: {len(other_energy_sectors)}")

    missing_elec = set(expected_sectors) - set(sectoral_elec_sectors)
    missing_gas = set(expected_sectors) - set(sectoral_gas_sectors)
    missing_other = set(expected_sectors) - set(other_energy_sectors)

    if missing_elec:
        print(f"⚠ Missing electricity sectors: {missing_elec}")
    if missing_gas:
        print(f"⚠ Missing gas sectors: {missing_gas}")
    if missing_other:
        print(f"⚠ Missing other energy sectors: {missing_other}")

    # Check regional coverage
    household_regions = set()
    for sheet in household_sheets:
        if '_' in sheet:
            region = sheet.split('_')[-1]
            household_regions.add(region)

    print(
        f"✓ Expected regions: {len(expected_regions)} | Found household regions: {len(household_regions)}")

    missing_regions = set(expected_regions) - household_regions
    if missing_regions:
        print(f"⚠ Missing household regions: {missing_regions}")

    print(f"\n✅ Enhanced energy demand tracking validation completed!")
    print(f"📊 Results file: {latest_file}")
    print(
        f"📈 Total energy demand sheets: {len(sectoral_elec_sheets + sectoral_gas_sheets + other_energy_sheets)}")
    print(f"🏠 Household regional sheets: {len(household_sheets)}")


if __name__ == "__main__":
    validate_enhanced_results()
