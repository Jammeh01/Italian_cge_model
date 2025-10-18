import pandas as pd

df = pd.read_excel('results/Italian_CGE_Enhanced_Dynamic_Results_20251017_215314.xlsx',
                   sheet_name='Households_Income')

print('All columns:')
for i, col in enumerate(df.columns):
    print(f'{i}: {col}')

print('\nScenario row:')
print(df.iloc[0].tolist())

print('\nFirst 10 rows, all columns:')
print(df.head(10))
