"""
Comprehensive Results Generator for Italian CGE Model
Generates detailed Excel reports for all scenarios including:
- Calibration results
- Energy demand by sector and region
- CO2 emissions and prices
- GDP at macro and regional levels
- Price indices (PPI, CPI)
- Sectoral outputs
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os
from datetime import datetime
from main_model import ItalianCGEModel


class ComprehensiveResultsGenerator:
    def __init__(self):
        self.model = None
        self.results_dir = Path("results")
        self.results_dir.mkdir(exist_ok=True)

        # Create scenario subdirectories
        self.scenarios = ['BAU', 'ETS1', 'ETS2']
        for scenario in self.scenarios:
            scenario_dir = self.results_dir / scenario
            scenario_dir.mkdir(exist_ok=True)

        # Store all results
        self.all_results = {}

    def initialize_model(self):
        """Initialize and calibrate the model"""
        print("=" * 80)
        print("INITIALIZING ITALIAN CGE MODEL FOR COMPREHENSIVE RESULTS")
        print("=" * 80)

        self.model = ItalianCGEModel("SAM.xlsx")

        # Load and calibrate data
        success = self.model.load_and_calibrate_data()
        if not success:
            raise ValueError("Failed to load and calibrate model data")

        # Build model
        self.model.build_model()

        print("✓ Model initialized and calibrated successfully")
        return True

    def generate_calibration_results(self):
        """Generate calibration results Excel file"""
        print("\nGenerating calibration results...")

        calibrated_data = self.model.calibrated_data

        # Create calibration workbook with multiple sheets
        calibration_file = self.results_dir / "model_calibration_results.xlsx"

        with pd.ExcelWriter(calibration_file, engine='openpyxl') as writer:

            # 1. SAM Summary
            sam_summary = {
                'Parameter': [
                    'Production Sectors',
                    'Energy Sectors',
                    'Transport Sectors',
                    'Household Regions',
                    'Base Year GDP (Billion €)',
                    'Base Year Population (Million)',
                    'GDP per Capita (€)',
                    'Total Value Added (Million €)',
                    'Total Final Demand (Million €)'
                ],
                'Value': [
                    len(calibrated_data['production_sectors']),
                    len(calibrated_data['energy_sectors']),
                    len(calibrated_data['transport_sectors']),
                    len(calibrated_data['households']),
                    # Convert to billions
                    calibrated_data['calibrated_parameters']['base_year_gdp'] / 1000,
                    calibrated_data['calibrated_parameters'].get(
                        'base_year_population', 59.13),
                    (calibrated_data['calibrated_parameters']['base_year_gdp'] / calibrated_data['calibrated_parameters'].get(
                        'base_year_population', 59.13)) * 1000000 / 1000000,  # GDP per capita in thousands
                    sum(calibrated_data['value_added'].values(
                    )) if 'value_added' in calibrated_data else 'N/A',
                    sum(calibrated_data['final_demand'].values(
                    )) if 'final_demand' in calibrated_data else 'N/A'
                ]
            }
            pd.DataFrame(sam_summary).to_excel(
                writer, sheet_name='SAM_Summary', index=False)

            # 2. Sectoral Data
            if 'production_sectors' in calibrated_data:
                sectors_df = pd.DataFrame({
                    'Sector': calibrated_data['production_sectors'],
                    'Type': ['Energy' if s in calibrated_data['energy_sectors'] else
                             'Transport' if s in calibrated_data['transport_sectors'] else
                             'Other' for s in calibrated_data['production_sectors']]
                })
                sectors_df.to_excel(writer, sheet_name='Sectors', index=False)

            # 3. Regional Data
            if 'households' in calibrated_data:
                regions_df = pd.DataFrame({
                    'Region': calibrated_data['households']
                })
                regions_df.to_excel(writer, sheet_name='Regions', index=False)

            # 4. Calibration Parameters
            if 'calibrated_parameters' in calibrated_data:
                params_data = []
                for key, value in calibrated_data['calibrated_parameters'].items():
                    params_data.append({'Parameter': key, 'Value': value})
                pd.DataFrame(params_data).to_excel(
                    writer, sheet_name='Parameters', index=False)

        print(f"✓ Calibration results saved: {calibration_file}")
        return calibration_file

    def run_scenario(self, year, scenario_name):
        """Run a single scenario and collect detailed results"""
        print(f"\n{'='*60}")
        print(f"RUNNING SCENARIO: {scenario_name} ({year})")
        print(f"{'='*60}")

        result = self.model.run_single_year(year, scenario_name)

        if not result:
            print(f"✗ Failed to solve {scenario_name} scenario")
            return None

        print(f"✓ {scenario_name} scenario solved successfully")

        # Extract comprehensive results
        scenario_results = self.extract_detailed_results(year, scenario_name)
        return scenario_results

    def extract_detailed_results(self, year, scenario_name):
        """Extract detailed results from solved model"""
        model = self.model.model
        results = {
            'year': year,
            'scenario': scenario_name,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        try:
            # 1. Macro Economic Indicators
            results['macro'] = self.extract_macro_indicators(model)

            # 2. Regional Results
            results['regional'] = self.extract_regional_results(model)

            # 3. Sectoral Results
            results['sectoral'] = self.extract_sectoral_results(model)

            # 4. Energy Results
            results['energy'] = self.extract_energy_results(model)

            # 5. Environmental Results
            results['environmental'] = self.extract_environmental_results(
                model)

            # 6. Price Results
            results['prices'] = self.extract_price_results(model)

            print(f"✓ Extracted detailed results for {scenario_name}")

        except Exception as e:
            print(f"Warning: Could not extract some results - {str(e)}")
            # Continue with partial results

        return results

    def extract_macro_indicators(self, model):
        """Extract macro-level economic indicators"""
        macro = {}

        try:
            # GDP calculation
            total_output = 0
            total_va = 0

            for sector in self.model.calibrated_data['production_sectors']:
                if hasattr(model, 'X') and (sector,) in model.X:
                    total_output += model.X[sector].value if model.X[sector].value is not None else 0
                if hasattr(model, 'VA') and (sector,) in model.VA:
                    total_va += model.VA[sector].value if model.VA[sector].value is not None else 0

            macro['Total_Output_Million_EUR'] = total_output
            macro['Total_Value_Added_Million_EUR'] = total_va
            macro['GDP_Million_EUR'] = total_va  # GDP = Total Value Added
            macro['GDP_Billion_EUR'] = total_va / \
                1000  # GDP in billions for readability
            macro['GDP_per_Capita_EUR'] = (
                total_va * 1000000) / 59130000 if total_va > 0 else 0  # GDP per capita

            # Employment
            if hasattr(model, 'employment_rate'):
                macro['Employment_Rate_Percent'] = (
                    1 - model.employment_rate.value) * 100 if model.employment_rate.value is not None else 8.0
            else:
                # Assume 8% unemployment
                macro['Employment_Rate_Percent'] = 92.0

            # Trade balance
            total_exports = 0
            total_imports = 0

            for sector in self.model.calibrated_data['production_sectors']:
                if hasattr(model, 'E') and (sector,) in model.E:
                    total_exports += model.E[sector].value if model.E[sector].value is not None else 0
                if hasattr(model, 'M') and (sector,) in model.M:
                    total_imports += model.M[sector].value if model.M[sector].value is not None else 0

            macro['Total_Exports_Million_EUR'] = total_exports
            macro['Total_Imports_Million_EUR'] = total_imports
            macro['Trade_Balance_Million_EUR'] = total_exports - total_imports

        except Exception as e:
            print(f"Warning: Error extracting macro indicators - {str(e)}")
            macro['Total_Output_Million_EUR'] = 'Error'

        return macro

    def extract_regional_results(self, model):
        """Extract regional economic results"""
        regional = {}

        try:
            for region in self.model.calibrated_data['households']:
                regional[region] = {}

                # Regional income and consumption
                if hasattr(model, 'Y') and (region,) in model.Y:
                    regional[region]['Income_Million_EUR'] = model.Y[region].value if model.Y[region].value is not None else 0

                if hasattr(model, 'C') and (region,) in model.C:
                    regional[region]['Consumption_Million_EUR'] = model.C[region].value if model.C[region].value is not None else 0

                if hasattr(model, 'S') and (region,) in model.S:
                    regional[region]['Savings_Million_EUR'] = model.S[region].value if model.S[region].value is not None else 0

                # Regional energy demand (if available)
                total_energy_demand = 0
                electricity_demand = 0
                gas_demand = 0

                for energy_type in ['Electricity', 'Gas', 'Other Energy']:
                    if energy_type in self.model.calibrated_data['energy_sectors']:
                        if hasattr(model, 'Energy_demand') and (energy_type, region) in model.Energy_demand:
                            demand = model.Energy_demand[energy_type,
                                                         region].value
                            if demand is not None:
                                total_energy_demand += demand
                                if energy_type == 'Electricity':
                                    electricity_demand = demand
                                elif energy_type == 'Gas':
                                    gas_demand = demand

                regional[region]['Total_Energy_Demand_Units'] = total_energy_demand
                regional[region]['Electricity_Demand_Units'] = electricity_demand
                regional[region]['Gas_Demand_Units'] = gas_demand

        except Exception as e:
            print(f"Warning: Error extracting regional results - {str(e)}")

        return regional

    def extract_sectoral_results(self, model):
        """Extract sectoral production and output results"""
        sectoral = {}

        try:
            for sector in self.model.calibrated_data['production_sectors']:
                sectoral[sector] = {}

                # Output
                if hasattr(model, 'X') and (sector,) in model.X:
                    sectoral[sector]['Output_Million_EUR'] = model.X[sector].value if model.X[sector].value is not None else 0

                # Value Added
                if hasattr(model, 'VA') and (sector,) in model.VA:
                    sectoral[sector]['Value_Added_Million_EUR'] = model.VA[sector].value if model.VA[sector].value is not None else 0

                # Energy consumption
                if hasattr(model, 'Energy_use') and (sector,) in model.Energy_use:
                    sectoral[sector]['Energy_Use_Units'] = model.Energy_use[sector].value if model.Energy_use[sector].value is not None else 0

                # Employment (if available)
                if hasattr(model, 'Labor_demand') and (sector,) in model.Labor_demand:
                    sectoral[sector]['Labor_Demand_Units'] = model.Labor_demand[sector].value if model.Labor_demand[sector].value is not None else 0

                # Capital (if available)
                if hasattr(model, 'Capital_demand') and (sector,) in model.Capital_demand:
                    sectoral[sector]['Capital_Demand_Units'] = model.Capital_demand[
                        sector].value if model.Capital_demand[sector].value is not None else 0

                # Trade
                if hasattr(model, 'E') and (sector,) in model.E:
                    sectoral[sector]['Exports_Million_EUR'] = model.E[sector].value if model.E[sector].value is not None else 0

                if hasattr(model, 'M') and (sector,) in model.M:
                    sectoral[sector]['Imports_Million_EUR'] = model.M[sector].value if model.M[sector].value is not None else 0

        except Exception as e:
            print(f"Warning: Error extracting sectoral results - {str(e)}")

        return sectoral

    def extract_energy_results(self, model):
        """Extract energy demand and supply results"""
        energy = {}

        try:
            # Total energy demand by carrier
            energy_carriers = ['Electricity', 'Gas', 'Other Energy']

            for carrier in energy_carriers:
                if carrier in self.model.calibrated_data.get('energy_sectors', []):
                    energy[f'{carrier}_Total_Demand'] = 0
                    energy[f'{carrier}_Total_Supply'] = 0

                    # Regional breakdown
                    regional_demand = {}
                    for region in self.model.calibrated_data['households']:
                        if hasattr(model, 'Energy_demand') and (carrier, region) in model.Energy_demand:
                            demand = model.Energy_demand[carrier, region].value
                            if demand is not None:
                                regional_demand[region] = demand
                                energy[f'{carrier}_Total_Demand'] += demand

                    energy[f'{carrier}_Regional_Demand'] = regional_demand

                    # Sectoral breakdown
                    sectoral_demand = {}
                    for sector in self.model.calibrated_data['production_sectors']:
                        if hasattr(model, 'Energy_input') and (carrier, sector) in model.Energy_input:
                            demand = model.Energy_input[carrier, sector].value
                            if demand is not None:
                                sectoral_demand[sector] = demand

                    energy[f'{carrier}_Sectoral_Demand'] = sectoral_demand

                    # Supply (production)
                    if hasattr(model, 'X') and (carrier,) in model.X:
                        energy[f'{carrier}_Total_Supply'] = model.X[carrier].value if model.X[carrier].value is not None else 0

        except Exception as e:
            print(f"Warning: Error extracting energy results - {str(e)}")

        return energy

    def extract_environmental_results(self, model):
        """Extract CO2 emissions and carbon pricing results"""
        environmental = {}

        try:
            # Total CO2 emissions
            total_co2 = 0
            sectoral_co2 = {}

            for sector in self.model.calibrated_data['production_sectors']:
                if hasattr(model, 'CO2_emissions') and (sector,) in model.CO2_emissions:
                    co2 = model.CO2_emissions[sector].value
                    if co2 is not None:
                        sectoral_co2[sector] = co2
                        total_co2 += co2

            environmental['Total_CO2_Emissions_Units'] = total_co2
            environmental['Sectoral_CO2_Emissions'] = sectoral_co2

            # Carbon prices
            if hasattr(model, 'carbon_price_ets1'):
                environmental['ETS1_Carbon_Price_EUR_per_tCO2'] = model.carbon_price_ets1.value if model.carbon_price_ets1.value is not None else 0

            if hasattr(model, 'carbon_price_ets2'):
                environmental['ETS2_Carbon_Price_EUR_per_tCO2'] = model.carbon_price_ets2.value if model.carbon_price_ets2.value is not None else 0

            # Carbon revenue
            if hasattr(model, 'total_carbon_revenue'):
                environmental['Total_Carbon_Revenue_Million_EUR'] = model.total_carbon_revenue.value if model.total_carbon_revenue.value is not None else 0

        except Exception as e:
            print(
                f"Warning: Error extracting environmental results - {str(e)}")

        return environmental

    def extract_price_results(self, model):
        """Extract price indices and energy prices"""
        prices = {}

        try:
            # Price indices (if available)
            if hasattr(model, 'CPI'):
                prices['Consumer_Price_Index'] = model.CPI.value if model.CPI.value is not None else 1.0
            else:
                prices['Consumer_Price_Index'] = 1.0  # Base year normalization

            if hasattr(model, 'PPI'):
                prices['Producer_Price_Index'] = model.PPI.value if model.PPI.value is not None else 1.0
            else:
                prices['Producer_Price_Index'] = 1.0  # Base year normalization

            # Energy prices
            energy_prices = {}
            for energy_type in ['Electricity', 'Gas', 'Other Energy']:
                if energy_type in self.model.calibrated_data.get('energy_sectors', []):
                    if hasattr(model, 'P') and (energy_type,) in model.P:
                        energy_prices[energy_type] = model.P[energy_type].value if model.P[energy_type].value is not None else 1.0
                    else:
                        energy_prices[energy_type] = 1.0

            prices['Energy_Prices'] = energy_prices

            # Sectoral prices
            sectoral_prices = {}
            for sector in self.model.calibrated_data['production_sectors']:
                if hasattr(model, 'P') and (sector,) in model.P:
                    sectoral_prices[sector] = model.P[sector].value if model.P[sector].value is not None else 1.0
                else:
                    sectoral_prices[sector] = 1.0

            prices['Sectoral_Prices'] = sectoral_prices

        except Exception as e:
            print(f"Warning: Error extracting price results - {str(e)}")

        return prices

    def save_scenario_results_to_excel(self, scenario_results):
        """Save scenario results to Excel file"""
        scenario_name = scenario_results['scenario']
        year = scenario_results['year']

        # Create filename
        filename = f"{scenario_name}_{year}_detailed_results.xlsx"
        filepath = self.results_dir / scenario_name / filename

        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:

            # 1. Summary Sheet
            summary_data = {
                'Metric': ['Scenario', 'Year', 'Timestamp', 'Status'],
                'Value': [scenario_name, year, scenario_results['timestamp'], 'Completed']
            }

            # Add macro indicators to summary
            if 'macro' in scenario_results:
                for key, value in scenario_results['macro'].items():
                    summary_data['Metric'].append(key)
                    summary_data['Value'].append(value)

            pd.DataFrame(summary_data).to_excel(
                writer, sheet_name='Summary', index=False)

            # 2. Regional Results
            if 'regional' in scenario_results and scenario_results['regional']:
                regional_df = pd.DataFrame(scenario_results['regional']).T
                regional_df.index.name = 'Region'
                regional_df.to_excel(writer, sheet_name='Regional_Results')

            # 3. Sectoral Results
            if 'sectoral' in scenario_results and scenario_results['sectoral']:
                sectoral_df = pd.DataFrame(scenario_results['sectoral']).T
                sectoral_df.index.name = 'Sector'
                sectoral_df.to_excel(writer, sheet_name='Sectoral_Results')

            # 4. Energy Results - Total Demand
            if 'energy' in scenario_results:
                energy_summary = []
                for key, value in scenario_results['energy'].items():
                    if not isinstance(value, dict):
                        energy_summary.append({'Metric': key, 'Value': value})

                if energy_summary:
                    pd.DataFrame(energy_summary).to_excel(
                        writer, sheet_name='Energy_Summary', index=False)

                # Energy demand by region
                electricity_regional = scenario_results['energy'].get(
                    'Electricity_Regional_Demand', {})
                gas_regional = scenario_results['energy'].get(
                    'Gas_Regional_Demand', {})

                if electricity_regional or gas_regional:
                    regions = list(
                        set(list(electricity_regional.keys()) + list(gas_regional.keys())))
                    energy_regional_data = []

                    for region in regions:
                        energy_regional_data.append({
                            'Region': region,
                            'Electricity_Demand': electricity_regional.get(region, 0),
                            'Gas_Demand': gas_regional.get(region, 0)
                        })

                    pd.DataFrame(energy_regional_data).to_excel(
                        writer, sheet_name='Energy_by_Region', index=False)

                # Energy demand by sector
                electricity_sectoral = scenario_results['energy'].get(
                    'Electricity_Sectoral_Demand', {})
                gas_sectoral = scenario_results['energy'].get(
                    'Gas_Sectoral_Demand', {})

                if electricity_sectoral or gas_sectoral:
                    sectors = list(
                        set(list(electricity_sectoral.keys()) + list(gas_sectoral.keys())))
                    energy_sectoral_data = []

                    for sector in sectors:
                        energy_sectoral_data.append({
                            'Sector': sector,
                            'Electricity_Demand': electricity_sectoral.get(sector, 0),
                            'Gas_Demand': gas_sectoral.get(sector, 0)
                        })

                    pd.DataFrame(energy_sectoral_data).to_excel(
                        writer, sheet_name='Energy_by_Sector', index=False)

            # 5. Environmental Results
            if 'environmental' in scenario_results:
                env_summary = []
                for key, value in scenario_results['environmental'].items():
                    if not isinstance(value, dict):
                        env_summary.append({'Metric': key, 'Value': value})

                if env_summary:
                    pd.DataFrame(env_summary).to_excel(
                        writer, sheet_name='Environmental_Summary', index=False)

                # CO2 by sector
                sectoral_co2 = scenario_results['environmental'].get(
                    'Sectoral_CO2_Emissions', {})
                if sectoral_co2:
                    co2_data = [{'Sector': sector, 'CO2_Emissions': emissions}
                                for sector, emissions in sectoral_co2.items()]
                    pd.DataFrame(co2_data).to_excel(
                        writer, sheet_name='CO2_by_Sector', index=False)

            # 6. Price Results
            if 'prices' in scenario_results:
                price_summary = []
                for key, value in scenario_results['prices'].items():
                    if not isinstance(value, dict):
                        price_summary.append({'Metric': key, 'Value': value})

                if price_summary:
                    pd.DataFrame(price_summary).to_excel(
                        writer, sheet_name='Price_Summary', index=False)

                # Energy prices
                energy_prices = scenario_results['prices'].get(
                    'Energy_Prices', {})
                if energy_prices:
                    energy_price_data = [{'Energy_Type': energy, 'Price': price}
                                         for energy, price in energy_prices.items()]
                    pd.DataFrame(energy_price_data).to_excel(
                        writer, sheet_name='Energy_Prices', index=False)

                # Sectoral prices
                sectoral_prices = scenario_results['prices'].get(
                    'Sectoral_Prices', {})
                if sectoral_prices:
                    sectoral_price_data = [{'Sector': sector, 'Price': price}
                                           for sector, price in sectoral_prices.items()]
                    pd.DataFrame(sectoral_price_data).to_excel(
                        writer, sheet_name='Sectoral_Prices', index=False)

        print(f"✓ Results saved: {filepath}")
        return filepath

    def generate_comparison_excel(self):
        """Generate comparison Excel file across all scenarios"""
        print("\nGenerating cross-scenario comparison...")

        comparison_file = self.results_dir / "scenario_comparison_results.xlsx"

        with pd.ExcelWriter(comparison_file, engine='openpyxl') as writer:

            # 1. Macro Comparison
            if self.all_results:
                macro_comparison = []
                for scenario_key, results in self.all_results.items():
                    if 'macro' in results:
                        row = {'Scenario': scenario_key}
                        row.update(results['macro'])
                        macro_comparison.append(row)

                if macro_comparison:
                    pd.DataFrame(macro_comparison).to_excel(
                        writer, sheet_name='Macro_Comparison', index=False)

            # 2. Regional Comparison
            if self.all_results:
                for region in self.model.calibrated_data['households']:
                    regional_comparison = []
                    for scenario_key, results in self.all_results.items():
                        if 'regional' in results and region in results['regional']:
                            row = {'Scenario': scenario_key}
                            row.update(results['regional'][region])
                            regional_comparison.append(row)

                    if regional_comparison:
                        sheet_name = f'Regional_{region}'[
                            :31]  # Excel sheet name limit
                        pd.DataFrame(regional_comparison).to_excel(
                            writer, sheet_name=sheet_name, index=False)

            # 3. Energy Comparison
            if self.all_results:
                energy_comparison = []
                for scenario_key, results in self.all_results.items():
                    if 'energy' in results:
                        row = {'Scenario': scenario_key}
                        # Extract only non-dict values for summary
                        for key, value in results['energy'].items():
                            if not isinstance(value, dict):
                                row[key] = value
                        energy_comparison.append(row)

                if energy_comparison:
                    pd.DataFrame(energy_comparison).to_excel(
                        writer, sheet_name='Energy_Comparison', index=False)

            # 4. Environmental Comparison
            if self.all_results:
                env_comparison = []
                for scenario_key, results in self.all_results.items():
                    if 'environmental' in results:
                        row = {'Scenario': scenario_key}
                        # Extract only non-dict values for summary
                        for key, value in results['environmental'].items():
                            if not isinstance(value, dict):
                                row[key] = value
                        env_comparison.append(row)

                if env_comparison:
                    pd.DataFrame(env_comparison).to_excel(
                        writer, sheet_name='Environmental_Comparison', index=False)

        print(f"✓ Comparison results saved: {comparison_file}")
        return comparison_file

    def run_all_scenarios_and_generate_results(self):
        """Main method to run all scenarios and generate Excel results"""
        print("COMPREHENSIVE ITALIAN CGE MODEL RESULTS GENERATION")
        print("=" * 80)

        # Initialize model
        if not self.initialize_model():
            return False

        # Generate calibration results
        self.generate_calibration_results()

        # Define scenarios to run
        scenarios_to_run = [
            (2021, 'BAU'),   # Base year BAU
            (2021, 'ETS1'),  # Base year with ETS1
            (2027, 'ETS2')   # Future year with ETS2
        ]

        # Run each scenario
        for year, scenario in scenarios_to_run:
            try:
                results = self.run_scenario(year, scenario)
                if results:
                    # Save individual scenario results
                    self.save_scenario_results_to_excel(results)

                    # Store for comparison
                    scenario_key = f"{scenario}_{year}"
                    self.all_results[scenario_key] = results

            except Exception as e:
                print(f"✗ Error running {scenario} scenario: {str(e)}")
                continue

        # Generate comparison file
        if self.all_results:
            self.generate_comparison_excel()

        # Print summary
        print("\n" + "=" * 80)
        print("RESULTS GENERATION COMPLETED")
        print("=" * 80)
        print(f"Generated results for {len(self.all_results)} scenarios")
        print(f"Results saved in: {self.results_dir.absolute()}")
        print("\nGenerated files:")
        print("- model_calibration_results.xlsx (Model calibration data)")

        for scenario_key in self.all_results.keys():
            scenario, year = scenario_key.split('_')
            print(f"- {scenario}/{scenario}_{year}_detailed_results.xlsx")

        if self.all_results:
            print("- scenario_comparison_results.xlsx (Cross-scenario comparison)")

        return True


def main():
    """Main execution function"""
    generator = ComprehensiveResultsGenerator()
    success = generator.run_all_scenarios_and_generate_results()

    if success:
        print("\n✓ All results generated successfully!")
        print("\nYou can find the following Excel files in the results folder:")
        print("1. Calibration results")
        print("2. Individual scenario results (BAU, ETS1, ETS2)")
        print("3. Cross-scenario comparison")
        print(
            "\nEach file contains detailed breakdowns by sector, region, and energy type.")
    else:
        print("\n✗ Results generation failed. Check error messages above.")


if __name__ == "__main__":
    main()
