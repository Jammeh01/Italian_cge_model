"""
CGE-I5 Model Report Generator - Part 6
Policy Scenarios
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_part6_report():
    """Create Part 6 of the CGE-I5 Model Report - Policy Scenarios"""
    
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # ==================== POLICY SCENARIOS ====================
    doc.add_heading('7. Policy Scenarios and Simulation Design', 0)
    
    doc.add_paragraph(
        'The CGE-I5 model evaluates the economic and environmental impacts of Italy\'s climate policies through '
        'three carefully designed scenarios spanning 2021 to 2040. These scenarios reflect different levels of '
        'ambition in carbon pricing and renewable energy support, aligned with European Union climate targets '
        'and Italy\'s National Energy and Climate Plan (NECP).'
    )
    
    # ===== 7.1 Scenario Overview =====
    doc.add_heading('7.1. Scenario Design Framework', 1)
    
    doc.add_paragraph(
        'The three scenarios are designed to capture a range of policy outcomes, from a baseline business-as-usual '
        'trajectory to ambitious decarbonization pathways:'
    )
    
    # Scenario comparison table
    scenario_table = doc.add_table(rows=5, cols=4)
    scenario_table.style = 'Light Grid Accent 1'
    
    scenario_header = scenario_table.rows[0].cells
    scenario_header[0].text = 'Dimension'
    scenario_header[1].text = 'BAU (Baseline)'
    scenario_header[2].text = 'ETS1 (Moderate)'
    scenario_header[3].text = 'ETS2 (Ambitious)'
    
    for cell in scenario_header:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    scenario_data = [
        ['Carbon Price (2025)', 'No explicit price', '€53.90/tCO₂', '€45.00/tCO₂'],
        ['Price Growth Rate', '—', '4% annually', '5% annually'],
        ['Price Stabilization', '—', 'MSR mechanism', 'PSM ceiling (€120)'],
        ['Regional Support', 'None', 'South/Islands: 80% subsidy', 'South/Islands: 80% subsidy']
    ]
    
    for i, scenario_row in enumerate(scenario_data):
        row_cells = scenario_table.rows[i + 1].cells
        for j, value in enumerate(scenario_row):
            row_cells[j].text = value
    
    doc.add_paragraph()
    
    doc.add_paragraph(
        'All scenarios share common assumptions on demographic trends, productivity growth, and world prices, '
        'isolating the impacts of climate policy design.'
    )
    
    # ===== 7.2 BAU Scenario =====
    doc.add_heading('7.2. BAU (Business-As-Usual) Scenario', 1)
    
    doc.add_heading('7.2.1. Definition and Rationale', 2)
    
    doc.add_paragraph(
        'The BAU scenario represents a counterfactual baseline without strengthened climate policies beyond those '
        'already in place by 2021. It serves as the reference against which policy scenarios are evaluated.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Key Assumptions:').bold = True
    
    bau_assumptions = [
        'No explicit carbon pricing: Sectors not covered by EU ETS face no carbon costs',
        
        'AEEI continues at historical rate: Energy efficiency improves autonomously at 1.8% per year, driven by '
        'technological progress and turnover of capital stock',
        
        'Renewable energy support: Existing subsidies and feed-in tariffs maintained at 2021 levels in real terms, '
        'but no new major support schemes',
        
        'Regulatory baseline: Current energy efficiency standards (e.g., building codes, vehicle emissions) remain, '
        'but no tightening beyond scheduled improvements',
        
        'International context: World fossil fuel prices follow IEA Stated Policies Scenario (STEPS), which assumes '
        'no strengthening of climate ambition globally'
    ]
    
    for assumption in bau_assumptions:
        doc.add_paragraph(assumption, style='List Bullet')
    
    doc.add_heading('7.2.2. Expected Outcomes', 2)
    
    doc.add_paragraph(
        'Under BAU, Italy experiences modest decarbonization driven by autonomous technological change and existing '
        'policies, but insufficient to meet EU 2030 and 2040 targets:'
    )
    
    bau_outcomes = [
        'CO₂ emissions decline from 466 MtCO₂ (2021) to approximately 380 MtCO₂ (2040), a 18% reduction',
        'Renewable electricity share rises from 35% (2021) to ~50% (2040), primarily from cost competitiveness',
        'GDP grows at 1.0-1.2% annually, driven by productivity gains offset by demographic decline',
        'Energy intensity decreases steadily due to AEEI, but fuel mix remains dominated by gas and oil',
        'Regional disparities persist: Northwest maintains highest GDP per capita, South lags in economic development'
    ]
    
    for outcome in bau_outcomes:
        doc.add_paragraph(outcome, style='List Bullet')
    
    doc.add_paragraph(
        'BAU represents the path of least policy intervention, useful for understanding what would happen without '
        'additional climate action.'
    )
    
    # ===== 7.3 ETS1 Scenario =====
    doc.add_heading('7.3. ETS1 (Moderate Ambition) Scenario', 1)
    
    doc.add_heading('7.3.1. Carbon Pricing Mechanism', 2)
    
    doc.add_paragraph(
        'ETS1 implements a carbon pricing system modeled on the EU Emissions Trading System (EU ETS) extension '
        'to sectors currently outside the scheme (transport, buildings, agriculture).'
    )
    
    p = doc.add_paragraph()
    p.add_run('Initial Carbon Price (2025): ').bold = True
    p.add_run('€53.90 per tonne of CO₂')
    
    doc.add_paragraph(
        'This starting price is calibrated to EU ETS market prices in 2023-2024, reflecting the post-reform market '
        'equilibrium with strengthened Linear Reduction Factor (4.2% annually) and Market Stability Reserve (MSR).'
    )
    
    p = doc.add_paragraph()
    p.add_run('Price Trajectory: ').bold = True
    p.add_run('4% annual growth rate (2025-2040)')
    
    doc.add_paragraph(
        'The 4% growth rate ensures the carbon price reaches approximately €120/tCO₂ by 2040, consistent with '
        'European Commission scenarios for achieving 55% emission reduction by 2030 and climate neutrality by 2050.'
    )
    
    # Carbon price trajectory table
    price_table = doc.add_table(rows=5, cols=2)
    price_table.style = 'Light Grid Accent 1'
    
    price_header = price_table.rows[0].cells
    price_header[0].text = 'Year'
    price_header[1].text = 'Carbon Price (€/tCO₂)'
    
    for cell in price_header:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    price_data = [
        ['2025', '53.90'],
        ['2030', '65.62'],
        ['2035', '79.87'],
        ['2040', '97.20']
    ]
    
    for i, price_row in enumerate(price_data):
        row_cells = price_table.rows[i + 1].cells
        for j, value in enumerate(price_row):
            row_cells[j].text = value
    
    doc.add_paragraph()
    
    doc.add_heading('7.3.2. Market Stability Reserve (MSR)', 2)
    
    doc.add_paragraph(
        'ETS1 incorporates the Market Stability Reserve mechanism to prevent excessive price volatility:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Mechanism Design:').bold = True
    
    msr_features = [
        'Threshold monitoring: Total allowances in circulation (TNAC) monitored annually',
        
        'Intake rule: If TNAC exceeds 833 million allowances, 24% of surplus withdrawn from auction and placed in reserve',
        
        'Release rule: If TNAC falls below 400 million allowances, 100 million allowances released from reserve',
        
        'Invalidation: Reserve allowances exceeding previous year\'s auctions are permanently canceled after 2023',
        
        'Price stabilization: MSR prevents price crashes from over-allocation while allowing price signals to drive '
        'mitigation investment'
    ]
    
    for feature in msr_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_paragraph(
        'In CGE-I5, MSR is modeled as a price smoothing mechanism that dampens year-to-year price fluctuations while '
        'maintaining the 4% long-run trend. This reflects the empirical observation that MSR reduces short-term '
        'volatility without fundamentally altering the price trajectory (Perino et al., 2022).'
    )
    
    doc.add_heading('7.3.3. Sectoral Coverage', 2)
    
    doc.add_paragraph(
        'ETS1 extends carbon pricing to sectors beyond the current EU ETS scope:'
    )
    
    # Sectoral coverage table
    coverage_table = doc.add_table(rows=7, cols=3)
    coverage_table.style = 'Light Grid Accent 1'
    
    coverage_header = coverage_table.rows[0].cells
    coverage_header[0].text = 'Sector'
    coverage_header[1].text = 'Coverage'
    coverage_header[2].text = 'Implementation Note'
    
    for cell in coverage_header:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    coverage_data = [
        ['Industry (IND)', '100%', 'Already in EU ETS'],
        ['Energy (GAS, OENERGY)', '100%', 'Large installations in EU ETS'],
        ['Road Transport (ROAD)', '80%', 'Fuel distributors (ETS2 design)'],
        ['Rail/Air/Water (RAIL, AIR, WATER)', '60%', 'Partial coverage, aviation in EU ETS'],
        ['Services (SERVICES)', '40%', 'Buildings heating fuel (ETS2 design)'],
        ['Agriculture (AGR)', '20%', 'Limited to large operations']
    ]
    
    for i, coverage_row in enumerate(coverage_data):
        row_cells = coverage_table.rows[i + 1].cells
        for j, value in enumerate(coverage_row):
            row_cells[j].text = value
    
    doc.add_paragraph()
    
    doc.add_paragraph(
        'Coverage rates reflect practical implementation constraints and align with EU ETS2 proposals for buildings '
        'and road transport.'
    )
    
    doc.add_heading('7.3.4. Revenue Recycling and Regional Support', 2)
    
    doc.add_paragraph(
        'Carbon pricing generates substantial government revenues, which are recycled to support economic transition:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Revenue Allocation:').bold = True
    
    revenue_allocation = [
        '40%: Lump-sum rebates to households (per capita basis), offsetting regressive impacts and maintaining '
        'purchasing power',
        
        '30%: Investment subsidies for renewable energy and energy efficiency, accelerating technology adoption',
        
        '20%: Regional development programs, with 80% subsidy rate for renewable investments in South and Islands '
        'regions to address historical underdevelopment',
        
        '10%: General budget support, reducing public debt or financing other public goods'
    ]
    
    for allocation in revenue_allocation:
        doc.add_paragraph(allocation, style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Southern Italy Acceleration Program:').bold = True
    
    doc.add_paragraph(
        'Recognizing persistent regional disparities, ETS1 includes targeted support for renewable energy deployment '
        'in South and Islands macro-regions:'
    )
    
    south_program = [
        'Renewable investment subsidy: 80% of capital costs for solar, wind, and biomass projects',
        'Rationale: Lower private capital availability and higher perceived risk in Southern regions',
        'Expected impact: Narrow regional gap in renewable capacity from 35% (2021) to 10% (2040)',
        'Co-benefits: Job creation in construction and O&M, reduced electricity imports, local economic stimulus'
    ]
    
    for item in south_program:
        doc.add_paragraph(item, style='List Bullet')
    
    # ===== 7.4 ETS2 Scenario =====
    doc.add_heading('7.4. ETS2 (Ambitious Decarbonization) Scenario', 1)
    
    doc.add_heading('7.4.1. Enhanced Carbon Pricing', 2)
    
    doc.add_paragraph(
        'ETS2 implements more ambitious carbon pricing aligned with achieving climate neutrality by 2050:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Initial Carbon Price (2025): ').bold = True
    p.add_run('€45.00 per tonne of CO₂')
    
    doc.add_paragraph(
        'ETS2 starts at a lower initial price than ETS1, reflecting the proposed EU ETS2 design for buildings and '
        'transport. The lower starting point aims to ensure political acceptability and gradual adjustment.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Price Trajectory: ').bold = True
    p.add_run('5% annual growth rate (2025-2040)')
    
    doc.add_paragraph(
        'The higher growth rate (5% vs. 4% in ETS1) reflects greater ambition, reaching approximately €115/tCO₂ '
        'by 2040. The steeper trajectory drives faster emissions reductions and accelerates the energy transition.'
    )
    
    # ETS2 price trajectory
    ets2_price_data = [
        ['2025', '45.00'],
        ['2030', '57.42'],
        ['2035', '73.24'],
        ['2040', '93.40']
    ]
    
    ets2_price_table = doc.add_table(rows=5, cols=2)
    ets2_price_table.style = 'Light Grid Accent 1'
    
    ets2_header = ets2_price_table.rows[0].cells
    ets2_header[0].text = 'Year'
    ets2_header[1].text = 'Carbon Price (€/tCO₂)'
    
    for cell in ets2_header:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    for i, row_data in enumerate(ets2_price_data):
        row_cells = ets2_price_table.rows[i + 1].cells
        for j, value in enumerate(row_data):
            row_cells[j].text = value
    
    doc.add_paragraph()
    
    doc.add_heading('7.4.2. Price Stability Mechanism (PSM)', 2)
    
    doc.add_paragraph(
        'Unlike ETS1\'s Market Stability Reserve, ETS2 employs a Price Stability Mechanism with explicit price bounds:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Price Ceiling: ').bold = True
    p.add_run('€120 per tonne of CO₂')
    
    doc.add_paragraph(
        'The ceiling protects against excessive price spikes that could threaten economic stability or political '
        'support. If the price reaches €120, additional allowances are released to stabilize the market.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Price Floor: ').bold = True
    p.add_run('€30 per tonne of CO₂ (implicit through reserve price)')
    
    doc.add_paragraph(
        'The floor prevents price collapse from over-allocation or economic shocks, maintaining minimum incentive '
        'for decarbonization investment. Implemented through minimum auction price.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Rationale:').bold = True
    
    doc.add_paragraph(
        'PSM provides greater certainty than MSR for long-term investment planning. Clear price bounds reduce '
        'regulatory risk, potentially lowering the cost of capital for renewable energy projects and accelerating '
        'deployment. The trade-off is less flexibility to adjust to unforeseen emission trends.'
    )
    
    doc.add_heading('7.4.3. Enhanced Regional Policy', 2)
    
    doc.add_paragraph(
        'ETS2 maintains the 80% subsidy for renewable investments in South and Islands but adds complementary policies:'
    )
    
    enhanced_policies = [
        'Skills training programs: €500 million for workforce development in renewable energy installation and '
        'maintenance, addressing local labor market constraints',
        
        'Grid infrastructure upgrades: €2 billion for transmission and distribution improvements in Southern regions, '
        'reducing curtailment of renewable generation',
        
        'Just transition support: €1 billion for communities affected by fossil fuel phase-out, supporting economic '
        'diversification and worker retraining',
        
        'SME green transition fund: €300 million in low-interest loans for small and medium enterprises to adopt '
        'clean technologies and improve energy efficiency'
    ]
    
    for policy in enhanced_policies:
        doc.add_paragraph(policy, style='List Bullet')
    
    doc.add_paragraph(
        'These complementary policies address non-price barriers to decarbonization, particularly important in regions '
        'with lower institutional capacity and higher financing costs.'
    )
    
    # ===== 7.5 Scenario Comparison =====
    doc.add_heading('7.5. Cross-Scenario Analysis Framework', 1)
    
    doc.add_heading('7.5.1. Key Performance Indicators', 2)
    
    doc.add_paragraph(
        'Scenario outcomes are evaluated using a comprehensive set of indicators:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Environmental Effectiveness:').bold = True
    
    env_indicators = [
        'Total CO₂ emissions (MtCO₂) and reduction relative to 2021 baseline',
        'Carbon intensity (kg CO₂ per € of GDP)',
        'Renewable electricity share (%)',
        'Energy intensity (MWh per € million of GDP)'
    ]
    
    for indicator in env_indicators:
        doc.add_paragraph(indicator, style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Economic Impact:').bold = True
    
    econ_indicators = [
        'GDP growth rate and level relative to BAU (%)',
        'Sectoral output changes, particularly energy-intensive industries',
        'Employment effects by sector and region',
        'Household welfare (Hicksian Equivalent Variation)',
        'Carbon pricing revenue and recycling impacts'
    ]
    
    for indicator in econ_indicators:
        doc.add_paragraph(indicator, style='List Bullet')
    
    p = doc.add_paragraph()
    p.add_run('Distributional Outcomes:').bold = True
    
    dist_indicators = [
        'Regional GDP and income disparities',
        'Household consumption by income quintile',
        'Regional renewable capacity distribution',
        'Employment creation in renewable energy by region'
    ]
    
    for indicator in dist_indicators:
        doc.add_paragraph(indicator, style='List Bullet')
    
    doc.add_heading('7.5.2. Simulation Protocol', 2)
    
    doc.add_paragraph(
        'All scenarios are simulated using consistent methodology:'
    )
    
    protocol_steps = [
        'Base year calibration: Model calibrated to 2021 SAM and validation checks passed',
        
        'Recursive dynamic solution: Model solved annually 2022-2040, with forward-looking expectations on prices '
        'and policy trajectory',
        
        'Convergence criteria: Each annual equilibrium solved to tolerance of 0.01% on all market clearing conditions',
        
        'Sensitivity analysis: Key parameters varied ±25% to assess robustness of results',
        
        'Comparison metric: All policy scenarios compared to BAU baseline using same underlying assumptions on '
        'demographics, productivity, and world prices'
    ]
    
    for i, step in enumerate(protocol_steps, 1):
        doc.add_paragraph(f'{i}. {step}', style='List Number')
    
    doc.add_heading('7.5.3. Limitations and Caveats', 2)
    
    doc.add_paragraph(
        'Several important limitations should be kept in mind when interpreting scenario results:'
    )
    
    limitations = [
        'Perfect foresight: Model assumes agents have perfect knowledge of future policies, likely overestimating '
        'smoothness of adjustment',
        
        'No uncertainty: Single deterministic path per scenario, ignoring stochastic shocks and policy uncertainty '
        'that affect real-world investment decisions',
        
        'Technology representation: Renewable energy modeled through aggregate investment and capacity, not explicit '
        'technology choices (solar vs. wind vs. others)',
        
        'Behavioral responses: Consumer preferences assumed stable; does not capture potential shifts in attitudes '
        'toward sustainability or green consumption',
        
        'International spillovers: Rest-of-world treated as exogenous; does not model carbon leakage or impacts of '
        'Italian policy on trade partners',
        
        'Innovation and learning: Technology costs decline exogenously (AEEI); does not endogenize induced innovation '
        'or learning-by-doing effects from policy'
    ]
    
    for limitation in limitations:
        doc.add_paragraph(limitation, style='List Bullet')
    
    doc.add_paragraph(
        'These limitations are inherent to CGE modeling and should be weighed against the model\'s strengths in '
        'capturing economy-wide interactions and general equilibrium effects. Results should be interpreted as '
        'illustrative scenarios rather than precise forecasts.'
    )
    
    # Save document
    filename = 'CGE-I5_Model_Report_Part6.docx'
    doc.save(filename)
    print(f"✓ Part 6 of CGE-I5 Model Report created: {filename}")
    print(f"  Sections included:")
    print(f"    - Policy Scenarios and Simulation Design")
    print(f"      • Scenario Design Framework")
    print(f"      • BAU (Business-As-Usual) Scenario")
    print(f"      • ETS1 (Moderate Ambition) with MSR mechanism")
    print(f"      • ETS2 (Ambitious) with PSM mechanism")
    print(f"      • Cross-Scenario Analysis Framework")
    return filename

if __name__ == "__main__":
    create_part6_report()
