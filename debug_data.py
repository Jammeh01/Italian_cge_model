import pandas as pd

df = pd.read_excel('results/Italian_CGE_Enhanced_Dynamic_Results_20251017_215314.xlsx',
                   sheet_name='Households_Income')

print('Checking ETS1 and ETS2 data availability:')
print('\nColumn 2 (should be ETS1 for Centre):')
print(f"Scenario: {df.iloc[0, 2]}")
print(f"Values (first 10): {df.iloc[2:12, 2].tolist()}")

print('\nColumn 3 (should be ETS2 for Centre):')
print(f"Scenario: {df.iloc[0, 3]}")
print(f"Values (first 10): {df.iloc[2:12, 3].tolist()}")

print('\nColumn 11 (should be ETS1 for Northwest):')
print(f"Column name: {df.columns[11]}")
print(f"Scenario: {df.iloc[0, 11]}")
print(f"Values (first 10): {df.iloc[2:12, 11].tolist()}")

print('\nAll last values (2040):')
print(f"Last row: {df.iloc[-1, :].tolist()}")
