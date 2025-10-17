"""
GDP Visualization Script for Italian CGE Model
Visualizes Real GDP across BAU, ETS1, and ETS2 scenarios (2021-2040)
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 11

# File path
results_file = Path(
    "src/results/Italian_CGE_Enhanced_Dynamic_Results_20251017_101220.xlsx")

# Read the GDP data from the "Macroeconomy_GDP" sheet
print("Reading GDP data from Excel file...")
df_raw = pd.read_excel(results_file, sheet_name='Macroeconomy_GDP')

# Display first few rows to see structure
print("\nRaw data structure:")
print(df_raw.head(10))

# The data is in wide format - need to transpose/restructure
# First row contains scenario labels, need to find the correct columns
# Looking for columns with GDP data for BAU, ETS1, ETS2

# Skip first two rows (headers), and extract the data
df_data = df_raw.iloc[2:].copy()  # Start from row 2 (index 2)
df_data.reset_index(drop=True, inplace=True)

# Identify columns
# First unnamed column should be Year
year_col = df_data.columns[0]
# Find GDP columns - they should contain Real_GDP_Total_Billion_EUR somewhere
gdp_col_bau = None
gdp_col_ets1 = None
gdp_col_ets2 = None

# Check the header structure - row 0 has scenarios
print("\nColumn headers:")
for i, col in enumerate(df_raw.columns):
    print(f"Column {i}: {col} = {df_raw.iloc[0, i]}")

# Based on the structure, identify GDP columns for each scenario
# Typically Real_GDP_Total_Billion_EUR is in specific columns
# Let's find them by checking column names and first row values

# Extract years
years = df_data[year_col].astype(float).values

# Find the GDP columns based on the header row
header_row = df_raw.iloc[0]
for i, (col_name, scenario) in enumerate(zip(df_raw.columns, header_row)):
    if 'Real_GDP' in str(col_name) or i == 2:  # Column index 2 often has BAU GDP
        if scenario == 'BAU' or (gdp_col_bau is None and i == 2):
            gdp_col_bau = df_raw.columns[i]
    if scenario == 'ETS1' and (gdp_col_ets1 is None):
        # Next column after finding ETS1 label
        if 'Real_GDP' in str(df_raw.columns[i]) or i == 5:
            gdp_col_ets1 = df_raw.columns[i]
    if scenario == 'ETS2' and (gdp_col_ets2 is None):
        if 'Real_GDP' in str(df_raw.columns[i]) or i == 6:
            gdp_col_ets2 = df_raw.columns[i]

# If not found automatically, use column indices
if gdp_col_bau is None:
    gdp_col_bau = df_raw.columns[2]  # Usually column 2
if gdp_col_ets1 is None:
    gdp_col_ets1 = df_raw.columns[5]  # Usually column 5
if gdp_col_ets2 is None:
    gdp_col_ets2 = df_raw.columns[6]  # Usually column 6

print(f"\nUsing columns:")
print(f"  Year: {year_col}")
print(f"  BAU GDP: {gdp_col_bau}")
print(f"  ETS1 GDP: {gdp_col_ets1}")
print(f"  ETS2 GDP: {gdp_col_ets2}")

# Extract GDP data
gdp_bau = df_data[gdp_col_bau].astype(float).values
gdp_ets1 = df_data[gdp_col_ets1].astype(float).values
gdp_ets2_raw = df_data[gdp_col_ets2].values

# ETS2 starts from 2027, so filter out NaN values
ets2_mask = pd.notna(gdp_ets2_raw)
years_ets2 = years[ets2_mask]
gdp_ets2 = gdp_ets2_raw[ets2_mask].astype(float)

print(f"\nGDP Data Summary:")
print(f"BAU years: {len(years)} ({years[0]}-{years[-1]})")
print(f"ETS1 years: {len(gdp_ets1)}")
print(f"ETS2 years: {len(gdp_ets2)} ({years_ets2[0]}-{years_ets2[-1]})")

# Create the visualization
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

# ============================================================
# PLOT 1: GDP Evolution for All Scenarios
# ============================================================
ax1.plot(years, gdp_bau, 'o-', linewidth=2.5, markersize=6,
         color='#2E86AB', label='BAU (Business as Usual)', alpha=0.9)
ax1.plot(years, gdp_ets1, 's-', linewidth=2.5, markersize=6,
         color='#A23B72', label='ETS1 (Industry)', alpha=0.9)
ax1.plot(years_ets2, gdp_ets2, '^-', linewidth=2.5, markersize=6,
         color='#F18F01', label='ETS2 (Buildings & Transport)', alpha=0.9)

# Add reference line for base year
ax1.axhline(y=gdp_bau[0], color='gray', linestyle='--', alpha=0.3, linewidth=1)
ax1.text(years[-1], gdp_bau[0], f' Base: €{gdp_bau[0]:.0f}B',
         verticalalignment='bottom', fontsize=9, color='gray')

# Formatting
ax1.set_xlabel('Year', fontsize=12, fontweight='bold')
ax1.set_ylabel('Real GDP (Billion EUR)', fontsize=12, fontweight='bold')
ax1.set_title('Italian Real GDP Evolution (2021-2040)\nComparison Across Climate Policy Scenarios',
              fontsize=14, fontweight='bold', pad=20)
ax1.legend(loc='upper left', fontsize=11, framealpha=0.95)
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.set_xlim(2020, 2041)

# Add value annotations for key years
key_years_idx = [0, len(years)//2, -1]  # 2021, middle year, 2040
for idx in key_years_idx:
    year = years[idx]
    ax1.text(year, gdp_bau[idx], f'€{gdp_bau[idx]:.0f}B',
             ha='center', va='bottom', fontsize=9, color='#2E86AB', fontweight='bold')
    ax1.text(year, gdp_ets1[idx], f'€{gdp_ets1[idx]:.0f}B',
             ha='center', va='bottom', fontsize=9, color='#A23B72', fontweight='bold')

# Add annotation for 2040
ax1.text(years_ets2[-1], gdp_ets2[-1], f'€{gdp_ets2[-1]:.0f}B',
         ha='center', va='bottom', fontsize=9, color='#F18F01', fontweight='bold')

# ============================================================
# PLOT 2: GDP Growth Rate (Year-over-Year)
# ============================================================
# Calculate growth rates
growth_bau = [(gdp_bau[i] - gdp_bau[i-1]) / gdp_bau[i-1] * 100
              for i in range(1, len(gdp_bau))]
growth_ets1 = [(gdp_ets1[i] - gdp_ets1[i-1]) / gdp_ets1[i-1] * 100
               for i in range(1, len(gdp_ets1))]
growth_ets2 = [(gdp_ets2[i] - gdp_ets2[i-1]) / gdp_ets2[i-1] * 100
               for i in range(1, len(gdp_ets2))]

years_growth = years[1:]
years_ets2_growth = years_ets2[1:]

ax2.plot(years_growth, growth_bau, 'o-', linewidth=2, markersize=5,
         color='#2E86AB', label='BAU', alpha=0.9)
ax2.plot(years_growth, growth_ets1, 's-', linewidth=2, markersize=5,
         color='#A23B72', label='ETS1', alpha=0.9)
ax2.plot(years_ets2_growth, growth_ets2, '^-', linewidth=2, markersize=5,
         color='#F18F01', label='ETS2', alpha=0.9)

# Add zero line
ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=1)

# Calculate and display average growth rates
avg_growth_bau = sum(growth_bau) / len(growth_bau)
avg_growth_ets1 = sum(growth_ets1) / len(growth_ets1)
avg_growth_ets2 = sum(growth_ets2) / len(growth_ets2)

# Add average lines
ax2.axhline(y=avg_growth_bau, color='#2E86AB',
            linestyle='--', alpha=0.4, linewidth=1.5)
ax2.axhline(y=avg_growth_ets1, color='#A23B72',
            linestyle='--', alpha=0.4, linewidth=1.5)
ax2.axhline(y=avg_growth_ets2, color='#F18F01',
            linestyle='--', alpha=0.4, linewidth=1.5)

# Add text box with averages
textstr = f'Average Annual Growth Rates:\nBAU: {avg_growth_bau:.2f}%\nETS1: {avg_growth_ets1:.2f}%\nETS2: {avg_growth_ets2:.2f}%'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
ax2.text(0.02, 0.98, textstr, transform=ax2.transAxes, fontsize=10,
         verticalalignment='top', bbox=props)

# Formatting
ax2.set_xlabel('Year', fontsize=12, fontweight='bold')
ax2.set_ylabel('GDP Growth Rate (%)', fontsize=12, fontweight='bold')
ax2.set_title('Year-over-Year GDP Growth Rates',
              fontsize=13, fontweight='bold', pad=15)
ax2.legend(loc='upper right', fontsize=11, framealpha=0.95)
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.set_xlim(2020, 2041)

plt.tight_layout()

# Save the figure
output_file = Path("figures/GDP_Evolution_2021_2040.png")
output_file.parent.mkdir(exist_ok=True)
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"\n✓ Figure saved to: {output_file}")

# Also save as PDF
pdf_file = Path("figures/GDP_Evolution_2021_2040.pdf")
plt.savefig(pdf_file, dpi=300, bbox_inches='tight')
print(f"✓ PDF saved to: {pdf_file}")

plt.show()

# ============================================================
# ADDITIONAL ANALYSIS: GDP Comparison Table
# ============================================================
print("\n" + "="*70)
print("GDP COMPARISON TABLE (Selected Years)")
print("="*70)

# Select key years
key_years = [2021, 2025, 2030, 2035, 2040]
print(f"\n{'Year':<8} {'BAU (€B)':<12} {'ETS1 (€B)':<12} {'ETS2 (€B)':<12} {'ETS1 vs BAU':<15} {'ETS2 vs BAU':<15}")
print("-" * 70)

for year in key_years:
    if year in years:
        idx = list(years).index(year)
        bau_val = gdp_bau[idx]
        ets1_val = gdp_ets1[idx]
        diff_ets1 = ((ets1_val - bau_val) / bau_val) * 100

        if year in years_ets2:
            idx_ets2 = list(years_ets2).index(year)
            ets2_val = gdp_ets2[idx_ets2]
            diff_ets2 = ((ets2_val - bau_val) / bau_val) * 100
            print(
                f"{year:<8} {bau_val:<12.1f} {ets1_val:<12.1f} {ets2_val:<12.1f} {diff_ets1:>+13.2f}% {diff_ets2:>+13.2f}%")
        else:
            print(
                f"{year:<8} {bau_val:<12.1f} {ets1_val:<12.1f} {'N/A':<12} {diff_ets1:>+13.2f}% {'N/A':<15}")

# Summary statistics
print("\n" + "="*70)
print("SUMMARY STATISTICS (2021-2040)")
print("="*70)
print(f"\nBAU Scenario:")
print(f"  Initial GDP (2021): €{gdp_bau[0]:.1f} billion")
print(f"  Final GDP (2040): €{gdp_bau[-1]:.1f} billion")
print(
    f"  Total Growth: {((gdp_bau[-1] - gdp_bau[0]) / gdp_bau[0] * 100):.1f}%")
print(f"  Average Annual Growth: {avg_growth_bau:.2f}%")

print(f"\nETS1 Scenario:")
print(f"  Initial GDP (2021): €{gdp_ets1[0]:.1f} billion")
print(f"  Final GDP (2040): €{gdp_ets1[-1]:.1f} billion")
print(
    f"  Total Growth: {((gdp_ets1[-1] - gdp_ets1[0]) / gdp_ets1[0] * 100):.1f}%")
print(f"  Average Annual Growth: {avg_growth_ets1:.2f}%")
print(
    f"  GDP Impact vs BAU (2040): {((gdp_ets1[-1] - gdp_bau[-1]) / gdp_bau[-1] * 100):+.2f}%")

print(f"\nETS2 Scenario (2027-2040):")
print(f"  Initial GDP (2027): €{gdp_ets2[0]:.1f} billion")
print(f"  Final GDP (2040): €{gdp_ets2[-1]:.1f} billion")
print(
    f"  Total Growth: {((gdp_ets2[-1] - gdp_ets2[0]) / gdp_ets2[0] * 100):.1f}%")
print(f"  Average Annual Growth: {avg_growth_ets2:.2f}%")
print(
    f"  GDP Impact vs BAU (2040): {((gdp_ets2[-1] - gdp_bau[-1]) / gdp_bau[-1] * 100):+.2f}%")

print("\n" + "="*70)
print("✓ GDP Visualization and Analysis Complete!")
print("="*70)
