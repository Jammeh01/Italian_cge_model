import pandas as pd

file = 'results/Italian_CGE_Enhanced_Dynamic_Results_20251018_103342.xlsx'

print("Checking sheet structures...")
print("\n1. Macroeconomy_GDP:")
gdp = pd.read_excel(file, sheet_name='Macroeconomy_GDP')
print(gdp.columns.tolist())
print(gdp.head())

print("\n2. Energy_Totals:")
energy = pd.read_excel(file, sheet_name='Energy_Totals')
print(energy.columns.tolist())
print(energy.head())

print("\n3. CO2_Emissions_Totals:")
co2 = pd.read_excel(file, sheet_name='CO2_Emissions_Totals')
print(co2.columns.tolist())
print(co2.head())

print("\n4. Renewable_Investment:")
renew = pd.read_excel(file, sheet_name='Renewable_Investment')
print(renew.columns.tolist())
print(renew.head())
