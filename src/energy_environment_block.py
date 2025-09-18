"""
Energy-Environment Block for Italian CGE Model
IPOPT-optimized CO2 emissions and ETS implementation
Includes ETS1 and ETS2 policies with proper carbon pricing
"""

import pyomo.environ as pyo
import numpy as np
from definitions import model_definitions


class EnergyEnvironmentBlock:
    """
    Energy-environment block implementing:
    - CO2 emission calculations by sector and region
    - Energy balance constraints with efficiency improvements
    - ETS1 and ETS2 carbon pricing mechanisms (realistic implementation)
    - Energy demand by household region and energy carrier
    - Carbon revenue recycling
    """

    def __init__(self, model, calibrated_data):
        self.model = model
        self.calibrated_data = calibrated_data
        self.sectors = calibrated_data['production_sectors']
        self.energy_sectors = calibrated_data['energy_sectors']
        self.household_regions = list(calibrated_data['households'].keys())
        self.params = calibrated_data['calibrated_parameters']

        # Current year for dynamic policies (set externally)
        self.current_year = model_definitions.base_year
        self.current_scenario = 'BAU'

        self.add_energy_environment_variables()
        self.add_energy_environment_parameters()
        self.add_energy_environment_constraints()

    def add_energy_environment_variables(self):
        """Add energy and environment variables"""

        # Remove any existing energy variables to avoid conflicts
        existing_vars = ['aeei', 'Energy_demand',
                         'TOT_Energy', 'CO2_emissions']
        for var_name in existing_vars:
            if hasattr(self.model, var_name):
                self.model.del_component(var_name)

        # Energy demand by sector and energy type (MWh - annual consumption)
        def energy_demand_bounds(model, es, user):
            if user in self.sectors:
                sector_data = self.params['sectors'].get(user, {})
                # Convert from MW to MWh (annual): base_energy_MW * 8760 hours
                base_energy_mw = sector_data.get(
                    'gross_output', 1000) * sector_data.get('energy_intensity', 0.1)
                base_energy = base_energy_mw * 8760  # Convert MW to MWh annual
            else:  # Household
                hh_data = self.params['households'].get(user, {})
                # 5% of consumption on energy, converted to MWh annual
                base_energy_mw = hh_data.get('consumption', 40000) * 0.05
                base_energy = base_energy_mw * 8760  # Convert MW to MWh annual

            return (0.001, base_energy * 2.0)  # Small positive lower bound

        self.model.Energy_demand = pyo.Var(
            self.energy_sectors, self.sectors + self.household_regions,
            domain=pyo.NonNegativeReals,
            bounds=energy_demand_bounds,
            initialize=lambda m, es, user: energy_demand_bounds(m, es, user)[
                1] * 0.5,
            doc="Energy consumption by type and user (MWh annual)"
        )

        # Total energy consumption by type (MWh annual)
        self.model.TOT_Energy = pyo.Var(
            self.energy_sectors,
            domain=pyo.NonNegativeReals,
            # Minimum 8760 MWh (equivalent to 1 MW continuous)
            bounds=(8760.0, None),
            initialize=8760000.0,   # 8.76 million MWh
            doc="Total consumption of each energy type (MWh annual)"
        )

        # CO2 emissions by user
        def emission_bounds(model, user):
            if user in self.sectors:
                sector_data = self.params['sectors'].get(user, {})
                base_output = sector_data.get('gross_output', 1000)
                co2_factor = sector_data.get('co2_factor', 0.5)
                base_emissions = base_output * co2_factor * \
                    0.001  # Convert to appropriate units
            else:  # Household
                hh_data = self.params['households'].get(user, {})
                base_emissions = hh_data.get(
                    'consumption', 40000) * 0.002  # Rough estimate

            return (0.0, base_emissions * 5.0)

        self.model.EM = pyo.Var(
            self.sectors + self.household_regions,
            domain=pyo.NonNegativeReals,
            bounds=emission_bounds,
            initialize=lambda m, user: emission_bounds(m, user)[1] * 0.5,
            doc="CO2 emissions by user"
        )

        # Total CO2 emissions
        self.model.Total_Emissions = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(1.0, None),
            initialize=50000.0,
            doc="Total CO2 emissions"
        )

        # ETS-related variables

        # Carbon price by policy (€/tCO2)
        self.model.carbon_price_ets1 = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.0, 300.0),  # Max €300/tCO2
            initialize=0.0,
            doc="ETS1 carbon price (€/tCO2)"
        )

        self.model.carbon_price_ets2 = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.0, 250.0),  # Max €250/tCO2
            initialize=0.0,
            doc="ETS2 carbon price (€/tCO2)"
        )

        # Policy cost on sectors (carbon payments)
        def policy_cost_bounds(model, j):
            sector_data = self.params['sectors'].get(j, {})
            base_output = sector_data.get('gross_output', 1000)
            max_cost = base_output * 0.1  # Max 10% of output value
            return (0.0, max_cost)

        self.model.PLC = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=policy_cost_bounds,
            initialize=0.0,
            doc="Policy cost of carbon pricing on sectors"
        )

        # ETS revenue by policy
        self.model.ETS1_revenue = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.0, None),
            initialize=0.0,
            doc="Revenue from ETS1"
        )

        self.model.ETS2_revenue = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.0, None),
            initialize=0.0,
            doc="Revenue from ETS2"
        )

        # Energy efficiency improvement rates (AEEI by sector)
        self.model.aeei = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=(0.0, 0.05),  # 0-5% annual improvement
            initialize=0.01,
            doc="Autonomous energy efficiency improvement rates"
        )

        # Renewable energy share
        self.model.Renewable_share = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.0, 1.0),
            initialize=0.38,  # Italy's 2021 level
            doc="Share of renewables in electricity"
        )

    def add_energy_environment_parameters(self):
        """Add energy and environment parameters"""

        # Energy-monetary conversion coefficients
        def get_energy_coeff(model, es, user):
            energy_data = self.params.get('energy', {})
            energy_coeffs = energy_data.get('energy_coeffs', {})
            return energy_coeffs.get(es, 1.0)  # Default 1.0

        self.model.coe = pyo.Param(
            self.energy_sectors, self.sectors + self.household_regions,
            initialize=get_energy_coeff,
            mutable=True,
            doc="Energy coefficient (physical/monetary conversion)"
        )

        # CO2 emission factors by energy type (for MWh annual consumption)
        def get_co2_factor(model, es):
            # Based on actual Italian emission factors - converted for MWh units
            co2_factors = {
                'Electricity': 350.0,   # kg CO2/MWh (0.350 kg CO2/kWh * 1000)
                'Gas': 2034.0,          # kg CO2/MWh equivalent for natural gas
                'Other Energy': 2680.0  # kg CO2/MWh equivalent for oil products
            }
            return co2_factors.get(es, 1000.0)

        self.model.co2_fac = pyo.Param(
            self.energy_sectors,
            initialize=get_co2_factor,
            doc="CO2 emission factors by energy type"
        )

        # ETS sector coverage parameters
        def is_ets1_sector(model, j):
            # ETS1 coverage: Industry, Gas, Other Energy, Air Transport, Water Transport
            ets1_sectors = model_definitions.ets1_policy['covered_sectors']
            sector_code = model_definitions.sector_mapping.get(j, j)
            return 1.0 if sector_code in ets1_sectors else 0.0

        def is_ets2_sector(model, j):
            # ETS2 coverage: Road Transport, Other Transport, Services
            ets2_sectors = model_definitions.ets2_policy['covered_sectors']
            sector_code = model_definitions.sector_mapping.get(j, j)
            return 1.0 if sector_code in ets2_sectors else 0.0

        self.model.ets1_coverage = pyo.Param(
            self.sectors,
            initialize=is_ets1_sector,
            mutable=True,
            doc="ETS1 sector coverage (1=covered, 0=not covered)"
        )

        self.model.ets2_coverage = pyo.Param(
            self.sectors,
            initialize=is_ets2_sector,
            mutable=True,
            doc="ETS2 sector coverage (1=covered, 0=not covered)"
        )

        # Free allocation rates (time-varying)
        self.model.free_alloc_ets1 = pyo.Param(
            initialize=model_definitions.ets1_policy['free_allocation_rate'],
            mutable=True,
            doc="Free allocation rate for ETS1"
        )

        self.model.free_alloc_ets2 = pyo.Param(
            initialize=model_definitions.ets2_policy['free_allocation_rate'],
            mutable=True,
            doc="Free allocation rate for ETS2"
        )

    def add_energy_environment_constraints(self):
        """Add energy-environment constraints"""

        self.add_energy_demand_constraints()
        self.add_emission_constraints()
        self.add_ets_policy_constraints()
        self.add_energy_indicators()

    def add_energy_demand_constraints(self):
        """Energy demand constraints with efficiency improvements"""

        def energy_demand_sectors_rule(model, es, j):
            """Energy demand by sectors with AEEI"""
            # Sectors use energy for production (from intermediate demand or direct energy use)
            if es in self.sectors:  # Energy sector provides energy commodity
                base_demand = model.X[es, j]  # Intermediate energy input
            else:
                # Direct energy use based on output and energy intensity
                sector_data = self.params['sectors'].get(j, {})
                energy_intensity = sector_data.get('energy_intensity', 0.1)
                base_demand = model.Z[j] * energy_intensity

            # Apply efficiency improvements
            efficiency_factor = (1 - model.aeei[j])

            return model.Energy_demand[es, j] == base_demand * model.coe[es, j] * efficiency_factor

        self.model.eq_energy_demand_sectors = pyo.Constraint(
            self.energy_sectors, self.sectors,
            rule=energy_demand_sectors_rule,
            doc="Energy demand by sectors with efficiency"
        )

        def energy_demand_households_rule(model, es, h):
            """Energy demand by households (by energy carrier and region)"""
            # Households consume energy directly (electricity, gas, heating oil)

            # Energy consumption shares by type and region
            if es == 'Electricity':
                # Electricity consumption (40% of household energy)
                energy_share = 0.4
            elif es == 'Gas':
                # Gas consumption varies by region (more in North)
                if h in ['NW', 'NE']:
                    energy_share = 0.45  # Northern regions use more gas
                elif h in ['CENTER']:
                    energy_share = 0.35  # Central regions moderate gas use
                else:  # SOUTH, ISLANDS
                    energy_share = 0.25  # Southern regions less gas, more other fuels
            else:  # Other Energy (oil products)
                energy_share = 0.15

            # Base energy demand from household consumption
            base_energy_consumption = model.C[h,
                                              es] if es in self.sectors else 0

            # Add direct household energy consumption
            total_household_consumption = sum(
                model.C[h, j] for j in self.sectors)
            household_energy_budget = total_household_consumption * \
                0.15  # 15% of budget on energy

            return model.Energy_demand[es, h] == household_energy_budget * energy_share * model.coe[es, h]

        self.model.eq_energy_demand_households = pyo.Constraint(
            self.energy_sectors, self.household_regions,
            rule=energy_demand_households_rule,
            doc="Energy demand by households and region"
        )

        def total_energy_balance_rule(model, es):
            """Total energy consumption by type"""
            all_users = self.sectors + self.household_regions
            return model.TOT_Energy[es] == sum(model.Energy_demand[es, user] for user in all_users)

        self.model.eq_total_energy_balance = pyo.Constraint(
            self.energy_sectors,
            rule=total_energy_balance_rule,
            doc="Total energy balance by type"
        )

    def add_emission_constraints(self):
        """CO2 emission calculation constraints"""

        def emissions_by_user_rule(model, user):
            """CO2 emissions by user (sectors and households)"""
            return model.EM[user] == sum(
                model.Energy_demand[es, user] * model.co2_fac[es]
                for es in self.energy_sectors
            )

        self.model.eq_emissions_by_user = pyo.Constraint(
            self.sectors + self.household_regions,
            rule=emissions_by_user_rule,
            doc="CO2 emissions by user"
        )

        def total_emissions_rule(model):
            """Total CO2 emissions"""
            all_users = self.sectors + self.household_regions
            return model.Total_Emissions == sum(model.EM[user] for user in all_users)

        self.model.eq_total_emissions = pyo.Constraint(
            rule=total_emissions_rule,
            doc="Total CO2 emissions"
        )

    def add_ets_policy_constraints(self):
        """ETS policy implementation constraints"""

        def policy_cost_ets1_rule(model, j):
            """Policy cost from ETS1 (paid allowances only)"""
            # Only ETS1-covered sectors pay carbon price
            # Only for emissions above free allocation

            if pyo.value(model.ets1_coverage[j]) > 0:
                # Sector is covered by ETS1
                paid_emissions = model.EM[j] * (1 - model.free_alloc_ets1)
                ets1_cost = model.carbon_price_ets1 * paid_emissions
            else:
                ets1_cost = 0.0

            return ets1_cost

        def policy_cost_ets2_rule(model, j):
            """Policy cost from ETS2 (paid allowances only)"""
            if pyo.value(model.ets2_coverage[j]) > 0:
                # Sector is covered by ETS2
                paid_emissions = model.EM[j] * (1 - model.free_alloc_ets2)
                ets2_cost = model.carbon_price_ets2 * paid_emissions
            else:
                ets2_cost = 0.0

            return ets2_cost

        def total_policy_cost_rule(model, j):
            """Total policy cost on sector j (ETS1 + ETS2)"""
            ets1_cost = policy_cost_ets1_rule(model, j)
            ets2_cost = policy_cost_ets2_rule(model, j)

            return model.PLC[j] == ets1_cost + ets2_cost

        self.model.eq_policy_cost = pyo.Constraint(
            self.sectors,
            rule=total_policy_cost_rule,
            doc="Total carbon policy cost by sector"
        )

        def ets1_revenue_rule(model):
            """Total ETS1 revenue"""
            ets1_revenue = 0
            for j in self.sectors:
                if pyo.value(model.ets1_coverage[j]) > 0:
                    paid_emissions = model.EM[j] * (1 - model.free_alloc_ets1)
                    ets1_revenue += model.carbon_price_ets1 * paid_emissions

            return model.ETS1_revenue == ets1_revenue

        self.model.eq_ets1_revenue = pyo.Constraint(
            rule=ets1_revenue_rule,
            doc="ETS1 revenue calculation"
        )

        def ets2_revenue_rule(model):
            """Total ETS2 revenue"""
            ets2_revenue = 0
            for j in self.sectors:
                if pyo.value(model.ets2_coverage[j]) > 0:
                    paid_emissions = model.EM[j] * (1 - model.free_alloc_ets2)
                    ets2_revenue += model.carbon_price_ets2 * paid_emissions

            return model.ETS2_revenue == ets2_revenue

        self.model.eq_ets2_revenue = pyo.Constraint(
            rule=ets2_revenue_rule,
            doc="ETS2 revenue calculation"
        )

    def add_energy_indicators(self):
        """Energy and environmental indicators"""

        def renewable_share_rule(model):
            """Renewable share in electricity generation"""
            # Simplified: renewable share grows over time
            total_electricity = model.TOT_Energy['Electricity']

            # Renewable electricity (assumed part of total)
            base_renewable_share = 0.38  # 2021 Italian level
            growth_years = max(0, self.current_year -
                               model_definitions.base_year)
            renewable_growth = model_definitions.energy_params['renewable_growth_rate']

            # Renewable share grows with policy support
            policy_boost = 0.0
            if self.current_scenario in ['ETS1', 'ETS2']:
                policy_boost = 0.02 * growth_years  # 2% additional annual growth

            target_share = min(0.8, base_renewable_share +
                               renewable_growth * growth_years + policy_boost)

            return model.Renewable_share == target_share

        self.model.eq_renewable_share = pyo.Constraint(
            rule=renewable_share_rule,
            doc="Renewable energy share"
        )

    def update_policy_parameters(self, year, scenario_name):
        """Update ETS policy parameters for given year and scenario"""

        self.current_year = year
        self.current_scenario = scenario_name

        if scenario_name == 'BAU':
            # No carbon pricing in BAU
            self.model.carbon_price_ets1.fix(0.0)
            self.model.carbon_price_ets2.fix(0.0)

        elif scenario_name == 'ETS1':
            # ETS1 active, ETS2 not yet active
            ets1_price = model_definitions.get_carbon_price(year, 'ETS1')
            self.model.carbon_price_ets1.fix(ets1_price)
            self.model.carbon_price_ets2.fix(0.0)

            # Update free allocation rate
            ets1_free_rate = model_definitions.get_free_allocation_rate(
                year, 'ETS1')
            self.model.free_alloc_ets1.set_value(ets1_free_rate)

        elif scenario_name == 'ETS2':
            # Both ETS1 and ETS2 active
            ets1_price = model_definitions.get_carbon_price(year, 'ETS1')
            ets2_price = model_definitions.get_carbon_price(year, 'ETS2')

            self.model.carbon_price_ets1.fix(ets1_price)
            self.model.carbon_price_ets2.fix(ets2_price)

            # Update free allocation rates
            ets1_free_rate = model_definitions.get_free_allocation_rate(
                year, 'ETS1')
            ets2_free_rate = model_definitions.get_free_allocation_rate(
                year, 'ETS2')

            self.model.free_alloc_ets1.set_value(ets1_free_rate)
            self.model.free_alloc_ets2.set_value(ets2_free_rate)

        # Update AEEI rates (energy efficiency improvements)
        base_aeei = model_definitions.energy_params['autonomous_energy_efficiency']
        years_elapsed = year - model_definitions.base_year

        for j in self.sectors:
            # Enhanced AEEI under carbon pricing
            if scenario_name in ['ETS1', 'ETS2']:
                sector_code = model_definitions.sector_mapping.get(j, j)
                if sector_code in model_definitions.get_ets_coverage(year):
                    # Covered sectors improve efficiency faster
                    enhanced_aeei = base_aeei * 1.5  # 50% faster improvement
                else:
                    enhanced_aeei = base_aeei
            else:
                enhanced_aeei = base_aeei

            # Cumulative efficiency improvement
            cumulative_aeei = 1 - (1 - enhanced_aeei) ** years_elapsed
            self.model.aeei[j].set_value(
                min(0.5, cumulative_aeei))  # Cap at 50%

        print(f"Updated ETS parameters for {scenario_name} in {year}:")
        if scenario_name != 'BAU':
            print(
                f"  ETS1 price: €{ets1_price:.1f}/tCO2" if 'ets1_price' in locals() else "")
            print(
                f"  ETS2 price: €{ets2_price:.1f}/tCO2" if 'ets2_price' in locals() else "")
            print(
                f"  ETS1 free allocation: {ets1_free_rate:.1%}" if 'ets1_free_rate' in locals() else "")

    def initialize_energy_environment_variables(self):
        """Initialize energy-environment variables"""

        print("Initializing energy-environment variables...")

        # Initialize energy demands
        for es in self.energy_sectors:
            total_demand = 0

            # Sector energy demand
            for j in self.sectors:
                if es in self.sectors:
                    # Energy as intermediate input
                    demand = self.params['sectors'].get(j, {}).get(
                        'input_coefficients', {}).get(es, 0.02) * 1000
                else:
                    # Direct energy use
                    sector_data = self.params['sectors'].get(j, {})
                    energy_intensity = sector_data.get('energy_intensity', 0.1)
                    demand = sector_data.get(
                        'gross_output', 1000) * energy_intensity * 0.1

                self.model.Energy_demand[es, j].set_value(max(0.001, demand))
                total_demand += demand

            # Household energy demand by region
            for h in self.household_regions:
                hh_data = self.params['households'].get(h, {})
                total_consumption = hh_data.get('consumption', 40000)

                if es == 'Electricity':
                    demand = total_consumption * 0.08  # 8% on electricity
                elif es == 'Gas':
                    if h in ['NW', 'NE']:
                        demand = total_consumption * 0.12  # Northern regions more gas
                    else:
                        demand = total_consumption * 0.06  # Southern regions less gas
                else:  # Other Energy
                    demand = total_consumption * 0.04  # 4% on oil products

                self.model.Energy_demand[es, h].set_value(demand)
                total_demand += demand

            self.model.TOT_Energy[es].set_value(total_demand)
            print(f"  {es}: Total demand = {total_demand:.1f}")

        # Initialize emissions
        total_emissions = 0
        all_users = self.sectors + self.household_regions

        for user in all_users:
            user_emissions = 0
            for es in self.energy_sectors:
                energy_demand = pyo.value(self.model.Energy_demand[es, user])
                co2_factor = pyo.value(self.model.co2_fac[es])
                user_emissions += energy_demand * co2_factor * \
                    0.001  # Scale to appropriate units

            self.model.EM[user].set_value(user_emissions)
            total_emissions += user_emissions

        self.model.Total_Emissions.set_value(total_emissions)
        print(f"  Total emissions: {total_emissions:.1f} units")

        # Initialize carbon prices (will be updated by scenario)
        self.model.carbon_price_ets1.set_value(0.0)
        self.model.carbon_price_ets2.set_value(0.0)

        # Initialize policy costs
        for j in self.sectors:
            self.model.PLC[j].set_value(0.0)

        self.model.ETS1_revenue.set_value(0.0)
        self.model.ETS2_revenue.set_value(0.0)

        # Initialize energy efficiency rates
        base_aeei = model_definitions.energy_params['autonomous_energy_efficiency']
        for j in self.sectors:
            self.model.aeei[j].set_value(base_aeei)

        # Initialize renewable share
        self.model.Renewable_share.set_value(0.38)  # Italian 2021 level

        print("Energy-environment variables initialization completed")

    def get_energy_environment_results(self, model_solution):
        """Extract energy-environment results"""

        results = {
            'energy_demand': {
                'by_sector': {},
                'by_household': {},
                'by_energy_type': {},
                'total_by_type': {}
            },
            'emissions': {
                'by_sector': {},
                'by_household': {},
                'by_region': {},
                'total_emissions': 0
            },
            'carbon_pricing': {
                'ets1_price': 0,
                'ets2_price': 0,
                'ets1_revenue': 0,
                'ets2_revenue': 0,
                'total_carbon_revenue': 0,
                'policy_costs_by_sector': {}
            },
            'energy_indicators': {
                'energy_intensity': 0,
                'carbon_intensity': 0,
                'renewable_share': 0
            }
        }

        # Energy demand results
        for es in self.energy_sectors:
            results['energy_demand']['total_by_type'][es] = pyo.value(
                model_solution.TOT_Energy[es])

            # By sector
            sector_demands = {}
            for j in self.sectors:
                sector_demands[j] = pyo.value(
                    model_solution.Energy_demand[es, j])
            results['energy_demand']['by_sector'][es] = sector_demands

            # By household region
            household_demands = {}
            for h in self.household_regions:
                household_demands[h] = pyo.value(
                    model_solution.Energy_demand[es, h])
            results['energy_demand']['by_household'][es] = household_demands

        # Emissions results
        results['emissions']['total_emissions'] = pyo.value(
            model_solution.Total_Emissions)

        for j in self.sectors:
            results['emissions']['by_sector'][j] = pyo.value(
                model_solution.EM[j])

        for h in self.household_regions:
            results['emissions']['by_household'][h] = pyo.value(
                model_solution.EM[h])

        # Regional emissions aggregation
        regional_emissions = {}
        for h in self.household_regions:
            regional_emissions[h] = results['emissions']['by_household'][h]
        results['emissions']['by_region'] = regional_emissions

        # Carbon pricing results
        results['carbon_pricing']['ets1_price'] = pyo.value(
            model_solution.carbon_price_ets1)
        results['carbon_pricing']['ets2_price'] = pyo.value(
            model_solution.carbon_price_ets2)
        results['carbon_pricing']['ets1_revenue'] = pyo.value(
            model_solution.ETS1_revenue)
        results['carbon_pricing']['ets2_revenue'] = pyo.value(
            model_solution.ETS2_revenue)
        results['carbon_pricing']['total_carbon_revenue'] = (
            results['carbon_pricing']['ets1_revenue'] +
            results['carbon_pricing']['ets2_revenue']
        )

        for j in self.sectors:
            results['carbon_pricing']['policy_costs_by_sector'][j] = pyo.value(
                model_solution.PLC[j])

        # Energy indicators
        total_energy = sum(results['energy_demand']['total_by_type'].values())
        total_gdp = sum(
            # Scale back
            pyo.value(model_solution.Z[j]) * 1000 for j in self.sectors)

        if total_gdp > 0:
            results['energy_indicators']['energy_intensity'] = total_energy / total_gdp

        if total_energy > 0:
            results['energy_indicators']['carbon_intensity'] = results['emissions']['total_emissions'] / total_energy

        results['energy_indicators']['renewable_share'] = pyo.value(
            model_solution.Renewable_share)

        return results

# Testing function


def test_energy_environment_block():
    """Test the energy-environment block"""

    print("Testing Energy-Environment Block...")

    # Create test model
    model = pyo.ConcreteModel("EnergyEnvironment_Test")

    # Create sample data
    from data_processor import DataProcessor
    processor = DataProcessor()
    processor.create_calibrated_placeholder()
    calibrated_data = processor.get_calibrated_data()

    # Need dummy production variables
    model.Z = pyo.Var(calibrated_data['production_sectors'], initialize=1000.0)
    model.X = pyo.Var(calibrated_data['production_sectors'],
                      calibrated_data['production_sectors'], initialize=50.0)
    model.C = pyo.Var(list(calibrated_data['households'].keys(
    )), calibrated_data['production_sectors'], initialize=100.0)

    # Create energy-environment block
    ee_block = EnergyEnvironmentBlock(model, calibrated_data)

    # Initialize variables
    ee_block.initialize_energy_environment_variables()

    # Test policy updates
    ee_block.update_policy_parameters(2025, 'ETS1')
    ee_block.update_policy_parameters(2030, 'ETS2')

    print(
        f"Variables created: {len([v for v in model.component_objects(pyo.Var)])}")
    print(
        f"Constraints created: {len([c for c in model.component_objects(pyo.Constraint)])}")
    print(
        f"Parameters created: {len([p for p in model.component_objects(pyo.Param)])}")

    print("Energy-environment block test completed successfully")

    return True


if __name__ == "__main__":
    test_energy_environment_block()
