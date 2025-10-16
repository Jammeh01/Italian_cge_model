import pandas as pd

# Read NEW Excel file with REDUCED CARBON COST PARAMETERS
df = pd.read_excel('src/results/Italian_CGE_Enhanced_Dynamic_Results_20251016_224344.xlsx',
                   sheet_name='Macroeconomy_GDP', skiprows=2)
df.columns = ['Year', 'GDP_pc_BAU', 'GDP_pc_ETS1',
              'GDP_pc_ETS2', 'GDP_BAU', 'GDP_ETS1', 'GDP_ETS2']

print("="*70)
print("GDP COMPARISON: BAU vs ETS1 (AFTER CARBON COST FIXES)")
print("="*70)
print("\nYears 2021-2030:")
for i in range(10):
    year = int(df.loc[i, 'Year'])
    bau = df.loc[i, 'GDP_BAU']
    ets1 = df.loc[i, 'GDP_ETS1']
    diff = ets1 - bau
    pct = 100 * diff / bau
    status = "✓" if diff < 0 else "❌"
    print(f'{year}: BAU={bau:7.2f}, ETS1={ets1:7.2f}, Diff={diff:+6.3f} ({pct:+.3f}%) {status}')

print("\nYears 2040-2050 (every 2 years):")
for i in [19, 21, 23, 25, 27, 29]:
    year = int(df.loc[i, 'Year'])
    bau = df.loc[i, 'GDP_BAU']
    ets1 = df.loc[i, 'GDP_ETS1']
    diff = ets1 - bau
    pct = 100 * diff / bau
    status = "✓" if diff < 0 else "❌"
    print(f'{year}: BAU={bau:7.2f}, ETS1={ets1:7.2f}, Diff={diff:+7.3f} ({pct:+.3f}%) {status}')

print("\n" + "="*70)
print("VALIDATION CHECKS:")
print("="*70)

# Check immediate impact (2022)
if df.loc[1, 'GDP_ETS1'] < df.loc[1, 'GDP_BAU']:
    diff_2022 = df.loc[1, 'GDP_ETS1'] - df.loc[1, 'GDP_BAU']
    pct_2022 = 100 * diff_2022 / df.loc[1, 'GDP_BAU']
    print(f"✅ FIXED: 2022 shows immediate negative impact: {pct_2022:.3f}%")
else:
    print("❌ PROBLEM: 2022 still shows no negative impact")

# Check gradual decline (not sudden)
gaps = []
for i in range(1, 30):
    gap = (df.loc[i, 'GDP_ETS1'] - df.loc[i, 'GDP_BAU']) / \
        df.loc[i, 'GDP_BAU'] * 100
    gaps.append(gap)

# Check for sudden jumps (>2% change in one year)
sudden_jumps = []
for i in range(1, len(gaps)):
    jump = abs(gaps[i] - gaps[i-1])
    if jump > 2.0:
        sudden_jumps.append((2021+i, jump))

if len(sudden_jumps) == 0:
    print("✅ FIXED: Smooth gradual decline (no sudden jumps >2%)")
else:
    print(f"❌ WARNING: Found {len(sudden_jumps)} sudden jumps: {sudden_jumps}")

# Check 2050 impact is reasonable (<5%)
impact_2050 = (df.loc[29, 'GDP_ETS1'] - df.loc[29,
               'GDP_BAU']) / df.loc[29, 'GDP_BAU'] * 100
if -5.0 < impact_2050 < -0.5:
    print(
        f"✅ FIXED: 2050 impact reasonable: {impact_2050:.2f}% (smooth transition)")
else:
    print(f"❌ ISSUE: 2050 impact {impact_2050:.2f}% (expected -0.5% to -5.0%)")

# Check baseline year (2021) identical
if abs(df.loc[0, 'GDP_ETS1'] - df.loc[0, 'GDP_BAU']) < 0.1:
    print(f"✅ Good: 2021 baseline identical (as expected)")

print("\n" + "="*70)
print("ECONOMIC REALISM CHECK:")
print("="*70)
print("Carbon pricing should show:")
print("  Year 1-5:   -0.05% to -0.20% (immediate small effect)")
print("  Year 10:    -0.20% to -0.50% (growing)")
print("  Year 20:    -0.50% to -1.50% (accumulating)")
print("  Year 30:    -1.00% to -3.00% (mature effect)")
print("\nActual results:")
print(f"  2022 (Year 1):  {gaps[0]:.3f}%")
print(f"  2030 (Year 9):  {gaps[8]:.3f}%")
print(f"  2040 (Year 19): {gaps[18]:.3f}%")
print(f"  2050 (Year 29): {gaps[28]:.3f}%")
