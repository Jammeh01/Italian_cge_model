import pandas as pd

energy = pd.read_excel('results/Italian_CGE_Enhanced_Dynamic_Results_20251017_215314.xlsx',
                       sheet_name='Household_Energy_by_Region')
expenditure = pd.read_excel('results/Italian_CGE_Enhanced_Dynamic_Results_20251017_215314.xlsx',
                            sheet_name='Households_Expenditure')

print('Energy data - Islands columns:')
for i, col in enumerate(energy.columns):
    if 'Islands' in str(col):
        scenario = energy.iloc[0, i]
        value_2040 = energy.iloc[-1, i]
        print(f'Col {i}: {col} -> Scenario: {scenario}, 2040 value: {value_2040}')

print('\n\nExpenditure data - Islands columns:')
for i, col in enumerate(expenditure.columns):
    if 'Islands' in str(col):
        scenario = expenditure.iloc[0, i]
        value_2040 = expenditure.iloc[-1, i]
        print(f'Col {i}: {col} -> Scenario: {scenario}, 2040 value: {value_2040}')

print('\n\nCalculating burden for Islands:')
# Find Islands energy and expenditure for BAU
for i, col in enumerate(energy.columns):
    if 'Islands' in str(col) and energy.iloc[0, i] == 'BAU':
        energy_val = energy.iloc[-1, i]
        print(f'Islands BAU Energy 2040: {energy_val} billion EUR')

for i, col in enumerate(expenditure.columns):
    if 'Islands' in str(col) and expenditure.iloc[0, i] == 'BAU':
        exp_val = expenditure.iloc[-1, i]
        print(f'Islands BAU Expenditure 2040: {exp_val} billion EUR')
        print(f'Burden: {(energy_val/exp_val)*100:.2f}%')
