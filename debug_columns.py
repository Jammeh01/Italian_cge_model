import pandas as pd

df = pd.read_excel('results/Italian_CGE_Enhanced_Dynamic_Results_20251017_215314.xlsx',
                   sheet_name='Households_Income')

print('Column mapping:')
for i, col in enumerate(df.columns):
    scenario = df.iloc[0, i]
    print(f"Col {i:2d}: {col:35s} -> Scenario: {scenario}")

regions = ['Centre', 'Islands', 'Northeast', 'Northwest', 'South']
print('\n\nRegion detection:')
for region in regions:
    cols = [i for i, col in enumerate(df.columns) if region in str(col)]
    print(f"{region:10s}: columns {cols}")
