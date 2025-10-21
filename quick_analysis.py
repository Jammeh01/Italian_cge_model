import pandas as pd
import numpy as np

# Load the Excel file
xl = pd.ExcelFile(
    'results/Italian_CGE_Enhanced_Dynamic_Results_20251021_151832.xlsx')

print("="*80)
print("ITALIAN CGE MODEL - DYNAMIC SIMULATION RESULTS (2021-2040)")
print("="*80)

# 1. GDP ANALYSIS
print("\n1. GDP EVOLUTION (Billion EUR)")
print("-"*80)
gdp_df = pd.read_excel(xl, 'Macroeconomy_GDP')
years = [2021, 2025, 2030, 2035, 2040]
for year in years:
    row = gdp_df[gdp_df.iloc[:, 0] == year]
    if not row.empty:
        idx = row.index[0]
        print(f"\n{year}:")
        print(
            f"  BAU:  GDP = €{row.iloc[0, 4]:.1f}B, Per Capita = €{row.iloc[0, 1]:.0f}k")
        print(
            f"  ETS1: GDP = €{row.iloc[0, 5]:.1f}B, Per Capita = €{row.iloc[0, 2]:.0f}k")
        if year >= 2027 and not pd.isna(row.iloc[0, 6]):
            print(
                f"  ETS2: GDP = €{row.iloc[0, 6]:.1f}B, Per Capita = €{row.iloc[0, 3]:.0f}k")

# 2. ENERGY DEMAND
print("\n\n2. TOTAL ENERGY DEMAND (TWh)")
print("-"*80)
energy_df = pd.read_excel(xl, 'Energy_Totals')
for year in [2021, 2030, 2040]:
    row = energy_df[energy_df.iloc[:, 0] == year]
    if not row.empty:
        # Electricity: cols 7, 8, 9
        # Gas: cols 16, 17, 18
        # Other: cols 25, 26, 27
        elec_bau = row.iloc[0, 7] / 1e6  # Convert to TWh
        elec_ets1 = row.iloc[0, 8] / 1e6
        gas_bau = row.iloc[0, 16] / 1e6
        gas_ets1 = row.iloc[0, 17] / 1e6
        other_bau = row.iloc[0, 25] / 1e6
        other_ets1 = row.iloc[0, 26] / 1e6

        print(f"\n{year}:")
        print(
            f"  BAU:  Elec={elec_bau:.1f}, Gas={gas_bau:.1f}, Other={other_bau:.1f} TWh")
        print(
            f"  ETS1: Elec={elec_ets1:.1f}, Gas={gas_ets1:.1f}, Other={other_ets1:.1f} TWh")
        if year >= 2027 and not pd.isna(row.iloc[0, 9]):
            elec_ets2 = row.iloc[0, 9] / 1e6
            gas_ets2 = row.iloc[0, 18] / 1e6
            other_ets2 = row.iloc[0, 27] / 1e6
            print(
                f"  ETS2: Elec={elec_ets2:.1f}, Gas={gas_ets2:.1f}, Other={other_ets2:.1f} TWh")

# 3. CO2 EMISSIONS
print("\n\n3. CO2 EMISSIONS (MtCO2)")
print("-"*80)
co2_df = pd.read_excel(xl, 'CO2_Emissions_Totals')
for year in [2021, 2025, 2030, 2035, 2040]:
    row = co2_df[co2_df.iloc[:, 0] == year]
    if not row.empty:
        # Total CO2: cols 10, 11, 12
        # Intensity: cols 1, 2, 3
        co2_bau = row.iloc[0, 10]
        co2_ets1 = row.iloc[0, 11]
        intensity_bau = row.iloc[0, 1]
        intensity_ets1 = row.iloc[0, 2]

        print(f"\n{year}:")
        print(
            f"  BAU:  Total={co2_bau:.1f} MtCO2, Intensity={intensity_bau:.1f} tCO2/M€")
        print(
            f"  ETS1: Total={co2_ets1:.1f} MtCO2, Intensity={intensity_ets1:.1f} tCO2/M€")
        if year >= 2027 and not pd.isna(row.iloc[0, 12]):
            co2_ets2 = row.iloc[0, 12]
            intensity_ets2 = row.iloc[0, 3]
            print(
                f"  ETS2: Total={co2_ets2:.1f} MtCO2, Intensity={intensity_ets2:.1f} tCO2/M€")

# 4. RENEWABLE ENERGY
print("\n\n4. RENEWABLE CAPACITY (GW)")
print("-"*80)
renewable_df = pd.read_excel(xl, 'Renewable_Capacity')
for year in [2021, 2030, 2040]:
    row = renewable_df[renewable_df.iloc[:, 0] == year]
    if not row.empty:
        # Cumulative capacity: cols 4, 5, 6
        cap_bau = row.iloc[0, 4]
        cap_ets1 = row.iloc[0, 5]

        print(f"\n{year}:")
        print(f"  BAU:  {cap_bau:.1f} GW")
        print(f"  ETS1: {cap_ets1:.1f} GW")
        if year >= 2027 and not pd.isna(row.iloc[0, 6]):
            cap_ets2 = row.iloc[0, 6]
            print(f"  ETS2: {cap_ets2:.1f} GW")

# 5. CARBON PRICING
print("\n\n5. CARBON PRICING (EUR/tCO2)")
print("-"*80)
policy_df = pd.read_excel(xl, 'Climate_Policy')
for year in [2021, 2030, 2040]:
    row = policy_df[policy_df.iloc[:, 0] == year]
    if not row.empty:
        ets1_price = row.iloc[0, 2]
        ets1_revenue = row.iloc[0, 5]

        print(f"\n{year}:")
        print(
            f"  ETS1: Price={ets1_price:.2f} EUR/tCO2, Revenue={ets1_revenue:.2f}B EUR")
        if year >= 2027 and not pd.isna(row.iloc[0, 8]):
            ets2_price = row.iloc[0, 8]
            ets2_revenue = row.iloc[0, 11]
            total_revenue = row.iloc[0, 14]
            print(
                f"  ETS2: Price={ets2_price:.2f} EUR/tCO2, Revenue={ets2_revenue:.2f}B EUR")
            print(f"  Total Revenue: {total_revenue:.2f}B EUR")

# 6. KEY COMPARISONS (2040)
print("\n\n6. KEY COMPARISONS - YEAR 2040")
print("="*80)

# Get 2040 data
gdp_2040 = gdp_df[gdp_df.iloc[:, 0] == 2040]
co2_2040 = co2_df[co2_df.iloc[:, 0] == 2040]
renewable_2040 = renewable_df[renewable_df.iloc[:, 0] == 2040]

if not gdp_2040.empty and not co2_2040.empty:
    gdp_bau = gdp_2040.iloc[0, 4]
    gdp_ets1 = gdp_2040.iloc[0, 5]
    gdp_ets2 = gdp_2040.iloc[0, 6]

    co2_bau = co2_2040.iloc[0, 10]
    co2_ets1 = co2_2040.iloc[0, 11]
    co2_ets2 = co2_2040.iloc[0, 12]

    cap_bau = renewable_2040.iloc[0, 4]
    cap_ets1 = renewable_2040.iloc[0, 5]
    cap_ets2 = renewable_2040.iloc[0, 6]

    print("\nETS1 vs BAU:")
    print(f"  GDP Impact: {((gdp_ets1/gdp_bau - 1)*100):.2f}%")
    print(f"  CO2 Reduction: {((co2_ets1/co2_bau - 1)*100):.2f}%")
    print(
        f"  Renewable Capacity: {cap_ets1:.1f} GW (+{cap_ets1-cap_bau:.1f} GW)")

    print("\nETS2 vs BAU:")
    print(f"  GDP Impact: {((gdp_ets2/gdp_bau - 1)*100):.2f}%")
    print(f"  CO2 Reduction: {((co2_ets2/co2_bau - 1)*100):.2f}%")
    print(
        f"  Renewable Capacity: {cap_ets2:.1f} GW (+{cap_ets2-cap_bau:.1f} GW)")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
