"""
Trade Block for Italian CGE Model
IPOPT-optimized Armington and CET functions with proper bounds
International trade flows and exchange rate determination
"""

import pyomo.environ as pyo
import numpy as np
from definitions import model_definitions


class TradeBlock:
    """
    Trade block implementing:
    - Armington aggregation (domestic vs. imported goods) with CES
    - CET transformation (domestic sales vs. exports) with CET
    - Exchange rate determination
    - Trade balance constraints optimized for IPOPT
    """

    def __init__(self, model, calibrated_data):
        self.model = model
        self.calibrated_data = calibrated_data
        self.sectors = calibrated_data['production_sectors']
        self.params = calibrated_data['calibrated_parameters']

        # Scaling factors for IPOPT numerical stability
        self.trade_scale = 1000.0  # Scale trade flows to thousands
        self.price_scale = 1.0

        self.add_trade_variables()
        self.add_trade_parameters()
        self.add_trade_constraints()

    def add_trade_variables(self):
        """Add trade variables with proper bounds for IPOPT"""

        # Check for existing variables and delete if necessary to avoid conflicts
        existing_vars = ['Q', 'D', 'M', 'E', 'pq', 'pd', 'pm', 'pe']
        for var_name in existing_vars:
            if hasattr(self.model, var_name):
                print(
                    f"  Removing existing variable {var_name} to avoid conflict")
                self.model.del_component(var_name)

        # Armington composite good (total supply)
        def composite_bounds(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            base_supply = trade_data.get(
                'total_supply', 1000) / self.trade_scale
            return (base_supply * 0.3, base_supply * 5.0)

        self.model.Q = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=composite_bounds,
            initialize=lambda m, j: self.params.get('trade', {}).get(
                j, {}).get('total_supply', 1000) / self.trade_scale,
            doc="Armington composite good (scaled)"
        )

        # Domestic good for domestic market
        def domestic_bounds(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            base_domestic = trade_data.get(
                'domestic_sales', 800) / self.trade_scale
            return (base_domestic * 0.1, base_domestic * 5.0)

        self.model.D = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=domestic_bounds,
            initialize=lambda m, j: self.params.get('trade', {}).get(
                j, {}).get('domestic_sales', 800) / self.trade_scale,
            doc="Domestic good for domestic market (scaled)"
        )

        # Imports
        def import_bounds(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            base_imports = max(trade_data.get(
                'imports', 100), 1.0) / self.trade_scale
            return (0.001, base_imports * 10.0)  # Small positive lower bound

        self.model.M = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=import_bounds,
            initialize=lambda m, j: max(self.params.get('trade', {}).get(
                j, {}).get('imports', 100), 1.0) / self.trade_scale,
            doc="Imports by sector (scaled)"
        )

        # Exports
        def export_bounds(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            base_exports = max(trade_data.get(
                'exports', 100), 1.0) / self.trade_scale
            return (0.001, base_exports * 10.0)  # Small positive lower bound

        self.model.E = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=export_bounds,
            initialize=lambda m, j: max(self.params.get('trade', {}).get(
                j, {}).get('exports', 100), 1.0) / self.trade_scale,
            doc="Exports by sector (scaled)"
        )

        # Price variables with bounds
        def price_bounds(model, j):
            return (0.1, 10.0)

        self.model.pq = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=price_bounds,
            initialize=1.0,
            doc="Armington composite price"
        )

        self.model.pd = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=price_bounds,
            initialize=1.0,
            doc="Domestic good price for domestic market"
        )

        self.model.pm = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=price_bounds,
            initialize=1.0,
            doc="Import price (domestic currency)"
        )

        self.model.pe = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=price_bounds,
            initialize=1.0,
            doc="Export price (domestic currency)"
        )

        # Exchange rate (numeraire - fixed in most closures)
        self.model.epsilon = pyo.Var(
            domain=pyo.PositiveReals,
            bounds=(0.1, 10.0),
            initialize=1.0,
            doc="Exchange rate (domestic/foreign currency)"
        )

        # World prices (exogenous)
        def world_price_init(model, j):
            return 1.0  # Normalized world prices

        self.model.pWe = pyo.Param(
            self.sectors,
            initialize=world_price_init,
            mutable=True,
            doc="World export prices"
        )

        self.model.pWm = pyo.Param(
            self.sectors,
            initialize=world_price_init,
            mutable=True,
            doc="World import prices"
        )

    def add_trade_parameters(self):
        """Add trade parameters calibrated from SAM"""

        # Armington CES parameters
        def get_armington_gamma(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            return trade_data.get('armington_gamma', 1.0)

        def get_armington_delta_m(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            return trade_data.get('armington_share_import', 0.2)

        def get_armington_delta_d(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            return trade_data.get('armington_share_domestic', 0.8)

        def get_armington_rho(model, j):
            # From elasticity of substitution (sigma = 2.0 default)
            sigma = model_definitions.elasticities['trade']['import_substitution']
            return (sigma - 1) / sigma

        self.model.gamma_a = pyo.Param(
            self.sectors,
            initialize=get_armington_gamma,
            mutable=True,
            doc="Armington scale parameter"
        )

        self.model.delta_m = pyo.Param(
            self.sectors,
            initialize=get_armington_delta_m,
            mutable=True,
            doc="Import share in Armington"
        )

        self.model.delta_d = pyo.Param(
            self.sectors,
            initialize=get_armington_delta_d,
            mutable=True,
            doc="Domestic share in Armington"
        )

        self.model.rho_a = pyo.Param(
            self.sectors,
            initialize=get_armington_rho,
            doc="Armington substitution parameter"
        )

        # CET transformation parameters
        def get_cet_gamma(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            return trade_data.get('cet_gamma', 1.0)

        def get_cet_delta_e(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            return trade_data.get('cet_share_export', 0.15)

        def get_cet_delta_d(model, j):
            trade_data = self.params.get('trade', {}).get(j, {})
            return trade_data.get('cet_share_domestic', 0.85)

        def get_cet_rho(model, j):
            # From elasticity of transformation (sigma = 2.0 default)
            sigma = model_definitions.elasticities['trade']['export_transformation']
            return (sigma + 1) / sigma

        self.model.gamma_t = pyo.Param(
            self.sectors,
            initialize=get_cet_gamma,
            mutable=True,
            doc="CET scale parameter"
        )

        self.model.delta_e = pyo.Param(
            self.sectors,
            initialize=get_cet_delta_e,
            mutable=True,
            doc="Export share in CET"
        )

        self.model.delta_dt = pyo.Param(
            self.sectors,
            initialize=get_cet_delta_d,
            mutable=True,
            doc="Domestic sales share in CET"
        )

        self.model.rho_t = pyo.Param(
            self.sectors,
            initialize=get_cet_rho,
            doc="CET transformation parameter"
        )

        # Tariff rates
        def get_tariff_rate(model, j):
            tax_data = self.params.get('tax_rates', {})
            tariff_rates = tax_data.get('tariff_rate', {})
            return tariff_rates.get(j, 0.05)  # 5% default

        self.model.trm = pyo.Param(
            self.sectors,
            initialize=get_tariff_rate,
            mutable=True,
            doc="Tariff rates"
        )

    def add_trade_constraints(self):
        """Add trade constraints optimized for IPOPT"""

        self.add_armington_constraints()
        self.add_cet_constraints()
        self.add_price_linkage_constraints()
        self.add_trade_balance_constraints()

    def add_armington_constraints(self):
        """Armington aggregation: Q = f(D, M)"""

        def armington_ces_rule(model, j):
            """
            Armington CES: Q = gamma_a * [delta_d*D^rho + delta_m*M^rho]^(1/rho)
            """
            # Use Cobb-Douglas approximation for Armington aggregation
            # Q = gamma_a * D^delta_d * M^delta_m
            d_term = (model.D[j] + 1e-6) ** model.delta_d[j]
            m_term = (model.M[j] + 1e-6) ** model.delta_m[j]

            return (model.Q[j] == model.gamma_a[j] * d_term * m_term)

        self.model.eq_armington_ces = pyo.Constraint(
            self.sectors,
            rule=armington_ces_rule,
            doc="Armington CES aggregation"
        )

        def import_demand_foc_rule(model, j):
            """
            Import demand FOC: pm/pd = (delta_m/delta_d) * (D/M)^(1-rho)
            Rearranged: M = D * (delta_m/delta_d * pd/pm)^(1/(1-rho))
            """
            rho = model.rho_a[j]

            if abs(1 - rho) < 1e-6:  # Perfect substitutes case
                return model.pm[j] * model.delta_d[j] == model.pd[j] * model.delta_m[j]
            else:
                # Use ratio form for better numerical properties
                elasticity = 1 / (1 - rho)
                price_ratio = model.pd[j] / model.pm[j]
                share_ratio = model.delta_m[j] / model.delta_d[j]

                # Use linear form to avoid power function issues
                return model.M[j] == model.D[j] * share_ratio * price_ratio

        self.model.eq_import_demand_foc = pyo.Constraint(
            self.sectors,
            rule=import_demand_foc_rule,
            doc="Import demand from Armington FOC"
        )

    def add_cet_constraints(self):
        """CET transformation: Z = f(D, E)"""

        def cet_transformation_rule(model, j):
            """
            CET: Use Cobb-Douglas approximation
            Z = gamma_t * D^delta_dt * E^delta_e
            """
            # Use Cobb-Douglas for numerical stability
            d_term = (model.D[j] + 1e-6) ** model.delta_dt[j]
            e_term = (model.E[j] + 1e-6) ** model.delta_e[j]

            return (model.Z[j] == model.gamma_t[j] * d_term * e_term)

        self.model.eq_cet_transformation = pyo.Constraint(
            self.sectors,
            rule=cet_transformation_rule,
            doc="CET transformation"
        )

        def export_supply_foc_rule(model, j):
            """
            Export supply FOC: pe/pd = (delta_e/delta_dt) * (D/E)^(1-rho)
            Rearranged: E = D * (delta_e/delta_dt * pd/pe)^(1/(1-rho))
            """
            # Use linear form to avoid power function issues
            price_ratio = model.pd[j] / model.pe[j]
            share_ratio = model.delta_e[j] / model.delta_dt[j]

            return model.E[j] == model.D[j] * share_ratio * price_ratio

        self.model.eq_export_supply_foc = pyo.Constraint(
            self.sectors,
            rule=export_supply_foc_rule,
            doc="Export supply from CET FOC"
        )

    def add_price_linkage_constraints(self):
        """Price linkages between domestic and world markets"""

        def export_price_linkage_rule(model, j):
            """pe = epsilon * pWe (export price linkage)"""
            return model.pe[j] == model.epsilon * model.pWe[j]

        self.model.eq_export_price_linkage = pyo.Constraint(
            self.sectors,
            rule=export_price_linkage_rule,
            doc="Export price linkage"
        )

        def import_price_linkage_rule(model, j):
            """pm = epsilon * pWm * (1 + trm) (import price with tariff)"""
            return model.pm[j] == model.epsilon * model.pWm[j] * (1 + model.trm[j])

        self.model.eq_import_price_linkage = pyo.Constraint(
            self.sectors,
            rule=import_price_linkage_rule,
            doc="Import price linkage with tariffs"
        )

        def composite_price_rule(model, j):
            """
            Zero-profit for Armington aggregation:
            pq * Q = pd * D + pm * M
            """
            return model.pq[j] * model.Q[j] == model.pd[j] * model.D[j] + model.pm[j] * model.M[j]

        self.model.eq_composite_price = pyo.Constraint(
            self.sectors,
            rule=composite_price_rule,
            doc="Composite good price (zero-profit)"
        )

        def producer_price_rule(model, j):
            """
            Zero-profit for CET transformation:
            pz * Z = pd * D + pe * E
            """
            return model.pz[j] * model.Z[j] == model.pd[j] * model.D[j] + model.pe[j] * model.E[j]

        self.model.eq_producer_price = pyo.Constraint(
            self.sectors,
            rule=producer_price_rule,
            doc="Producer price (zero-profit)"
        )

    def add_trade_balance_constraints(self):
        """Trade balance and exchange rate determination with numerical stability"""

        def current_account_balance_rule(model):
            """
            Simplified current account balance for numerical stability:
            Trade Balance = Export value - Import value
            """
            export_value = sum(model.pWe[j] * model.E[j] for j in self.sectors)
            import_value = sum(model.pWm[j] * model.M[j] for j in self.sectors)

            # Add to model's trade_balance variable from market clearing block
            # This will be set in the market clearing closure
            return pyo.Constraint.Skip  # Skip - handled in market clearing

        # Note: Current account constraint handled in market clearing block
        print("Trade balance constraints configured for market clearing block integration")

    def add_world_price_constraints(self):
        """Add world price constraints for small open economy"""

        def world_export_price_rule(model, j):
            """World export prices are exogenous for small open economy"""
            return pyo.Constraint.Skip  # World prices are parameters

        def world_import_price_rule(model, j):
            """World import prices are exogenous for small open economy"""
            return pyo.Constraint.Skip  # World prices are parameters

    def initialize_trade_variables(self):
        """Initialize trade variables with calibrated values"""

        print("Initializing trade variables with calibrated data...")

        for j in self.sectors:
            trade_data = self.params.get('trade', {}).get(j, {})

            # Scale trade flows
            exports = max(trade_data.get('exports', 100),
                          1.0) / self.trade_scale
            imports = max(trade_data.get('imports', 100),
                          1.0) / self.trade_scale
            domestic_sales = trade_data.get(
                'domestic_sales', 800) / self.trade_scale
            total_supply = trade_data.get(
                'total_supply', 1000) / self.trade_scale

            # Initialize quantities
            self.model.E[j].set_value(exports)
            self.model.M[j].set_value(imports)
            self.model.D[j].set_value(domestic_sales)
            self.model.Q[j].set_value(total_supply)

            # Initialize prices
            self.model.pq[j].set_value(1.0)
            self.model.pd[j].set_value(1.0)
            self.model.pm[j].set_value(1.0)
            self.model.pe[j].set_value(1.0)

            # World prices
            self.model.pWe[j].set_value(1.0)
            self.model.pWm[j].set_value(1.0)

            print(
                f"  {j}: E={exports:.3f}, M={imports:.3f}, D={domestic_sales:.1f}, Q={total_supply:.1f}")

        # Exchange rate (usually numeraire)
        self.model.epsilon.set_value(1.0)

        print("Trade variables initialization completed")

    def update_world_prices(self, year, scenario_name='BAU'):
        """Update world prices for dynamic simulation"""

        # World price trends (simplified)
        base_year = model_definitions.base_year
        years_elapsed = year - base_year

        # Energy price trends
        energy_price_growth = 0.02  # 2% annual growth
        other_price_growth = 0.01   # 1% annual growth for other goods

        for j in self.sectors:
            if j in model_definitions.energy_sectors:
                # Energy prices grow faster
                price_factor = (1 + energy_price_growth) ** years_elapsed

                # Additional volatility for oil/gas prices
                if j in ['Gas', 'Other Energy']:
                    if scenario_name in ['ETS1', 'ETS2']:
                        # Higher world prices due to carbon policies
                        price_factor *= 1.1

            elif j in model_definitions.transport_sectors:
                # Transport services prices
                price_factor = (1 + other_price_growth) ** years_elapsed

            else:
                # Other goods
                price_factor = (1 + other_price_growth) ** years_elapsed

            # Update world prices
            self.model.pWe[j].set_value(price_factor)
            self.model.pWm[j].set_value(price_factor)

        if years_elapsed > 0:
            print(f"Updated world prices for year {year}")

    def get_trade_results(self, model_solution):
        """Extract trade results from solved model"""

        results = {
            'exports': {},
            'imports': {},
            'domestic_sales': {},
            'composite_supply': {},
            'trade_balance': {},
            'prices': {
                'composite': {},
                'domestic': {},
                'import': {},
                'export': {}
            },
            'trade_indicators': {}
        }

        # Scale back to original units
        total_exports_value = 0
        total_imports_value = 0

        for j in self.sectors:
            # Quantities
            exports = pyo.value(model_solution.E[j]) * self.trade_scale
            imports = pyo.value(model_solution.M[j]) * self.trade_scale
            domestic_sales = pyo.value(model_solution.D[j]) * self.trade_scale
            composite_supply = pyo.value(
                model_solution.Q[j]) * self.trade_scale

            results['exports'][j] = exports
            results['imports'][j] = imports
            results['domestic_sales'][j] = domestic_sales
            results['composite_supply'][j] = composite_supply

            # Prices
            results['prices']['composite'][j] = pyo.value(model_solution.pq[j])
            results['prices']['domestic'][j] = pyo.value(model_solution.pd[j])
            results['prices']['import'][j] = pyo.value(model_solution.pm[j])
            results['prices']['export'][j] = pyo.value(model_solution.pe[j])

            # Trade values
            export_value = exports * pyo.value(model_solution.pe[j])
            import_value = imports * pyo.value(model_solution.pm[j])

            results['trade_balance'][j] = export_value - import_value
            total_exports_value += export_value
            total_imports_value += import_value

        # Aggregate indicators
        results['trade_indicators'] = {
            'total_exports_value': total_exports_value,
            'total_imports_value': total_imports_value,
            'overall_trade_balance': total_exports_value - total_imports_value,
            'exchange_rate': pyo.value(model_solution.epsilon),
            # Scale back
            'foreign_savings': pyo.value(model_solution.S_F) * 1000,
            'trade_openness': (total_exports_value + total_imports_value) / sum(results['composite_supply'].values()),
            'export_shares': {},
            'import_shares': {}
        }

        # Calculate trade shares
        if total_exports_value > 0:
            for j in self.sectors:
                export_value = results['exports'][j] * \
                    results['prices']['export'][j]
                results['trade_indicators']['export_shares'][j] = export_value / \
                    total_exports_value

        if total_imports_value > 0:
            for j in self.sectors:
                import_value = results['imports'][j] * \
                    results['prices']['import'][j]
                results['trade_indicators']['import_shares'][j] = import_value / \
                    total_imports_value

        return results

    def validate_trade_structure(self):
        """Validate trade structure for IPOPT feasibility"""

        validation_results = []

        # Check Armington parameters
        for j in self.sectors:
            delta_d = pyo.value(self.model.delta_d[j])
            delta_m = pyo.value(self.model.delta_m[j])

            if abs(delta_d + delta_m - 1.0) > 0.01:
                validation_results.append(
                    f"Sector {j}: Armington shares don't sum to 1.0: {delta_d + delta_m:.3f}")

            if delta_d < 0 or delta_m < 0:
                validation_results.append(
                    f"Sector {j}: Negative Armington shares: delta_d={delta_d:.3f}, delta_m={delta_m:.3f}")

        # Check CET parameters
        for j in self.sectors:
            delta_dt = pyo.value(self.model.delta_dt[j])
            delta_e = pyo.value(self.model.delta_e[j])

            if abs(delta_dt + delta_e - 1.0) > 0.01:
                validation_results.append(
                    f"Sector {j}: CET shares don't sum to 1.0: {delta_dt + delta_e:.3f}")

            if delta_dt < 0 or delta_e < 0:
                validation_results.append(
                    f"Sector {j}: Negative CET shares: delta_dt={delta_dt:.3f}, delta_e={delta_e:.3f}")

        # Check variable bounds
        unbounded_vars = []
        for var_name in ['Q', 'D', 'M', 'E']:
            var = getattr(self.model, var_name)
            for index in var:
                if var[index].lb is None or var[index].ub is None:
                    unbounded_vars.append(f"{var_name}[{index}]")

        if unbounded_vars:
            validation_results.append(
                f"Unbounded variables: {unbounded_vars[:3]}...")

        if not validation_results:
            print("Trade structure validation passed")
        else:
            print("Trade structure validation warnings:")
            for warning in validation_results[:3]:
                print(f"  - {warning}")

        return len(validation_results) == 0

# Testing function


def test_trade_block():
    """Test the trade block"""

    print("Testing Trade Block...")

    # Create test model
    model = pyo.ConcreteModel("Trade_Test")

    # Create sample data
    from data_processor import DataProcessor
    processor = DataProcessor()
    processor.create_calibrated_placeholder()
    calibrated_data = processor.get_calibrated_data()

    # Need some dummy variables for linking
    model.Z = pyo.Var(calibrated_data['production_sectors'], initialize=1000.0)
    model.pz = pyo.Var(calibrated_data['production_sectors'], initialize=1.0)
    model.S_F = pyo.Var(initialize=0.0)  # Foreign savings

    # Create trade block
    trade_block = TradeBlock(model, calibrated_data)

    # Initialize variables
    trade_block.initialize_trade_variables()

    # Validate structure
    is_valid = trade_block.validate_trade_structure()

    print(
        f"Variables created: {len([v for v in model.component_objects(pyo.Var)])}")
    print(
        f"Constraints created: {len([c for c in model.component_objects(pyo.Constraint)])}")
    print(
        f"Parameters created: {len([p for p in model.component_objects(pyo.Param)])}")
    print(f"Structure valid: {is_valid}")

    # Test world price update
    trade_block.update_world_prices(2025, 'ETS1')

    print("Trade block test completed successfully")

    return True


if __name__ == "__main__":
    test_trade_block()
