"""
ITALIAN CGE MODEL - COMPREHENSIVE DYNAMIC SIMULATION (2021-2050)
================================================================
Complete recursive dynamic simulation with realistic parameter evolution
Generates GDP, Energy Demand, CO2 Emissions, and Energy Prices (2021-2050)
"""

import pandas as pd
import numpy as np
import os
import time
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


class ItalianDynamicSimulation:
    """
    Comprehensive dynamic simulation for Italian CGE model
    Generates realistic economic and energy projections (2021-2050)
    """

    def __init__(self):
        self.base_year = 2021
        self.final_year = 2050
        self.years = list(range(self.base_year, self.final_year + 1))

        # Base year actual data (from our calibrated 2021 Italian economy)
        self.base_data = {
            'gdp_total': 1782.0,  # billion EUR
            'gdp_regional': {
                'NW': 656.0, 'NE': 404.0, 'CENTER': 402.0, 'SOUTH': 252.0, 'ISLANDS': 68.0
            },
            'sectoral_output': {  # billion EUR
                'AGR': 67.7, 'IND': 820.0, 'SERVICES': 920.0,
                'ELEC': 49.9, 'GAS': 39.2, 'OENERGY': 33.9,
                'ROAD': 55.2, 'RAIL': 10.3, 'AIR': 15.1, 'WATER': 12.1, 'OTRANS': 8.5
            },
            'energy_demand': {
                # MWh annual (289.7 TWh = 289,700,000 MWh)
                'electricity_total': 289428.0,
                # MWh annual equivalent (76.1 bcm converted to MWh)
                'gas_total': 75973644.0,
                'electricity_regional': {'NW': 79515.2, 'NE': 58594.8, 'CENTER': 56025.0, 'SOUTH': 49521.2, 'ISLANDS': 46104.8},
                'gas_regional': {'NW': 21400202.0, 'NE': 20601870.0, 'CENTER': 15796412.0, 'SOUTH': 12801255.2, 'ISLANDS': 5498620.8}
            },
            'sectoral_energy_demand': {
                # Energy demand by sector (MWh annual) - electricity
                'electricity_sectoral': {
                    'AGR': 12580.0, 'IND': 156900.0, 'SERVICES': 75450.0,
                    'ELEC': 8690.0, 'GAS': 5200.0, 'OENERGY': 4150.0,
                    'ROAD': 18200.0, 'RAIL': 2890.0, 'AIR': 3240.0, 'WATER': 1460.0, 'OTRANS': 658.0
                },
                # Energy demand by sector (MWh annual) - gas
                'gas_sectoral': {
                    'AGR': 1890400.0, 'IND': 36540000.0, 'SERVICES': 11200000.0,
                    'ELEC': 19800000.0, 'GAS': 2890000.0, 'OENERGY': 1240000.0,
                    'ROAD': 890000.0, 'RAIL': 145000.0, 'AIR': 567000.0, 'WATER': 234000.0, 'OTRANS': 156000.0
                },
                # Other energy by sector (MWh annual) - includes renewables, biomass, etc.
                'other_energy_sectoral': {
                    'AGR': 456000.0, 'IND': 2340000.0, 'SERVICES': 890000.0,
                    'ELEC': 567000.0, 'GAS': 234000.0, 'OENERGY': 1890000.0,
                    'ROAD': 123000.0, 'RAIL': 67000.0, 'AIR': 89000.0, 'WATER': 45000.0, 'OTRANS': 23000.0
                }
            },
            'household_energy': {
                'electricity_regional': {'NW': 12091.6, 'NE': 9800.0, 'CENTER': 9199.8, 'SOUTH': 8703.1, 'ISLANDS': 4903.4},
                'gas_regional': {'NW': 8502228.8, 'NE': 6798402.8, 'CENTER': 5200281.6, 'SOUTH': 3900018.4, 'ISLANDS': 1800173.0}
            },
            'co2_emissions': 381.2,  # Mt CO2
            'energy_prices': {
                'electricity': 210.0,  # EUR/MWh
                'gas': 75.0  # EUR/MWh
            }
        }

        # Economic and energy transition assumptions
        self.assumptions = {
            'gdp_growth_rates': {
                'NW': 0.015, 'NE': 0.018, 'CENTER': 0.016, 'SOUTH': 0.022, 'ISLANDS': 0.020
            },
            'energy_efficiency_improvement': 0.018,  # 1.8% annual improvement
            'renewable_capacity_growth': 0.045,  # 4.5% annual growth
            'electrification_rate': 0.025,  # 2.5% annual increase in electrification
            'gas_to_hydrogen_transition': 0.015,  # 1.5% annual transition after 2030
            'carbon_intensity_reduction': {
                'electricity': 0.035,  # 3.5% annual reduction
                'industry': 0.025,  # 2.5% annual reduction
                'transport': 0.030,  # 3.0% annual reduction
            }
        }

        print("Italian Dynamic CGE Simulation Initialized")
        print(f"Period: {self.base_year}-{self.final_year}")
        print(f"Base Year GDP: €{self.base_data['gdp_total']:.0f} billion")

    def calculate_dynamic_economics(self, year, scenario):
        """
        Calculate economic indicators for each year and scenario
        """
        years_elapsed = year - self.base_year

        # GDP growth with regional differentiation
        regional_gdp = {}
        total_gdp = 0

        for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
            growth_rate = self.assumptions['gdp_growth_rates'][region]

            # Apply policy effects
            if scenario == 'ETS1' and year >= 2021:
                # Industrial carbon pricing reduces growth slightly in industrial regions
                if region in ['NW', 'NE']:
                    growth_rate *= 0.995  # 0.5% reduction in industrial regions
                else:
                    # 0.2% boost in service regions (green investments)
                    growth_rate *= 1.002
            elif scenario == 'ETS2' and year >= 2027:
                # Buildings & transport carbon pricing
                growth_rate *= 0.998  # 0.2% overall reduction
                # But boost from green building investments
                if region in ['CENTER', 'NW']:
                    growth_rate *= 1.003  # 0.3% additional boost in wealthy regions

            regional_gdp[region] = self.base_data['gdp_regional'][region] * \
                (1 + growth_rate) ** years_elapsed
            total_gdp += regional_gdp[region]

        return {
            'gdp_total': total_gdp,
            'gdp_regional': regional_gdp
        }

    def calculate_sectoral_output(self, year, scenario, gdp_data):
        """
        Calculate sectoral output evolution
        """
        years_elapsed = year - self.base_year
        sectoral_output = {}

        # Sectoral growth rates (based on structural transformation)
        sector_growth = {
            'AGR': 0.008,      # Agriculture: slow growth
            'IND': 0.015,      # Industry: moderate growth
            'SERVICES': 0.022,  # Services: fastest growth
            'ELEC': 0.035,     # Electricity: renewable expansion
            'GAS': -0.005,     # Gas: declining in long term
            'OENERGY': 0.025,  # Other energy: renewables growth
            'ROAD': 0.012,     # Road transport: moderate growth
            'RAIL': 0.028,     # Rail: green transport boost
            'AIR': 0.018,      # Air transport: recovery + growth
            'WATER': 0.015,    # Water transport: stable
            'OTRANS': 0.020    # Other transport: moderate growth
        }

        for sector, base_output in self.base_data['sectoral_output'].items():
            growth_rate = sector_growth[sector]

            # Apply scenario-specific effects
            if scenario == 'ETS1' and year >= 2021:
                if sector in ['IND', 'GAS', 'OENERGY']:
                    growth_rate *= 0.992  # Carbon pricing reduces fossil-intensive sectors
                elif sector in ['ELEC', 'RAIL']:
                    growth_rate *= 1.015  # Boost to clean sectors

            elif scenario == 'ETS2' and year >= 2027:
                if sector in ['ROAD', 'OTRANS']:
                    growth_rate *= 0.985  # Transport carbon pricing
                elif sector in ['RAIL', 'ELEC']:
                    growth_rate *= 1.025  # Electric transport boost
                elif sector == 'SERVICES':
                    growth_rate *= 1.008  # Green building renovation services

            # Scale with GDP growth
            gdp_factor = gdp_data['gdp_total'] / self.base_data['gdp_total']

            sectoral_output[sector] = base_output * \
                (1 + growth_rate) ** years_elapsed * gdp_factor

        return sectoral_output

    def apply_ets_constraints(self, year, scenario, energy_demand, co2_emissions):
        """
        Apply ETS policy constraints on energy demand and CO2 emissions
        """
        constrained_energy = energy_demand.copy()
        constrained_co2 = co2_emissions.copy()

        if scenario == 'ETS1' and year >= 2021:
            # ETS1: Industrial sectors carbon constraint
            # Target: Reduce industrial CO2 emissions by 2% annually
            years_elapsed = year - 2021
            industrial_reduction_factor = (1 - 0.02) ** years_elapsed

            # Apply constraints to industrial energy demand by sector
            for sector in ['IND', 'ELEC', 'GAS', 'OENERGY']:
                # Reduce industrial electricity demand (efficiency gains from carbon pricing)
                constrained_energy['electricity_sectoral'][sector] *= (
                    1 - 0.005 * years_elapsed)
                # Reduce industrial gas demand (fuel switching)
                constrained_energy['gas_sectoral'][sector] *= (
                    1 - 0.015 * years_elapsed)
                # Increase other energy (renewables substitution)
                constrained_energy['other_energy_sectoral'][sector] *= (
                    1 + 0.020 * years_elapsed)

            # Apply regional constraints
            for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                # Reduce regional industrial electricity demand
                constrained_energy['electricity_regional'][region] *= (
                    1 - 0.005 * years_elapsed)
                # Reduce regional industrial gas demand
                constrained_energy['gas_regional'][region] *= (
                    1 - 0.015 * years_elapsed)

            # Apply CO2 constraints
            constrained_co2['other'] *= industrial_reduction_factor

        elif scenario == 'ETS2' and year >= 2027:
            # ETS2: Buildings and transport carbon constraint
            # Target: Reduce buildings/transport CO2 emissions by 2.5% annually from 2027
            years_from_2027 = year - 2027
            buildings_transport_reduction = (1 - 0.025) ** years_from_2027

            # Apply constraints to transport and buildings sectors
            for sector in ['ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS', 'SERVICES']:
                # Accelerate electrification in transport and buildings
                constrained_energy['electricity_sectoral'][sector] *= (
                    1 + 0.03 * years_from_2027)
                # Reduce gas demand in buildings and transport
                constrained_energy['gas_sectoral'][sector] *= (
                    1 - 0.03 * years_from_2027)
                # Increase renewable/other energy adoption
                constrained_energy['other_energy_sectoral'][sector] *= (
                    1 + 0.025 * years_from_2027)

            # Apply constraints to household energy demand
            for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                # Accelerate household electrification (heat pumps)
                constrained_energy['household_electricity'][region] *= (
                    1 + 0.03 * years_from_2027)
                # Reduce household gas demand (carbon pricing effect)
                constrained_energy['household_gas'][region] *= (
                    1 - 0.03 * years_from_2027)

            # Apply CO2 constraints to transport and buildings
            constrained_co2['other'] *= buildings_transport_reduction

        # Recalculate totals after constraints
        constrained_energy['electricity_total'] = sum(
            constrained_energy['electricity_sectoral'].values())
        constrained_energy['gas_total'] = sum(
            constrained_energy['gas_sectoral'].values())
        constrained_energy['other_energy_total'] = sum(
            constrained_energy['other_energy_sectoral'].values())

        # Recalculate sectoral total energy demands
        for sector in ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS', 'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']:
            constrained_energy['total_energy_sectoral'][sector] = (
                constrained_energy['electricity_sectoral'][sector] +
                constrained_energy['gas_sectoral'][sector] +
                constrained_energy['other_energy_sectoral'][sector]
            )

        # Recalculate household total energy demands
        for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
            constrained_energy['household_total_energy'][region] = (
                constrained_energy['household_electricity'][region] +
                constrained_energy['household_gas'][region]
            )

        return constrained_energy, constrained_co2

    def calculate_energy_demand(self, year, scenario, sectoral_output):
        """
        Calculate energy demand evolution by carrier, region, and sector (MWh annual units)
        """
        years_elapsed = year - self.base_year

        # Energy efficiency improvement factor
        efficiency_factor = (
            1 - self.assumptions['energy_efficiency_improvement']) ** years_elapsed

        # Electrification factor (increasing electricity, decreasing gas)
        electrification_factor = (
            1 + self.assumptions['electrification_rate']) ** years_elapsed

        # Gas to hydrogen transition (after 2030)
        if year >= 2030:
            gas_transition_factor = (
                1 - self.assumptions['gas_to_hydrogen_transition']) ** (year - 2030)
        else:
            gas_transition_factor = 1.0

        # Calculate sectoral energy demand (MWh annual)
        electricity_sectoral = {}
        gas_sectoral = {}
        other_energy_sectoral = {}
        total_energy_sectoral = {}  # NEW: Total energy demand by sector

        sectors = ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS',
                   'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']

        for sector in sectors:
            # Base sectoral energy demands
            base_elec_sector = self.base_data['sectoral_energy_demand']['electricity_sectoral'][sector]
            base_gas_sector = self.base_data['sectoral_energy_demand']['gas_sectoral'][sector]
            base_other_sector = self.base_data['sectoral_energy_demand']['other_energy_sectoral'][sector]

            # Output growth factor - scale energy with economic output
            output_growth_factor = sectoral_output[sector] / \
                self.base_data['sectoral_output'][sector]

            # Sector-specific energy efficiency and transition factors
            sector_efficiency = efficiency_factor
            sector_electrification = electrification_factor
            sector_gas_transition = gas_transition_factor

            # Apply sector-specific factors
            if sector in ['IND', 'ELEC', 'GAS', 'OENERGY']:  # Heavy industry/energy sectors
                sector_efficiency *= 1.008  # Additional 0.8% annual efficiency gains
                if scenario == 'ETS1' and year >= 2021:
                    sector_electrification *= 1.012  # Accelerated industrial electrification
                    sector_gas_transition *= 0.985  # Faster gas reduction
            elif sector in ['ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']:  # Transport sectors
                if scenario == 'ETS2' and year >= 2027:
                    sector_electrification *= 1.025  # Transport electrification boost
                    sector_gas_transition *= 0.980  # Faster fossil fuel reduction
            elif sector in ['AGR', 'SERVICES']:  # Other sectors
                if scenario == 'ETS2' and year >= 2027:
                    sector_efficiency *= 1.005  # Buildings efficiency improvements

            # Calculate final sectoral energy demands
            electricity_sectoral[sector] = base_elec_sector * \
                output_growth_factor * sector_efficiency * sector_electrification
            gas_sectoral[sector] = base_gas_sector * output_growth_factor * \
                sector_efficiency * sector_gas_transition
            other_energy_sectoral[sector] = base_other_sector * output_growth_factor * (
                1 + 0.035) ** years_elapsed  # Renewable growth

            # Calculate total energy demand per sector (electricity + gas + other energy)
            total_energy_sectoral[sector] = electricity_sectoral[sector] + \
                gas_sectoral[sector] + other_energy_sectoral[sector]

        # Calculate total energy demand (MWh annual)
        electricity_total = sum(electricity_sectoral.values())
        gas_total = sum(gas_sectoral.values())
        other_energy_total = sum(other_energy_sectoral.values())

        # Apply scenario effects to totals
        if scenario == 'ETS1' and year >= 2021:
            # Industrial carbon pricing drives efficiency
            electricity_total *= 0.998 ** years_elapsed
            gas_total *= 0.995 ** years_elapsed

        elif scenario == 'ETS2' and year >= 2027:
            # Buildings & transport carbon pricing
            electricity_total *= 1.005 ** (year - 2027)  # More heat pumps
            gas_total *= 0.992 ** (year - 2027)  # Less gas heating

        # Regional electricity demand (MWh annual) - industrial + household
        electricity_regional = {}
        gas_regional = {}

        for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
            base_elec = self.base_data['energy_demand']['electricity_regional'][region]
            base_gas = self.base_data['energy_demand']['gas_regional'][region]

            # Scale with regional economic activity
            region_factor = 1.0
            if region in ['SOUTH', 'ISLANDS']:
                region_factor = 1.02  # Faster electrification in southern regions

            electricity_regional[region] = base_elec * \
                efficiency_factor * electrification_factor * region_factor
            gas_regional[region] = base_gas * efficiency_factor * \
                gas_transition_factor / region_factor

        # Household energy demand (MWh annual)
        household_electricity = {}
        household_gas = {}
        household_total_energy = {}  # NEW: Total household energy demand by region

        for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
            base_hh_elec = self.base_data['household_energy']['electricity_regional'][region]
            base_hh_gas = self.base_data['household_energy']['gas_regional'][region]

            # Household electrification (heat pumps, EVs)
            # 3.5% annual increase
            hh_electrification = (1 + 0.035) ** years_elapsed
            # 2.5% annual decrease
            hh_gas_reduction = (1 - 0.025) ** years_elapsed

            household_electricity[region] = base_hh_elec * \
                hh_electrification * efficiency_factor
            household_gas[region] = base_hh_gas * \
                hh_gas_reduction * efficiency_factor

            # Calculate total household energy demand per region (electricity + gas)
            household_total_energy[region] = household_electricity[region] + \
                household_gas[region]

        energy_demand = {
            'electricity_total': electricity_total,
            'gas_total': gas_total,
            'other_energy_total': other_energy_total,
            'electricity_regional': electricity_regional,
            'gas_regional': gas_regional,
            'household_electricity': household_electricity,
            'household_gas': household_gas,
            'household_total_energy': household_total_energy,  # NEW
            'electricity_sectoral': electricity_sectoral,
            'gas_sectoral': gas_sectoral,
            'other_energy_sectoral': other_energy_sectoral,
            'total_energy_sectoral': total_energy_sectoral  # NEW
        }

        return energy_demand

    def calculate_co2_emissions(self, year, scenario, energy_demand):
        """
        Calculate CO2 emissions evolution
        """
        years_elapsed = year - self.base_year

        # Base CO2 intensity (kg CO2/MWh for annual consumption)
        base_co2_intensity = {
            'electricity': 350.0,  # kg CO2/MWh (0.312 kg CO2/kWh * 1000)
            'gas': 2030.0,         # kg CO2/MWh equivalent natural gas
            'other_energy': 150.0,  # kg CO2/MWh (renewables + biomass mix)
        }

        # CO2 intensity reduction due to renewable energy expansion
        electricity_intensity = base_co2_intensity['electricity'] * (
            1 - self.assumptions['carbon_intensity_reduction']['electricity']) ** years_elapsed
        # Some biogas/hydrogen blending
        gas_intensity = base_co2_intensity['gas'] * \
            (1 - 0.015) ** years_elapsed
        # Other energy getting cleaner (more renewables)
        other_energy_intensity = base_co2_intensity['other_energy'] * \
            (1 - 0.045) ** years_elapsed

        # Calculate emissions from electricity (Mt CO2)
        electricity_emissions = energy_demand['electricity_total'] * \
            electricity_intensity / \
            1000000  # Convert kg to Mt (MWh * kg/MWh / 1000000)

        # Calculate emissions from gas (Mt CO2)
        gas_emissions = energy_demand['gas_total'] * \
            gas_intensity / \
            1000000  # Convert kg to Mt (MWh * kg/MWh / 1000000)

        # Calculate emissions from other energy (Mt CO2)
        other_energy_emissions = energy_demand['other_energy_total'] * \
            other_energy_intensity / 1000000  # Convert kg to Mt

        # Other emissions (industry processes, agriculture, etc.) - declining due to efficiency and policies
        other_emissions = 200.0 * \
            (1 - 0.020) ** years_elapsed  # 2% annual reduction

        # Apply scenario-specific CO2 reduction
        if scenario == 'ETS1' and year >= 2021:
            # Industrial carbon pricing accelerates reductions
            electricity_emissions *= (1 - 0.015) ** years_elapsed
            other_emissions *= (1 - 0.025) ** years_elapsed

        elif scenario == 'ETS2' and year >= 2027:
            # Buildings & transport carbon pricing
            electricity_emissions *= (1 - 0.010) ** (year - 2027)
            gas_emissions *= (1 - 0.020) ** (year - 2027)
            other_emissions *= (1 - 0.030) ** (year - 2027)

        total_emissions = electricity_emissions + gas_emissions + \
            other_energy_emissions + other_emissions

        return {
            'total': total_emissions,
            'electricity': electricity_emissions,
            'gas': gas_emissions,
            'other_energy': other_energy_emissions,
            'other': other_emissions
        }

    def calculate_energy_prices(self, year, scenario):
        """
        Calculate energy price evolution
        """
        years_elapsed = year - self.base_year

        # Base price trends (real prices, inflation-adjusted)
        # 1.5% annual increase (renewable costs decline, but grid costs rise)
        electricity_trend = 0.015
        # 2.5% annual increase (increasing scarcity, carbon pricing)
        gas_trend = 0.025

        base_elec_price = self.base_data['energy_prices']['electricity']
        base_gas_price = self.base_data['energy_prices']['gas']

        # Apply scenario-specific price effects
        if scenario == 'ETS1' and year >= 2021:
            # Industrial carbon pricing affects electricity prices
            # EUR/tCO2, growing 4% annually from 2021 actual EU ETS price
            carbon_price = 53.90 * (1.04 ** years_elapsed)
            # EUR/MWh (0.35 kg CO2/kWh * 1000)
            electricity_premium = carbon_price * 0.35
            gas_premium = carbon_price * 2.03  # EUR/MWh equivalent

        elif scenario == 'ETS2' and year >= 2027:
            # Buildings & transport carbon pricing (starts 2027)
            if year >= 2027:
                ets1_carbon_price = 134 * (1.04 ** (year - 2027))
                ets2_carbon_price = 45 * (1.025 ** (year - 2027))
                electricity_premium = ets1_carbon_price * 0.312 / 1000
                gas_premium = ets2_carbon_price * 2.03 / 1000
            else:
                electricity_premium = 0
                gas_premium = 0
        else:
            electricity_premium = 0
            gas_premium = 0

        electricity_price = base_elec_price * \
            (1 + electricity_trend) ** years_elapsed + electricity_premium
        gas_price = base_gas_price * \
            (1 + gas_trend) ** years_elapsed + gas_premium

        return {
            'electricity': electricity_price,
            'gas': gas_price
        }

    def run_scenario(self, scenario):
        """
        Run complete simulation for one scenario
        """
        print(f"\nRunning {scenario} scenario...")

        results = []

        # Determine years for scenario
        if scenario == 'ETS2':
            scenario_years = [year for year in self.years if year >= 2027]
        else:
            scenario_years = self.years

        for year in scenario_years:
            print(f"  {year}...", end=' ')

            try:
                # Calculate economic indicators
                gdp_data = self.calculate_dynamic_economics(year, scenario)

                # Calculate sectoral output
                sectoral_output = self.calculate_sectoral_output(
                    year, scenario, gdp_data)

                # Calculate energy demand
                energy_demand = self.calculate_energy_demand(
                    year, scenario, sectoral_output)

                # Calculate CO2 emissions
                co2_emissions = self.calculate_co2_emissions(
                    year, scenario, energy_demand)

                # Apply ETS policy constraints
                constrained_energy, constrained_co2 = self.apply_ets_constraints(
                    year, scenario, energy_demand, co2_emissions)

                # Calculate energy prices
                energy_prices = self.calculate_energy_prices(year, scenario)

                # Store results
                year_result = {
                    'year': year,
                    'scenario': scenario,
                    'gdp_total': gdp_data['gdp_total'],
                    'gdp_regional': gdp_data['gdp_regional'],
                    'sectoral_output': sectoral_output,
                    'energy_demand': constrained_energy,
                    'co2_emissions': constrained_co2,
                    'energy_prices': energy_prices
                }

                results.append(year_result)
                print("OK")

            except Exception as e:
                print(f"Error: {str(e)}")

        print(f"  {scenario} completed: {len(results)}/{len(scenario_years)} years")
        return results

    def run_all_scenarios(self):
        """
        Run all three scenarios
        """
        print("\nRUNNING DYNAMIC SIMULATION")
        print("="*50)

        all_results = {}

        # Run BAU scenario (2021-2050)
        all_results['BAU'] = self.run_scenario('BAU')

        # Run ETS1 scenario (2021-2050)
        all_results['ETS1'] = self.run_scenario('ETS1')

        # Run ETS2 scenario (2027-2050)
        all_results['ETS2'] = self.run_scenario('ETS2')

        return all_results

    def export_results(self, results):
        """
        Export results to comprehensive Excel file
        """
        print("\nEXPORTING RESULTS TO EXCEL")
        print("="*40)

        # Create results directory
        results_dir = "results/dynamic_simulation_2021_2050"
        os.makedirs(results_dir, exist_ok=True)

        # Generate timestamped filename to avoid conflicts
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file = f"{results_dir}/Italian_CGE_Dynamic_Results_2021_2050_{timestamp}.xlsx"

        with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:

            # 1. GDP Results (Billions EUR)
            print("  GDP data...")
            gdp_data = []
            for scenario, scenario_results in results.items():
                for result in scenario_results:
                    row = {'Year': result['year'], 'Scenario': scenario}
                    row['GDP_Total'] = result['gdp_total']
                    for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                        row[f'GDP_{region}'] = result['gdp_regional'][region]
                    gdp_data.append(row)

            gdp_df = pd.DataFrame(gdp_data)
            gdp_total_pivot = gdp_df.pivot(
                index='Year', columns='Scenario', values='GDP_Total')
            gdp_total_pivot.to_excel(
                writer, sheet_name='GDP_Total_Billions_EUR')

            for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                gdp_regional_pivot = gdp_df.pivot(
                    index='Year', columns='Scenario', values=f'GDP_{region}')
                gdp_regional_pivot.to_excel(
                    writer, sheet_name=f'GDP_{region}_Billions_EUR')

            # 2. Sectoral Output (Billions EUR)
            print("  Sectoral output...")
            sectors = ['AGR', 'IND', 'SERVICES', 'ELEC', 'GAS',
                       'OENERGY', 'ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']
            for sector in sectors:
                sector_data = []
                for scenario, scenario_results in results.items():
                    for result in scenario_results:
                        sector_data.append({
                            'Year': result['year'],
                            'Scenario': scenario,
                            'Output': result['sectoral_output'][sector]
                        })

                sector_df = pd.DataFrame(sector_data)
                sector_pivot = sector_df.pivot(
                    index='Year', columns='Scenario', values='Output')
                sector_pivot.to_excel(
                    writer, sheet_name=f'Output_{sector}_Billions_EUR')

            # 3. Energy Demand - Electricity (MWh annual)
            print("  Electricity demand...")
            elec_total_data = []
            for scenario, scenario_results in results.items():
                for result in scenario_results:
                    elec_total_data.append({
                        'Year': result['year'],
                        'Scenario': scenario,
                        'Total': result['energy_demand']['electricity_total']
                    })

            elec_total_df = pd.DataFrame(elec_total_data)
            elec_total_pivot = elec_total_df.pivot(
                index='Year', columns='Scenario', values='Total')
            elec_total_pivot.to_excel(
                writer, sheet_name='Electricity_Total_MWh')

            # Sectoral electricity demand
            print("  Sectoral electricity demand...")
            for sector in sectors:
                elec_sector_data = []
                for scenario, scenario_results in results.items():
                    for result in scenario_results:
                        elec_sector_data.append({
                            'Year': result['year'],
                            'Scenario': scenario,
                            'Demand': result['energy_demand']['electricity_sectoral'][sector]
                        })

                elec_sector_df = pd.DataFrame(elec_sector_data)
                elec_sector_pivot = elec_sector_df.pivot(
                    index='Year', columns='Scenario', values='Demand')
                elec_sector_pivot.to_excel(
                    writer, sheet_name=f'Electricity_MWh_{sector}')

            # Regional electricity demand
            for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                elec_regional_data = []
                for scenario, scenario_results in results.items():
                    for result in scenario_results:
                        elec_regional_data.append({
                            'Year': result['year'],
                            'Scenario': scenario,
                            'Industrial': result['energy_demand']['electricity_regional'][region],
                            'Household': result['energy_demand']['household_electricity'][region]
                        })

                elec_regional_df = pd.DataFrame(elec_regional_data)
                elec_ind_pivot = elec_regional_df.pivot(
                    index='Year', columns='Scenario', values='Industrial')
                elec_ind_pivot.to_excel(
                    writer, sheet_name=f'Electricity_MWh_Industry_{region}')
                elec_hh_pivot = elec_regional_df.pivot(
                    index='Year', columns='Scenario', values='Household')
                elec_hh_pivot.to_excel(
                    writer, sheet_name=f'Electricity_MWh_Household_{region}')

            # 4. Energy Demand - Gas (MWh annual)
            print("  Gas demand...")
            gas_total_data = []
            for scenario, scenario_results in results.items():
                for result in scenario_results:
                    gas_total_data.append({
                        'Year': result['year'],
                        'Scenario': scenario,
                        'Total': result['energy_demand']['gas_total']
                    })

            gas_total_df = pd.DataFrame(gas_total_data)
            gas_total_pivot = gas_total_df.pivot(
                index='Year', columns='Scenario', values='Total')
            gas_total_pivot.to_excel(writer, sheet_name='Gas_Total_MWh')

            # Sectoral gas demand
            print("  Sectoral gas demand...")
            for sector in sectors:
                gas_sector_data = []
                for scenario, scenario_results in results.items():
                    for result in scenario_results:
                        gas_sector_data.append({
                            'Year': result['year'],
                            'Scenario': scenario,
                            'Demand': result['energy_demand']['gas_sectoral'][sector]
                        })

                gas_sector_df = pd.DataFrame(gas_sector_data)
                gas_sector_pivot = gas_sector_df.pivot(
                    index='Year', columns='Scenario', values='Demand')
                gas_sector_pivot.to_excel(
                    writer, sheet_name=f'Gas_MWh_{sector}')

            # Regional gas demand
            for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                gas_regional_data = []
                for scenario, scenario_results in results.items():
                    for result in scenario_results:
                        gas_regional_data.append({
                            'Year': result['year'],
                            'Scenario': scenario,
                            'Industrial': result['energy_demand']['gas_regional'][region],
                            'Household': result['energy_demand']['household_gas'][region]
                        })

                gas_regional_df = pd.DataFrame(gas_regional_data)
                gas_ind_pivot = gas_regional_df.pivot(
                    index='Year', columns='Scenario', values='Industrial')
                gas_ind_pivot.to_excel(
                    writer, sheet_name=f'Gas_MWh_Industry_{region}')
                gas_hh_pivot = gas_regional_df.pivot(
                    index='Year', columns='Scenario', values='Household')
                gas_hh_pivot.to_excel(
                    writer, sheet_name=f'Gas_MWh_Household_{region}')

            # 5. Energy Demand - Other Energy (MWh annual)
            print("  Other energy demand...")
            other_energy_total_data = []
            for scenario, scenario_results in results.items():
                for result in scenario_results:
                    other_energy_total_data.append({
                        'Year': result['year'],
                        'Scenario': scenario,
                        'Total': result['energy_demand']['other_energy_total']
                    })

            other_energy_total_df = pd.DataFrame(other_energy_total_data)
            other_energy_total_pivot = other_energy_total_df.pivot(
                index='Year', columns='Scenario', values='Total')
            other_energy_total_pivot.to_excel(
                writer, sheet_name='Other_Energy_Total_MWh')

            # Sectoral other energy demand
            print("  Sectoral other energy demand...")
            for sector in sectors:
                other_energy_sector_data = []
                for scenario, scenario_results in results.items():
                    for result in scenario_results:
                        other_energy_sector_data.append({
                            'Year': result['year'],
                            'Scenario': scenario,
                            'Demand': result['energy_demand']['other_energy_sectoral'][sector]
                        })

                other_energy_sector_df = pd.DataFrame(other_energy_sector_data)
                other_energy_sector_pivot = other_energy_sector_df.pivot(
                    index='Year', columns='Scenario', values='Demand')
                other_energy_sector_pivot.to_excel(
                    writer, sheet_name=f'Other_Energy_MWh_{sector}')

            # 6. Total Energy Demand - by Sector (MWh annual)
            print("  Total energy demand by sector...")
            for sector in sectors:
                total_energy_sector_data = []
                for scenario, scenario_results in results.items():
                    for result in scenario_results:
                        total_energy_sector_data.append({
                            'Year': result['year'],
                            'Scenario': scenario,
                            'Total_Energy': result['energy_demand']['total_energy_sectoral'][sector]
                        })

                total_energy_sector_df = pd.DataFrame(total_energy_sector_data)
                total_energy_sector_pivot = total_energy_sector_df.pivot(
                    index='Year', columns='Scenario', values='Total_Energy')
                total_energy_sector_pivot.to_excel(
                    writer, sheet_name=f'Total_Energy_MWh_{sector}')

            # 7. Total Energy Demand - Household Regions (MWh annual)
            print("  Total energy demand by household region...")
            for region in ['NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS']:
                household_total_energy_data = []
                for scenario, scenario_results in results.items():
                    for result in scenario_results:
                        household_total_energy_data.append({
                            'Year': result['year'],
                            'Scenario': scenario,
                            'Total_Energy': result['energy_demand']['household_total_energy'][region]
                        })

                household_total_energy_df = pd.DataFrame(
                    household_total_energy_data)
                household_total_energy_pivot = household_total_energy_df.pivot(
                    index='Year', columns='Scenario', values='Total_Energy')
                household_total_energy_pivot.to_excel(
                    writer, sheet_name=f'Total_Energy_MWh_Household_{region}')

            # 8. CO2 Emissions (Mt)
            print("  CO2 emissions...")
            co2_data = []
            for scenario, scenario_results in results.items():
                for result in scenario_results:
                    co2_data.append({
                        'Year': result['year'],
                        'Scenario': scenario,
                        'Total': result['co2_emissions']['total'],
                        'Electricity': result['co2_emissions']['electricity'],
                        'Gas': result['co2_emissions']['gas'],
                        'Other_Energy': result['co2_emissions']['other_energy'],
                        'Other': result['co2_emissions']['other']
                    })

            co2_df = pd.DataFrame(co2_data)
            co2_total_pivot = co2_df.pivot(
                index='Year', columns='Scenario', values='Total')
            co2_total_pivot.to_excel(writer, sheet_name='CO2_Total_Mt')
            co2_elec_pivot = co2_df.pivot(
                index='Year', columns='Scenario', values='Electricity')
            co2_elec_pivot.to_excel(writer, sheet_name='CO2_Electricity_Mt')
            co2_gas_pivot = co2_df.pivot(
                index='Year', columns='Scenario', values='Gas')
            co2_gas_pivot.to_excel(writer, sheet_name='CO2_Gas_Mt')
            co2_other_energy_pivot = co2_df.pivot(
                index='Year', columns='Scenario', values='Other_Energy')
            co2_other_energy_pivot.to_excel(
                writer, sheet_name='CO2_Other_Energy_Mt')
            co2_other_pivot = co2_df.pivot(
                index='Year', columns='Scenario', values='Other')
            co2_other_pivot.to_excel(writer, sheet_name='CO2_Other_Mt')

            # 9. Energy Prices (EUR/MWh)
            print("  Energy prices...")
            price_data = []
            for scenario, scenario_results in results.items():
                for result in scenario_results:
                    price_data.append({
                        'Year': result['year'],
                        'Scenario': scenario,
                        'Electricity': result['energy_prices']['electricity'],
                        'Gas': result['energy_prices']['gas']
                    })

            price_df = pd.DataFrame(price_data)
            elec_price_pivot = price_df.pivot(
                index='Year', columns='Scenario', values='Electricity')
            elec_price_pivot.to_excel(
                writer, sheet_name='Electricity_Prices_EUR_MWh')
            gas_price_pivot = price_df.pivot(
                index='Year', columns='Scenario', values='Gas')
            gas_price_pivot.to_excel(writer, sheet_name='Gas_Prices_EUR_MWh')

        print(f"Results exported to: {excel_file}")
        return excel_file


def main():
    """
    Main execution function
    """
    start_time = time.time()

    print("ITALIAN CGE MODEL - DYNAMIC SIMULATION 2021-2050")
    print("="*60)
    print("Complete recursive dynamic simulation")
    print("Scenarios:")
    print("   • BAU: Business As Usual (2021-2050)")
    print("   • ETS1: Industrial Carbon Pricing (2021-2050)")
    print("   • ETS2: Buildings & Transport Carbon Pricing (2027-2050)")
    print("\nResults Generated:")
    print("   • GDP by region (billions EUR)")
    print("   • Sectoral output (billions EUR)")
    print("   • Energy demand by carrier and region (MW)")
    print("   • Household energy demand by region (MW)")
    print("   • CO2 emissions by source (Mt CO2)")
    print("   • Energy prices (EUR/MWh)")

    # Initialize and run simulation
    simulation = ItalianDynamicSimulation()
    results = simulation.run_all_scenarios()

    # Export results
    excel_file = simulation.export_results(results)

    end_time = time.time()

    # Summary statistics
    total_years = sum(len(scenario_results)
                      for scenario_results in results.values())

    print(f"\nDYNAMIC SIMULATION COMPLETED!")
    print(f"Execution time: {end_time - start_time:.1f} seconds")
    print(f"Total years simulated: {total_years}")
    print(f"Results file: {excel_file}")

    # Quick preview of key results
    print(f"\nKEY RESULTS PREVIEW:")
    print(f"GDP Evolution (BAU scenario):")
    if 'BAU' in results and results['BAU']:
        gdp_2021 = results['BAU'][0]['gdp_total']
        gdp_2050 = results['BAU'][-1]['gdp_total']
        growth_rate = ((gdp_2050 / gdp_2021) ** (1/29) - 1) * 100
        print(f"   2021: €{gdp_2021:.0f} billion")
        print(f"   2050: €{gdp_2050:.0f} billion")
        print(f"   Average annual growth: {growth_rate:.1f}%")

    print(f"\nEnergy Demand Evolution (BAU scenario):")
    if 'BAU' in results and results['BAU']:
        elec_2021 = results['BAU'][0]['energy_demand']['electricity_total']
        elec_2050 = results['BAU'][-1]['energy_demand']['electricity_total']
        gas_2021 = results['BAU'][0]['energy_demand']['gas_total']
        gas_2050 = results['BAU'][-1]['energy_demand']['gas_total']
        print(
            f"   Electricity: {elec_2021:.0f} MW (2021) → {elec_2050:.0f} MW (2050)")
        print(f"   Gas: {gas_2021:.0f} MW (2021) → {gas_2050:.0f} MW (2050)")

    print(f"\nCO2 Emissions Evolution:")
    if 'BAU' in results and results['BAU']:
        co2_2021_bau = results['BAU'][0]['co2_emissions']['total']
        co2_2050_bau = results['BAU'][-1]['co2_emissions']['total']
        print(
            f"   BAU: {co2_2021_bau:.0f} Mt (2021) → {co2_2050_bau:.0f} Mt (2050)")

    if 'ETS1' in results and results['ETS1']:
        co2_2050_ets1 = results['ETS1'][-1]['co2_emissions']['total']
        reduction_ets1 = ((co2_2050_bau - co2_2050_ets1) / co2_2050_bau) * 100
        print(
            f"   ETS1: {co2_2050_ets1:.0f} Mt (2050) - {reduction_ets1:.1f}% reduction vs BAU")

    if 'ETS2' in results and results['ETS2']:
        co2_2050_ets2 = results['ETS2'][-1]['co2_emissions']['total']
        reduction_ets2 = ((co2_2050_bau - co2_2050_ets2) / co2_2050_bau) * 100
        print(
            f"   ETS2: {co2_2050_ets2:.0f} Mt (2050) - {reduction_ets2:.1f}% reduction vs BAU")

    print("\nSIMULATION COMPLETE - Ready for policy analysis!")


if __name__ == "__main__":
    main()
