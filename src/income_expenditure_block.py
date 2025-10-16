"""
Income and Expenditure Block for Italian CGE Model
IPOPT-optimized household behavior and government accounts
LES demand system with proper bounds for 5 Italian macro-regions
"""

import pyomo.environ as pyo
import numpy as np
from definitions import model_definitions


class IncomeExpenditureBlock:
    """
    Income and expenditure block covering:
    - Household utility and consumption (LES demand system)
    - Regional household behavior (NW, NE, Center, South, Islands)
    - Government revenues and expenditures
    - Savings and investment equilibrium
    - Income distribution across Italian regions
    """

    def __init__(self, model, calibrated_data):
        self.model = model
        self.calibrated_data = calibrated_data
        self.sectors = calibrated_data['production_sectors']
        self.factors = calibrated_data['factors']
        self.household_regions = list(calibrated_data['households'].keys())
        self.params = calibrated_data['calibrated_parameters']

        # Scaling factors for IPOPT
        self.income_scale = 1000.0  # Scale income to thousands
        self.consumption_scale = 1000.0

        self.add_income_expenditure_variables()
        self.add_income_expenditure_parameters()
        self.add_income_expenditure_constraints()

    def add_income_expenditure_variables(self):
        """Add variables for household and government behavior"""

        # Household income variables (scaled)
        def income_bounds(model, h):
            hh_data = self.params['households'].get(h, {})
            base_income = hh_data.get('income', 50000) / self.income_scale
            # 50% to 300% of base
            return (base_income * 0.5, base_income * 3.0)

        self.model.Y_H = pyo.Var(
            self.household_regions,
            domain=pyo.NonNegativeReals,
            bounds=income_bounds,
            initialize=lambda m, h: self.params['households'].get(
                h, {}).get('income', 50000) / self.income_scale,
            doc="Household disposable income (scaled)"
        )

        # Total household consumption expenditure
        def consumption_bounds(model, h):
            hh_data = self.params['households'].get(h, {})
            base_consumption = hh_data.get(
                'consumption', 40000) / self.consumption_scale
            return (base_consumption * 0.3, base_consumption * 3.0)

        self.model.C_H = pyo.Var(
            self.household_regions,
            domain=pyo.NonNegativeReals,
            bounds=consumption_bounds,
            initialize=lambda m, h: self.params['households'].get(
                h, {}).get('consumption', 40000) / self.consumption_scale,
            doc="Total household consumption expenditure (scaled)"
        )

        # Household savings
        def savings_bounds(model, h):
            hh_data = self.params['households'].get(h, {})
            base_savings = max(hh_data.get(
                'income', 50000) - hh_data.get('consumption', 40000), 1000) / self.income_scale
            return (0.0, base_savings * 5.0)

        self.model.S_H = pyo.Var(
            self.household_regions,
            domain=pyo.NonNegativeReals,
            bounds=savings_bounds,
            initialize=lambda m, h: max(self.params['households'].get(h, {}).get('income', 50000) -
                                        self.params['households'].get(h, {}).get('consumption', 40000), 1000) / self.income_scale,
            doc="Household savings (scaled)"
        )

        # Sectoral consumption by household (LES demand)
        def sectoral_consumption_bounds(model, h, j):
            hh_data = self.params['households'].get(h, {})
            consumption_pattern = hh_data.get('consumption_pattern', {})
            base_consumption = consumption_pattern.get(
                j, 1000) / self.consumption_scale
            # Ensure minimum consumption is not too small
            min_consumption = max(base_consumption * 0.1, 0.001)
            max_consumption = base_consumption * 5.0
            return (min_consumption, max_consumption)

        self.model.C = pyo.Var(
            self.household_regions, self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=sectoral_consumption_bounds,
            initialize=lambda m, h, j: max(self.params['households'].get(h, {}).get(
                'consumption_pattern', {}).get(j, 1000) / self.consumption_scale, 0.001),
            doc="Sectoral consumption by household (scaled)"
        )

        # Government variables
        def gov_income_bounds():
            gov_data = self.params.get('government', {})
            base_revenue = gov_data.get('revenue', 100000) / self.income_scale
            return (base_revenue * 0.5, base_revenue * 2.0)

        self.model.Y_G = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=gov_income_bounds(),
            initialize=self.params.get('government', {}).get(
                'revenue', 100000) / self.income_scale,
            doc="Total government revenue (scaled)"
        )

        self.model.C_G = pyo.Var(
            domain=pyo.NonNegativeReals,
            # Gov can run deficits
            bounds=lambda m: (0.0, pyo.value(m.Y_G) * 1.5),
            initialize=self.params.get('government', {}).get(
                'revenue', 100000) * 0.8 / self.consumption_scale,
            doc="Total government consumption (scaled)"
        )

        self.model.S_G = pyo.Var(
            domain=pyo.Reals,  # Can be negative (deficit)
            bounds=lambda m: (-pyo.value(m.Y_G), pyo.value(m.Y_G)),
            initialize=self.params.get('government', {}).get(
                'deficit', 0) / self.income_scale,
            doc="Government savings/deficit (scaled)"
        )

        # Government consumption by sector
        def gov_sectoral_bounds(model, j):
            gov_data = self.params.get('government', {})
            consumption_pattern = gov_data.get('consumption', {})
            base_consumption = consumption_pattern.get(
                j, 5000) / self.consumption_scale
            # Ensure minimum consumption is not too small
            min_consumption = max(base_consumption * 0.01, 0.001)
            return (min_consumption, base_consumption * 5.0)

        self.model.G = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=gov_sectoral_bounds,
            initialize=lambda m, j: max(self.params.get('government', {}).get(
                'consumption', {}).get(j, 5000) / self.consumption_scale, 0.001),
            doc="Government consumption by sector (scaled)"
        )

        # Investment variables
        def investment_bounds():
            inv_data = self.params.get('investment', {})
            base_investment = inv_data.get(
                'total_investment', 200000) / self.income_scale
            return (base_investment * 0.3, base_investment * 3.0)

        self.model.I_T = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=investment_bounds(),
            initialize=self.params.get('investment', {}).get(
                'total_investment', 200000) / self.income_scale,
            doc="Total investment (scaled)"
        )

        self.model.S_F = pyo.Var(
            domain=pyo.Reals,  # Foreign savings can be negative
            bounds=(-investment_bounds()[1], investment_bounds()[1]),
            initialize=self.params.get('trade', {}).get(
                'overall_trade_balance', 0) / self.income_scale,
            doc="Foreign savings (trade deficit, scaled)"
        )

        # Investment by sector of origin
        def sectoral_investment_bounds(model, j):
            inv_data = self.params.get('investment', {})
            sectoral_investment = inv_data.get('sectoral_investment', {})
            base_investment = sectoral_investment.get(
                j, 10000) / self.income_scale
            # Ensure minimum investment is not too small
            min_investment = max(base_investment * 0.01, 0.001)
            return (min_investment, base_investment * 5.0)

        self.model.I = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=sectoral_investment_bounds,
            initialize=lambda m, j: max(self.params.get('investment', {}).get(
                'sectoral_investment', {}).get(j, 10000) / self.income_scale, 0.001),
            doc="Investment by sector of origin (scaled)"
        )

        # Tax variables
        self.model.Tz = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=(0.0, None),
            initialize=1.0,
            doc="Indirect tax revenue by sector"
        )

        self.model.Tm = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=(0.0, None),
            initialize=0.5,
            doc="Tariff revenue by sector"
        )

        self.model.Td = pyo.Var(
            self.household_regions,
            domain=pyo.NonNegativeReals,
            bounds=(0.0, None),
            initialize=5.0,
            doc="Direct tax revenue by household"
        )

        # Composite prices (consumer prices)
        def price_bounds(model, j):
            # More conservative price bounds to avoid numerical issues
            return (0.5, 5.0)

        self.model.pq = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=price_bounds,
            initialize=1.0,
            doc="Composite prices (consumer prices)"
        )

        # Import prices
        self.model.pm = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=price_bounds,
            initialize=1.0,
            doc="Import prices"
        )

        # Import quantities
        def import_bounds(model, j):
            sector_data = self.params['sectors'].get(j, {})
            base_imports = sector_data.get(
                'imports', 100) / self.consumption_scale
            return (0.0, base_imports * 10.0)

        self.model.M = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=import_bounds,
            initialize=lambda m, j: self.params['sectors'].get(
                j, {}).get('imports', 100) / self.consumption_scale,
            doc="Import quantities by sector"
        )

        # Export prices
        self.model.pe = pyo.Var(
            self.sectors,
            domain=pyo.PositiveReals,
            bounds=lambda m, j: (0.5, 5.0),  # Same conservative bounds
            initialize=1.0,
            doc="Export prices"
        )

        # Export quantities
        def export_bounds(model, j):
            sector_data = self.params['sectors'].get(j, {})
            base_exports = sector_data.get(
                'exports', 50) / self.consumption_scale
            return (0.0, base_exports * 10.0)

        self.model.E = pyo.Var(
            self.sectors,
            domain=pyo.NonNegativeReals,
            bounds=export_bounds,
            initialize=lambda m, j: self.params['sectors'].get(
                j, {}).get('exports', 50) / self.consumption_scale,
            doc="Export quantities by sector"
        )

    def add_income_expenditure_parameters(self):
        """Add LES demand parameters and other behavioral parameters"""

        # LES utility function parameters - marginal budget shares
        def get_beta_les(model, h, j):
            hh_data = self.params['households'].get(h, {})
            budget_shares = hh_data.get('budget_shares', {})
            # Ensure budget shares sum to 1.0 for each household
            if budget_shares:
                return budget_shares.get(j, 0.0)
            else:
                # Equal shares if no specific data
                return 1.0 / len(self.sectors)

        self.model.beta_les = pyo.Param(
            self.household_regions, self.sectors,
            initialize=get_beta_les,
            mutable=True,
            doc="LES marginal budget shares"
        )

        # Add a validation constraint to ensure budget shares sum to 1
        def budget_share_sum_rule(model, h):
            """Sum of budget shares must equal 1 for each household"""
            return sum(model.beta_les[h, j] for j in self.sectors) == 1.0

        # Note: This will be added as a constraint later if needed

        # LES subsistence consumption (gamma) - simplified as zero for most goods
        def get_gamma_les(model, h, j):
            # Simplified: very small positive values to avoid numerical issues
            return 0.001  # Small positive value for all goods

        self.model.gamma_les = pyo.Param(
            self.household_regions, self.sectors,
            initialize=get_gamma_les,
            mutable=True,
            doc="LES subsistence consumption"
        )

        # Tax rates (as parameters, can be updated for policy scenarios)
        def get_direct_tax_rate(model, h):
            tax_data = self.params.get('tax_rates', {})
            direct_rates = tax_data.get('direct_tax_rate', {})
            # Map household regions to SAM names for tax rates
            hh_data = self.params['households'].get(h, {})
            sam_name = hh_data.get('sam_name', f'Households({h})')
            return direct_rates.get(sam_name, 0.15)  # 15% default

        self.model.td = pyo.Param(
            self.household_regions,
            initialize=get_direct_tax_rate,
            mutable=True,
            doc="Direct tax rates"
        )

        def get_indirect_tax_rate(model, j):
            tax_data = self.params.get('tax_rates', {})
            indirect_rates = tax_data.get('indirect_tax_rate', {})
            return indirect_rates.get(j, 0.10)  # 10% default

        self.model.tz = pyo.Param(
            self.sectors,
            initialize=get_indirect_tax_rate,
            mutable=True,
            doc="Indirect tax rates"
        )

        def get_tariff_rate(model, j):
            tax_data = self.params.get('tax_rates', {})
            tariff_rates = tax_data.get('tariff_rate', {})
            return tariff_rates.get(j, 0.05)  # 5% default

        self.model.tm = pyo.Param(
            self.sectors,
            initialize=get_tariff_rate,
            mutable=True,
            doc="Tariff rates"
        )

        # Savings rates (can be endogenous or fixed)
        def get_savings_rate(model, h):
            hh_data = self.params['households'].get(h, {})
            return hh_data.get('savings_rate', 0.15)  # 15% default

        self.model.mps = pyo.Param(
            self.household_regions,
            initialize=get_savings_rate,
            mutable=True,
            doc="Marginal propensity to save"
        )

        # Government consumption shares
        def get_gov_share(model, j):
            gov_data = self.params.get('government', {})
            consumption_shares = gov_data.get('consumption_shares', {})
            return consumption_shares.get(j, 1.0 / len(self.sectors))

        self.model.gov_share = pyo.Param(
            self.sectors,
            initialize=get_gov_share,
            mutable=True,
            doc="Government consumption shares"
        )

        # Investment shares
        def get_inv_share(model, j):
            inv_data = self.params.get('investment', {})
            investment_shares = inv_data.get('sectoral_investment_shares', {})
            return investment_shares.get(j, 1.0 / len(self.sectors))

        self.model.inv_share = pyo.Param(
            self.sectors,
            initialize=get_inv_share,
            mutable=True,
            doc="Investment shares by sector"
        )

    def add_income_expenditure_constraints(self):
        """Add constraints for income-expenditure equilibrium"""

        self.add_income_distribution_constraints()
        self.add_household_behavior_constraints()
        self.add_government_constraints()
        self.add_investment_constraints()
        self.add_macroeconomic_balances()

    def add_income_distribution_constraints(self):
        """Define how factor income is distributed to households"""

        # Household income from factor ownership
        def household_income_rule(model, h):
            """
            Y_H[h] = sum(factor_income[f] * ownership_share[h,f]) - taxes[h]
            """
            # Factor income before taxes
            gross_factor_income = 0
            for f in self.factors:
                total_factor_income = sum(
                    model.pf[f] * model.F[f, j] for j in self.sectors)
                factor_dist = self.params.get('factor_distribution', {})
                f_dist = factor_dist.get(f, {})
                # Equal distribution if not specified
                share = f_dist.get(h, 0.2)
                gross_factor_income += total_factor_income * share

            # Net income after taxes
            return model.Y_H[h] == gross_factor_income - model.Td[h]

        self.model.eq_household_income = pyo.Constraint(
            self.household_regions,
            rule=household_income_rule,
            doc="Household income from factor ownership"
        )

    def add_household_behavior_constraints(self):
        """Household consumption and savings behavior (LES demand system)"""

        # Household budget constraint
        def household_budget_rule(model, h):
            """Y_H = C_H + S_H"""
            return model.Y_H[h] == model.C_H[h] + model.S_H[h]

        self.model.eq_household_budget = pyo.Constraint(
            self.household_regions,
            rule=household_budget_rule,
            doc="Household budget constraint"
        )

        # Household savings function
        def household_savings_rule(model, h):
            """S_H = mps * Y_H (marginal propensity to save)"""
            return model.S_H[h] == model.mps[h] * model.Y_H[h]

        self.model.eq_household_savings = pyo.Constraint(
            self.household_regions,
            rule=household_savings_rule,
            doc="Household savings function"
        )

        # Total consumption expenditure identity
        def consumption_expenditure_rule(model, h):
            """C_H = sum(pq[j] * C[h,j])"""
            return model.C_H[h] == sum(model.pq[j] * model.C[h, j] for j in self.sectors)

        self.model.eq_consumption_expenditure = pyo.Constraint(
            self.household_regions,
            rule=consumption_expenditure_rule,
            doc="Consumption expenditure identity"
        )

        # LES demand system
        def les_demand_rule(model, h, j):
            """
            Linear Expenditure System (LES) demand:
            C[h,j] = gamma[h,j] + (beta[h,j] / pq[j]) * (C_H[h] - sum(pq[i] * gamma[h,i]))
            Modified to avoid division by zero: pq[j] * C[h,j] = pq[j] * gamma[h,j] + beta[h,j] * supernumerary_income
            """
            # Calculate supernumerary income (total consumption minus subsistence)
            subsistence_expenditure = sum(
                model.pq[i] * model.gamma_les[h, i] for i in self.sectors)
            supernumerary_income = model.C_H[h] - subsistence_expenditure

            # LES demand equation - reformulated to avoid division
            # pq[j] * C[h,j] = pq[j] * gamma[h,j] + beta[h,j] * supernumerary_income
            return (model.pq[j] * model.C[h, j] ==
                    model.pq[j] * model.gamma_les[h, j] +
                    model.beta_les[h, j] * supernumerary_income)

        self.model.eq_les_demand = pyo.Constraint(
            self.household_regions, self.sectors,
            rule=les_demand_rule,
            doc="LES demand system"
        )

    def add_government_constraints(self):
        """Government budget and expenditure constraints"""

        # Government revenue
        def government_revenue_rule(model):
            """
            Y_G = direct_taxes + indirect_taxes + tariffs + carbon_revenue

            Following ThreeME approach:
            - Carbon revenue from ETS1 and ETS2 is recycled through government budget
            - Can be used for: (1) reducing deficit, (2) transfers to households, (3) green investment
            """
            direct_taxes = sum(model.Td[h] for h in self.household_regions)
            indirect_taxes = sum(model.Tz[j] for j in self.sectors)
            tariffs = sum(model.Tm[j] for j in self.sectors)

            # Carbon revenue from ETS policies (key addition for ETS scenarios)
            carbon_revenue = 0
            if hasattr(model, 'Carbon_Revenue'):
                # Use total carbon revenue from energy-environment block
                carbon_revenue = model.Carbon_Revenue
            elif hasattr(model, 'PLC'):
                # Fallback: sum policy costs from all sectors
                carbon_revenue = sum(model.PLC[j] for j in self.sectors)

            return model.Y_G == direct_taxes + indirect_taxes + tariffs + carbon_revenue

        self.model.eq_government_revenue = pyo.Constraint(
            rule=government_revenue_rule,
            doc="Government revenue including carbon revenue"
        )

        # Tax revenue definitions
        def direct_tax_revenue_rule(model, h):
            """Td[h] = td[h] * gross_factor_income[h]"""
            # Factor income before tax
            gross_factor_income = 0
            for f in self.factors:
                total_factor_income = sum(
                    model.pf[f] * model.F[f, j] for j in self.sectors)
                factor_dist = self.params.get('factor_distribution', {})
                f_dist = factor_dist.get(f, {})
                share = f_dist.get(h, 0.2)
                gross_factor_income += total_factor_income * share

            return model.Td[h] == model.td[h] * gross_factor_income

        self.model.eq_direct_tax_revenue = pyo.Constraint(
            self.household_regions,
            rule=direct_tax_revenue_rule,
            doc="Direct tax revenue"
        )

        def indirect_tax_revenue_rule(model, j):
            """Tz[j] = tz[j] * pz[j] * Z[j]"""
            return model.Tz[j] == model.tz[j] * model.pz[j] * model.Z[j]

        self.model.eq_indirect_tax_revenue = pyo.Constraint(
            self.sectors,
            rule=indirect_tax_revenue_rule,
            doc="Indirect tax revenue"
        )

        def tariff_revenue_rule(model, j):
            """Tm[j] = tm[j] * pm[j] * M[j]"""
            return model.Tm[j] == model.tm[j] * model.pm[j] * model.M[j]

        self.model.eq_tariff_revenue = pyo.Constraint(
            self.sectors,
            rule=tariff_revenue_rule,
            doc="Tariff revenue"
        )

        # Government budget constraint
        def government_budget_rule(model):
            """Y_G = C_G + S_G"""
            return model.Y_G == model.C_G + model.S_G

        self.model.eq_government_budget = pyo.Constraint(
            rule=government_budget_rule,
            doc="Government budget constraint"
        )

        # Government consumption expenditure
        def government_consumption_expenditure_rule(model):
            """C_G = sum(pq[j] * G[j])"""
            return model.C_G == sum(model.pq[j] * model.G[j] for j in self.sectors)

        self.model.eq_government_consumption_expenditure = pyo.Constraint(
            rule=government_consumption_expenditure_rule,
            doc="Government consumption expenditure"
        )

        # Government demand by sector
        def government_demand_rule(model, j):
            """G[j] = gov_share[j] * C_G / pq[j] - reformulated to avoid division"""
            """pq[j] * G[j] = gov_share[j] * C_G"""
            return model.pq[j] * model.G[j] == model.gov_share[j] * model.C_G

        self.model.eq_government_demand = pyo.Constraint(
            self.sectors,
            rule=government_demand_rule,
            doc="Government sectoral demand"
        )

    def add_investment_constraints(self):
        """Investment demand and financing"""

        # Total investment identity
        def total_investment_rule(model):
            """I_T = sum(pq[j] * I[j])"""
            return model.I_T == sum(model.pq[j] * model.I[j] for j in self.sectors)

        self.model.eq_total_investment = pyo.Constraint(
            rule=total_investment_rule,
            doc="Total investment identity"
        )

        # Investment demand by sector of origin
        def investment_demand_rule(model, j):
            """I[j] = inv_share[j] * I_T / pq[j] - reformulated to avoid division"""
            """pq[j] * I[j] = inv_share[j] * I_T"""
            return model.pq[j] * model.I[j] == model.inv_share[j] * model.I_T

        self.model.eq_investment_demand = pyo.Constraint(
            self.sectors,
            rule=investment_demand_rule,
            doc="Investment demand by sector"
        )

    def add_macroeconomic_balances(self):
        """Macroeconomic balance constraints"""

        # Savings-investment balance
        def savings_investment_balance_rule(model):
            """Private savings + Government savings + Foreign savings = Investment"""
            private_savings = sum(model.S_H[h] for h in self.household_regions)
            government_savings = model.S_G
            foreign_savings = model.S_F
            total_investment = model.I_T

            return private_savings + government_savings + foreign_savings == total_investment

        self.model.eq_savings_investment_balance = pyo.Constraint(
            rule=savings_investment_balance_rule,
            doc="Savings-investment balance"
        )

        # Current account balance (definition of foreign savings)
        def current_account_balance_rule(model):
            """S_F = Imports - Exports (in domestic currency)"""
            total_imports = sum(model.pm[j] * model.M[j] for j in self.sectors)
            total_exports = sum(model.pe[j] * model.E[j] for j in self.sectors)

            return model.S_F == total_imports - total_exports

        self.model.eq_current_account_balance = pyo.Constraint(
            rule=current_account_balance_rule,
            doc="Current account balance"
        )

    def initialize_income_expenditure_variables(self):
        """Initialize variables with calibrated values"""

        print("Initializing income-expenditure variables...")

        # Initialize household variables
        for h in self.household_regions:
            if h in self.params['households']:
                hh_data = self.params['households'][h]

                # Scale values
                income = hh_data.get('income', 50000) / self.income_scale
                consumption = hh_data.get(
                    'consumption', 40000) / self.consumption_scale
                savings = max(income - consumption, 0.001)

                self.model.Y_H[h].set_value(income)
                self.model.C_H[h].set_value(consumption)
                self.model.S_H[h].set_value(savings)

                # Initialize sectoral consumption
                consumption_pattern = hh_data.get('consumption_pattern', {})
                for j in self.sectors:
                    sectoral_consumption = consumption_pattern.get(
                        j, consumption / len(self.sectors)) / self.consumption_scale
                    self.model.C[h, j].set_value(sectoral_consumption)

                print(
                    f"  {h}: Income={income:.1f}, Consumption={consumption:.1f}, Savings={savings:.3f}")

        # Initialize government variables
        gov_data = self.params.get('government', {})
        if gov_data:
            revenue = gov_data.get('revenue', 100000) / self.income_scale
            consumption = gov_data.get(
                'revenue', 100000) * 0.8 / self.consumption_scale
            savings = revenue - consumption

            self.model.Y_G.set_value(revenue)
            self.model.C_G.set_value(consumption)
            self.model.S_G.set_value(savings)

            # Government sectoral consumption
            gov_consumption_pattern = gov_data.get('consumption', {})
            for j in self.sectors:
                sectoral_consumption = gov_consumption_pattern.get(
                    j, consumption / len(self.sectors)) / self.consumption_scale
                self.model.G[j].set_value(sectoral_consumption)

            print(
                f"  Government: Revenue={revenue:.1f}, Consumption={consumption:.1f}, Savings={savings:.1f}")

        # Initialize investment variables
        inv_data = self.params.get('investment', {})
        if inv_data:
            total_investment = inv_data.get(
                'total_investment', 200000) / self.income_scale
            self.model.I_T.set_value(total_investment)

            sectoral_investment = inv_data.get('sectoral_investment', {})
            for j in self.sectors:
                investment = sectoral_investment.get(
                    j, total_investment / len(self.sectors)) / self.income_scale
                self.model.I[j].set_value(investment)

            print(f"  Investment: Total={total_investment:.1f}")

        # Initialize foreign savings
        trade_data = self.params.get('trade', {})
        trade_balance = trade_data.get(
            'overall_trade_balance', 0) / self.income_scale
        self.model.S_F.set_value(-trade_balance)  # Negative of trade balance

        # Initialize tax revenues (small positive values)
        for h in self.household_regions:
            self.model.Td[h].set_value(5.0)

        for j in self.sectors:
            self.model.Tz[j].set_value(1.0)
            self.model.Tm[j].set_value(0.5)

        print("Income-expenditure initialization completed")

    def update_policy_parameters(self, scenario_name, year):
        """Update policy parameters for different scenarios"""

        if scenario_name == 'BAU':
            # No policy changes in BAU
            pass

        elif scenario_name in ['ETS1', 'ETS2']:
            # Update tax rates if carbon revenue recycling through tax cuts
            base_carbon_price = model_definitions.get_scenario_carbon_price(
                scenario_name, year)

            if base_carbon_price > 0:
                # Reduce income tax rates slightly (carbon revenue recycling)
                reduction_factor = min(
                    0.2, base_carbon_price / 100.0)  # Max 20% reduction

                for h in self.household_regions:
                    current_rate = pyo.value(self.model.td[h])
                    new_rate = current_rate * (1 - reduction_factor)
                    self.model.td[h].set_value(
                        max(0.05, new_rate))  # Minimum 5% tax rate

                print(
                    f"Updated tax rates for {scenario_name} in {year}: reduction factor = {reduction_factor:.1%}")

    def get_income_expenditure_results(self, model_solution):
        """Extract income-expenditure results from solved model"""

        results = {
            'household_income': {},
            'household_consumption': {},
            'household_savings': {},
            'sectoral_consumption': {},
            'government_revenue': 0,
            'government_consumption': {},
            'government_savings': 0,
            'investment_total': 0,
            'investment_sectoral': {},
            'tax_revenues': {'direct': {}, 'indirect': {}, 'tariffs': {}, 'carbon_revenue': 0},
            'savings_investment_balance': {}
        }

        # Scale back to original units
        for h in self.household_regions:
            results['household_income'][h] = pyo.value(
                model_solution.Y_H[h]) * self.income_scale
            results['household_consumption'][h] = pyo.value(
                model_solution.C_H[h]) * self.consumption_scale
            results['household_savings'][h] = pyo.value(
                model_solution.S_H[h]) * self.income_scale

            # Sectoral consumption
            sectoral_consumption = {}
            for j in self.sectors:
                sectoral_consumption[j] = pyo.value(
                    model_solution.C[h, j]) * self.consumption_scale
            results['sectoral_consumption'][h] = sectoral_consumption

        # Government
        results['government_revenue'] = pyo.value(
            model_solution.Y_G) * self.income_scale
        results['government_savings'] = pyo.value(
            model_solution.S_G) * self.income_scale

        for j in self.sectors:
            results['government_consumption'][j] = pyo.value(
                model_solution.G[j]) * self.consumption_scale

        # Investment
        results['investment_total'] = pyo.value(
            model_solution.I_T) * self.income_scale
        for j in self.sectors:
            results['investment_sectoral'][j] = pyo.value(
                model_solution.I[j]) * self.income_scale

        # Tax revenues (including carbon revenue)
        for h in self.household_regions:
            results['tax_revenues']['direct'][h] = pyo.value(
                model_solution.Td[h])

        for j in self.sectors:
            results['tax_revenues']['indirect'][j] = pyo.value(
                model_solution.Tz[j])
            results['tax_revenues']['tariffs'][j] = pyo.value(
                model_solution.Tm[j])

        # Carbon revenue from ETS policies (key metric for policy analysis)
        if hasattr(model_solution, 'Carbon_Revenue'):
            results['tax_revenues']['carbon_revenue'] = pyo.value(
                model_solution.Carbon_Revenue)
        elif hasattr(model_solution, 'PLC'):
            results['tax_revenues']['carbon_revenue'] = sum(
                pyo.value(model_solution.PLC[j]) for j in self.sectors)
        else:
            results['tax_revenues']['carbon_revenue'] = 0.0

        # Aggregate calculations
        results['total_household_income'] = sum(
            results['household_income'].values())
        results['total_household_consumption'] = sum(
            results['household_consumption'].values())
        results['total_household_savings'] = sum(
            results['household_savings'].values())
        results['total_government_consumption'] = sum(
            results['government_consumption'].values())
        results['total_private_savings'] = results['total_household_savings']
        results['foreign_savings'] = pyo.value(
            model_solution.S_F) * self.income_scale

        # Savings-investment balance check
        total_savings = (results['total_private_savings'] +
                         results['government_savings'] +
                         results['foreign_savings'])
        results['savings_investment_balance'] = {
            'total_savings': total_savings,
            'total_investment': results['investment_total'],
            'balance_error': abs(total_savings - results['investment_total'])
        }

        return results

# Testing function


def test_income_expenditure_block():
    """Test the income-expenditure block"""

    print("Testing Income-Expenditure Block...")

    # Create test model
    model = pyo.ConcreteModel("IncomeExpenditure_Test")

    # Create sample data
    from data_processor import DataProcessor
    processor = DataProcessor()
    processor.create_calibrated_placeholder()
    calibrated_data = processor.get_calibrated_data()

    # Need some dummy production variables for linking
    model.pq = pyo.Var(calibrated_data['production_sectors'], initialize=1.0)
    model.pz = pyo.Var(calibrated_data['production_sectors'], initialize=1.0)
    model.pm = pyo.Var(calibrated_data['production_sectors'], initialize=1.0)
    model.pe = pyo.Var(calibrated_data['production_sectors'], initialize=1.0)
    model.pf = pyo.Var(calibrated_data['factors'], initialize=1.0)
    model.Z = pyo.Var(calibrated_data['production_sectors'], initialize=1000.0)
    model.F = pyo.Var(
        calibrated_data['factors'], calibrated_data['production_sectors'], initialize=500.0)
    model.M = pyo.Var(calibrated_data['production_sectors'], initialize=100.0)
    model.E = pyo.Var(calibrated_data['production_sectors'], initialize=150.0)

    # Create income-expenditure block
    ie_block = IncomeExpenditureBlock(model, calibrated_data)

    # Initialize variables
    ie_block.initialize_income_expenditure_variables()

    print(
        f"Variables created: {len([v for v in model.component_objects(pyo.Var)])}")
    print(
        f"Constraints created: {len([c for c in model.component_objects(pyo.Constraint)])}")
    print(
        f"Parameters created: {len([p for p in model.component_objects(pyo.Param)])}")

    # Test policy parameter update
    ie_block.update_policy_parameters('ETS1', 2025)

    print("Income-expenditure block test completed successfully")

    return True


if __name__ == "__main__":
    test_income_expenditure_block()
