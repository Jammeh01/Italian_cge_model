import pandas as pd
import os

results_dir = 'results'
files = [f for f in os.listdir(results_dir) if f.startswith(
    'Italian_CGE_Enhanced_Dynamic_Results_') and f.endswith('.xlsx')]
latest_file = max(files, key=lambda x: os.path.getctime(
    os.path.join(results_dir, x)))
excel_file = os.path.join(results_dir, latest_file)

print(f"Reading: {latest_file}")

# Check Macroeconomy_GDP columns
print("\n" + "="*70)
print("Macroeconomy_GDP sheet:")
df_gdp = pd.read_excel(excel_file, sheet_name='Macroeconomy_GDP', nrows=10)
print(f"Columns: {list(df_gdp.columns)}")
print(f"\nFirst few rows:")
print(df_gdp)

# Check CO2_Emissions_Totals columns
print("\n" + "="*70)
print("CO2_Emissions_Totals sheet:")
df_co2 = pd.read_excel(excel_file, sheet_name='CO2_Emissions_Totals', nrows=10)
print(f"Columns: {list(df_co2.columns)}")
print(f"\nFirst few rows:")
print(df_co2)
