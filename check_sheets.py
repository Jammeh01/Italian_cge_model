import pandas as pd

xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251018_103342.xlsx')
print('Available sheets:')
for i, sheet in enumerate(xl.sheet_names, 1):
    print(f'{i}. {sheet}')
