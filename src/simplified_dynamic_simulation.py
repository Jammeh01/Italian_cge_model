"""
🇮🇹 ITALIAN CGE MODEL - SIMPLIFIED DYNAMIC SIMULATION (2021-2050)
================================================================
Recursive Dynamic Simulation using existing model structure
BAU: 2021-2050, ETS1: 2021-2050, ETS2: 2027-2050
"""

from scenarios.ETS1_scenario import ETS1_scenario
from scenarios.ETS2_scenario import ETS2_scenario
from scenarios.BAU_scenario import BAU_scenario
import sys
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import existing scenarios
sys.path.append('.')
sys.path.append('..')


def run_dynamic_simulation():
    """
    Run dynamic simulation using existing scenario modules
    """
    print("🇮🇹 ITALIAN CGE MODEL - DYNAMIC SIMULATION 2021-2050")
    print("="*60)

    # Years to simulate
    years = list(range(2021, 2051))  # 2021-2050

    # Initialize results storage
    all_results = {
        'BAU': {},
        'ETS1': {},
        'ETS2': {}
    }

    print("📊 Running scenarios with dynamic adjustments...")

    # 1. BAU Scenario (2021-2050)
    print("\n📈 BAU Scenario (Business As Usual)")
    try:
        bau_results = []
        for year in years:
            print(f"  📅 Year {year}...", end=' ')

            # Run BAU scenario with year-specific adjustments
            result = BAU_scenario(year=year)
            if result and result.get('solved', False):
                # Extract key results
                year_data = {
                    'year': year,
                    'scenario': 'BAU',
                    # Convert to billions
                    'gdp_total': result.get('total_value_added', 0) / 1000,
                    'gdp_nw': result.get('value_added_NW', 0) / 1000,
                    'gdp_ne': result.get('value_added_NE', 0) / 1000,
                    'gdp_center': result.get('value_added_CENTER', 0) / 1000,
                    'gdp_south': result.get('value_added_SOUTH', 0) / 1000,
                    'gdp_islands': result.get('value_added_ISLANDS', 0) / 1000,
                    # Convert to Mt
                    'co2_total': result.get('total_co2_emissions', 0) / 1000,
                    # Convert to TWh
                    'electricity_demand': result.get('total_electricity_demand', 0) / 1000,
                    # Convert to bcm
                    'gas_demand': result.get('total_gas_demand', 0) / 1000,
                    # EUR/MWh
                    'electricity_price': result.get('electricity_price', 150),
                    'gas_price': result.get('gas_price', 45),  # EUR/MWh
                }

                # Sectoral outputs (millions EUR)
                for sector in ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS', 'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']:
                    year_data[f'output_{sector}'] = result.get(
                        f'output_{sector}', 0)

                # Regional energy demand
                for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                    year_data[f'electricity_demand_{region}'] = result.get(
                        f'electricity_demand_{region}', 0) / 1000
                    year_data[f'gas_demand_{region}'] = result.get(
                        f'gas_demand_{region}', 0) / 1000
                    year_data[f'household_electricity_{region}'] = result.get(
                        f'household_electricity_{region}', 0) / 1000
                    year_data[f'household_gas_{region}'] = result.get(
                        f'household_gas_{region}', 0) / 1000

                bau_results.append(year_data)
                print("✅")
            else:
                print("❌")

        all_results['BAU'] = bau_results
        print(
            f"  📊 BAU completed: {len(bau_results)}/{len(years)} years successful")

    except Exception as e:
        print(f"  ❌ BAU scenario error: {str(e)}")

    # 2. ETS1 Scenario (2021-2050)
    print("\n💰 ETS1 Scenario (Industrial Carbon Pricing)")
    try:
        ets1_results = []
        for year in years:
            print(f"  📅 Year {year}...", end=' ')

            # Calculate dynamic carbon price (starts at €100/tCO2, grows 3% annually)
            carbon_price = 100 * (1.03 ** (year - 2021))

            result = ETS1_scenario(year=year, carbon_price=carbon_price)
            if result and result.get('solved', False):
                # Extract key results (same structure as BAU)
                year_data = {
                    'year': year,
                    'scenario': 'ETS1',
                    'carbon_price': carbon_price,
                    'gdp_total': result.get('total_value_added', 0) / 1000,
                    'gdp_nw': result.get('value_added_NW', 0) / 1000,
                    'gdp_ne': result.get('value_added_NE', 0) / 1000,
                    'gdp_center': result.get('value_added_CENTER', 0) / 1000,
                    'gdp_south': result.get('value_added_SOUTH', 0) / 1000,
                    'gdp_islands': result.get('value_added_ISLANDS', 0) / 1000,
                    'co2_total': result.get('total_co2_emissions', 0) / 1000,
                    'electricity_demand': result.get('total_electricity_demand', 0) / 1000,
                    'gas_demand': result.get('total_gas_demand', 0) / 1000,
                    'electricity_price': result.get('electricity_price', 150),
                    'gas_price': result.get('gas_price', 45),
                }

                # Add sectoral and regional data (same as BAU)
                for sector in ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS', 'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']:
                    year_data[f'output_{sector}'] = result.get(
                        f'output_{sector}', 0)

                for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                    year_data[f'electricity_demand_{region}'] = result.get(
                        f'electricity_demand_{region}', 0) / 1000
                    year_data[f'gas_demand_{region}'] = result.get(
                        f'gas_demand_{region}', 0) / 1000
                    year_data[f'household_electricity_{region}'] = result.get(
                        f'household_electricity_{region}', 0) / 1000
                    year_data[f'household_gas_{region}'] = result.get(
                        f'household_gas_{region}', 0) / 1000

                ets1_results.append(year_data)
                print("✅")
            else:
                print("❌")

        all_results['ETS1'] = ets1_results
        print(
            f"  📊 ETS1 completed: {len(ets1_results)}/{len(years)} years successful")

    except Exception as e:
        print(f"  ❌ ETS1 scenario error: {str(e)}")

    # 3. ETS2 Scenario (2027-2050)
    print("\n🌱 ETS2 Scenario (Buildings & Transport Carbon Pricing)")
    try:
        ets2_results = []
        ets2_years = list(range(2027, 2051))  # ETS2 starts in 2027

        for year in ets2_years:
            print(f"  📅 Year {year}...", end=' ')

            # Calculate dynamic carbon prices
            # ETS1 industrial price: €134/tCO2 in 2027, grows 3%
            # ETS2 buildings/transport price: €45/tCO2 in 2027, grows 5%
            ets1_price = 134 * (1.03 ** (year - 2027))
            ets2_price = 45 * (1.05 ** (year - 2027))

            result = ETS2_scenario(
                year=year, ets1_price=ets1_price, ets2_price=ets2_price)
            if result and result.get('solved', False):
                # Extract key results
                year_data = {
                    'year': year,
                    'scenario': 'ETS2',
                    'ets1_carbon_price': ets1_price,
                    'ets2_carbon_price': ets2_price,
                    'gdp_total': result.get('total_value_added', 0) / 1000,
                    'gdp_nw': result.get('value_added_NW', 0) / 1000,
                    'gdp_ne': result.get('value_added_NE', 0) / 1000,
                    'gdp_center': result.get('value_added_CENTER', 0) / 1000,
                    'gdp_south': result.get('value_added_SOUTH', 0) / 1000,
                    'gdp_islands': result.get('value_added_ISLANDS', 0) / 1000,
                    'co2_total': result.get('total_co2_emissions', 0) / 1000,
                    'electricity_demand': result.get('total_electricity_demand', 0) / 1000,
                    'gas_demand': result.get('total_gas_demand', 0) / 1000,
                    'electricity_price': result.get('electricity_price', 150),
                    'gas_price': result.get('gas_price', 45),
                }

                # Add sectoral and regional data
                for sector in ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS', 'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']:
                    year_data[f'output_{sector}'] = result.get(
                        f'output_{sector}', 0)

                for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                    year_data[f'electricity_demand_{region}'] = result.get(
                        f'electricity_demand_{region}', 0) / 1000
                    year_data[f'gas_demand_{region}'] = result.get(
                        f'gas_demand_{region}', 0) / 1000
                    year_data[f'household_electricity_{region}'] = result.get(
                        f'household_electricity_{region}', 0) / 1000
                    year_data[f'household_gas_{region}'] = result.get(
                        f'household_gas_{region}', 0) / 1000

                ets2_results.append(year_data)
                print("✅")
            else:
                print("❌")

        all_results['ETS2'] = ets2_results
        print(
            f"  📊 ETS2 completed: {len(ets2_results)}/{len(ets2_years)} years successful")

    except Exception as e:
        print(f"  ❌ ETS2 scenario error: {str(e)}")

    return all_results


def export_results_to_excel(results):
    """
    Export dynamic simulation results to comprehensive Excel file
    """
    print("\n📊 EXPORTING RESULTS TO EXCEL")
    print("="*40)

    # Create results directory
    results_dir = "results/dynamic_simulation_2021_2050"
    os.makedirs(results_dir, exist_ok=True)

    # File path
    excel_file = f"{results_dir}/Italian_CGE_Dynamic_Results_2021_2050_Complete.xlsx"

    with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:

        # 1. GDP Results Summary
        print("  📈 GDP data...")
        gdp_data = []
        for scenario, scenario_results in results.items():
            for year_result in scenario_results:
                gdp_data.append({
                    'Year': year_result['year'],
                    'Scenario': scenario,
                    'GDP_Total': year_result['gdp_total'],
                    'GDP_NW': year_result['gdp_nw'],
                    'GDP_NE': year_result['gdp_ne'],
                    'GDP_CENTER': year_result['gdp_center'],
                    'GDP_SOUTH': year_result['gdp_south'],
                    'GDP_ISLANDS': year_result['gdp_islands']
                })

        if gdp_data:
            gdp_df = pd.DataFrame(gdp_data)
            # Total GDP by scenario
            gdp_total_pivot = gdp_df.pivot(
                index='Year', columns='Scenario', values='GDP_Total')
            gdp_total_pivot.to_excel(
                writer, sheet_name='GDP_Total_Billions_EUR')

            # Regional GDP breakdowns
            for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                gdp_regional = gdp_df.pivot(
                    index='Year', columns='Scenario', values=f'GDP_{region}')
                gdp_regional.to_excel(
                    writer, sheet_name=f'GDP_{region}_Billions_EUR')

        # 2. Sectoral Output
        print("  🏭 Sectoral output...")
        sectors = ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS',
                   'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']
        for sector in sectors:
            sector_data = []
            for scenario, scenario_results in results.items():
                for year_result in scenario_results:
                    if f'output_{sector}' in year_result:
                        sector_data.append({
                            'Year': year_result['year'],
                            'Scenario': scenario,
                            'Output': year_result[f'output_{sector}']
                        })

            if sector_data:
                sector_df = pd.DataFrame(sector_data)
                sector_pivot = sector_df.pivot(
                    index='Year', columns='Scenario', values='Output')
                sector_pivot.to_excel(
                    writer, sheet_name=f'Output_{sector}_MEUR')

        # 3. Energy Demand - Electricity by region
        print("  ⚡ Electricity demand...")
        regions = ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']
        for region in regions:
            elec_data = []
            for scenario, scenario_results in results.items():
                for year_result in scenario_results:
                    if f'electricity_demand_{region}' in year_result:
                        elec_data.append({
                            'Year': year_result['year'],
                            'Scenario': scenario,
                            'Industrial': year_result[f'electricity_demand_{region}'],
                            'Household': year_result.get(f'household_electricity_{region}', 0)
                        })

            if elec_data:
                elec_df = pd.DataFrame(elec_data)
                elec_ind_pivot = elec_df.pivot(
                    index='Year', columns='Scenario', values='Industrial')
                elec_ind_pivot.to_excel(
                    writer, sheet_name=f'Electricity_TWh_Industry_{region}')
                elec_hh_pivot = elec_df.pivot(
                    index='Year', columns='Scenario', values='Household')
                elec_hh_pivot.to_excel(
                    writer, sheet_name=f'Electricity_TWh_Household_{region}')

        # 4. Energy Demand - Gas by region
        print("  🔥 Gas demand...")
        for region in regions:
            gas_data = []
            for scenario, scenario_results in results.items():
                for year_result in scenario_results:
                    if f'gas_demand_{region}' in year_result:
                        gas_data.append({
                            'Year': year_result['year'],
                            'Scenario': scenario,
                            'Industrial': year_result[f'gas_demand_{region}'],
                            'Household': year_result.get(f'household_gas_{region}', 0)
                        })

            if gas_data:
                gas_df = pd.DataFrame(gas_data)
                gas_ind_pivot = gas_df.pivot(
                    index='Year', columns='Scenario', values='Industrial')
                gas_ind_pivot.to_excel(
                    writer, sheet_name=f'Gas_bcm_Industry_{region}')
                gas_hh_pivot = gas_df.pivot(
                    index='Year', columns='Scenario', values='Household')
                gas_hh_pivot.to_excel(
                    writer, sheet_name=f'Gas_bcm_Household_{region}')

        # 5. CO2 Emissions
        print("  🌍 CO2 emissions...")
        co2_data = []
        for scenario, scenario_results in results.items():
            for year_result in scenario_results:
                co2_data.append({
                    'Year': year_result['year'],
                    'Scenario': scenario,
                    'CO2_Total': year_result['co2_total']
                })

        if co2_data:
            co2_df = pd.DataFrame(co2_data)
            co2_pivot = co2_df.pivot(
                index='Year', columns='Scenario', values='CO2_Total')
            co2_pivot.to_excel(writer, sheet_name='CO2_Total_Mt')

        # 6. Energy Prices
        print("  💰 Energy prices...")
        price_data = []
        for scenario, scenario_results in results.items():
            for year_result in scenario_results:
                price_data.append({
                    'Year': year_result['year'],
                    'Scenario': scenario,
                    'Electricity_Price': year_result['electricity_price'],
                    'Gas_Price': year_result['gas_price']
                })

        if price_data:
            price_df = pd.DataFrame(price_data)
            elec_price_pivot = price_df.pivot(
                index='Year', columns='Scenario', values='Electricity_Price')
            elec_price_pivot.to_excel(
                writer, sheet_name='Electricity_Prices_EUR_MWh')
            gas_price_pivot = price_df.pivot(
                index='Year', columns='Scenario', values='Gas_Price')
            gas_price_pivot.to_excel(writer, sheet_name='Gas_Prices_EUR_MWh')

        # 7. Carbon Prices (for ETS scenarios)
        print("  💸 Carbon prices...")
        carbon_price_data = []
        for scenario, scenario_results in results.items():
            for year_result in scenario_results:
                if scenario == 'ETS1' and 'carbon_price' in year_result:
                    carbon_price_data.append({
                        'Year': year_result['year'],
                        'Scenario': scenario,
                        'Carbon_Price': year_result['carbon_price']
                    })
                elif scenario == 'ETS2' and 'ets1_carbon_price' in year_result:
                    carbon_price_data.append({
                        'Year': year_result['year'],
                        'Scenario': f'{scenario}_Industrial',
                        'Carbon_Price': year_result['ets1_carbon_price']
                    })
                    carbon_price_data.append({
                        'Year': year_result['year'],
                        'Scenario': f'{scenario}_Buildings_Transport',
                        'Carbon_Price': year_result['ets2_carbon_price']
                    })

        if carbon_price_data:
            carbon_df = pd.DataFrame(carbon_price_data)
            carbon_pivot = carbon_df.pivot(
                index='Year', columns='Scenario', values='Carbon_Price')
            carbon_pivot.to_excel(writer, sheet_name='Carbon_Prices_EUR_tCO2')

    print(f"✅ Results exported to: {excel_file}")
    return excel_file


def main():
    """
    Main execution function
    """
    start_time = time.time()

    print("🇮🇹 ITALIAN CGE MODEL - DYNAMIC SIMULATION 2021-2050")
    print("="*60)
    print("📊 Scenarios:")
    print("   • BAU: Business As Usual (2021-2050)")
    print("   • ETS1: Industrial Carbon Pricing (2021-2050)")
    print("   • ETS2: Buildings & Transport Carbon Pricing (2027-2050)")

    # Run simulation
    results = run_dynamic_simulation()

    # Export results
    excel_file = export_results_to_excel(results)

    end_time = time.time()

    # Summary
    total_years = sum(len(scenario_results)
                      for scenario_results in results.values())

    print(f"\n🎉 DYNAMIC SIMULATION COMPLETED!")
    print(f"⏱️  Execution time: {end_time - start_time:.1f} seconds")
    print(f"📊 Total years simulated: {total_years}")
    print(f"📁 Results file: {excel_file}")
    print("\n📈 Key Results Available:")
    print("   • GDP evolution by region (2021-2050)")
    print("   • Sectoral output trajectories")
    print("   • Energy demand patterns (electricity & gas)")
    print("   • Household energy consumption")
    print("   • CO2 emissions pathways")
    print("   • Energy and carbon price evolution")
    print("\n✅ Ready for policy analysis!")


if __name__ == "__main__":
    main()
