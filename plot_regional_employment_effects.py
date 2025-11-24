"""
Plot regional employment effects from renewable energy investment (ETS2 2040).

This script visualizes job creation across Italian regions from renewable energy
deployment, showing both construction phase job-years and permanent O&M employment.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Regional renewable capacity shares from ETS2 2040 simulation
regions = ['South', 'Islands', 'Northwest', 'Centre', 'Northeast']
capacity_shares = [42.0, 23.9, 13.7, 11.9, 8.5]  # percentage

# Total additional capacity 2021-2040 in ETS2: 192 GW (252 GW total - 60 GW baseline)
total_additional_capacity_gw = 192

# Calculate regional capacity in GW
regional_capacity_gw = [total_additional_capacity_gw *
                        (share/100) for share in capacity_shares]

# Employment multipliers (based on IRENA 2021, Fragkos et al. 2021)
# mid-point of 15-20 jobs/MW (cumulative job-years)
construction_jobs_per_mw = 17.5
om_jobs_per_mw = 0.4  # mid-point of 0.3-0.5 jobs/MW (permanent)

# Calculate employment effects
construction_jobs = [cap * 1000 * construction_jobs_per_mw /
                     1000 for cap in regional_capacity_gw]  # thousands
om_jobs = [cap * 1000 * om_jobs_per_mw /
           1000 for cap in regional_capacity_gw]  # thousands

# Create visualization
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Color scheme
colors = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#9B59B6']

# Panel 1: Construction Phase Job-Years
ax1 = axes[0]
bars1 = ax1.barh(regions, construction_jobs, color=colors,
                 alpha=0.85, edgecolor='black', linewidth=1.2)

# Add value labels
for i, (bar, value) in enumerate(zip(bars1, construction_jobs)):
    ax1.text(value + 20, bar.get_y() + bar.get_height()/2,
             f'{value:.0f}k job-years\n({capacity_shares[i]:.1f}% capacity)',
             va='center', ha='left', fontsize=10, fontweight='bold')

ax1.set_xlabel('Construction Phase Employment (Thousand Job-Years)',
               fontsize=11, fontweight='bold')
ax1.set_title('(a) Construction Phase Job Creation\n2021-2040 Renewable Buildout',
              fontsize=12, fontweight='bold', pad=15)
ax1.grid(True, alpha=0.3, linestyle=':', linewidth=0.8, axis='x')
ax1.set_xlim(0, max(construction_jobs) * 1.25)

# Panel 2: Permanent O&M Jobs
ax2 = axes[1]
bars2 = ax2.barh(regions, om_jobs, color=colors, alpha=0.85,
                 edgecolor='black', linewidth=1.2)

# Add value labels
for i, (bar, value, cap) in enumerate(zip(bars2, om_jobs, regional_capacity_gw)):
    ax2.text(value + 0.5, bar.get_y() + bar.get_height()/2,
             f'{value:.1f}k jobs\n({cap:.1f} GW)',
             va='center', ha='left', fontsize=10, fontweight='bold')

ax2.set_xlabel('Permanent O&M Employment (Thousand Jobs)',
               fontsize=11, fontweight='bold')
ax2.set_title('(b) Permanent Operations & Maintenance Jobs\nSteady-State Employment (2040)',
              fontsize=12, fontweight='bold', pad=15)
ax2.grid(True, alpha=0.3, linestyle=':', linewidth=0.8, axis='x')
ax2.set_xlim(0, max(om_jobs) * 1.25)

# Overall title
fig.suptitle('Regional Employment Effects from Renewable Energy Investment\nETS2 Scenario (2040) - 192 GW Additional Capacity',
             fontsize=14, fontweight='bold', y=0.98)

# Add summary box
total_construction = sum(construction_jobs)
total_om = sum(om_jobs)
summary_text = (f'National Total:\n'
                f'Construction: {total_construction:.0f}k job-years\n'
                f'Permanent O&M: {total_om:.1f}k jobs\n'
                f'\n'
                f'Multipliers Used:\n'
                f'Construction: 17.5 jobs/MW\n'
                f'O&M: 0.4 jobs/MW')

fig.text(0.5, -0.02, summary_text, ha='center', fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
         family='monospace')

plt.tight_layout(rect=[0, 0.05, 1, 0.96])

# Save figure
plt.savefig('results/regional_employment_renewable_investment.png',
            dpi=300, bbox_inches='tight')
plt.savefig('results/regional_employment_renewable_investment.pdf',
            bbox_inches='tight')
print("✓ Regional employment effects plot saved to results/")

plt.show()
