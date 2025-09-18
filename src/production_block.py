"""
Production Block for Italian CGE Model
IPOPT-optimized production functions with proper bounds and scaling
ThreeME-style CES production structure with energy nesting
"""

import pyomo.environ as pyo
import numpy as np
from definitions import model_definitions


class ProductionBlock:
    """
    Production block implementing:
    - CES production functions (Value-added and intermediate aggregates)
    - Energy-Capital-Labor nested structure following ThreeME
    - Factor demand equations with proper bounds for IPOPT
    - Intermediate input demands with realistic coefficients
    - Energy demand with efficiency improvements (AEEI)
    """

    def __init__(self, model, calibrated_data):
        self.model = model
        self.calibrated_data = calibrated_data
        self.sectors = calibrated_data['production_sectors']
        self.factors = calibrated_data['factors']
        self.energy_sectors = calibrated_data['energy_sectors']
        self.params = calibrated_data['calibrated_parameters']

        # Scaling factors for IPOPT numerical stability
        self.output_scale = 1000.0  # Scale outputs to thousands
        self.price_scale = 1.0      # Prices remain at 1.0 scale

        self.add_production_variables()
        self.add_production_parameters()
        self.add_production_constraints()

    def add_production_variables(self):
        """Add production variables with proper bounds for IPOPT"""

        # Gross output by sector (scaled)
        def output_bounds(model, j):
            sector_data = self.params['sectors'].get(j, {})
            base_output = sector_data.get(
                'gross_output', 1000) / self.output_scale
            # 10% to 500% of base
            return (base_output * 0.1, base_output * 5.0)

        self.model.Z = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=output_bounds,
            initialize=lambda m, j: self.params['sectors'].get(
                j, {}).get('gross_output', 1000) / self.output_scale,
            doc="Gross output by sector (scaled)"
        )

        # Value-added aggregate
        def va_bounds(model, j):
            sector_data = self.params['sectors'].get(j, {})
            base_va = sector_data.get('value_added', 600) / self.output_scale
            return (base_va * 0.1, base_va * 5.0)

        self.model.VA = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=va_bounds,
            initialize=lambda m, j: self.params['sectors'].get(
                j, {}).get('value_added', 600) / self.output_scale,
            doc="Value-added aggregate"
        )

        # Energy-Capital-Labor aggregate (for energy-using sectors)
        self.model.EKL = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=va_bounds,
            initialize=lambda m, j: self.params['sectors'].get(
                j, {}).get('value_added', 600) / self.output_scale,
            doc="Energy-Capital-Labor aggregate"
        )

        # Capital-Labor aggregate
        self.model.KL = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=lambda m, j: (0.1, va_bounds(
                m, j)[1]),  # Higher minimum bound
            initialize=lambda m, j: max(self.params['sectors'].get(j, {}).get(
                'value_added', 600) * 0.8 / self.output_scale, 0.1),
            doc="Capital-Labor aggregate"
        )

        # Factor demands
        def factor_bounds(model, f, j):
            sector_data = self.params['sectors'].get(j, {})
            factor_payments = sector_data.get('factor_payments', {})
            base_demand = factor_payments.get(f, 300) / self.output_scale
            # Ensure minimum factor demand is never too small to avoid numerical issues
            min_demand = max(base_demand * 0.1, 0.01)  # At least 0.01 units
            return (min_demand, base_demand * 5.0)

        self.model.F = pyo.Var(
            self.factors, self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=factor_bounds,
            initialize=lambda m, f, j: max(self.params['sectors'].get(j, {}).get(
                'factor_payments', {}).get(f, 300) / self.output_scale, 0.01),
            doc="Factor demand"
        )

        # Energy demand (MWh annual units)
        def energy_bounds(model, j):
            sector_data = self.params['sectors'].get(j, {})
            # Base energy in economic units converted to MWh annual
            base_energy_economic = sector_data.get(
                'gross_output', 1000) * sector_data.get('energy_intensity', 0.1)
            # Convert economic units to MWh (using average conversion factor)
            base_energy_mwh = base_energy_economic * 8760  # Annual hours conversion
            base_energy = base_energy_mwh / self.output_scale
            # Ensure minimum energy is substantial enough to avoid numerical issues
            # At least 8.76 MWh (1 kW continuous)
            min_energy = max(8.76, base_energy * 0.01)
            return (min_energy, base_energy * 10.0)

        self.model.EN = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=energy_bounds,
            initialize=lambda m, j: max(self.params['sectors'].get(j, {}).get('gross_output', 1000) *
                                        self.params['sectors'].get(j, {}).get('energy_intensity', 0.1) * 8760 / self.output_scale, 8.76),
            doc="Energy demand (MWh annual)"
        )

        # Intermediate input demands
        def intermediate_bounds(model, i, j):
            sector_data = self.params['sectors'].get(j, {})
            input_coeffs = sector_data.get('input_coefficients', {})
            base_intermediate = input_coeffs.get(
                i, 0.02) * sector_data.get('gross_output', 1000)
            base_intermediate = base_intermediate / self.output_scale
            return (0.0, base_intermediate * 10.0)

        self.model.X = pyo.Var(
            self.sectors, self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=intermediate_bounds,
            initialize=lambda m, i, j: self.params['sectors'].get(j, {}).get('input_coefficients', {}).get(i, 0.02) *
            self.params['sectors'].get(j, {}).get(
                'gross_output', 1000) / self.output_scale,
            doc="Intermediate input demands"
        )

        # Price variables with bounds
        def price_bounds(model, j):
            return (0.1, 10.0)  # Prices between 10% and 1000% of base

        self.model.pz = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=price_bounds,
            initialize=1.0,
            doc="Producer prices"
        )

        self.model.pva = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=price_bounds,
            initialize=1.0,
            doc="Value-added prices"
        )

        self.model.pf = pyo.Var(
            self.factors,
            domain=pyo.PositiveReals,
            bounds=(0.1, 10.0),
            initialize=1.0,
            doc="Factor prices"
        )

    def add_production_parameters(self):
        """Add production parameters calibrated from SAM"""

        # CES substitution elasticities (from literature and ThreeME)
        elasticities = {
            'va_substitution': 0.7,     # Between KL and Energy
            'kl_substitution': 0.4,     # Between Capital and Labor
            'energy_substitution': 1.2,  # Between energy types
            'intermediate_substitution': 0.5  # Between intermediate inputs
        }

        # Value-added CES parameters
        def get_va_alpha(model, j):
            sector_data = self.params['sectors'].get(j, {})
            return sector_data.get('value_added', 600) / self.output_scale

        def get_va_rho(model, j):
            sigma = elasticities['va_substitution']
            return (sigma - 1) / sigma

        self.model.alpha_va = pyo.Param(
            self.sectors,
            initialize=get_va_alpha,
            mutable=True,
            doc="Value-added scale parameter"
        )

        self.model.rho_va = pyo.Param(
            self.sectors,
            initialize=get_va_rho,
            doc="Value-added substitution parameter"
        )

        # Energy-Capital-Labor shares
        def get_energy_share(model, j):
            sector_data = self.params['sectors'].get(j, {})
            if sector_data.get('is_energy_sector', False):
                return 0.4  # Energy sectors use more energy
            elif sector_data.get('is_transport_sector', False):
                return 0.3  # Transport sectors use significant energy
            else:
                return 0.1  # Other sectors use less energy

        def get_kl_share(model, j):
            return 1.0 - get_energy_share(model, j)

        self.model.delta_en = pyo.Param(
            self.sectors,
            initialize=get_energy_share,
            doc="Energy share in VA aggregate"
        )

        self.model.delta_kl = pyo.Param(
            self.sectors,
            initialize=get_kl_share,
            doc="Capital-Labor share in VA aggregate"
        )

        # Capital-Labor shares
        def get_labor_share(model, j):
            sector_data = self.params['sectors'].get(j, {})
            factor_coeffs = sector_data.get('factor_coefficients', {})
            return factor_coeffs.get('Labour', 0.6)

        def get_capital_share(model, j):
            return 1.0 - get_labor_share(model, j)

        self.model.delta_l = pyo.Param(
            self.sectors,
            initialize=get_labor_share,
            doc="Labor share in KL aggregate"
        )

        self.model.delta_k = pyo.Param(
            self.sectors,
            initialize=get_capital_share,
            doc="Capital share in KL aggregate"
        )

        # Intermediate input coefficients (Leontief for simplicity)
        def get_input_coeff(model, i, j):
            if i == j:
                return 0.0  # No self-consumption
            sector_data = self.params['sectors'].get(j, {})
            input_coeffs = sector_data.get('input_coefficients', {})
            return input_coeffs.get(i, 0.02)  # Default 2%

        self.model.a_ij = pyo.Param(
            self.sectors, self.sectors,
            initialize=get_input_coeff,
            mutable=True,
            doc="Input-output coefficients"
        )

        # Energy intensity coefficients
        def get_energy_coeff(model, j):
            sector_data = self.params['sectors'].get(j, {})
            return sector_data.get('energy_intensity', 0.1)

        self.model.e_j = pyo.Param(
            self.sectors,
            initialize=get_energy_coeff,
            mutable=True,
            doc="Energy intensity coefficients"
        )

        # Autonomous Energy Efficiency Improvement (AEEI) rates
        self.model.aeei = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=(0.0, 0.05),  # 0-5% annual improvement
            initialize=0.01,
            doc="AEEI rates by sector"
        )

        # Total Factor Productivity (TFP) growth
        self.model.tfp_growth = pyo.Var(
            self.sectors,
            domain=pyo.Reals,
            bounds=(-0.02, 0.05),  # -2% to +5% annual growth
            initialize=0.015,
            doc="TFP growth rates by sector"
        )

    def add_production_constraints(self):
        """Add production constraints optimized for IPOPT"""

        # Production function (Leontief between VA and intermediates)
        def production_function_rule(model, j):
            """Z = min(VA/va_coeff, INTERM/int_coeff)"""
            # Simplified as fixed coefficients for IPOPT stability
            sector_data = self.params['sectors'].get(j, {})
            va_share = sector_data.get('value_added', 600) / sector_data.get(
                'gross_output', 1000) if sector_data.get('gross_output', 1000) > 0 else 0.7
            return model.Z[j] == va_share * model.VA[j] + (1 - va_share) * sum(model.X[i, j] for i in self.sectors)

        self.model.eq_production = pyo.Constraint(
            self.sectors,
            rule=production_function_rule,
            doc="Production function"
        )

        # Value-added CES function (Energy-Capital-Labor aggregate)
        def value_added_ces_rule(model, j):
            """VA = alpha_va * [delta_en*EN^rho + delta_kl*KL^rho]^(1/rho)"""
            # Use Cobb-Douglas form as CES approximation
            # VA = alpha_va * EN^delta_en * KL^delta_kl

            # For numerical stability, ensure positive base values
            en_term = (model.EN[j] + 1e-6) ** model.delta_en[j]
            kl_term = (model.KL[j] + 1e-6) ** model.delta_kl[j]

            return model.VA[j] == model.alpha_va[j] * en_term * kl_term

        self.model.eq_value_added_ces = pyo.Constraint(
            self.sectors,
            rule=value_added_ces_rule,
            doc="Value-added CES function (linearized)"
        )

        # Capital-Labor CES function
        def capital_labor_ces_rule(model, j):
            """KL = [delta_l*L^rho + delta_k*K^rho]^(1/rho)"""
            # Use Cobb-Douglas form as CES approximation
            # KL = alpha_kl * L^delta_l * K^delta_k

            # For numerical stability, ensure positive base values
            labor_term = (model.F['Labour', j] + 1e-6) ** model.delta_l[j]
            capital_term = (model.F['Capital', j] + 1e-6) ** model.delta_k[j]

            return model.KL[j] == labor_term * capital_term

        self.model.eq_capital_labor_ces = pyo.Constraint(
            self.sectors,
            rule=capital_labor_ces_rule,
            doc="Capital-Labor aggregate (linearized)"
        )

        # Energy demand function with AEEI (MWh annual)
        def energy_demand_rule(model, j):
            """EN = e_j * Z * (1 - AEEI) * (1 + TFP_growth) * 8760 [MWh annual]"""
            efficiency_factor = (1 - model.aeei[j])
            tfp_factor = (1 + model.tfp_growth[j])
            # Convert to annual MWh: energy intensity * output * efficiency * 8760 hours
            return model.EN[j] == model.e_j[j] * model.Z[j] * efficiency_factor * tfp_factor * 8760

        self.model.eq_energy_demand = pyo.Constraint(
            self.sectors,
            rule=energy_demand_rule,
            doc="Energy demand with efficiency improvements (MWh annual)"
        )

        # Intermediate input demands (Leontief)
        def intermediate_demand_rule(model, i, j):
            """X[i,j] = a_ij[i,j] * Z[j]"""
            return model.X[i, j] == model.a_ij[i, j] * model.Z[j]

        self.model.eq_intermediate_demand = pyo.Constraint(
            self.sectors, self.sectors,
            rule=intermediate_demand_rule,
            doc="Intermediate input demands"
        )

        # Factor demand FOCs (simplified to avoid division)
        def labor_demand_foc_rule(model, j):
            """Labor demand from marginal productivity condition"""
            # Simplified: pf_L * F_L = pva * marginal_share_L
            # Avoid division by reformulating as: pf_L * F_L = pva * delta_l * KL
            return (model.pf['Labour'] * model.F['Labour', j] ==
                    model.pva[j] * model.delta_l[j] * model.KL[j])

        self.model.eq_labor_demand_foc = pyo.Constraint(
            self.sectors,
            rule=labor_demand_foc_rule,
            doc="Labor demand FOC (no division)"
        )

        def capital_demand_foc_rule(model, j):
            """Capital demand from marginal productivity condition"""
            # Simplified: pf_K * F_K = pva * marginal_share_K
            # Avoid division by reformulating as: pf_K * F_K = pva * delta_k * KL
            return (model.pf['Capital'] * model.F['Capital', j] ==
                    model.pva[j] * model.delta_k[j] * model.KL[j])

        self.model.eq_capital_demand_foc = pyo.Constraint(
            self.sectors,
            rule=capital_demand_foc_rule,
            doc="Capital demand FOC (no division)"
        )

        # Zero-profit conditions (price equations)
        def zero_profit_rule(model, j):
            """pz = pva * va_share + sum(pq[i] * a_ij[i,j])"""
            sector_data = self.params['sectors'].get(j, {})
            va_share = (sector_data.get('value_added', 600) /
                        sector_data.get('gross_output', 1000) if sector_data.get('gross_output', 1000) > 0 else 0.7)

            # Simplified: assume pq=1
            intermediate_cost = sum(model.a_ij[i, j] for i in self.sectors)

            return model.pz[j] == model.pva[j] * va_share + intermediate_cost

        self.model.eq_zero_profit = pyo.Constraint(
            self.sectors,
            rule=zero_profit_rule,
            doc="Zero-profit condition"
        )

    def initialize_production_variables(self):
        """Initialize production variables with SAM-calibrated values"""

        print("Initializing production variables with calibrated data...")

        for j in self.sectors:
            if j in self.params['sectors']:
                sector_data = self.params['sectors'][j]

                # Scale values
                gross_output = sector_data.get(
                    'gross_output', 1000) / self.output_scale
                value_added = sector_data.get(
                    'value_added', 600) / self.output_scale

                # Initialize quantities
                self.model.Z[j].set_value(gross_output)
                self.model.VA[j].set_value(value_added)
                self.model.KL[j].set_value(
                    value_added * 0.8)  # Most of VA is KL
                self.model.EKL[j].set_value(value_added)

                # Initialize energy (convert to MWh annual)
                energy_demand_economic = (
                    gross_output * sector_data.get('energy_intensity', 0.1))
                energy_demand_mwh = energy_demand_economic * 8760  # Convert to annual MWh
                self.model.EN[j].set_value(max(8.76, energy_demand_mwh))

                # Initialize factors
                factor_payments = sector_data.get('factor_payments', {})
                for f in self.factors:
                    payment = factor_payments.get(f, 300) / self.output_scale
                    self.model.F[f, j].set_value(payment)

                # Initialize intermediate inputs
                input_coeffs = sector_data.get('input_coefficients', {})
                for i in self.sectors:
                    coeff = input_coeffs.get(i, 0.02)
                    intermediate_demand = coeff * gross_output
                    self.model.X[i, j].set_value(intermediate_demand)

                print(
                    f"  {j}: Output={gross_output:.1f}, VA={value_added:.1f}, Energy={energy_demand_mwh:.1f} MWh")

            # Initialize prices
            self.model.pz[j].set_value(1.0)
            self.model.pva[j].set_value(1.0)

        # Initialize factor prices
        for f in self.factors:
            self.model.pf[f].set_value(1.0)

        print("Production block initialization completed")

    def update_dynamic_parameters(self, year):
        """Update parameters for dynamic recursive model"""

        base_year = model_definitions.base_year
        years_elapsed = year - base_year

        # Update TFP growth (exogenous)
        productivity_growth = model_definitions.macro_params['productivity_growth_rate']
        for j in self.sectors:
            self.model.tfp_growth[j].set_value(productivity_growth)

        # Update AEEI (energy efficiency improvement)
        aeei_rate = model_definitions.energy_params['autonomous_energy_efficiency']
        for j in self.sectors:
            # Cumulative efficiency improvement
            cumulative_aeei = 1 - (1 - aeei_rate) ** years_elapsed
            self.model.aeei[j].set_value(
                min(0.5, cumulative_aeei))  # Cap at 50%

        # Update input coefficients for technological change
        for i in self.sectors:
            for j in self.sectors:
                if i != j:
                    base_coeff = self.params['sectors'].get(j, {}).get(
                        'input_coefficients', {}).get(i, 0.02)
                    # Slight reduction in input coefficients due to efficiency gains
                    # 0.5% annual reduction
                    new_coeff = base_coeff * (0.995 ** years_elapsed)
                    self.model.a_ij[i, j].set_value(new_coeff)

        print(f"Updated dynamic parameters for year {year}")
        print(f"  TFP growth: {productivity_growth:.1%}")
        print(f"  Cumulative AEEI: {cumulative_aeei:.1%}")

    def get_production_results(self, model_solution):
        """Extract production results from solved model"""

        results = {
            'gross_output': {},
            'value_added': {},
            'factor_demands': {f: {} for f in self.factors},
            'energy_demand': {},
            'intermediate_demands': {},
            'producer_prices': {},
            'factor_prices': {}
        }

        for j in self.sectors:
            # Scale back to original units
            results['gross_output'][j] = pyo.value(
                model_solution.Z[j]) * self.output_scale
            results['value_added'][j] = pyo.value(
                model_solution.VA[j]) * self.output_scale
            results['energy_demand'][j] = pyo.value(
                model_solution.EN[j]) * self.output_scale
            results['producer_prices'][j] = pyo.value(model_solution.pz[j])

            for f in self.factors:
                results['factor_demands'][f][j] = pyo.value(
                    model_solution.F[f, j]) * self.output_scale

            # Intermediate demands
            intermediate_dict = {}
            for i in self.sectors:
                intermediate_dict[i] = pyo.value(
                    model_solution.X[i, j]) * self.output_scale
            results['intermediate_demands'][j] = intermediate_dict

        for f in self.factors:
            results['factor_prices'][f] = pyo.value(model_solution.pf[f])

        # Calculate aggregates
        results['total_output'] = sum(results['gross_output'].values())
        results['total_value_added'] = sum(results['value_added'].values())
        results['total_energy'] = sum(results['energy_demand'].values())

        return results

    def validate_production_structure(self):
        """Validate production structure for IPOPT feasibility"""

        validation_results = []

        # Check if all variables have proper bounds
        unbounded_vars = []
        for var in [self.model.Z, self.model.VA, self.model.F]:
            for index in var:
                if var[index].lb is None or var[index].ub is None:
                    unbounded_vars.append(f"{var.name}[{index}]")

        if unbounded_vars:
            validation_results.append(
                # Show first 5
                f"Unbounded variables: {unbounded_vars[:5]}...")

        # Check parameter consistency
        for j in self.sectors:
            if j in self.params['sectors']:
                sector_data = self.params['sectors'][j]

                # Check if factor shares sum to reasonable values
                factor_coeffs = sector_data.get('factor_coefficients', {})
                factor_sum = sum(factor_coeffs.values())
                if factor_sum > 1.0:
                    validation_results.append(
                        f"Sector {j}: Factor shares sum to {factor_sum:.2f} > 1.0")

                # Check if input coefficients are reasonable
                input_coeffs = sector_data.get('input_coefficients', {})
                input_sum = sum(input_coeffs.values())
                if input_sum > 0.8:  # Should not exceed 80% of output
                    validation_results.append(
                        f"Sector {j}: Input coefficients sum to {input_sum:.2f}")

        # Check CES parameter consistency
        for j in self.sectors:
            rho_va = pyo.value(self.model.rho_va[j])
            if abs(rho_va) > 10:  # Very high substitution elasticity
                validation_results.append(
                    f"Sector {j}: Very high CES parameter rho={rho_va:.2f}")

        if not validation_results:
            print("Production structure validation passed")
        else:
            print("Production structure validation warnings:")
            for warning in validation_results[:5]:  # Show first 5 warnings
                print(f"  - {warning}")

        return len(validation_results) == 0

# Testing function


def test_production_block():
    """Test the production block with sample data"""

    print("Testing Production Block...")

    # Create minimal test model
    model = pyo.ConcreteModel("Production_Test")

    # Create sample calibrated data
    from data_processor import DataProcessor
    processor = DataProcessor()
    processor.create_calibrated_placeholder()
    calibrated_data = processor.get_calibrated_data()

    # Create production block
    prod_block = ProductionBlock(model, calibrated_data)

    # Initialize variables
    prod_block.initialize_production_variables()

    # Validate structure
    is_valid = prod_block.validate_production_structure()

    # Test results
    print(
        f"Variables created: {len([v for v in model.component_objects(pyo.Var)])}")
    print(
        f"Constraints created: {len([c for c in model.component_objects(pyo.Constraint)])}")
    print(
        f"Parameters created: {len([p for p in model.component_objects(pyo.Param)])}")
    print(f"Structure valid: {is_valid}")

    # Test dynamic parameter update
    prod_block.update_dynamic_parameters(2025)

    print("Production block test completed successfully")

    return True


if __name__ == "__main__":
    test_production_block()
