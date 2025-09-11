"""
Complete Italian CGE Model Execution Script
Run all three scenarios (BAU, ETS1, ETS2) with full dynamic simulation (2021-2050)
Based on ThreeME model structure with IPOPT optimization
"""

import os
import sys
import time
from datetime import datetime
import pandas as pd
import numpy as np

# Add current directory to path
sys.path.append('.')

# Import the main model and scenario runners
from main_model import ItalianCGEModel
from definitions import model_definitions

class ItalianCGERunner:
    """
    Complete runner for Italian CGE model scenarios
    Executes BAU, ETS1, and ETS2 scenarios with full comparison
    """
    
    def __init__(self, sam_file="SAM.xlsx", results_dir="italian_cge_results"):
        self.sam_file = sam_file
        self.results_dir = results_dir
        self.scenarios = ['BAU', 'ETS1', 'ETS2']
        self.time_horizon = list(range(2021, 2051, 1))  # Annual timesteps
        
        # Results storage
        self.all_results = {}
        
        # Create results directory
        os.makedirs(self.results_dir, exist_ok=True)
        
        print(f"Italian CGE Model Runner initialized")
        print(f"Results directory: {self.results_dir}")
        print(f"Time horizon: {self.time_horizon[0]}-{self.time_horizon[-1]} (annual)")
        print(f"Scenarios: {', '.join(self.scenarios)}")
    
    def setup_environment(self):
        """Check and setup model environment"""
        
        print("\n" + "="*60)
        print("ENVIRONMENT SETUP")
        print("="*60)
        
        # Check required packages
        required_packages = ['pyomo', 'pandas', 'numpy', 'openpyxl']
        missing_packages = []
        
        for package in required_packages:
            try:
                __import__(package)
                print(f"✓ {package} available")
            except ImportError:
                missing_packages.append(package)
                print(f"✗ {package} missing")
        
        if missing_packages:
            print(f"\nMissing packages: {', '.join(missing_packages)}")
            print("Install with: pip install " + " ".join(missing_packages))
            return False
        
        # Check IPOPT solver
        try:
            from pyomo.opt import SolverFactory
            solver = SolverFactory('ipopt')
            if solver.available():
                print("✓ IPOPT solver available")
            else:
                print("✗ IPOPT solver not available")
                return False
        except Exception as e:
            print(f"✗ Error checking IPOPT: {e}")
            return False
        
        # Check SAM file
        if os.path.exists(self.sam_file):
            print(f"✓ SAM file found: {self.sam_file}")
        elif os.path.exists(os.path.join('data', self.sam_file)):
            self.sam_file = os.path.join('data', self.sam_file)
            print(f"✓ SAM file found: {self.sam_file}")
        else:
            print(f"⚠ SAM file not found: {self.sam_file}")
            print("  Will use calibrated placeholder data")
        
        print("✓ Environment setup completed")
        return True
    
    def run_single_scenario(self, scenario_name, years_subset=None):
        """Run a single scenario"""
        
        years_to_run = years_subset or self.time_horizon
        
        print(f"\n{'='*70}")
        print(f"RUNNING SCENARIO: {scenario_name}")
        print(f"Years: {years_to_run[0]}-{years_to_run[-1]} ({len(years_to_run)} periods)")
        print(f"{'='*70}")
        
        # Create model instance
        model = ItalianCGEModel(self.sam_file)
        
        try:
            # Load and calibrate data
            print(f"Loading data for {scenario_name}...")
            success = model.load_and_calibrate_data()
            if not success:
                print(f"✗ Data loading failed for {scenario_name}")
                return {}
            
            # Build model
            print(f"Building model for {scenario_name}...")
            model.build_model()
            
            # Run dynamic scenario
            print(f"Running dynamic simulation for {scenario_name}...")
            scenario_results = model.run_dynamic_scenario(
                scenario_name, 
                start_year=years_to_run[0], 
                end_year=years_to_run[-1],
                save_results=True
            )
            
            if scenario_results:
                # Generate scenario report
                model.generate_scenario_report(scenario_results, scenario_name)
                
                print(f"✓ {scenario_name} scenario completed successfully")
                print(f"  Years solved: {len(scenario_results)}")
                
                # Store results
                self.all_results[scenario_name] = scenario_results
                return scenario_results
            else:
                print(f"✗ {scenario_name} scenario failed")
                return {}
                
        except Exception as e:
            print(f"✗ Error in {scenario_name} scenario: {str(e)}")
            import traceback
            traceback.print_exc()
            return {}
    
    def run_all_scenarios(self, test_run=False):
        """Run all scenarios"""
        
        print(f"\n{'='*80}")
        print(f"ITALIAN CGE MODEL - FULL SCENARIO ANALYSIS")
        print(f"{'='*80}")
        print(f"Model: Italian CGE with ThreeME structure")
        print(f"Solver: IPOPT optimization")
        print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if test_run:
            # Test run: only selected years
            test_years = [2021, 2025, 2030, 2040, 2050]
            print(f"TEST RUN - Selected years: {test_years}")
            years_to_run = test_years
        else:
            # Full run: all years
            years_to_run = self.time_horizon
        
        start_time = time.time()
        
        # Run scenarios in order
        for scenario in self.scenarios:
            scenario_start = time.time()
            
            results = self.run_single_scenario(scenario, years_to_run)
            
            scenario_time = time.time() - scenario_start
            print(f"  {scenario} completed in {scenario_time/60:.1f} minutes")
            
            if not results:
                print(f"  ⚠ {scenario} failed - continuing with other scenarios")
        
        total_time = time.time() - start_time
        
        print(f"\n{'='*80}")
        print(f"ALL SCENARIOS COMPLETED")
        print(f"Total runtime: {total_time/60:.1f} minutes")
        print(f"Successful scenarios: {len(self.all_results)}/{len(self.scenarios)}")
        print(f"{'='*80}")
        
        # Generate comparison analysis
        if len(self.all_results) >= 2:
            self.generate_scenario_comparison()
        
        return self.all_results
    
    def generate_scenario_comparison(self):
        """Generate comprehensive scenario comparison"""
        
        print(f"\n{'='*60}")
        print(f"GENERATING SCENARIO COMPARISON")
        print(f"{'='*60}")
        
        if len(self.all_results) < 2:
            print("Need at least 2 scenarios for comparison")
            return
        
        comparison_dir = os.path.join(self.results_dir, "scenario_comparison")
        os.makedirs(comparison_dir, exist_ok=True)
        
        # Get common years
        all_years = []
        for scenario_results in self.all_results.values():
            all_years.extend(scenario_results.keys())
        common_years = sorted(list(set(all_years)))
        
        print(f"Comparing {len(self.all_results)} scenarios across {len(common_years)} years")
        
        # Create comparison dataframes
        comparison_data = {}
        
        # Economic indicators
        economic_indicators = {
            'GDP_expenditure': ('production', 'total_output'),
            'Total_Value_Added': ('production', 'total_value_added'),
            'Unemployment_Rate': ('market_clearing', 'factor_markets', 'unemployment_rate'),
            'Total_Consumption': ('income_expenditure', 'total_household_consumption'),
            'Total_Investment': ('income_expenditure', 'investment_total'),
            'Trade_Balance': ('trade', 'trade_indicators', 'overall_trade_balance')
        }
        
        for indicator, path in economic_indicators.items():
            comparison_data[indicator] = {}
            
            for scenario_name, scenario_results in self.all_results.items():
                indicator_values = []
                
                for year in common_years:
                    if year in scenario_results:
                        result = scenario_results[year]
                        
                        # Navigate through nested dictionary
                        value = result
                        for key in path:
                            value = value.get(key, {})
                            if not isinstance(value, dict):
                                break
                        
                        if isinstance(value, (int, float)):
                            indicator_values.append(value)
                        else:
                            indicator_values.append(0)
                    else:
                        indicator_values.append(np.nan)
                
                comparison_data[indicator][scenario_name] = indicator_values
        
        # Environmental indicators
        environmental_indicators = {
            'Total_Emissions': ('energy_environment', 'emissions', 'total_emissions'),
            'Carbon_Intensity': ('macro_indicators', 'environmental_indicators', 'carbon_intensity'),
            'Energy_Intensity': ('macro_indicators', 'environmental_indicators', 'energy_intensity'),
            'ETS1_Price': ('energy_environment', 'carbon_pricing', 'ets1_price'),
            'ETS2_Price': ('energy_environment', 'carbon_pricing', 'ets2_price'),
            'Total_Carbon_Revenue': ('energy_environment', 'carbon_pricing', 'total_carbon_revenue')
        }
        
        for indicator, path in environmental_indicators.items():
            comparison_data[indicator] = {}
            
            for scenario_name, scenario_results in self.all_results.items():
                indicator_values = []
                
                for year in common_years:
                    if year in scenario_results:
                        result = scenario_results[year]
                        
                        # Navigate through nested dictionary
                        value = result
                        for key in path:
                            value = value.get(key, {})
                            if not isinstance(value, dict):
                                break
                        
                        if isinstance(value, (int, float)):
                            indicator_values.append(value)
                        else:
                            indicator_values.append(0)
                    else:
                        indicator_values.append(np.nan)
                
                comparison_data[indicator][scenario_name] = indicator_values
        
        # Regional indicators (household income by region)
        if self.all_results:
            first_scenario = list(self.all_results.values())[0]
            if common_years and common_years[0] in first_scenario:
                first_year_result = first_scenario[common_years[0]]
                ie_results = first_year_result.get('income_expenditure', {})
                
                if 'household_income' in ie_results:
                    regions = list(ie_results['household_income'].keys())
                    
                    for region in regions:
                        indicator_name = f'Income_{region}'
                        comparison_data[indicator_name] = {}
                        
                        for scenario_name, scenario_results in self.all_results.items():
                            indicator_values = []
                            
                            for year in common_years:
                                if year in scenario_results:
                                    result = scenario_results[year]
                                    ie_result = result.get('income_expenditure', {})
                                    household_income = ie_result.get('household_income', {})
                                    value = household_income.get(region, 0)
                                    indicator_values.append(value)
                                else:
                                    indicator_values.append(np.nan)
                            
                            comparison_data[indicator_name][scenario_name] = indicator_values
        
        # Save comparison data to Excel
        comparison_file = os.path.join(comparison_dir, "scenario_comparison.xlsx")
        with pd.ExcelWriter(comparison_file, engine='openpyxl') as writer:
            
            for indicator, scenario_data in comparison_data.items():
                if scenario_data:  # Only include indicators with data
                    df = pd.DataFrame(scenario_data, index=common_years)
                    df.to_excel(writer, sheet_name=indicator)
        
        print(f"✓ Scenario comparison saved: {comparison_file}")
        
        # Generate summary report
        self.generate_summary_report(comparison_data, common_years, comparison_dir)
    
    def generate_summary_report(self, comparison_data, years, output_dir):
        """Generate summary comparison report"""
        
        report_file = os.path.join(output_dir, "scenario_summary_report.txt")
        
        report_lines = []
        report_lines.append("="*80)
        report_lines.append("ITALIAN CGE MODEL - SCENARIO COMPARISON SUMMARY")
        report_lines.append("="*80)
        report_lines.append("")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Time horizon: {years[0]}-{years[-1]}")
        report_lines.append(f"Scenarios compared: {', '.join(self.all_results.keys())}")
        report_lines.append("")
        
        # Key scenario differences
        report_lines.append("SCENARIO DESCRIPTIONS:")
        scenario_descriptions = {
            'BAU': 'Business as Usual - No additional climate policies',
            'ETS1': f'ETS Phase 1 - €{model_definitions.ets1_policy["base_carbon_price"]}/tCO2 starting 2021, sectors: {", ".join(model_definitions.ets1_policy["covered_sectors"])}',
            'ETS2': f'ETS Phase 1+2 - Extended coverage starting 2027, ETS2 price: €{model_definitions.ets2_policy["base_carbon_price"]}/tCO2'
        }
        
        for scenario in self.all_results.keys():
            if scenario in scenario_descriptions:
                report_lines.append(f"  {scenario}: {scenario_descriptions[scenario]}")
        
        report_lines.append("")
        
        # Key findings
        report_lines.append("KEY FINDINGS:")
        
        if len(years) >= 2:
            start_year = years[0]
            end_year = years[-1]
            
            # GDP comparison
            if 'GDP_expenditure' in comparison_data:
                report_lines.append("\n  ECONOMIC IMPACT:")
                gdp_data = comparison_data['GDP_expenditure']
                
                for scenario in gdp_data.keys():
                    values = gdp_data[scenario]
                    if len(values) >= 2 and not np.isnan(values[0]) and not np.isnan(values[-1]):
                        start_gdp = values[0]
                        end_gdp = values[-1]
                        years_span = len(values) - 1
                        
                        if start_gdp > 0 and years_span > 0:
                            growth_rate = (end_gdp / start_gdp) ** (1/years_span) - 1
                            report_lines.append(f"    {scenario}: {growth_rate*100:.2f}% avg annual GDP growth")
            
            # Emissions comparison
            if 'Total_Emissions' in comparison_data:
                report_lines.append("\n  ENVIRONMENTAL IMPACT:")
                emissions_data = comparison_data['Total_Emissions']
                
                for scenario in emissions_data.keys():
                    values = emissions_data[scenario]
                    if len(values) >= 2 and not np.isnan(values[0]) and not np.isnan(values[-1]):
                        start_emissions = values[0]
                        end_emissions = values[-1]
                        
                        if start_emissions > 0:
                            emissions_change = (end_emissions / start_emissions - 1) * 100
                            report_lines.append(f"    {scenario}: {emissions_change:+.1f}% total emissions change ({start_year}-{end_year})")
            
            # Carbon pricing results
            if 'Total_Carbon_Revenue' in comparison_data:
                report_lines.append("\n  CARBON PRICING REVENUE (Final Year):")
                revenue_data = comparison_data['Total_Carbon_Revenue']
                
                for scenario in revenue_data.keys():
                    values = revenue_data[scenario]
                    if values and not np.isnan(values[-1]) and values[-1] > 0:
                        final_revenue = values[-1]
                        report_lines.append(f"    {scenario}: €{final_revenue:,.0f} ({end_year})")
        
        report_lines.append("")
        report_lines.append("="*80)
        
        # Save report
        with open(report_file, 'w') as f:
            f.write("\n".join(report_lines))
        
        print(f"✓ Summary report saved: {report_file}")
        
        # Print key findings to console
        print("\nKEY FINDINGS SUMMARY:")
        for line in report_lines[-15:]:  # Last 15 lines
            if line.strip():
                print(line)

def main():
    """Main execution function"""
    
    print("ITALIAN CGE MODEL - COMPLETE EXECUTION")
    print("="*60)
    print("ThreeME-style recursive dynamic CGE model")
    print("Three scenarios: BAU, ETS1, ETS2")
    print("Time horizon: 2021-2050 (annual)")
    print("Solver: IPOPT optimization")
    print("="*60)
    
    # Create runner
    runner = ItalianCGERunner()
    
    # Setup environment
    if not runner.setup_environment():
        print("Environment setup failed. Please check requirements.")
        return False
    
    # Ask user for run type
    print("\nSelect run type:")
    print("1. Test run (selected years: 2021, 2025, 2030, 2040, 2050)")
    print("2. Full run (all years: 2021-2050)")
    print("3. Single scenario test (BAU 2021 only)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    try:
        if choice == '1':
            print("\nStarting TEST RUN...")
            results = runner.run_all_scenarios(test_run=True)
            
        elif choice == '2':
            print("\nStarting FULL RUN...")
            print("Warning: This may take several hours to complete!")
            confirm = input("Continue? (y/n): ").strip().lower()
            
            if confirm in ['y', 'yes']:
                results = runner.run_all_scenarios(test_run=False)
            else:
                print("Full run cancelled.")
                return False
                
        elif choice == '3':
            print("\nStarting SINGLE SCENARIO TEST...")
            results = runner.run_single_scenario('BAU', [2021])
            
        else:
            print("Invalid choice. Running test instead.")
            results = runner.run_all_scenarios(test_run=True)
        
        # Final summary
        print(f"\n{'='*60}")
        print("EXECUTION COMPLETED")
        print(f"{'='*60}")
        
        if results:
            print(f"✓ Successfully completed scenarios: {len(results)}")
            print(f"✓ Results saved in: {runner.results_dir}")
            print("\nNext steps:")
            print("- Review scenario reports in results folders")
            print("- Check scenario_comparison/ for comparative analysis")
            print("- Use Excel files for detailed data analysis")
        else:
            print("✗ No scenarios completed successfully")
            print("Check error messages above for troubleshooting")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\nExecution interrupted by user.")
        return False
    
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Italian CGE Model execution completed!")
    else:
        print("\n⚠ Execution completed with errors.")