"""
🇮🇹 ITALIAN CGE MODEL - RECURSIVE DYNAMIC SIMULATION (2021-2050)
================================================================
Comprehensive Dynamic Simulation with Energy Demand, CO2 Emissions, and Economic Results
BAU: 2021-2050, ETS1: 2021-2050, ETS2: 2027-2050
"""

from definitions import model_definitions
from data_processor import DataProcessor
from main_model import ItalianCGEModel
import pyomo.environ as pyo
import pandas as pd
import numpy as np
import os
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import model components


class DynamicCGESimulation:
    """
    Recursive Dynamic CGE Simulation for Italy (2021-2050)
    Implements forward-looking dynamic adjustments with energy transition
    """

    def __init__(self):
        self.base_year = 2021
        self.final_year = 2050
        self.years = list(range(self.base_year, self.final_year + 1))

        # Scenario definitions
        self.scenarios = {
            'BAU': {'start_year': 2021, 'carbon_price': 0, 'description': 'Business As Usual'},
            'ETS1': {'start_year': 2021, 'carbon_price': 100, 'description': 'Industrial Carbon Pricing'},
            'ETS2': {'start_year': 2027, 'carbon_price': 45, 'description': 'Buildings & Transport Carbon Pricing'}
        }

        # Results storage
        self.results = {
            'gdp': {},
            'sectoral_output': {},
            'energy_demand_electricity': {},
            'energy_demand_gas': {},
            'co2_emissions': {},
            'energy_prices': {},
            'household_energy_demand': {}
        }

        # Initialize data processor
        self.data_processor = DataProcessor("data/SAM.xlsx")
        self.data_processor.load_and_process_sam()
        self.calibrated_data = self.data_processor.get_calibrated_data()

        print("🚀 Dynamic CGE Simulation Initialized")
        print(f"📅 Simulation Period: {self.base_year}-{self.final_year}")
        print(f"🎯 Scenarios: {list(self.scenarios.keys())}")

    def calculate_dynamic_parameters(self, year, scenario):
        """
        Calculate dynamic parameters for each year based on:
        - Population growth
        - Productivity growth
        - Energy efficiency improvements
        - Renewable energy expansion
        """
        base_params = self.calibrated_data.copy()

        # Years since base year
        years_elapsed = year - self.base_year

        # 1. Population and labor force dynamics
        # 0.1% annual growth (Italy's demographic transition)
        population_growth_rate = 0.001
        population_factor = (1 + population_growth_rate) ** years_elapsed

        # 2. Productivity growth by sector
        productivity_growth = {
            'AGR': 0.015,  # 1.5% agriculture productivity growth
            'IND': 0.020,  # 2.0% industry productivity growth
            'SER': 0.018,  # 1.8% services productivity growth
            'ELE': 0.025,  # 2.5% electricity sector innovation
            'GAS': 0.010,  # 1.0% gas sector efficiency
            'OIL': 0.008   # 0.8% oil sector improvements
        }

        # 3. Energy efficiency improvements
        energy_efficiency_improvement = 0.015  # 1.5% annual improvement
        efficiency_factor = (
            1 - energy_efficiency_improvement) ** years_elapsed

        # 4. Renewable energy expansion
        renewable_growth_rate = 0.035  # 3.5% annual renewable capacity growth
        renewable_factor = (1 + renewable_growth_rate) ** years_elapsed

        # 5. Carbon pricing effects (only for ETS scenarios)
        carbon_price = 0
        if scenario == 'ETS1' and year >= 2021:
            # Industrial carbon pricing: starts at €100/tCO2, grows 3% annually
            carbon_price = 100 * (1.03 ** years_elapsed)
        elif scenario == 'ETS2' and year >= 2027:
            # Buildings & transport carbon pricing: starts at €45/tCO2 in 2027
            years_from_2027 = year - 2027
            carbon_price = 45 * \
                (1.05 ** years_from_2027) if years_from_2027 >= 0 else 0

        # Update parameters
        dynamic_params = base_params.copy()

        # Update population-dependent parameters
        for reg in model_definitions.regions:
            if f'POP_{reg}' in dynamic_params:
                dynamic_params[f'POP_{reg}'] *= population_factor
            if f'LAB_{reg}' in dynamic_params:
                dynamic_params[f'LAB_{reg}'] *= population_factor

        # Update productivity parameters
        for sec in model_definitions.sectors:
            if f'PROD_{sec}' in dynamic_params:
                growth_rate = productivity_growth.get(sec, 0.015)
                dynamic_params[f'PROD_{sec}'] *= (1 +
                                                  growth_rate) ** years_elapsed

        # Update energy efficiency
        for sec in model_definitions.sectors:
            for fuel in ['ELE', 'GAS', 'OIL']:
                param_name = f'ENERGY_INT_{sec}_{fuel}'
                if param_name in dynamic_params:
                    dynamic_params[param_name] *= efficiency_factor

        # Update renewable capacity
        if 'RENEWABLE_CAP' in dynamic_params:
            dynamic_params['RENEWABLE_CAP'] *= renewable_factor

        # Update carbon pricing
        dynamic_params['CARBON_PRICE'] = carbon_price

        return dynamic_params

    def run_single_year_simulation(self, year, scenario, dynamic_params):
        """
        Run CGE model for a single year with dynamic parameters
        """
        try:
            # Initialize model
            model = ItalianCGEModel()
            model.calibrated_data = dynamic_params
            model.current_year = year
            model.current_scenario = scenario

            # Build and solve model
            model.build_model()

            # Apply scenario-specific constraints
            if scenario == 'ETS1' and year >= 2021:
                # Add industrial carbon pricing constraint
                model.model.carbon_constraint_industrial = pyo.Constraint(
                    expr=model.model.CO2_IND <= model.model.CO2_IND_BASE *
                    (1 - 0.02 * (year - 2021))
                )
            elif scenario == 'ETS2' and year >= 2027:
                # Add buildings & transport carbon pricing constraint
                model.model.carbon_constraint_buildings = pyo.Constraint(
                    expr=model.model.CO2_HH <= model.model.CO2_HH_BASE *
                    (1 - 0.025 * (year - 2027))
                )

            # Solve model
            solution_status = model.solve_model(time_limit=600)

            if solution_status in ['optimal', 'feasible']:
                # Extract results
                results = self.extract_year_results(model, year, scenario)
                return results
            else:
                print(
                    f"⚠️  Warning: {scenario} {year} - Solution status: {solution_status}")
                return None

        except Exception as e:
            print(f"❌ Error in {scenario} {year}: {str(e)}")
            return None

    def extract_year_results(self, model, year, scenario):
        """
        Extract comprehensive results from solved model
        """
        results = {
            'year': year,
            'scenario': scenario,
            'gdp': {},
            'sectoral_output': {},
            'energy_demand': {},
            'co2_emissions': {},
            'energy_prices': {},
            'household_energy': {}
        }

        try:
            # 1. GDP by region (billions EUR)
            for reg in model_definitions.regions:
                gdp_value = 0
                for sec in model_definitions.sectors:
                    var_name = f'VA_{sec}_{reg}'
                    if hasattr(model.model, var_name):
                        var = getattr(model.model, var_name)
                        # Convert to billions
                        gdp_value += pyo.value(var) / 1000
                results['gdp'][reg] = gdp_value

            # Total GDP
            results['gdp']['TOTAL'] = sum(results['gdp'].values())

            # 2. Sectoral Output by sector and region (millions EUR)
            for sec in model_definitions.sectors:
                results['sectoral_output'][sec] = {}
                for reg in model_definitions.regions:
                    var_name = f'X_{sec}_{reg}'
                    if hasattr(model.model, var_name):
                        var = getattr(model.model, var_name)
                        results['sectoral_output'][sec][reg] = pyo.value(var)
                    else:
                        results['sectoral_output'][sec][reg] = 0

            # 3. Energy Demand by carrier and sector (TWh for electricity, bcm for gas)
            energy_carriers = ['ELE', 'GAS']
            for carrier in energy_carriers:
                results['energy_demand'][carrier] = {}
                for sec in model_definitions.sectors:
                    results['energy_demand'][carrier][sec] = {}
                    for reg in model_definitions.regions:
                        # Energy demand variable
                        var_name = f'ENERGY_{carrier}_{sec}_{reg}'
                        if hasattr(model.model, var_name):
                            var = getattr(model.model, var_name)
                            value = pyo.value(var)
                            # Convert to appropriate units
                            if carrier == 'ELE':
                                value = value / 1000  # Convert to TWh
                            elif carrier == 'GAS':
                                value = value / 1000  # Convert to bcm
                            results['energy_demand'][carrier][sec][reg] = value
                        else:
                            results['energy_demand'][carrier][sec][reg] = 0

            # 4. Household Energy Demand by region
            for carrier in energy_carriers:
                results['household_energy'][carrier] = {}
                for reg in model_definitions.regions:
                    var_name = f'ENERGY_HH_{carrier}_{reg}'
                    if hasattr(model.model, var_name):
                        var = getattr(model.model, var_name)
                        value = pyo.value(var)
                        if carrier == 'ELE':
                            value = value / 1000  # TWh
                        elif carrier == 'GAS':
                            value = value / 1000  # bcm
                        results['household_energy'][carrier][reg] = value
                    else:
                        results['household_energy'][carrier][reg] = 0

            # 5. CO2 Emissions by sector (Mt CO2)
            results['co2_emissions'] = {}
            for sec in model_definitions.sectors:
                co2_total = 0
                for reg in model_definitions.regions:
                    var_name = f'CO2_{sec}_{reg}'
                    if hasattr(model.model, var_name):
                        var = getattr(model.model, var_name)
                        co2_total += pyo.value(var)
                results['co2_emissions'][sec] = co2_total / \
                    1000  # Convert to Mt

            # Total CO2 emissions
            results['co2_emissions']['TOTAL'] = sum(
                results['co2_emissions'].values())

            # 6. Energy Prices (EUR/MWh)
            for carrier in energy_carriers:
                var_name = f'P_{carrier}'
                if hasattr(model.model, var_name):
                    var = getattr(model.model, var_name)
                    results['energy_prices'][carrier] = pyo.value(var)
                else:
                    # Fallback prices
                    if carrier == 'ELE':
                        results['energy_prices'][carrier] = 150  # EUR/MWh
                    elif carrier == 'GAS':
                        results['energy_prices'][carrier] = 45   # EUR/MWh

            return results

        except Exception as e:
            print(
                f"⚠️  Error extracting results for {scenario} {year}: {str(e)}")
            return None

    def run_full_simulation(self):
        """
        Run complete dynamic simulation for all scenarios and years
        """
        print("\n🚀 STARTING DYNAMIC CGE SIMULATION")
        print("="*60)

        total_simulations = 0
        successful_simulations = 0

        for scenario in ['BAU', 'ETS1', 'ETS2']:
            print(f"\n📊 Running {scenario} scenario...")

            scenario_results = []

            for year in self.years:
                # Check if scenario is active for this year
                if scenario == 'ETS2' and year < 2027:
                    continue  # ETS2 starts in 2027

                print(f"  📅 Simulating {scenario} {year}...", end=' ')

                # Calculate dynamic parameters
                dynamic_params = self.calculate_dynamic_parameters(
                    year, scenario)

                # Run simulation
                year_results = self.run_single_year_simulation(
                    year, scenario, dynamic_params)

                total_simulations += 1

                if year_results:
                    scenario_results.append(year_results)
                    successful_simulations += 1
                    print("✅")
                else:
                    print("❌")

            # Store scenario results
            self.results[scenario] = scenario_results

        print(f"\n✅ SIMULATION COMPLETE")
        print(f"📊 Total simulations: {total_simulations}")
        print(f"✅ Successful: {successful_simulations}")
        print(
            f"📈 Success rate: {successful_simulations/total_simulations*100:.1f}%")

        return self.results

    def export_results_to_excel(self):
        """
        Export all simulation results to comprehensive Excel file
        """
        print("\n📊 EXPORTING RESULTS TO EXCEL")
        print("="*40)

        # Create results directory
        results_dir = "results/dynamic_simulation_2021_2050"
        os.makedirs(results_dir, exist_ok=True)

        # File path
        excel_file = f"{results_dir}/Italian_CGE_Dynamic_Results_2021_2050_Complete.xlsx"

        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:

            # 1. GDP Results (Billions EUR)
            print("  📈 Exporting GDP data...")
            gdp_data = []
            for scenario in ['BAU', 'ETS1', 'ETS2']:
                if scenario in self.results:
                    for result in self.results[scenario]:
                        row = {'Year': result['year'], 'Scenario': scenario}
                        row.update({f'GDP_{reg}': result['gdp'].get(
                            reg, 0) for reg in model_definitions.regions})
                        row['GDP_TOTAL'] = result['gdp'].get('TOTAL', 0)
                        gdp_data.append(row)

            if gdp_data:
                gdp_df = pd.DataFrame(gdp_data)
                gdp_pivot = gdp_df.pivot(
                    index='Year', columns='Scenario', values='GDP_TOTAL')
                gdp_pivot.to_excel(writer, sheet_name='GDP_Total_Billions_EUR')

                # Regional GDP breakdown
                for reg in model_definitions.regions:
                    gdp_regional = gdp_df.pivot(
                        index='Year', columns='Scenario', values=f'GDP_{reg}')
                    gdp_regional.to_excel(
                        writer, sheet_name=f'GDP_{reg}_Billions_EUR')

            # 2. Sectoral Output (Millions EUR)
            print("  🏭 Exporting sectoral output...")
            for sec in model_definitions.sectors:
                sectoral_data = []
                for scenario in ['BAU', 'ETS1', 'ETS2']:
                    if scenario in self.results:
                        for result in self.results[scenario]:
                            row = {'Year': result['year'],
                                   'Scenario': scenario}
                            if sec in result['sectoral_output']:
                                row.update({f'{sec}_{reg}': result['sectoral_output'][sec].get(reg, 0)
                                           for reg in model_definitions.regions})
                            sectoral_data.append(row)

                if sectoral_data:
                    sectoral_df = pd.DataFrame(sectoral_data)
                    for reg in model_definitions.regions:
                        if f'{sec}_{reg}' in sectoral_df.columns:
                            sectoral_pivot = sectoral_df.pivot(
                                index='Year', columns='Scenario', values=f'{sec}_{reg}')
                            sectoral_pivot.to_excel(
                                writer, sheet_name=f'Output_{sec}_{reg}_MEUR')

            # 3. Energy Demand - Electricity (TWh)
            print("  ⚡ Exporting electricity demand...")
            for sec in model_definitions.sectors:
                elec_data = []
                for scenario in ['BAU', 'ETS1', 'ETS2']:
                    if scenario in self.results:
                        for result in self.results[scenario]:
                            row = {'Year': result['year'],
                                   'Scenario': scenario}
                            if 'ELE' in result['energy_demand'] and sec in result['energy_demand']['ELE']:
                                row.update({f'ELE_{sec}_{reg}': result['energy_demand']['ELE'][sec].get(reg, 0)
                                           for reg in model_definitions.regions})
                            elec_data.append(row)

                if elec_data:
                    elec_df = pd.DataFrame(elec_data)
                    for reg in model_definitions.regions:
                        if f'ELE_{sec}_{reg}' in elec_df.columns:
                            elec_pivot = elec_df.pivot(
                                index='Year', columns='Scenario', values=f'ELE_{sec}_{reg}')
                            elec_pivot.to_excel(
                                writer, sheet_name=f'Electricity_TWh_{sec}_{reg}')

            # 4. Energy Demand - Gas (bcm)
            print("  🔥 Exporting gas demand...")
            for sec in model_definitions.sectors:
                gas_data = []
                for scenario in ['BAU', 'ETS1', 'ETS2']:
                    if scenario in self.results:
                        for result in self.results[scenario]:
                            row = {'Year': result['year'],
                                   'Scenario': scenario}
                            if 'GAS' in result['energy_demand'] and sec in result['energy_demand']['GAS']:
                                row.update({f'GAS_{sec}_{reg}': result['energy_demand']['GAS'][sec].get(reg, 0)
                                           for reg in model_definitions.regions})
                            gas_data.append(row)

                if gas_data:
                    gas_df = pd.DataFrame(gas_data)
                    for reg in model_definitions.regions:
                        if f'GAS_{sec}_{reg}' in gas_df.columns:
                            gas_pivot = gas_df.pivot(
                                index='Year', columns='Scenario', values=f'GAS_{sec}_{reg}')
                            gas_pivot.to_excel(
                                writer, sheet_name=f'Gas_bcm_{sec}_{reg}')

            # 5. Household Energy Demand
            print("  🏠 Exporting household energy demand...")
            for carrier in ['ELE', 'GAS']:
                hh_energy_data = []
                for scenario in ['BAU', 'ETS1', 'ETS2']:
                    if scenario in self.results:
                        for result in self.results[scenario]:
                            row = {'Year': result['year'],
                                   'Scenario': scenario}
                            if carrier in result['household_energy']:
                                row.update({f'HH_{carrier}_{reg}': result['household_energy'][carrier].get(reg, 0)
                                           for reg in model_definitions.regions})
                            hh_energy_data.append(row)

                if hh_energy_data:
                    hh_df = pd.DataFrame(hh_energy_data)
                    for reg in model_definitions.regions:
                        if f'HH_{carrier}_{reg}' in hh_df.columns:
                            hh_pivot = hh_df.pivot(
                                index='Year', columns='Scenario', values=f'HH_{carrier}_{reg}')
                            unit = 'TWh' if carrier == 'ELE' else 'bcm'
                            hh_pivot.to_excel(
                                writer, sheet_name=f'Household_{carrier}_{unit}_{reg}')

            # 6. CO2 Emissions (Mt CO2)
            print("  🌍 Exporting CO2 emissions...")
            co2_data = []
            for scenario in ['BAU', 'ETS1', 'ETS2']:
                if scenario in self.results:
                    for result in self.results[scenario]:
                        row = {'Year': result['year'], 'Scenario': scenario}
                        row.update({f'CO2_{sec}': result['co2_emissions'].get(
                            sec, 0) for sec in model_definitions.sectors})
                        row['CO2_TOTAL'] = result['co2_emissions'].get(
                            'TOTAL', 0)
                        co2_data.append(row)

            if co2_data:
                co2_df = pd.DataFrame(co2_data)
                co2_pivot = co2_df.pivot(
                    index='Year', columns='Scenario', values='CO2_TOTAL')
                co2_pivot.to_excel(writer, sheet_name='CO2_Total_Mt')

                # Sectoral CO2 breakdown
                for sec in model_definitions.sectors:
                    co2_sectoral = co2_df.pivot(
                        index='Year', columns='Scenario', values=f'CO2_{sec}')
                    co2_sectoral.to_excel(writer, sheet_name=f'CO2_{sec}_Mt')

            # 7. Energy Prices (EUR/MWh)
            print("  💰 Exporting energy prices...")
            price_data = []
            for scenario in ['BAU', 'ETS1', 'ETS2']:
                if scenario in self.results:
                    for result in self.results[scenario]:
                        row = {'Year': result['year'], 'Scenario': scenario}
                        row.update({f'Price_{carrier}': result['energy_prices'].get(carrier, 0)
                                   for carrier in ['ELE', 'GAS']})
                        price_data.append(row)

            if price_data:
                price_df = pd.DataFrame(price_data)
                for carrier in ['ELE', 'GAS']:
                    price_pivot = price_df.pivot(
                        index='Year', columns='Scenario', values=f'Price_{carrier}')
                    price_pivot.to_excel(
                        writer, sheet_name=f'Prices_{carrier}_EUR_MWh')

        print(f"✅ Results exported to: {excel_file}")
        return excel_file


def main():
    """
    Main execution function for dynamic CGE simulation
    """
    print("🇮🇹 ITALIAN CGE MODEL - DYNAMIC SIMULATION 2021-2050")
    print("="*60)
    print("📊 Scenarios:")
    print("   • BAU: Business As Usual (2021-2050)")
    print("   • ETS1: Industrial Carbon Pricing (2021-2050)")
    print("   • ETS2: Buildings & Transport Carbon Pricing (2027-2050)")
    print("\n📈 Results Generated:")
    print("   • GDP by region (billions EUR)")
    print("   • Sectoral output (millions EUR)")
    print("   • Energy demand by carrier and sector (TWh, bcm)")
    print("   • Household energy demand by region")
    print("   • CO2 emissions (Mt CO2)")
    print("   • Energy prices (EUR/MWh)")

    start_time = time.time()

    # Initialize and run simulation
    simulation = DynamicCGESimulation()
    results = simulation.run_full_simulation()

    # Export results
    excel_file = simulation.export_results_to_excel()

    end_time = time.time()

    print(f"\n🎉 DYNAMIC SIMULATION COMPLETED!")
    print(f"⏱️  Total execution time: {end_time - start_time:.1f} seconds")
    print(f"📁 Results file: {excel_file}")
    print("\n✅ Ready for policy analysis and scenario comparison!")


if __name__ == "__main__":
    main()
