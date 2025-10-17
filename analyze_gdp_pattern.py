"""
Analyze GDP pattern to understand the end-of-simulation behavior
"""
import pandas as pd
import os

# Find latest results file
results_dir = "results"
files = [f for f in os.listdir(results_dir)
         if f.startswith('Italian_CGE_Enhanced_Dynamic_Results_')
         and f.endswith('.xlsx')]
files.sort(reverse=True)
excel_file = os.path.join(results_dir, files[0])

print(f"Analyzing: {files[0]}")
print("="*80)

# Read GDP data
df = pd.read_excel(excel_file, sheet_name='Macroeconomy_GDP', index_col=0)

# Extract series
years = df.index[2:]
bau = df.iloc[2:, 0].astype(float)
ets1 = df.iloc[2:, 1].astype(float)
ets2 = df.iloc[2:, 2].dropna().astype(float)

# Calculate percentage differences
ets1_diff = ((ets1 - bau) / bau * 100)
ets2_diff = ((ets2 - bau.loc[ets2.index]) / bau.loc[ets2.index] * 100)

print("\nGDP VALUES (Billion EUR) AND IMPACTS (% vs BAU):")
print("="*80)
print(f"{'Year':<6} {'BAU':>10} {'ETS1':>10} {'ETS2':>10} {'ETS1 Impact':>12} {'ETS2 Impact':>12}")
print("-"*80)

# Show key years
key_years = [2021, 2025, 2030, 2035, 2040, 2045, 2046, 2047, 2048, 2049, 2050]
for year in key_years:
    if year in bau.index:
        bau_val = bau.loc[year]
        ets1_val = ets1.loc[year]
        ets1_impact = ets1_diff.loc[year]

        if year in ets2.index:
            ets2_val = ets2.loc[year]
            ets2_impact = ets2_diff.loc[year]
            print(f"{year:<6} {bau_val:>10.1f} {ets1_val:>10.1f} {ets2_val:>10.1f} "
                  f"{ets1_impact:>11.3f}% {ets2_impact:>11.3f}%")
        else:
            print(f"{year:<6} {bau_val:>10.1f} {ets1_val:>10.1f} {'N/A':>10} "
                  f"{ets1_impact:>11.3f}% {'N/A':>12}")

print("\n" + "="*80)
print("PATTERN ANALYSIS:")
print("="*80)

# Analyze the trend in last 10 years
print("\nLast 10 Years Trend (2041-2050):")
print("-"*80)
for year in range(2041, 2051):
    if year in ets1_diff.index:
        change_ets1 = ets1_diff.loc[year] - \
            ets1_diff.loc[year-1] if year > 2041 else 0
        if year in ets2_diff.index:
            change_ets2 = ets2_diff.loc[year] - \
                ets2_diff.loc[year-1] if year >= 2028 else 0
            print(f"{year}: ETS1 impact = {ets1_diff.loc[year]:.3f}% (Δ={change_ets1:+.3f}pp), "
                  f"ETS2 impact = {ets2_diff.loc[year]:.3f}% (Δ={change_ets2:+.3f}pp)")
        else:
            print(f"{year}: ETS1 impact = {ets1_diff.loc[year]:.3f}% (Δ={change_ets1:+.3f}pp), "
                  f"ETS2 impact = N/A")

# Check carbon prices
print("\n" + "="*80)
print("CARBON PRICING EVOLUTION:")
print("="*80)

carbon_df = pd.read_excel(excel_file, sheet_name='Carbon_Policy', index_col=0)
print("\nCarbon Prices (EUR/tCO2):")
years_carbon = carbon_df.index[2:]
print(f"{'Year':<6} {'ETS1 Price':>12} {'ETS2 Price':>12}")
print("-"*40)
for year in [2021, 2030, 2040, 2045, 2048, 2049, 2050]:
    if year in years_carbon:
        ets1_price = carbon_df.loc[year, carbon_df.columns[0]]
        ets2_price = carbon_df.loc[year,
                                   carbon_df.columns[3]] if year >= 2027 else "N/A"
        print(f"{year:<6} {ets1_price:>12.2f} {str(ets2_price):>12}")

# Check emissions
print("\n" + "="*80)
print("CO2 EMISSIONS EVOLUTION:")
print("="*80)

co2_df = pd.read_excel(excel_file, sheet_name='CO2_Emissions', index_col=0)
print(f"\n{'Year':<6} {'BAU (MtCO2)':>12} {'ETS1 (MtCO2)':>13} {'ETS2 (MtCO2)':>13}")
print("-"*50)
for year in [2021, 2030, 2040, 2045, 2048, 2049, 2050]:
    if year in co2_df.index:
        bau_co2 = co2_df.loc[year, co2_df.columns[0]]
        ets1_co2 = co2_df.loc[year, co2_df.columns[1]]
        ets2_co2 = co2_df.loc[year, co2_df.columns[2]
                              ] if year >= 2027 else "N/A"
        print(f"{year:<6} {bau_co2:>12.1f} {ets1_co2:>13.1f} {str(ets2_co2):>13}")
