"""
Publication-ready map exactly matching the reference image style
Map on left, economic indicators bar chart on right
"""

import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import json
import numpy as np

# Import model data
from src.italy_2021_data import REGIONAL_GDP, REGIONAL_SPECIALIZATION, POPULATION_2021, GDP_2021
from src.definitions import model_definitions

# Get population shares
REGIONAL_POPULATION_SHARES = model_definitions.regional_population_shares

# Set up output directory
output_dir = Path("figures")

print("Creating publication-ready map matching reference image...")
print("=" * 70)

# Load NUTS boundaries
nuts_path = output_dir / "NUTS_RG_20M_2021_4326.geojson"

with open(nuts_path, 'r', encoding='utf-8') as f:
    nuts_data = json.load(f)
nuts = gpd.GeoDataFrame.from_features(nuts_data['features'])

# Filter for Italy NUTS2
nuts2_it = nuts[(nuts["LEVL_CODE"] == 2) & (nuts["CNTR_CODE"] == "IT")].copy()

# Create mapping
nuts2_to_macro = {
    "ITC1": "Northwest", "ITC2": "Northwest", "ITC3": "Northwest", "ITC4": "Northwest",
    "ITH1": "Northeast", "ITH2": "Northeast", "ITH3": "Northeast", "ITH4": "Northeast", "ITH5": "Northeast",
    "ITI1": "Central", "ITI2": "Central", "ITI3": "Central", "ITI4": "Central",
    "ITF1": "South", "ITF2": "South", "ITF3": "South", "ITF4": "South", "ITF5": "South", "ITF6": "South",
    "ITG1": "Islands", "ITG2": "Islands",
}

macro_to_model = {
    "Northwest": "NW", "Northeast": "NE", "Central": "CENTER",
    "South": "SOUTH", "Islands": "ISLANDS"
}

nuts2_it["macro_region"] = nuts2_it["NUTS_ID"].map(nuts2_to_macro)
nuts2_it["model_code"] = nuts2_it["macro_region"].map(macro_to_model)

# Prepare economic data
economic_data = []
for macro_name, model_code in macro_to_model.items():
    gdp_millions = REGIONAL_GDP[model_code]
    pop_share = REGIONAL_POPULATION_SHARES[model_code]
    population = POPULATION_2021 * pop_share
    ind_share = REGIONAL_SPECIALIZATION[model_code]['industry']

    economic_data.append({
        "macro_region": macro_name,
        "gdp_share": (gdp_millions / GDP_2021) * 100,
        "pop_share": pop_share * 100,
        "industrial_share": ind_share * 100,
    })

econ_df = pd.DataFrame(economic_data)

# Dissolve regions
macro_gdf = nuts2_it.dissolve(
    by="macro_region", aggfunc='first', as_index=False)

# Merge economic data
macro_gdf = macro_gdf.merge(econ_df, on="macro_region", how="left")

# Define colors matching reference
colors = {
    "Northwest": "#2B7CB9",
    "Northeast": "#62A845",
    "Central": "#F39237",
    "South": "#D73A42",
    "Islands": "#9467BD",
}

# Create figure with two panels
fig = plt.figure(figsize=(18, 9), dpi=300)
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.1], wspace=0.12)

# ===== LEFT PANEL: MAP =====
ax_map = fig.add_subplot(gs[0])

for macro_name, color in colors.items():
    macro_subset = macro_gdf[macro_gdf["macro_region"] == macro_name]
    macro_subset.plot(ax=ax_map, color=color, alpha=0.95,
                      edgecolor="black", linewidth=1.5)

# Internal boundaries
nuts2_it.boundary.plot(ax=ax_map, linewidth=0.25, color="white", alpha=0.7)

ax_map.set_axis_off()
ax_map.set_xlim([6.5, 18.8])
ax_map.set_ylim([36.5, 47.5])
# Title removed as requested

# Legend for map - positioned much lower to avoid covering Islands
legend_elements = [
    mpatches.Patch(facecolor=colors[name], edgecolor='black',
                   label=name, linewidth=1)
    for name in ["Northwest", "Northeast", "Central", "South", "Islands"]
]
legend = ax_map.legend(handles=legend_elements,
                       title='Macro-regions',
                       loc='lower left',
                       # Moved significantly lower
                       bbox_to_anchor=(0.02, -0.05),
                       fontsize=11,
                       title_fontsize=12,
                       frameon=True,
                       fancybox=False,
                       framealpha=0.95,
                       edgecolor='black',
                       borderpad=0.8)
legend.get_frame().set_linewidth(1.2)

# ===== RIGHT PANEL: BAR CHART =====
ax_bar = fig.add_subplot(gs[1])

# Prepare data for grouped bars (matching reference image order)
regions_order = ["Northwest", "Northeast", "Central", "South", "Islands"]
econ_df = econ_df.set_index('macro_region').loc[regions_order].reset_index()

x = np.arange(len(regions_order))
width = 0.25

# Create bars matching reference colors
gdp_color = "#2B7CB9"      # Blue
pop_color = "#62A845"      # Green
ind_color = "#F39237"      # Orange

bars1 = ax_bar.bar(x - width, econ_df['gdp_share'], width,
                   label='GDP Share (%)', color=gdp_color,
                   alpha=0.9, edgecolor='black', linewidth=0.8)
bars2 = ax_bar.bar(x, econ_df['pop_share'], width,
                   label='Population Share (%)', color=pop_color,
                   alpha=0.9, edgecolor='black', linewidth=0.8)
bars3 = ax_bar.bar(x + width, econ_df['industrial_share'], width,
                   label='Industrial Share (%)', color=ind_color,
                   alpha=0.9, edgecolor='black', linewidth=0.8)

# Add value labels on bars


def add_value_labels(bars, values):
    for bar, val in zip(bars, values):
        height = bar.get_height()
        ax_bar.text(bar.get_x() + bar.get_width()/2., height,
                    f'{val:.0f}%',
                    ha='center', va='bottom', fontsize=9, fontweight='bold')


add_value_labels(bars1, econ_df['gdp_share'])
add_value_labels(bars2, econ_df['pop_share'])
add_value_labels(bars3, econ_df['industrial_share'])

# Chart styling
ax_bar.set_ylabel('Percentage (%)', fontsize=13, fontweight='bold')
# Title removed as requested
ax_bar.set_xticks(x)
ax_bar.set_xticklabels(regions_order, fontsize=11, fontweight='normal')
ax_bar.set_ylim([0, 40])
ax_bar.yaxis.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
ax_bar.set_axisbelow(True)

# Legend
ax_bar.legend(fontsize=10, loc='upper right', frameon=True,
              edgecolor='black', framealpha=0.95, borderpad=0.8)

# Spines
for spine in ax_bar.spines.values():
    spine.set_edgecolor('black')
    spine.set_linewidth(1.2)

# Overall title removed as requested

# Footer credits removed as requested

# Save
output_png = output_dir / "Italy_macro_regions_reference_style.png"
output_pdf = output_dir / "Italy_macro_regions_reference_style.pdf"

plt.savefig(output_png, dpi=300, bbox_inches='tight', facecolor='white')
plt.savefig(output_pdf, format='pdf', bbox_inches='tight', facecolor='white')

print(f"✓ Created: {output_png.name}")
print(f"✓ Created: {output_pdf.name}")

plt.close()

# Print summary
print("\n" + "=" * 70)
print("REGIONAL ECONOMIC INDICATORS SUMMARY (2021)")
print("=" * 70)
print(f"{'Region':<15} {'GDP %':<10} {'Population %':<15} {'Industrial %':<15}")
print("-" * 70)
for _, row in econ_df.iterrows():
    print(f"{row['macro_region']:<15} {row['gdp_share']:>7.1f}   {row['pop_share']:>12.1f}   {row['industrial_share']:>12.1f}")
print("=" * 70)
print("\n✓ Publication-ready visualization complete!")
