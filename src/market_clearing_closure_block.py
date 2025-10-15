"""
Market Clearing and Closure Block for Italian CGE Model
IPOPT-optimized equilibrium conditions and closure rules
ThreeME-style recursive dynamic closure
"""

import pyomo.environ as pyo
from definitions import model_definitions


class MarketClearingClosureBlock:
    """
    Market clearing and closure block implementing:
    - Factor market clearing (labor and capital)
    - Goods market clearing (Walras' law)
    - Savings-investment balance
    - Government budget constraint
    - Current account balance
    - Recursive dynamic closure rules
    """

    def __init__(self, model, calibrated_data):
        self.model = model
        self.calibrated_data = calibrated_data
        self.sectors = calibrated_data['production_sectors']
        self.factors = calibrated_data['factors']
        self.household_regions = list(calibrated_data['households'].keys())
        self.params = calibrated_data['calibrated_parameters']

        self.add_closure_variables()
        self.add_market_clearing_constraints()
        self.add_macroeconomic_closure()

    def add_closure_variables(self):
        """Add variables needed for market clearing and closure"""

        # Factor supplies (endogenous or fixed depending on closure)
        def factor_supply_bounds(model, f):
            total_demand = sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get(f, 300)
                               # Scale to thousands
                               for j in self.sectors) / 1000
            # More flexible bounds to accommodate capital stock growth
            if f == 'Capital':
                # Very flexible bounds for capital stock to handle multi-year growth (2021-2050)
                # Base 2021 capital ~118, by 2050 could be ~2000+ with accumulation
                return (total_demand * 0.1, total_demand * 20.0)
            else:
                # Tighter bounds for other factors like labor
                return (total_demand * 0.8, total_demand * 1.5)

        self.model.FS = pyo.Var(
            self.factors,
            domain=pyo.NonNegativeReals,
            bounds=factor_supply_bounds,
            initialize=lambda m, f: sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get(f, 300)
                                        for j in self.sectors) / 1000,
            doc="Total factor supply (scaled)"
        )

        # Unemployment rate (for labor market flexibility)
        self.model.unemployment_rate = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.05, 0.20),  # 5-20% unemployment - tighter bounds
            initialize=0.08,      # 8% initial unemployment
            doc="Unemployment rate"
        )

        # Capital utilization rate
        self.model.capital_utilization = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.7, 1.1),    # 70-110% utilization - tighter bounds
            initialize=0.85,      # 85% initial utilization
            doc="Capital utilization rate"
        )

        # Macro closure variables with better scaling
        self.model.savings_investment_gap = pyo.Var(
            domain=pyo.Reals,
            bounds=(-5000, 5000),  # Tighter bounds
            initialize=0.0,
            doc="Savings-investment gap (scaled)"
        )

        self.model.government_balance = pyo.Var(
            domain=pyo.Reals,
            bounds=(-20000, 10000),  # Tighter bounds, allowing deficits
            initialize=-2000.0,      # Start with small deficit
            doc="Government budget balance (scaled)"
        )

        # Trade balance with proper bounds
        self.model.trade_balance = pyo.Var(
            domain=pyo.Reals,
            bounds=(-8000, 8000),   # ±8 billion trade balance
            initialize=0.0,
            doc="Trade balance (exports - imports, scaled)"
        )

        # Price level (for nominal anchor)
        self.model.price_level = pyo.Var(
            domain=pyo.PositiveReals,
            bounds=(0.5, 2.0),
            initialize=1.0,
            doc="General price level"
        )

    def add_market_clearing_constraints(self):
        """Market clearing constraints"""

        # Factor market clearing
        def labor_market_clearing_rule(model):
            """Labor supply = Labor demand * (1 + unemployment rate)"""
            total_labor_demand = sum(model.F['Labour', j]
                                     for j in self.sectors)
            return model.FS['Labour'] == total_labor_demand * (1 + model.unemployment_rate)

        self.model.eq_labor_market_clearing = pyo.Constraint(
            rule=labor_market_clearing_rule,
            doc="Labor market clearing with unemployment"
        )

        def capital_market_clearing_rule(model):
            """Capital supply = Capital demand / utilization rate"""
            total_capital_demand = sum(
                model.F['Capital', j] for j in self.sectors)
            return model.FS['Capital'] * model.capital_utilization == total_capital_demand

        self.model.eq_capital_market_clearing = pyo.Constraint(
            rule=capital_market_clearing_rule,
            doc="Capital market clearing with utilization"
        )

        # Goods market clearing (Walras' Law)
        def goods_market_clearing_rule(model, i):
            """Supply = Demand for each good"""
            # Supply
            supply = model.Q[i]

            # Demand components
            household_demand = sum(model.C[h, i]
                                   for h in self.household_regions)
            government_demand = model.G[i]
            investment_demand = model.I[i]
            intermediate_demand = sum(model.X[i, j] for j in self.sectors)

            total_demand = (household_demand + government_demand +
                            investment_demand + intermediate_demand)

            return supply == total_demand

        self.model.eq_goods_market_clearing = pyo.Constraint(
            self.sectors,
            rule=goods_market_clearing_rule,
            doc="Goods market clearing"
        )

    def add_macroeconomic_closure(self):
        """Macroeconomic closure constraints"""

        # Remove any existing closure constraints to avoid conflicts
        existing_constraints = ['eq_savings_investment_balance', 'eq_government_balance',
                                'eq_price_level', 'eq_trade_balance']
        for const_name in existing_constraints:
            if hasattr(self.model, const_name):
                self.model.del_component(const_name)

        # Savings-investment balance
        def savings_investment_balance_rule(model):
            """Private savings + Government savings + Foreign savings = Investment"""
            private_savings = sum(model.S_H[h] for h in self.household_regions)
            government_savings = model.S_G
            foreign_savings = model.S_F
            total_investment = model.I_T

            total_savings = private_savings + government_savings + foreign_savings

            return model.savings_investment_gap == total_savings - total_investment

        self.model.eq_savings_investment_balance = pyo.Constraint(
            rule=savings_investment_balance_rule,
            doc="Savings-investment balance"
        )

        # Government budget balance
        def government_balance_rule(model):
            """Government revenue - Government expenditure = Government balance"""
            return model.government_balance == model.Y_G - (model.C_G + model.S_G)

        self.model.eq_government_balance = pyo.Constraint(
            rule=government_balance_rule,
            doc="Government budget balance"
        )

        # Price level definition (CPI-based)
        def price_level_rule(model):
            """Price level as weighted average of consumer prices"""
            # Use household consumption weights
            total_weight = 0
            weighted_prices = 0

            for h in self.household_regions:
                hh_data = self.params['households'].get(h, {})
                consumption_pattern = hh_data.get('consumption_pattern', {})
                total_consumption = sum(consumption_pattern.values())

                if total_consumption > 0:
                    for j in self.sectors:
                        weight = consumption_pattern.get(
                            j, 0) / total_consumption
                        weighted_prices += weight * model.pq[j]
                        total_weight += weight

            if total_weight > 0:
                return model.price_level == weighted_prices / total_weight
            else:
                return model.price_level == 1.0

        self.model.eq_price_level = pyo.Constraint(
            rule=price_level_rule,
            doc="Price level definition"
        )

        # Trade balance constraint
        def trade_balance_rule(model):
            """Trade balance: exports - imports = trade balance"""
            total_exports = sum(model.pWe[j] * model.E[j]
                                for j in self.sectors) / 1000  # Scale
            total_imports = sum(model.pWm[j] * model.M[j]
                                for j in self.sectors) / 1000  # Scale
            return model.trade_balance == (total_exports - total_imports)

        self.model.eq_trade_balance = pyo.Constraint(
            rule=trade_balance_rule,
            doc="Trade balance definition"
        )

    def apply_closure_rule(self, closure_type='recursive_dynamic', year=None):
        """Apply specific closure rule for the model with numerical stability"""

        print(f"Applying closure rule: {closure_type}")

        if closure_type == 'recursive_dynamic':
            """
            Numerically stable recursive dynamic closure:
            - Labor supply adjusts (with unemployment)
            - Capital stock predetermined 
            - Government balance adjusts
            - Trade balance adjusts
            - Exchange rate is numeraire
            """

            # Labor market: employment adjusts with unemployment
            self.model.unemployment_rate.setlb(0.06)  # Minimum 6% unemployment
            self.model.unemployment_rate.setub(
                0.15)  # Maximum 15% unemployment

            # Capital market: capital stock is predetermined
            if year and year > model_definitions.base_year:
                # Future years: capital stock fixed from previous period
                capital_stock = self.calculate_capital_stock(year)
                # Update bounds to accommodate the new capital stock value
                self.model.FS['Capital'].setlb(capital_stock * 0.5)
                self.model.FS['Capital'].setub(capital_stock * 1.5)
                self.model.FS['Capital'].fix(capital_stock)
                print(
                    f"Fixed capital stock for year {year}: {capital_stock:.2f}")
            else:
                # Base year: calibrated capital stock
                base_capital = sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get('Capital', 300)
                                   for j in self.sectors) / 1000
                self.model.FS['Capital'].fix(base_capital)
                print(f"Fixed base year capital stock: {base_capital:.2f}")

            # Government closure: balance adjusts (spending largely fixed)
            self.model.government_balance.unfix()
            if hasattr(self.model, 'C_G'):
                self.model.C_G.setub(
                    self.model.C_G.value * 1.1 if self.model.C_G.value else 1000)
                self.model.C_G.setlb(
                    self.model.C_G.value * 0.9 if self.model.C_G.value else 500)

            # Investment adjusts to savings
            self.model.savings_investment_gap.fix(0.0)  # Force balance

            # Trade closure: balance adjusts (competitive small open economy)
            self.model.trade_balance.unfix()

            # Exchange rate is numeraire
            if hasattr(self.model, 'epsilon'):
                self.model.epsilon.fix(1.0)

            # Price level adjusts
            if hasattr(self.model, 'price_level'):
                self.model.price_level.unfix()

        elif closure_type == 'balanced_closure':
            """
            Balanced closure for base year calibration:
            - All key balances maintained
            - Limited adjustment flexibility
            """

            # Fixed unemployment at natural rate
            self.model.unemployment_rate.fix(0.08)

            # Fixed trade balance
            self.model.trade_balance.fix(0.0)

            # Fixed government balance (small deficit)
            self.model.government_balance.fix(-1000.0)  # 1 billion deficit

            # Fixed investment-savings gap
            self.model.savings_investment_gap.fix(0.0)

            # Exchange rate numeraire
            if hasattr(self.model, 'epsilon'):
                self.model.epsilon.fix(1.0)

            print("Applied balanced closure for calibration")

        print(f"✓ Closure rule applied: {closure_type}")

    def calculate_capital_stock(self, year):
        """Calculate capital stock for recursive dynamics"""

        from definitions import model_definitions

        base_year = model_definitions.base_year
        years_elapsed = year - base_year

        if years_elapsed <= 0:
            # Base year capital stock
            return sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get('Capital', 300)
                       for j in self.sectors) / 1000

        # Recursive capital accumulation: K(t) = K(t-1) * (1 - depreciation) + I(t-1)
        base_capital = sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get('Capital', 300)
                           for j in self.sectors) / 1000

        # Simplified capital accumulation (would normally track year-by-year)
        depreciation_rate = 0.05  # 5% annual depreciation
        investment_rate = 0.20    # 20% of base capital as annual investment

        # Simple approximation: K(t) = K(0) * (1 - δ + investment_rate)^t
        growth_factor = (1 - depreciation_rate +
                         investment_rate) ** years_elapsed
        return base_capital * growth_factor

    def validate_equilibrium(self, model):
        """Validate that the model solution represents a valid equilibrium"""

        print("Validating equilibrium conditions...")

        validation_passed = True
        tolerance = 1e-3  # Tolerance for equilibrium checks

        try:
            # Check factor market clearing
            if hasattr(model, 'FS') and hasattr(model, 'F'):
                for f in self.factors:
                    if hasattr(model.FS, '__getitem__') and hasattr(model.F, '__getitem__'):
                        total_supply = pyo.value(model.FS[f])
                        total_demand = sum(pyo.value(model.F[f, j]) for j in self.sectors
                                           if (f, j) in model.F)

                        if abs(total_supply - total_demand) > tolerance * total_supply:
                            print(
                                f"  ⚠ Factor {f} market imbalance: Supply={total_supply:.3f}, Demand={total_demand:.3f}")
                            validation_passed = False
                        else:
                            print(f"  ✓ Factor {f} market clears")

            # Check goods market clearing (Walras' Law)
            goods_balance_error = 0.0
            if hasattr(model, 'Q') and hasattr(model, 'C_H'):
                for j in self.sectors:
                    if hasattr(model.Q, '__getitem__'):
                        supply = pyo.value(model.Q[j])

                        # Calculate total demand (household + government + investment + intermediate)
                        hh_demand = 0.0
                        if hasattr(model.C_H, '__getitem__'):
                            for h in self.household_regions:
                                if (h, j) in model.C_H:
                                    hh_demand += pyo.value(model.C_H[h, j])

                        # Simple balance check (would include all demand components)
                        balance = abs(supply - hh_demand)
                        goods_balance_error += balance

                        if balance > tolerance * supply:
                            print(
                                f"  ⚠ Good {j} market imbalance: {balance:.3f}")

            if goods_balance_error < tolerance * 100:  # Scaled tolerance
                print("  ✓ Goods markets approximately clear")
            else:
                print(
                    f"  ⚠ Goods market total imbalance: {goods_balance_error:.3f}")
                validation_passed = False

            # Check savings-investment balance
            if hasattr(model, 'savings_investment_gap'):
                gap = pyo.value(model.savings_investment_gap)
                if abs(gap) > tolerance * 1000:  # Scaled tolerance
                    print(f"  ⚠ Savings-investment gap: {gap:.3f}")
                    validation_passed = False
                else:
                    print("  ✓ Savings-investment balance")

            # Check price positivity
            price_vars = ['pz', 'pd', 'pe', 'pm', 'pq']
            for price_var in price_vars:
                if hasattr(model, price_var):
                    var = getattr(model, price_var)
                    if hasattr(var, '__iter__'):
                        for j in self.sectors:
                            if hasattr(var, '__getitem__') and j in var:
                                price_val = pyo.value(var[j])
                                if price_val <= 0:
                                    print(
                                        f"  ⚠ Non-positive price: {price_var}[{j}] = {price_val}")
                                    validation_passed = False

            if validation_passed:
                print("✓ Equilibrium validation passed")
            else:
                print("⚠ Equilibrium validation found issues")

        except Exception as e:
            print(f"  ✗ Equilibrium validation error: {e}")
            validation_passed = False

        return validation_passed

    def initialize_closure_variables(self):
        """Initialize closure variables with reasonable values"""

        print("Initializing closure variables...")

        # Initialize factor supplies
        if hasattr(self.model, 'FS'):
            for f in self.factors:
                if hasattr(self.model.FS, '__getitem__'):
                    # Base on calibrated factor payments
                    base_supply = sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get(f, 300)
                                      for j in self.sectors) / 1000
                    self.model.FS[f].set_value(base_supply)

        # Initialize macro variables
        if hasattr(self.model, 'unemployment_rate'):
            self.model.unemployment_rate.set_value(0.08)  # 8% unemployment

        if hasattr(self.model, 'capital_utilization'):
            self.model.capital_utilization.set_value(0.85)  # 85% utilization

        if hasattr(self.model, 'savings_investment_gap'):
            self.model.savings_investment_gap.set_value(0.0)  # Initial balance

        if hasattr(self.model, 'government_balance'):
            self.model.government_balance.set_value(-1000.0)  # Small deficit

        if hasattr(self.model, 'trade_balance'):
            self.model.trade_balance.set_value(0.0)  # Balanced trade initially

        if hasattr(self.model, 'price_level'):
            self.model.price_level.set_value(1.0)  # Base price level

        print("✓ Closure variables initialized")

    def update_factor_supplies(self, year):
        """Update factor supplies for recursive dynamics"""

        from definitions import model_definitions

        base_year = model_definitions.base_year
        years_elapsed = year - base_year

        if years_elapsed <= 0:
            return  # No update needed for base year

        # Labor supply growth (population + participation rate changes)
        labor_growth_rate = 0.002  # 0.2% annual growth

        # Update labor supply
        if hasattr(self.model, 'FS') and 'Labour' in self.factors:
            base_labor = sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get('Labour', 300)
                             for j in self.sectors) / 1000
            new_labor_supply = base_labor * \
                (1 + labor_growth_rate) ** years_elapsed
            if hasattr(self.model.FS, '__getitem__'):
                self.model.FS['Labour'].set_value(new_labor_supply)

        # Capital supply handled separately in calculate_capital_stock method

        print(f"Updated factor supplies for year {year}")

        # Labor force growth
        labor_growth = model_definitions.macro_params['labor_force_growth_rate']
        base_labor = sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get('Labour', 600)
                         for j in self.sectors) / 1000

        new_labor_supply = base_labor * (1 + labor_growth) ** years_elapsed

        # Don't fix here if using recursive dynamic closure
        # (will be determined endogenously through unemployment)
        if not self.model.FS['Labour'].is_fixed():
            self.model.FS['Labour'].set_value(new_labor_supply)

        print(f"Updated factor supplies for year {year}")
        print(f"  Labor supply growth: {labor_growth:.1%} annually")
        print(f"  Capital stock: {self.calculate_capital_stock(year):.1f}")

    def initialize_closure_variables(self):
        """Initialize closure variables"""

        print("Initializing market clearing variables...")

        # Initialize factor supplies
        for f in self.factors:
            total_supply = sum(self.params['sectors'].get(j, {}).get('factor_payments', {}).get(f, 300)
                               for j in self.sectors) / 1000
            self.model.FS[f].set_value(total_supply)
            print(f"  {f} supply: {total_supply:.1f}")

        # Initialize unemployment and utilization
        self.model.unemployment_rate.set_value(0.08)  # 8% initial unemployment
        self.model.capital_utilization.set_value(0.85)  # 85% utilization

        # Initialize macro variables
        self.model.savings_investment_gap.set_value(0.0)
        self.model.government_balance.set_value(0.0)
        self.model.price_level.set_value(1.0)

        print("Market clearing variables initialized")

    def get_closure_results(self, model_solution):
        """Extract closure and equilibrium results"""

        results = {
            'factor_markets': {},
            'goods_markets': {},
            'macro_balances': {},
            'equilibrium_indicators': {}
        }

        # Factor market results
        for f in self.factors:
            results['factor_markets'][f] = {
                'supply': pyo.value(model_solution.FS[f]) * 1000,  # Scale back
                'total_demand': sum(pyo.value(model_solution.F[f, j]) for j in self.sectors) * 1000,
                'price': pyo.value(model_solution.pf[f])
            }

        results['factor_markets']['unemployment_rate'] = pyo.value(
            model_solution.unemployment_rate)
        results['factor_markets']['capital_utilization'] = pyo.value(
            model_solution.capital_utilization)

        # Macro balances
        results['macro_balances']['savings_investment_gap'] = pyo.value(
            model_solution.savings_investment_gap) * 1000
        results['macro_balances']['government_balance'] = pyo.value(
            model_solution.government_balance) * 1000
        results['macro_balances']['price_level'] = pyo.value(
            model_solution.price_level)

        # Goods market pressures (should be zero in equilibrium)
        goods_market_balance = {}
        for i in self.sectors:
            supply = pyo.value(model_solution.Q[i])

            household_demand = sum(
                pyo.value(model_solution.C[h, i]) for h in self.household_regions)
            government_demand = pyo.value(model_solution.G[i])
            investment_demand = pyo.value(model_solution.I[i])
            intermediate_demand = sum(
                pyo.value(model_solution.X[i, j]) for j in self.sectors)

            total_demand = household_demand + government_demand + \
                investment_demand + intermediate_demand
            goods_market_balance[i] = abs(supply - total_demand)

        results['goods_markets'] = goods_market_balance

        # Equilibrium indicators
        max_goods_imbalance = max(
            goods_market_balance.values()) if goods_market_balance else 0

        results['equilibrium_indicators'] = {
            'max_goods_imbalance': max_goods_imbalance,
            'walras_law_satisfied': max_goods_imbalance < 1e-6,
            'macro_consistent': abs(results['macro_balances']['savings_investment_gap']) < 1e-3,
            'employment_rate': 1 - results['factor_markets']['unemployment_rate']
        }

        return results

    def validate_equilibrium(self, model_solution):
        """Validate model equilibrium conditions"""

        validation_results = []
        tolerance = 1e-6

        # Check factor market clearing
        for f in self.factors:
            supply = pyo.value(model_solution.FS[f])
            if f == 'Labour':
                # Account for unemployment
                effective_supply = supply / \
                    (1 + pyo.value(model_solution.unemployment_rate))
            elif f == 'Capital':
                # Account for utilization
                effective_supply = supply * \
                    pyo.value(model_solution.capital_utilization)
            else:
                effective_supply = supply

            demand = sum(
                pyo.value(model_solution.F[f, j]) for j in self.sectors)
            imbalance = abs(effective_supply - demand) / max(demand, 1e-10)

            if imbalance > tolerance:
                validation_results.append(
                    f"Factor market {f} imbalance: {imbalance:.2e}")

        # Check goods market clearing
        max_goods_imbalance = 0
        for i in self.sectors:
            supply = pyo.value(model_solution.Q[i])

            household_demand = sum(
                pyo.value(model_solution.C[h, i]) for h in self.household_regions)
            government_demand = pyo.value(model_solution.G[i])
            investment_demand = pyo.value(model_solution.I[i])
            intermediate_demand = sum(
                pyo.value(model_solution.X[i, j]) for j in self.sectors)

            total_demand = household_demand + government_demand + \
                investment_demand + intermediate_demand
            imbalance = abs(supply - total_demand) / max(total_demand, 1e-10)

            max_goods_imbalance = max(max_goods_imbalance, imbalance)

        if max_goods_imbalance > tolerance:
            validation_results.append(
                f"Max goods market imbalance: {max_goods_imbalance:.2e}")

        # Check savings-investment balance
        si_gap = abs(pyo.value(model_solution.savings_investment_gap))
        if si_gap > tolerance:
            validation_results.append(f"Savings-investment gap: {si_gap:.2e}")

        if not validation_results:
            print("Equilibrium validation passed")
            return True
        else:
            print("Equilibrium validation warnings:")
            for warning in validation_results[:3]:
                print(f"  - {warning}")
            return False

# Testing function


def test_market_clearing_block():
    """Test the market clearing and closure block"""

    print("Testing Market Clearing and Closure Block...")

    # Create test model
    model = pyo.ConcreteModel("MarketClearing_Test")

    # Create sample data
    from data_processor import DataProcessor
    processor = DataProcessor()
    processor.create_calibrated_placeholder()
    calibrated_data = processor.get_calibrated_data()

    # Need dummy variables from other blocks
    sectors = calibrated_data['production_sectors']
    households = list(calibrated_data['households'].keys())
    factors = calibrated_data['factors']

    model.F = pyo.Var(factors, sectors, initialize=500.0)
    model.pf = pyo.Var(factors, initialize=1.0)
    model.Q = pyo.Var(sectors, initialize=1000.0)
    model.C = pyo.Var(households, sectors, initialize=100.0)
    model.G = pyo.Var(sectors, initialize=50.0)
    model.I = pyo.Var(sectors, initialize=200.0)
    model.X = pyo.Var(sectors, sectors, initialize=50.0)
    model.S_H = pyo.Var(households, initialize=5000.0)
    model.S_G = pyo.Var(initialize=10000.0)
    model.S_F = pyo.Var(initialize=-5000.0)
    model.I_T = pyo.Var(initialize=200000.0)
    model.Y_G = pyo.Var(initialize=150000.0)
    model.C_G = pyo.Var(initialize=120000.0)
    model.pq = pyo.Var(sectors, initialize=1.0)
    model.epsilon = pyo.Var(initialize=1.0)

    # Create market clearing block
    mc_block = MarketClearingClosureBlock(model, calibrated_data)

    # Initialize variables
    mc_block.initialize_closure_variables()

    # Test different closure rules
    mc_block.apply_closure_rule('recursive_dynamic', 2025)

    print(
        f"Variables created: {len([v for v in model.component_objects(pyo.Var)])}")
    print(
        f"Constraints created: {len([c for c in model.component_objects(pyo.Constraint)])}")

    # Test factor supply update
    mc_block.update_factor_supplies(2030)

    print("Market clearing and closure block test completed successfully")

    return True


if __name__ == "__main__":
    test_market_clearing_block()
