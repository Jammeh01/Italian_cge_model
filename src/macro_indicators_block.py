"""
Macro Indicators Block for Italian CGE Model
GDP calculation, price indices, and welfare measures
"""

import pyomo.environ as pyo
from definitions import model_definitions

class MacroIndicatorsBlock:
    """
    Macro indicators block calculating:
    - GDP (expenditure, income, and production approaches)
    - Price indices (CPI, PPI, GDP deflator)
    - Regional GDP and welfare measures
    - Energy and environmental indicators
    """
    
    def __init__(self, model, calibrated_data):
        self.model = model
        self.calibrated_data = calibrated_data
        self.sectors = calibrated_data['production_sectors']
        self.factors = calibrated_data['factors']
        self.household_regions = list(calibrated_data['households'].keys())
        self.params = calibrated_data['calibrated_parameters']
        
        self.add_macro_variables()
        self.add_macro_constraints()
    
    def add_macro_variables(self):
        """Add macroeconomic indicator variables"""
        
        # GDP measures
        self.model.GDP_exp = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(100000, 5000000),  # Reasonable bounds for Italian GDP
            initialize=self.params.get('base_year_gdp', 1782000),
            doc="GDP by expenditure approach"
        )
        
        self.model.GDP_inc = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(100000, 5000000),
            initialize=self.params.get('base_year_gdp', 1782000),
            doc="GDP by income approach"
        )
        
        # Price indices
        self.model.CPI = pyo.Var(
            domain=pyo.PositiveReals,
            bounds=(0.5, 3.0),
            initialize=1.0,
            doc="Consumer Price Index"
        )
        
        self.model.GDP_deflator = pyo.Var(
            domain=pyo.PositiveReals,
            bounds=(0.5, 3.0),
            initialize=1.0,
            doc="GDP Deflator"
        )
        
        # Regional GDP
        def regional_gdp_bounds(model, h):
            hh_data = self.params['households'].get(h, {})
            pop_share = hh_data.get('population_share', 0.2)
            base_gdp = self.params.get('base_year_gdp', 1782000) * pop_share
            return (base_gdp * 0.3, base_gdp * 3.0)
        
        self.model.Regional_GDP = pyo.Var(
            self.household_regions,
            domain=pyo.NonNegativeReals,
            bounds=regional_gdp_bounds,
            initialize=lambda m, h: self.params['households'].get(h, {}).get('income', 100000),
            doc="Regional GDP"
        )
        
        # Welfare measures
        self.model.Social_Welfare = pyo.Var(
            domain=pyo.Reals,
            initialize=100000.0,
            doc="Aggregate social welfare index"
        )
        
        # Environmental indicators
        self.model.Carbon_Intensity = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.0, 10.0),
            initialize=1.0,
            doc="Carbon intensity (emissions per unit GDP)"
        )
        
        self.model.Energy_Intensity = pyo.Var(
            domain=pyo.NonNegativeReals,
            bounds=(0.0, 10.0),
            initialize=1.0,
            doc="Energy intensity (energy per unit GDP)"
        )
    
    def add_macro_constraints(self):
        """Add macroeconomic indicator constraints"""
        
        # GDP by expenditure
        def gdp_expenditure_rule(model):
            """GDP = C + I + G + (E - M)"""
            consumption = sum(model.C_H[h] for h in self.household_regions) * 1000  # Scale back
            investment = model.I_T * 1000
            government = model.C_G * 1000
            net_exports = sum(model.pe[j] * model.E[j] - model.pm[j] * model.M[j] 
                             for j in self.sectors) * 1000
            
            return model.GDP_exp == consumption + investment + government + net_exports
        
        self.model.eq_gdp_expenditure = pyo.Constraint(
            rule=gdp_expenditure_rule,
            doc="GDP by expenditure"
        )
        
        # GDP by income
        def gdp_income_rule(model):
            """GDP = Factor payments + Taxes"""
            factor_payments = sum(model.pf[f] * model.FS[f] for f in self.factors) * 1000
            indirect_taxes = sum(model.Tz[j] for j in self.sectors)
            tariffs = sum(model.Tm[j] for j in self.sectors)
            
            return model.GDP_inc == factor_payments + indirect_taxes + tariffs
        
        self.model.eq_gdp_income = pyo.Constraint(
            rule=gdp_income_rule,
            doc="GDP by income"
        )
        
        # Consumer Price Index
        def cpi_rule(model):
            """CPI based on household consumption basket"""
            # Use average consumption weights across regions
            total_weight = 0
            weighted_prices = 0
            
            for h in self.household_regions:
                hh_data = self.params['households'].get(h, {})
                consumption_pattern = hh_data.get('consumption_pattern', {})
                total_consumption = sum(consumption_pattern.values())
                
                if total_consumption > 0:
                    region_weight = hh_data.get('population_share', 0.2)
                    
                    for j in self.sectors:
                        item_weight = consumption_pattern.get(j, 0) / total_consumption
                        weighted_prices += region_weight * item_weight * model.pq[j]
                        total_weight += region_weight * item_weight
            
            if total_weight > 0.01:  # Avoid division by very small numbers
                return model.CPI == weighted_prices / total_weight
            else:
                return model.CPI == 1.0
        
        self.model.eq_cpi = pyo.Constraint(
            rule=cpi_rule,
            doc="Consumer Price Index"
        )
        
        # GDP Deflator
        def gdp_deflator_rule(model):
            """GDP deflator (numeraire)"""
            return model.GDP_deflator == 1.0  # Fixed as numeraire
        
        self.model.eq_gdp_deflator = pyo.Constraint(
            rule=gdp_deflator_rule,
            doc="GDP deflator (numeraire)"
        )
        
        # Regional GDP
        def regional_gdp_rule(model, h):
            """Regional GDP based on regional income"""
            hh_data = self.params['households'].get(h, {})
            pop_share = hh_data.get('population_share', 0.2)
            
            return model.Regional_GDP[h] == model.Y_H[h] * 1000 / (1 - 0.15)  # Adjust for savings rate
        
        self.model.eq_regional_gdp = pyo.Constraint(
            self.household_regions,
            rule=regional_gdp_rule,
            doc="Regional GDP"
        )
        
        # Social welfare (simplified utilitarian)
        def social_welfare_rule(model):
            """Social welfare = sum of regional utility"""
            return model.Social_Welfare == sum(model.Y_H[h] * 1000 for h in self.household_regions)
        
        self.model.eq_social_welfare = pyo.Constraint(
            rule=social_welfare_rule,
            doc="Social welfare index"
        )
        
        # Carbon intensity
        def carbon_intensity_rule(model):
            """Carbon intensity = Total emissions / GDP"""
            return model.Carbon_Intensity * model.GDP_exp == model.Total_Emissions
        
        self.model.eq_carbon_intensity = pyo.Constraint(
            rule=carbon_intensity_rule,
            doc="Carbon intensity"
        )
        
        # Energy intensity
        def energy_intensity_rule(model):
            """Energy intensity = Total energy / GDP"""
            total_energy = sum(model.TOT_Energy[es] for es in ['Electricity', 'Gas', 'Other Energy'] 
                             if es in self.calibrated_data['energy_sectors'])
            return model.Energy_Intensity * model.GDP_exp == total_energy
        
        self.model.eq_energy_intensity = pyo.Constraint(
            rule=energy_intensity_rule,
            doc="Energy intensity"
        )
    
    def get_macro_results(self, model_solution):
        """Extract macroeconomic results"""
        
        results = {
            'gdp_measures': {
                'gdp_expenditure': pyo.value(model_solution.GDP_exp),
                'gdp_income': pyo.value(model_solution.GDP_inc),
                'gdp_average': (pyo.value(model_solution.GDP_exp) + pyo.value(model_solution.GDP_inc)) / 2
            },
            'price_indices': {
                'cpi': pyo.value(model_solution.CPI),
                'gdp_deflator': pyo.value(model_solution.GDP_deflator)
            },
            'regional_gdp': {},
            'welfare_measures': {
                'social_welfare': pyo.value(model_solution.Social_Welfare)
            },
            'environmental_indicators': {
                'carbon_intensity': pyo.value(model_solution.Carbon_Intensity),
                'energy_intensity': pyo.value(model_solution.Energy_Intensity)
            }
        }
        
        # Regional results
        for h in self.household_regions:
            results['regional_gdp'][h] = pyo.value(model_solution.Regional_GDP[h])
        
        return results

def test_macro_indicators():
    """Test macro indicators block"""
    
    print("Testing Macro Indicators Block...")
    
    # Create test model with dummy variables
    model = pyo.ConcreteModel("MacroTest")
    
    from data_processor import DataProcessor
    processor = DataProcessor()
    processor.create_calibrated_placeholder()
    calibrated_data = processor.get_calibrated_data()
    
    # Add required dummy variables
    sectors = calibrated_data['production_sectors']
    households = list(calibrated_data['households'].keys())
    factors = calibrated_data['factors']
    
    model.C_H = pyo.Var(households, initialize=40.0)
    model.I_T = pyo.Var(initialize=200.0)
    model.C_G = pyo.Var(initialize=120.0)
    model.pe = pyo.Var(sectors, initialize=1.0)
    model.pm = pyo.Var(sectors, initialize=1.0)
    model.E = pyo.Var(sectors, initialize=150.0)
    model.M = pyo.Var(sectors, initialize=100.0)
    model.pf = pyo.Var(factors, initialize=1.0)
    model.FS = pyo.Var(factors, initialize=500.0)
    model.Tz = pyo.Var(sectors, initialize=10.0)
    model.Tm = pyo.Var(sectors, initialize=5.0)
    model.pq = pyo.Var(sectors, initialize=1.0)
    model.Y_H = pyo.Var(households, initialize=50.0)
    model.Total_Emissions = pyo.Var(initialize=50000.0)
    model.TOT_Energy = pyo.Var(['Electricity', 'Gas', 'Other Energy'], initialize=1000.0)
    
    # Create macro indicators block
    macro_block = MacroIndicatorsBlock(model, calibrated_data)
    
    print(f"Variables created: {len([v for v in model.component_objects(pyo.Var)])}")
    print(f"Constraints created: {len([c for c in model.component_objects(pyo.Constraint)])}")
    
    print("Macro indicators block test completed successfully")
    
    return True

if __name__ == "__main__":
    test_macro_indicators()