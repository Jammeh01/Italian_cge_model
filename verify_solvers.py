#!/usr/bin/env python3
"""
Italian CGE Model - Solver Verification Script
This script verifies that Pyomo and optimization solvers are working correctly.
"""

import pyomo.environ as pyo
import sys
import os

def test_solver(solver_name, test_nonlinear=False):
    """Test if a solver is available and working"""
    print(f"\n{'='*50}")
    print(f"Testing {solver_name.upper()} Solver")
    print(f"{'='*50}")
    
    try:
        # Create solver factory
        opt = pyo.SolverFactory(solver_name)
        
        # Check availability
        if not opt.available():
            print(f"❌ {solver_name} is not available")
            return False
            
        print(f"✅ {solver_name} is available")
        print(f"   Executable: {opt.executable()}")
        
        # Create test model
        model = pyo.ConcreteModel()
        
        if test_nonlinear:
            # Nonlinear test problem (for IPOPT)
            model.x = pyo.Var(bounds=(0.1, 5))
            model.y = pyo.Var(bounds=(0.1, 5))
            model.obj = pyo.Objective(expr=model.x**2 + model.y**2, sense=pyo.minimize)
            model.constraint1 = pyo.Constraint(expr=model.x * model.y >= 2)
        else:
            # Linear test problem
            model.x = pyo.Var(bounds=(0, 4))
            model.y = pyo.Var(bounds=(0, None))
            model.obj = pyo.Objective(expr=2*model.x + 3*model.y, sense=pyo.minimize)
            model.constraint1 = pyo.Constraint(expr=model.x + model.y >= 1)
        
        # Solve with minimal output
        results = opt.solve(model, tee=False)
        
        # Check results
        if results.solver.status == pyo.SolverStatus.ok:
            if results.solver.termination_condition == pyo.TerminationCondition.optimal:
                print(f"✅ {solver_name} solved test problem successfully!")
                print(f"   Status: {results.solver.status}")
                print(f"   Termination: {results.solver.termination_condition}")
                print(f"   Optimal x: {pyo.value(model.x):.6f}")
                print(f"   Optimal y: {pyo.value(model.y):.6f}")
                print(f"   Optimal objective: {pyo.value(model.obj):.6f}")
                return True
            else:
                print(f"⚠️  {solver_name} terminated with: {results.solver.termination_condition}")
                return False
        else:
            print(f"❌ {solver_name} failed with status: {results.solver.status}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing {solver_name}: {str(e)}")
        return False

def main():
    """Main verification function"""
    print("Italian CGE Model - Solver Verification")
    print("="*60)
    
    # Check Python and Pyomo versions
    print(f"Python version: {sys.version}")
    try:
        import pyomo
        print(f"Pyomo version: {pyomo.__version__}")
    except:
        print("Pyomo version: Available (version check failed)")
    
    # Test solvers
    solvers_tested = []
    
    # Test IPOPT (nonlinear solver - primary for CGE models)
    ipopt_works = test_solver('ipopt', test_nonlinear=True)
    solvers_tested.append(('IPOPT', ipopt_works))
    
    # Test Gurobi (commercial solver - backup)
    gurobi_works = test_solver('gurobi', test_nonlinear=False)
    solvers_tested.append(('Gurobi', gurobi_works))
    
    # Test other available solvers
    other_solvers = ['glpk', 'cbc', 'scip']
    for solver in other_solvers:
        try:
            opt = pyo.SolverFactory(solver)
            if opt.available():
                works = test_solver(solver, test_nonlinear=False)
                solvers_tested.append((solver.upper(), works))
        except:
            pass
    
    # Summary
    print(f"\n{'='*60}")
    print("SOLVER VERIFICATION SUMMARY")
    print(f"{'='*60}")
    
    working_solvers = []
    for solver_name, works in solvers_tested:
        status = "✅ WORKING" if works else "❌ FAILED"
        print(f"{solver_name:12} : {status}")
        if works:
            working_solvers.append(solver_name)
    
    print(f"\nTotal working solvers: {len(working_solvers)}")
    
    if 'IPOPT' in working_solvers:
        print("\n🎉 EXCELLENT! IPOPT is working - perfect for CGE models!")
    elif len(working_solvers) > 0:
        print(f"\n✅ Good! You have {len(working_solvers)} working solver(s)")
    else:
        print("\n❌ WARNING: No working solvers found!")
        
    # CGE model readiness check
    print(f"\n{'='*60}")
    print("CGE MODEL READINESS CHECK")
    print(f"{'='*60}")
    
    if 'IPOPT' in working_solvers:
        print("✅ READY: Your environment is fully configured for the Italian CGE model!")
        print("   - IPOPT nonlinear solver is available")
        print("   - You can run complex CGE optimizations")
    elif 'Gurobi' in working_solvers:
        print("⚠️  PARTIAL: Gurobi is available but IPOPT is preferred for CGE models")
        print("   - Linear/quadratic problems will work")
        print("   - Some nonlinear CGE features may be limited")
    else:
        print("❌ NOT READY: No suitable solvers for CGE models")
        print("   - Please install IPOPT or another nonlinear solver")

if __name__ == "__main__":
    main()