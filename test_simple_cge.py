#!/usr/bin/env python3
"""
Simple CGE Model Test Script
Bypasses complex features to test basic solving capability
"""

import os
import sys
import numpy as np
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# Add src directory to path
sys.path.append('src')


def create_simple_cge():
    """Create a simplified CGE model for testing"""

    print("CREATING SIMPLIFIED CGE MODEL FOR TESTING")
    print("=" * 50)

    # Create model
    model = pyo.ConcreteModel(name="Simple_CGE_Test")

    # Sets
    model.sectors = pyo.Set(initialize=['AGR', 'IND', 'SER'])
    model.factors = pyo.Set(initialize=['Labour', 'Capital'])
    model.households = pyo.Set(initialize=['HH1', 'HH2'])

    # Parameters (simplified values)
    model.alpha = pyo.Param(model.sectors, model.factors,
                            initialize={('AGR', 'Labour'): 0.6, ('AGR', 'Capital'): 0.4,
                                        ('IND', 'Labour'): 0.4, ('IND', 'Capital'): 0.6,
                                        ('SER', 'Labour'): 0.7, ('SER', 'Capital'): 0.3})

    model.io_coeff = pyo.Param(model.sectors, model.sectors, default=0.1)

    # Variables
    model.X = pyo.Var(model.sectors, bounds=(
        10, 2000), initialize=100)  # Output
    model.F = pyo.Var(model.factors, model.sectors, bounds=(
        1, 1000), initialize=50)  # Factor demand
    model.C = pyo.Var(model.households, model.sectors,
                      bounds=(1, 500), initialize=20)  # Consumption
    model.wf = pyo.Var(model.factors, bounds=(0.5, 2.0),
                       initialize=1.0)  # Factor prices
    model.p = pyo.Var(model.sectors, bounds=(
        0.5, 2.0), initialize=1.0)   # Prices

    # Factor supplies (fixed)
    model.FS = pyo.Param(model.factors, initialize={
                         'Labour': 300, 'Capital': 200})

    # Objective (dummy - just sum of outputs)
    def obj_rule(m):
        return sum(m.X[j] for j in m.sectors)
    model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)

    # Constraints

    # 1. Production function (Cobb-Douglas)
    def production_rule(m, j):
        return m.X[j] == pyo.prod(m.F[f, j]**m.alpha[j, f] for f in m.factors)
    model.production = pyo.Constraint(model.sectors, rule=production_rule)

    # 2. Factor market clearing
    def factor_market_rule(m, f):
        return m.FS[f] == sum(m.F[f, j] for j in m.sectors)
    model.factor_market = pyo.Constraint(
        model.factors, rule=factor_market_rule)

    # 3. Simple goods market clearing
    def goods_market_rule(m, i):
        demand = sum(m.C[h, i] for h in m.households)
        return m.X[i] >= demand  # Allow some slack
    model.goods_market = pyo.Constraint(model.sectors, rule=goods_market_rule)

    # 4. Budget constraints (simplified)
    def budget_rule(m, h):
        income = 100  # Fixed income
        return sum(m.p[j] * m.C[h, j] for j in m.sectors) <= income
    model.budget = pyo.Constraint(model.households, rule=budget_rule)

    print(f"Model created with:")
    print(f"  Variables: {len([v for v in model.component_objects(pyo.Var)])}")
    print(
        f"  Constraints: {len([c for c in model.component_objects(pyo.Constraint)])}")

    return model


def solve_simple_model(model):
    """Solve the simplified model"""

    print("\nSOLVING SIMPLIFIED MODEL")
    print("-" * 30)

    # Create solver
    solver = SolverFactory('ipopt')

    # Simple solver options
    solver.options['tol'] = 1e-3
    solver.options['max_iter'] = 200
    solver.options['print_level'] = 3
    solver.options['linear_solver'] = 'mumps'

    try:
        # Solve
        results = solver.solve(model, tee=True)

        print(f"\nSOLVER RESULTS:")
        print(f"  Status: {results.solver.status}")
        print(f"  Termination: {results.solver.termination_condition}")

        if results.solver.termination_condition == pyo.TerminationCondition.optimal:
            print("✓ SIMPLE MODEL SOLVED SUCCESSFULLY!")

            print("\nSolution Summary:")
            print("Outputs:")
            for j in model.sectors:
                print(f"  {j}: {pyo.value(model.X[j]):.2f}")

            print("Factor Prices:")
            for f in model.factors:
                print(f"  {f}: {pyo.value(model.wf[f]):.3f}")

            return True
        else:
            print("✗ Simple model failed to solve")
            return False

    except Exception as e:
        print(f"✗ Solving error: {e}")
        return False


def main():
    """Main test function"""

    # Change to model directory
    os.chdir(
        r"c:\Users\Jamme002\OneDrive - Universiteit Utrecht\Documents\italian_cge_model")

    print("SIMPLE CGE MODEL SOLVER TEST")
    print("=" * 40)

    # Create and solve simple model
    model = create_simple_cge()
    success = solve_simple_model(model)

    if success:
        print("\n✓ Basic CGE solving capability confirmed")
        print("The issue is likely in the complex model structure")
        print("Recommend simplifying the full model constraints")
    else:
        print("\n✗ Even simple CGE model fails")
        print("Check IPOPT installation and basic setup")

    return success


if __name__ == "__main__":
    main()
