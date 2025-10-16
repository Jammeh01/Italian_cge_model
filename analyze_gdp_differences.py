"""
Analyze GDP Differences Between Scenarios
"""
import pandas as pd
import numpy as np

# Load data
excel_file = 'results/Italian_CGE_Enhanced_Dynamic_Results_20251015_170800.xlsx'
gdp_df = pd.read_excel(excel_file, sheet_name='Macroeconomy_GDP', index_col=0)

# Extract data
years = gdp_df.index[2:]
bau = gdp_df.iloc[2:, 3].astype(float)
bau.index = years
ets1 = gdp_df.iloc[2:, 4].astype(float)
ets1.index = years
ets2 = gdp_df.iloc[2:, 5].dropna().astype(float)

print("\n" + "="*70)
print("GDP COMPARISON ANALYSIS: BAU vs ETS1 vs ETS2")
print("="*70)

print("\nDETAILED GDP VALUES (Billion EUR) AND DIFFERENCES:")
print("-"*70)
print(f"{'Year':<6} {'BAU':>8} {'ETS1':>8} {'ETS2':>8} {'ETS1 Diff':>12} {'ETS2 Diff':>12}")
print("-"*70)

key_years = [2021, 2025, 2027, 2030, 2035, 2040, 2045, 2050]
for year in key_years:
    if year in bau.index:
        bau_val = bau.loc[year]
        ets1_val = ets1.loc[year]
        ets1_pct = ((ets1_val - bau_val) / bau_val) * 100

        if year >= 2027 and year in ets2.index:
            ets2_val = ets2.loc[year]
            ets2_pct = ((ets2_val - bau_val) / bau_val) * 100
            print(
                f"{year:<6} {bau_val:8.2f} {ets1_val:8.2f} {ets2_val:8.2f} {ets1_pct:>+11.4f}% {ets2_pct:>+11.4f}%")
        else:
            print(
                f"{year:<6} {bau_val:8.2f} {ets1_val:8.2f} {'N/A':>8} {ets1_pct:>+11.4f}% {'N/A':>12}")

print("-"*70)

# Calculate average absolute differences
ets1_diff = ((ets1 - bau) / bau) * 100
ets2_years = ets2.index
bau_ets2 = bau.loc[ets2_years]
ets2_diff = ((ets2 - bau_ets2) / bau_ets2) * 100

print("\nSTATISTICAL SUMMARY:")
print("-"*70)
print(f"ETS1 vs BAU:")
print(f"  Average difference: {ets1_diff.mean():+.4f}%")
print(
    f"  Maximum difference: {ets1_diff.max():+.4f}% (year {ets1_diff.idxmax()})")
print(
    f"  Minimum difference: {ets1_diff.min():+.4f}% (year {ets1_diff.idxmin()})")
print(f"  Standard deviation: {ets1_diff.std():.4f}%")

print(f"\nETS2 vs BAU (2027-2050):")
print(f"  Average difference: {ets2_diff.mean():+.4f}%")
print(
    f"  Maximum difference: {ets2_diff.max():+.4f}% (year {ets2_diff.idxmax()})")
print(
    f"  Minimum difference: {ets2_diff.min():+.4f}% (year {ets2_diff.idxmin()})")
print(f"  Standard deviation: {ets2_diff.std():.4f}%")

print("\n" + "="*70)
print("CUMULATIVE ECONOMIC IMPACT (2021-2050)")
print("="*70)

# Calculate cumulative GDP
bau_cumulative = bau.sum()
ets1_cumulative = ets1.sum()
ets2_cumulative = ets2.sum()

print(f"\nCumulative GDP (sum of all years):")
print(f"  BAU:  {bau_cumulative:,.2f} Billion EUR")
print(f"  ETS1: {ets1_cumulative:,.2f} Billion EUR ({((ets1_cumulative-bau_cumulative)/bau_cumulative)*100:+.4f}%)")
print(
    f"  ETS2: {ets2_cumulative:,.2f} Billion EUR ({((ets2_cumulative-bau.loc[ets2.index].sum())/bau.loc[ets2.index].sum())*100:+.4f}%)")

print("\n" + "="*70)
print("GROWTH RATE ANALYSIS")
print("="*70)

# Calculate annual growth rates
bau_growth = bau.pct_change() * 100
ets1_growth = ets1.pct_change() * 100
ets2_growth = ets2.pct_change() * 100

print(f"\nAverage Annual Growth Rates:")
print(f"  BAU:  {bau_growth.mean():.3f}%")
print(f"  ETS1: {ets1_growth.mean():.3f}%")
print(f"  ETS2: {ets2_growth.mean():.3f}%")

print("\n" + "="*70)
