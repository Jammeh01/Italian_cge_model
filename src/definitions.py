"""
Definitions and Sets for Italian CGE Model
Based on actual SAM data with Italian regional disaggregation
Dynamic recursive model structure following ThreeME approach
Author: Italian CGE Model (2021-2040)

EU ETS Implementation:
- ETS1 (EU ETS Phase 4): €53.90/tCO2e starting 2021, Market Stability Reserve (no formal ceiling)
- ETS2 (Buildings/Transport): €45.0/tCO2e starting 2027, Price Stability Mechanism (€22-€45/tCO2e range)
"""

import pandas as pd
import numpy as np
import os


class ModelDefinitions:
    """
    Define all sets, parameters, and initial data structures for the Italian CGE model
    Based on actual SAM.xlsx data structure
    """

    def __init__(self):
        # Model time structure
        self.base_year = 2021
        self.final_year = 2040
        self.time_periods = list(range(2021, 2041))  # Annual time steps

        # Base year calibration targets (Updated to correct 2021 values)
        # €1,782 billion (current prices) - 2021 actual GDP
        self.base_year_gdp = 1782.0
        self.base_year_population = 59.13  # 59.13 million people - 2021 actual population

        # Italy 2021 CO2 emissions from fuel combustion (ISPRA, GSE, Eurostat)
        # Total CO2 from fuel combustion: ~466 MtCO2
        # Breakdown:
        #   - Electricity grid: 96.7 MtCO2 (310 TWh × 312 kg/MWh)
        #   - Natural gas end-use: 145.4 MtCO2 (720 TWh × 202 kg/MWh)
        #   - Other energy (oil + coal - renewables): 224.0 MtCO2
        # NOTE: This excludes process emissions, agriculture, land use
        # MtCO2 (updated with grid mix)
        self.italy_2021_co2_fuel_combustion = 466.1
        # tCO2/Million EUR (fuel combustion only)
        self.italy_2021_co2_intensity_fuel_combustion = 0.261  # 466.1 / 1782.0

        # Renewable energy characteristics
        # 100% renewable electricity in model
        self.renewable_electricity_share_2021 = 1.0
        self.renewable_technologies = [
            'solar_pv', 'wind_onshore', 'wind_offshore', 'hydro', 'geothermal', 'biomass']

        # Define Italian macro-regions for household disaggregation (actual SAM structure)
        self.italian_regions = {
            'NW': {'name': 'Northwest', 'sam_name': 'Households(NW)', 'description': 'Lombardy, Piedmont, Valle d\'Aosta, Liguria'},
            'NE': {'name': 'Northeast', 'sam_name': 'Households(NE)', 'description': 'Veneto, Trentino-Alto Adige, Friuli-Venezia Giulia, Emilia-Romagna'},
            'CENTER': {'name': 'Center', 'sam_name': 'Households(Centre)', 'description': 'Tuscany, Umbria, Marche, Lazio'},
            'SOUTH': {'name': 'South', 'sam_name': 'Households(South)', 'description': 'Abruzzo, Molise, Campania, Puglia, Basilicata, Calabria'},
            'ISLANDS': {'name': 'Islands', 'sam_name': 'Households(Islands)', 'description': 'Sicily, Sardinia'}
        }

        # Regional population shares (2021 data)
        self.regional_population_shares = {
            'NW': 0.269,    # 26.9% - 15.9 million
            'NE': 0.191,    # 19.1% - 11.3 million
            'CENTER': 0.199,  # 19.9% - 11.8 million
            'SOUTH': 0.233,  # 23.3% - 13.8 million
            'ISLANDS': 0.108  # 10.8% - 6.4 million
        }

        # Load actual SAM structure
        self.load_sam_structure()

        # Define energy sectors (disaggregated in SAM)
        # CO2 factors for fuel combustion - Italy 2021 data (ISPRA, GSE, Eurostat)
        # NOTE: Electricity represents TOTAL GRID MIX (renewable + fossil)
        # Option B: Grid Mix Approach for CGE realism and decarbonization modeling
        self.energy_sectors_detail = {
            'ELECTRICITY': {
                'sam_name': 'Electricity',
                'description': 'Total grid electricity (renewable + fossil mix, 35% renewable in 2021)',
                # kg CO2/MWh from grid electricity (weighted average 2021)
                # Formula: base_factor × (1 - renewable_share)
                # 2021: 312 kg/MWh with 35% renewable
                # As renewable share grows, this factor decreases dynamically
                'co2_factor_fuel_combustion': 312.0,
                # Total emissions from electricity grid: 96.7 MtCO2 (310 TWh × 312 kg/MWh)
                'italy_2021_fuel_combustion_mtco2': 96.7,
                'renewable_share_2021': 0.35,  # 35% renewable, increases over time
                'renewable_target_2030': 0.55,  # EU target 55% by 2030
                'renewable_target_2040': 0.80,  # Projected 80% by 2040
                'energy_sources': ['renewable_electricity', 'gas_power', 'coal_power', 'oil_power'],
                'decarbonization_pathway': 'dynamic',  # CO2 factor decreases as renewables grow
                'consumption_2021_twh': 310.0  # Calibration target
            },
            'GAS': {
                'sam_name': 'Gas',
                'description': 'Natural gas for heating, industry, commercial (excludes power generation)',
                # kg CO2/MWh from natural gas combustion
                'co2_factor_fuel_combustion': 202.0,
                # Total emissions from gas end-use: 145.4 MtCO2 (720 TWh × 202 kg/MWh)
                # NOTE: Gas power generation emissions are in ELECTRICITY sector above
                'italy_2021_fuel_combustion_mtco2': 145.4,
                'end_uses': ['heating', 'industrial_process', 'commercial'],
                # Calibration target (non-power only)
                'consumption_2021_twh': 720.0
            },
            'OTHER_ENERGY': {
                'sam_name': 'Other Energy',
                'description': 'Oil products, coal, and direct renewable energy (biomass, solar thermal)',
                # kg CO2/MWh from fossil fuel combustion (weighted average)
                # Oil: 350 kg/MWh, Coal: 400 kg/MWh, Renewables: 0 kg/MWh
                'co2_factor_fuel_combustion': 350.0,
                # Total emissions: 224.0 MtCO2 (580 TWh oil + 60 TWh coal, excluding 150 TWh renewables)
                'italy_2021_fuel_combustion_mtco2': 224.0,
                'fossil_sources': ['oil_products', 'petroleum', 'coal', 'direct_renewables'],
                'oil_products_twh': 580.0,
                'coal_twh': 60.0,
                'direct_renewables_twh': 150.0,  # Biomass, solar thermal, etc.
                'consumption_2021_twh': 790.0  # Calibration target
            }
        }

        # Define transport sectors (disaggregated in SAM)
        # CO2 factors and emissions from fuel combustion only - Italy 2021 data (ISPRA)
        self.transport_sectors_detail = {
            'ROAD': {
                'sam_name': 'Road Transport',
                'description': 'Road freight and passenger transport fuel combustion',
                'co2_factor_fuel_combustion': 231.0,  # kg CO2/MWh from fuel combustion
                # MtCO2 from road transport fuel combustion
                'italy_2021_fuel_combustion_mtco2': 89.1
            },
            'RAIL': {
                'sam_name': 'Rail Transport',
                'description': 'Railway transport fuel combustion',
                'co2_factor_fuel_combustion': 85.0,   # kg CO2/MWh from fuel combustion
                # MtCO2 from rail transport fuel combustion
                'italy_2021_fuel_combustion_mtco2': 1.8
            },
            'AIR': {
                'sam_name': 'Air Transport',
                'description': 'Aviation fuel combustion',
                'co2_factor_fuel_combustion': 315.0,  # kg CO2/MWh from aviation fuel combustion
                'italy_2021_fuel_combustion_mtco2': 12.4  # MtCO2 from aviation fuel combustion
            },
            'WATER': {
                'sam_name': 'Water Transport',
                'description': 'Maritime fuel combustion',
                'co2_factor_fuel_combustion': 317.0,  # kg CO2/MWh from marine fuel combustion
                'italy_2021_fuel_combustion_mtco2': 8.7   # MtCO2 from maritime fuel combustion
            },
            'OTHER_TRANSPORT': {
                'sam_name': 'Other Transport',
                'description': 'Other transport fuel combustion',
                # kg CO2/MWh from fuel combustion (average)
                'co2_factor_fuel_combustion': 250.0,
                # MtCO2 from other transport fuel combustion
                'italy_2021_fuel_combustion_mtco2': 3.2
            }
        }

        # Initialize model structure
        self.initialize_model_structure()

        # ETS policy definitions
        self.define_ets_policies()

    def load_sam_structure(self):
        """Load actual SAM structure from SAM.xlsx"""

        try:
            # Try to load the actual SAM data
            sam_file_path = os.path.join('data', 'SAM.xlsx')
            if not os.path.exists(sam_file_path):
                sam_file_path = 'SAM.xlsx'

            if os.path.exists(sam_file_path):
                self.sam_data = pd.read_excel(sam_file_path, index_col=0)
                print(
                    f"Successfully loaded actual SAM with {self.sam_data.shape[0]} accounts")
                self.extract_sam_structure_from_data()
            else:
                print("SAM.xlsx not found, using known structure from code")
                self.use_known_sam_structure()

        except Exception as e:
            print(f"Error loading SAM: {e}. Using known structure.")
            self.use_known_sam_structure()

    def extract_sam_structure_from_data(self):
        """Extract structure from loaded SAM data"""

        all_accounts = list(self.sam_data.columns)

        # Production sectors (from actual SAM)
        self.production_sectors_sam = [
            'Agriculture', 'Industry', 'Electricity', 'Gas', 'Other Energy',
            'Road Transport', 'Rail Transport', 'Air Transport', 'Water Transport',
            'Other Transport', 'other Sectors (14)'
        ]

        # Verify sectors exist in SAM
        self.production_sectors_sam = [
            s for s in self.production_sectors_sam if s in all_accounts]

        # Household regions from SAM
        self.household_regions_sam = [
            'Households(NW)', 'Households(NE)', 'Households(Centre)',
            'Households(South)', 'Households(Islands)'
        ]

        # Factors from SAM
        self.factors_sam = ['Labour', 'Capital']

        # Institutions from SAM
        self.institutions_sam = ['Government',
                                 'Firms', 'Capital Account', 'Rest of World']

        # Additional SAM accounts
        self.other_sam_accounts = [acc for acc in all_accounts
                                   if acc not in (self.production_sectors_sam +
                                                  self.household_regions_sam +
                                                  self.factors_sam +
                                                  self.institutions_sam)]

        print(
            f"Extracted {len(self.production_sectors_sam)} production sectors")
        print(f"Extracted {len(self.household_regions_sam)} household regions")
        print(f"Other SAM accounts: {self.other_sam_accounts}")

    def use_known_sam_structure(self):
        """Use known SAM structure from the code"""

        self.production_sectors_sam = [
            'Agriculture', 'Industry', 'Electricity', 'Gas', 'Other Energy',
            'Road Transport', 'Rail Transport', 'Air Transport', 'Water Transport',
            'Other Transport', 'other Sectors (14)'
        ]

        self.household_regions_sam = [
            'Households(NW)', 'Households(NE)', 'Households(Centre)',
            'Households(South)', 'Households(Islands)'
        ]

        self.factors_sam = ['Labour', 'Capital']
        self.institutions_sam = ['Government',
                                 'Firms', 'Capital Account', 'Rest of World']
        self.other_sam_accounts = ['Taxes on products and imports']

    def initialize_model_structure(self):
        """Initialize all model sets and mappings"""

        # Create model sector codes
        self.sector_mapping = {
            'Agriculture': 'AGR',
            'Industry': 'IND',
            'Electricity': 'ELEC',
            'Gas': 'GAS',
            'Other Energy': 'OENERGY',
            'Road Transport': 'ROAD',
            'Rail Transport': 'RAIL',
            'Air Transport': 'AIR',
            'Water Transport': 'WATER',
            'Other Transport': 'OTRANS',
            'other Sectors (14)': 'SERVICES'
        }

        # Model sets
        self.sectors = list(self.sector_mapping.values())
        self.factors = ['LAB', 'CAP']
        self.households = list(self.italian_regions.keys())

        # Energy and transport classifications
        self.energy_sectors = ['ELEC', 'GAS', 'OENERGY']
        self.transport_sectors = ['ROAD', 'RAIL', 'AIR', 'WATER', 'OTRANS']

        # Non-energy sectors
        self.non_energy_sectors = [
            s for s in self.sectors if s not in self.energy_sectors]

        # Service sectors (for ETS2)
        self.service_sectors = ['SERVICES']

        print(f"Model structure initialized:")
        print(f"  Production sectors: {len(self.sectors)}")
        print(f"  Energy sectors: {self.energy_sectors}")
        print(f"  Transport sectors: {self.transport_sectors}")
        print(f"  Household regions: {self.households}")

    def define_ets_policies(self):
        """Define ETS policy parameters and coverage"""

        # ETS1 Policy (starts 2021) - EU ETS Phase 4
        self.ets1_policy = {
            'start_year': 2021,
            # €53.90/tCO2e in 2021 (actual EU ETS price)
            'base_carbon_price': 53.90,
            'price_growth_rate': 0.04,   # 4% annual growth
            # No formal price ceiling - relies on Market Stability Reserve (MSR)
            'price_cap': None,
            'has_msr': True,            # Market Stability Reserve mechanism
            # Based on your specification
            'covered_sectors': ['IND', 'GAS', 'OENERGY', 'AIR', 'WATER'],
            'free_allocation_rate': 0.8,  # 80% free allowances initially
            'free_allocation_decline': 0.02,  # 2% annual decline
        }

        # ETS2 Policy (starts 2027) - EU ETS for buildings and transport
        self.ets2_policy = {
            'start_year': 2027,
            # €45.0/tCO2e in 2027 (EU ETS2 starting price)
            'base_carbon_price': 45.0,
            'price_growth_rate': 0.025,  # 2.5% annual growth
            # Price Stability Mechanism (PSM) ceiling at €45/tCO2e
            'price_cap': 45.0,
            # Price Stability Mechanism (PSM) floor at €22/tCO2e
            'price_floor': 22.0,
            'has_psm': True,            # Price Stability Mechanism
            # Based on your specification
            'covered_sectors': ['ROAD', 'OTRANS', 'SERVICES'],
            'free_allocation_rate': 0.6,  # 60% free allowances initially
            'free_allocation_decline': 0.03,  # 3% annual decline
        }

        # Combined ETS coverage
        self.all_ets_sectors = list(set(self.ets1_policy['covered_sectors'] +
                                        self.ets2_policy['covered_sectors']))

        # Non-ETS sectors
        self.non_ets_sectors = [
            s for s in self.sectors if s not in self.all_ets_sectors]

    def get_carbon_price(self, year, policy='ETS1'):
        """Calculate carbon price for given year and policy with EU ETS specifications"""

        if policy == 'ETS1':
            if year < self.ets1_policy['start_year']:
                return 0.0

            years_elapsed = year - self.ets1_policy['start_year']
            base_price = self.ets1_policy['base_carbon_price']  # €53.90/tCO2e
            growth_rate = self.ets1_policy['price_growth_rate']

            price = base_price * (1 + growth_rate) ** years_elapsed

            # ETS1 has no formal price cap - Market Stability Reserve manages supply
            # In practice, we can set a high ceiling for modeling purposes
            if self.ets1_policy['has_msr']:
                # MSR mechanism - no hard cap but extreme prices unlikely
                return min(price, 300.0)  # Practical upper bound for modeling
            else:
                return price

        elif policy == 'ETS2':
            if year < self.ets2_policy['start_year']:
                return 0.0

            years_elapsed = year - self.ets2_policy['start_year']
            base_price = self.ets2_policy['base_carbon_price']  # €45.0/tCO2e
            growth_rate = self.ets2_policy['price_growth_rate']
            price_cap = self.ets2_policy['price_cap']  # €45.0/tCO2e ceiling
            price_floor = self.ets2_policy['price_floor']  # €22.0/tCO2e floor

            price = base_price * (1 + growth_rate) ** years_elapsed

            # ETS2 has Price Stability Mechanism (PSM) with ceiling and floor
            if self.ets2_policy['has_psm']:
                return max(price_floor, min(price, price_cap))
            else:
                return price

        return 0.0

    def get_ets_coverage(self, year):
        """Get ETS sector coverage for a given year"""

        covered_sectors = []

        # ETS1 sectors
        if year >= self.ets1_policy['start_year']:
            covered_sectors.extend(self.ets1_policy['covered_sectors'])

        # ETS2 sectors
        if year >= self.ets2_policy['start_year']:
            covered_sectors.extend(self.ets2_policy['covered_sectors'])

        return list(set(covered_sectors))

    def get_free_allocation_rate(self, year, policy='ETS1'):
        """Get free allocation rate for given year and policy"""

        if policy == 'ETS1':
            if year < self.ets1_policy['start_year']:
                return 1.0

            years_elapsed = year - self.ets1_policy['start_year']
            initial_rate = self.ets1_policy['free_allocation_rate']
            decline_rate = self.ets1_policy['free_allocation_decline']

            rate = initial_rate - decline_rate * years_elapsed
            return max(0.1, rate)  # Minimum 10%

        elif policy == 'ETS2':
            if year < self.ets2_policy['start_year']:
                return 1.0

            years_elapsed = year - self.ets2_policy['start_year']
            initial_rate = self.ets2_policy['free_allocation_rate']
            decline_rate = self.ets2_policy['free_allocation_decline']

            rate = initial_rate - decline_rate * years_elapsed
            return max(0.05, rate)  # Minimum 5%

        return 1.0

    def initialize_parameters(self):
        """Initialize default model parameters"""

        # Macroeconomic parameters
        self.macro_params = {
            # 0.1% annual population decline (Italy trend)
            'population_growth_rate': 0.001,
            'labor_force_growth_rate': -0.002,    # -0.2% annual labor force decline
            'productivity_growth_rate': 0.008,     # 0.8% annual productivity growth
            'depreciation_rate': 0.05,             # 5% capital depreciation
            'discount_rate': 0.03,                 # 3% social discount rate
        }

        # Energy parameters
        self.energy_params = {
            'autonomous_energy_efficiency': 0.01,  # 1% annual AEEI
            'electricity_renewable_share': 0.35,   # 35.0% renewables in 2021
            'renewable_growth_rate': 0.05,         # 5% annual renewable growth
        }

        # Trade parameters
        self.trade_params = {
            'armington_elasticity': 2.0,           # Substitution between imports and domestic
            # Transformation between exports and domestic sales
            'export_transformation_elasticity': 2.0,
        }

        # Elasticity parameters (based on literature)
        self.elasticities = {
            'production': {
                'factor_substitution': 0.7,        # Between labor and capital
                'energy_substitution': 1.2,        # Between energy types
                'material_substitution': 0.5,      # Between intermediate inputs
            },
            'consumption': {
                'income_elasticity': 0.8,          # Income elasticity of demand
                'price_elasticity': -0.5,          # Own-price elasticity
                'cross_price_elasticity': 0.2,     # Cross-price elasticity
            },
            'trade': {
                'import_substitution': 2.0,        # Armington elasticity
                'export_transformation': 2.0,      # CET elasticity
            }
        }

    def create_scenario_definitions(self):
        """Define the three policy scenarios with EU ETS specifications"""

        scenarios = {
            'BAU': {
                'name': 'Business as Usual',
                'description': 'No additional climate policies beyond existing',
                'carbon_price_ets1': False,
                'carbon_price_ets2': False,
                'additional_policies': False,
                'renewable_targets': False,
            },

            'ETS1': {
                'name': 'EU ETS Phase 4',
                'description': f'EU ETS Phase 4 for {", ".join(self.ets1_policy["covered_sectors"])} starting 2021 (€53.90/tCO2e base price)',
                'carbon_price_ets1': True,
                'carbon_price_ets2': False,
                'additional_policies': False,
                'renewable_targets': True,
                'covered_sectors': self.ets1_policy['covered_sectors'],
                'price_mechanism': 'Market Stability Reserve (MSR)'
            },

            'ETS2': {
                'name': 'EU ETS Phase 4 + Buildings/Transport',
                'description': f'Extended EU ETS coverage including buildings/transport {", ".join(self.ets2_policy["covered_sectors"])} from 2027 (€45.0/tCO2e base price)',
                'carbon_price_ets1': True,
                'carbon_price_ets2': True,
                'additional_policies': True,
                'renewable_targets': True,
                'covered_sectors': self.all_ets_sectors,
                'ets1_mechanism': 'Market Stability Reserve (MSR)',
                'ets2_mechanism': 'Price Stability Mechanism (PSM)'
            }
        }

        return scenarios

    def get_scenario_carbon_price(self, scenario_name, year):
        """Get carbon price for a specific scenario and year"""

        if scenario_name == 'BAU':
            return 0.0

        elif scenario_name == 'ETS1':
            return self.get_carbon_price(year, 'ETS1')

        elif scenario_name == 'ETS2':
            # Both ETS1 and ETS2 prices apply to different sectors
            ets1_price = self.get_carbon_price(year, 'ETS1')
            ets2_price = self.get_carbon_price(year, 'ETS2')

            # Return average weighted by sectoral coverage (simplified)
            if year >= self.ets2_policy['start_year']:
                return (ets1_price + ets2_price) / 2
            else:
                return ets1_price

        return 0.0

    def validate_model_structure(self):
        """Validate model structure consistency"""

        validation_results = []

        # Check sector coverage
        if len(self.sectors) != 11:
            validation_results.append(
                f"Expected 11 sectors, found {len(self.sectors)}")

        # Check regional coverage
        if len(self.households) != 5:
            validation_results.append(
                f"Expected 5 household regions, found {len(self.households)}")

        # Check population shares sum to 1
        pop_sum = sum(self.regional_population_shares.values())
        if abs(pop_sum - 1.0) > 0.001:
            validation_results.append(
                f"Population shares sum to {pop_sum}, should be 1.0")

        # Check ETS coverage
        total_ets_sectors = len(
            set(self.ets1_policy['covered_sectors'] + self.ets2_policy['covered_sectors']))
        if total_ets_sectors == 0:
            validation_results.append("No sectors covered by ETS policies")

        return validation_results


# Create global instance
model_definitions = ModelDefinitions()
model_definitions.initialize_parameters()

# Validate structure
validation_errors = model_definitions.validate_model_structure()
if validation_errors:
    print("Model structure validation warnings:")
    for error in validation_errors:
        print(f"  - {error}")
else:
    print("Model structure validation passed")

# Print summary
print(f"\nItalian CGE Model Definitions Summary:")
print(
    f"Time horizon: {model_definitions.base_year}-{model_definitions.final_year}")
print(f"Base year GDP target: €{model_definitions.base_year_gdp} billion")
print(
    f"Base year population: {model_definitions.base_year_population} million")
print(f"Production sectors: {len(model_definitions.sectors)}")
print(f"Energy sectors: {model_definitions.energy_sectors}")
print(f"Transport sectors: {model_definitions.transport_sectors}")
print(f"Household regions: {model_definitions.households}")
print(f"ETS1 coverage: {model_definitions.ets1_policy['covered_sectors']}")
print(f"ETS2 coverage: {model_definitions.ets2_policy['covered_sectors']}")
