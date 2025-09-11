import numpy as np
import pandas as pd
import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import matplotlib.pyplot as plt

# Test basic imports
print("✓ NumPy version:", np.__version__)
print("✓ Pandas version:", pd.__version__)
try:
    import pyomo
    print("✓ Pyomo version:", pyomo.__version__)
except AttributeError:
    print("✓ Pyomo imported successfully (version info unavailable)")

# Test IPOPT solver
try:
    solver = SolverFactory('ipopt')
    if solver.available():
        print("✓ IPOPT solver available")
    else:
        print("✗ IPOPT solver not available")
except:
    print("✗ Error accessing IPOPT solver")

# Test Excel reading
try:
    # This should work if openpyxl is installed
    df = pd.DataFrame({'test': [1, 2, 3]})
    df.to_excel('test.xlsx', index=False)
    df_read = pd.read_excel('test.xlsx')
    print("✓ Excel read/write working")
    import os
    os.remove('test.xlsx')
except:
    print("✗ Excel read/write not working")

print("\nSetup verification complete!")
