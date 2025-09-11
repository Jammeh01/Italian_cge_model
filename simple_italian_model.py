"""
Stable Italian CGE Model - Simplified version for 2021 Italian data
"""

import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import time
from datetime import datetime

# Import model components
from data_processor import DataProcessor
from production_block import ProductionBlock
from income_expenditure_block import IncomeExpenditureBlock
from trade_block import TradeBlock
from energy_environment_block import EnergyEnvironmentBlock
from market_clearing_closure_block import MarketClearingClosureBlock


class StableItalianCGEModel:
    """Stable Italian CGE Model for 2021 data"""

    def __init__(self, sam_file_path="data/SAM.xlsx"):
        self.sam_file_path = sam_file_path
        self.model = None
        self.calibrated_data = None
        self.blocks = {}
        self.solution = None
        self.current_year = 2021
        self.current_scenario = 'BAU'

    def load_and_calibrate_data(self):
        """Load and calibrate SAM data"""

        print("LOADING DATA:")
        print("-" * 40)

        self.data_processor = DataProcessor(sam_file_path=self.sam_file_path)

        if not self.data_processor.load_and_process_sam():
            print("✗ Failed to load SAM data")
            return False

        self.calibrated_data = self.data_processor.get_calibrated_data()
        print(
            f"✓ Data loaded: {len(self.calibrated_data['production_sectors'])} sectors")
        return True

    def build_model(self):
        """Build CGE model"""

        print("\nBUILDING MODEL:")
        print("-" * 40)

        self.model = pyo.ConcreteModel("Stable_Italian_CGE")

        print("Building blocks...")
        self.blocks['production'] = ProductionBlock(
            self.model, self.calibrated_data)
        self.blocks['income_expenditure'] = IncomeExpenditureBlock(
            self.model, self.calibrated_data)
        self.blocks['trade'] = TradeBlock(self.model, self.calibrated_data)
        self.blocks['energy_environment'] = EnergyEnvironmentBlock(
            self.model, self.calibrated_data)
        self.blocks['market_clearing'] = MarketClearingClosureBlock(
            self.model, self.calibrated_data)

        print("✓ Model built successfully")
        return True

    def solve_model(self):
        """Solve model with IPOPT"""

        print(f"\nSOLVING MODEL:")
        print("-" * 40)

        # Initialize variables
        print("Initializing variables...")
        for block_name, block in self.blocks.items():
            if hasattr(block, 'initialize_variables'):
                block.initialize_variables()

        # Create solver
        solver = SolverFactory('ipopt')

        # Conservative settings
        solver.options['tol'] = 1e-2
        solver.options['constr_viol_tol'] = 1e-2
        solver.options['max_iter'] = 300
        solver.options['max_cpu_time'] = 1800
        solver.options['print_level'] = 3

        print("Starting solve...")
        start_time = time.time()

        try:
            self.solution = solver.solve(self.model, tee=True)
            solve_time = time.time() - start_time

            if self.solution.solver.termination_condition == pyo.TerminationCondition.optimal:
                print(
                    f"✓ Model solved successfully in {solve_time:.1f} seconds")
                return True
            else:
                print(
                    f"✗ Solve failed: {self.solution.solver.termination_condition}")
                return False

        except Exception as e:
            print(f"✗ Solver error: {e}")
            return False

    def run_analysis(self):
        """Run complete analysis"""

        print("=" * 60)
        print("STABLE ITALIAN CGE MODEL - 2021")
        print("=" * 60)

        if not self.load_and_calibrate_data():
            return False

        if not self.build_model():
            return False

        if not self.solve_model():
            return False

        print("\n✓ Analysis completed successfully")
        return True


def main():
    """Main execution"""
    model = StableItalianCGEModel()

    try:
        if model.run_analysis():
            print("\nSUCCESS: Model solved with 2021 Italian data")
        else:
            print("\nFAILED: Model could not be solved")
    except Exception as e:
        print(f"\nERROR: {e}")


if __name__ == "__main__":
    main()
