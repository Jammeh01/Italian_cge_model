"""
CGE-I5 Model Report Generator - Part 3
Model Structure and Methodology
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_page_number(doc):
    """Add page numbers to document"""
    sections = doc.sections
    for section in sections:
        footer = section.footer
        footer.is_linked_to_previous = False
        paragraph = footer.paragraphs[0]
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = paragraph.add_run()

def create_part3_report():
    """Create Part 3 of the CGE-I5 Model Report - Model Structure and Methodology"""
    
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # ==================== MODEL STRUCTURE AND METHODOLOGY ====================
    doc.add_heading('4. Model Structure and Methodology', 0)
    
    doc.add_paragraph(
        'The CGE-I5 model is a recursive dynamic computable general equilibrium model designed to capture '
        'the complex interactions between economic activity, energy systems, and environmental outcomes in '
        'Italy. This section provides a comprehensive description of the model structure, including the '
        'representation of production, consumption, trade, energy-environment linkages, and market clearing '
        'conditions.'
    )
    
    # ===== 4.1 Model Overview =====
    doc.add_heading('4.1. Overall Model Architecture', 1)
    
    doc.add_paragraph(
        'The CGE-I5 model consists of six integrated blocks that collectively determine equilibrium prices '
        'and quantities across all markets:'
    )
    
    blocks = [
        'Production Block: Determines sectoral output, factor demands, and intermediate input requirements',
        'Income-Expenditure Block: Governs household and government income, consumption, and savings',
        'Trade Block: Models international trade flows with import-export decisions',
        'Energy-Environment Block: Tracks energy demand, CO₂ emissions, and climate policy instruments',
        'Market Clearing Block: Ensures supply-demand equilibrium in all markets',
        'Macro Indicators Block: Calculates aggregate economic indicators (GDP, CPI, PPI)'
    ]
    
    for block in blocks:
        doc.add_paragraph(block, style='List Bullet')
    
    doc.add_paragraph(
        'The model employs a bottom-up aggregation approach where sectoral and regional components are '
        'solved simultaneously to achieve general equilibrium. The recursive dynamic framework links '
        'consecutive periods through capital accumulation, labor force evolution, and technological progress.'
    )
    
    # Add a simple flowchart description
    p = doc.add_paragraph()
    p.add_run('Model Flow: ').bold = True
    p.add_run(
        'The model solves iteratively within each time period: (1) Production sectors optimize output '
        'given prices → (2) Factor markets clear → (3) Households and government make consumption decisions → '
        '(4) Energy demand and emissions determined → (5) Trade flows adjust → (6) Market clearing achieved → '
        '(7) Macro indicators calculated. This equilibrium solution for period t becomes the basis for '
        'dynamic updating to period t+1.'
    )
    
    # ===== 4.2 Production Block =====
    doc.add_heading('4.2. Production Block', 1)
    
    doc.add_heading('4.2.1. Sectoral Disaggregation', 2)
    
    doc.add_paragraph(
        'The production side of the economy is disaggregated into 11 sectors, chosen to provide adequate '
        'detail for energy and climate policy analysis while maintaining computational tractability:'
    )
    
    # Create sectors table
    table = doc.add_table(rows=12, cols=3)
    table.style = 'Light Grid Accent 1'
    
    # Header
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Sector Code'
    header_cells[1].text = 'Sector Name'
    header_cells[2].text = 'Key Characteristics'
    
    for cell in header_cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    # Data
    sectors_data = [
        ['AGR', 'Agriculture', 'Primary production, land-intensive'],
        ['IND', 'Industry', 'Manufacturing, construction, mining'],
        ['RENEW', 'Renewables', 'Solar, wind, hydro, biomass electricity'],
        ['GAS', 'Gas', 'Natural gas supply and distribution'],
        ['OENERGY', 'Other Energy', 'Oil products, coal, direct renewables'],
        ['ROAD', 'Road Transport', 'Passenger and freight road transport'],
        ['RAIL', 'Rail Transport', 'Railway passenger and freight'],
        ['AIR', 'Air Transport', 'Aviation services'],
        ['WATER', 'Water Transport', 'Maritime and inland waterways'],
        ['OTRANS', 'Other Transport', 'Other transport services'],
        ['SERVICES', 'Services', 'Aggregated service sectors (14 sub-sectors)']
    ]
    
    for i, sector_data in enumerate(sectors_data):
        row_cells = table.rows[i + 1].cells
        for j, value in enumerate(sector_data):
            row_cells[j].text = value
    
    doc.add_paragraph()
    
    doc.add_heading('4.2.2. Production Technology', 2)
    
    doc.add_paragraph(
        'Production in each sector follows a nested Constant Elasticity of Substitution (CES) structure, '
        'commonly employed in energy-CGE models (Burniaux & Truong, 2002). The nesting structure captures '
        'different degrees of substitutability between input categories:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Level 1 - Gross Output: ').bold = True
    p.add_run(
        'Gross output (Z) is produced using value-added (VA) and intermediate inputs (X) in fixed proportions '
        '(Leontief technology). This reflects the short-run rigidity of input-output relationships.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Level 2 - Value-Added: ').bold = True
    p.add_run(
        'The value-added aggregate combines an Energy-Capital-Labor (EKL) composite with a substitution '
        'elasticity of 0.7. This allows for moderate substitution between energy and other primary factors.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Level 3 - Capital-Labor-Energy: ').bold = True
    p.add_run(
        'A Capital-Labor (KL) composite is formed with substitution elasticity of 0.4, reflecting limited '
        'short-run substitutability. This KL composite then combines with Energy (EN) in the EKL nest.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Level 4 - Energy Composite: ').bold = True
    p.add_run(
        'Energy demand is disaggregated into three carriers (renewables, gas, other energy) with substitution '
        'elasticity of 1.2, allowing for fuel switching in response to relative price changes and carbon pricing.'
    )
    
    doc.add_heading('4.2.3. Factor Markets', 2)
    
    doc.add_paragraph(
        'The model includes two primary factors of production:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Labor: ').bold = True
    p.add_run(
        'Labor is mobile across sectors within each region but immobile across regions (reflecting realistic '
        'labor market segmentation in Italy). The aggregate labor supply in each region is exogenous, growing '
        'according to demographic projections. Wage rates adjust to clear regional labor markets, with '
        'unemployment determined by the gap between labor supply and demand.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Capital: ').bold = True
    p.add_run(
        'Capital is sector-specific in the short run but mobile across sectors in the long run through investment '
        'and depreciation. The capital stock in period t+1 equals the undepreciated capital from period t plus '
        'new investment. The rental rate of capital adjusts to equalize returns across sectors net of adjustment costs.'
    )
    
    # ===== 4.3 Income-Expenditure Block =====
    doc.add_heading('4.3. Income-Expenditure Block', 1)
    
    doc.add_heading('4.3.1. Household Behavior', 2)
    
    doc.add_paragraph(
        'Households are disaggregated into five macro-regions corresponding to Italy\'s geographical divisions. '
        'Household income consists of factor payments (wages and capital returns), transfers from government, '
        'and remittances. Household consumption follows a Linear Expenditure System (LES), which allows for '
        'non-homothetic preferences with subsistence consumption levels.'
    )
    
    doc.add_paragraph(
        'The LES specification ensures that as income rises, expenditure shares shift toward luxury goods and '
        'services, reflecting empirical consumption patterns (Frisch parameters calibrated to Italian data). '
        'Household savings are determined residually after consumption and direct taxes.'
    )
    
    doc.add_heading('4.3.2. Government', 2)
    
    doc.add_paragraph(
        'Government revenue comes from multiple sources:'
    )
    
    gov_revenue = [
        'Direct taxes on household and corporate income (rates exogenous)',
        'Indirect taxes on production and consumption (sector-specific ad valorem rates)',
        'Import tariffs (generally low given EU membership)',
        'Carbon pricing revenue from EU ETS (in policy scenarios)'
    ]
    
    for item in gov_revenue:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_paragraph(
        'Government expenditure includes:'
    )
    
    gov_expenditure = [
        'Public consumption of goods and services (exogenous in real terms)',
        'Transfers to households (including carbon revenue recycling in policy scenarios)',
        'Subsidies to sectors (including renewable energy support)'
    ]
    
    for item in gov_expenditure:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_paragraph(
        'The government fiscal balance (deficit/surplus) is endogenous in the base year but follows an '
        'exogenous path in projections, with adjustments through transfers to maintain fiscal targets.'
    )
    
    # ===== 4.4 Trade Block =====
    doc.add_heading('4.4. Trade Block', 1)
    
    doc.add_heading('4.4.1. Import Specification', 2)
    
    doc.add_paragraph(
        'The model employs the Armington (1969) assumption for imports, treating domestic and imported goods '
        'as imperfect substitutes. Composite demand for each commodity is satisfied by a CES aggregate of '
        'domestic production and imports:'
    )
    
    doc.add_paragraph(
        'Q = [δ_D · D^(-ρ) + δ_M · M^(-ρ)]^(-1/ρ)'
    )
    
    doc.add_paragraph(
        'where Q is composite supply, D is domestic production, M is imports, δ are share parameters, '
        'and ρ = (σ-1)/σ where σ is the Armington elasticity of substitution. The Armington elasticity is '
        'calibrated sector-specifically, with higher values for homogeneous goods (e.g., energy commodities) '
        'and lower values for differentiated products (e.g., services).'
    )
    
    doc.add_heading('4.4.2. Export Specification', 2)
    
    doc.add_paragraph(
        'Exports are modeled using a Constant Elasticity of Transformation (CET) function, allowing producers '
        'to allocate output between domestic sales and exports based on relative prices:'
    )
    
    doc.add_paragraph(
        'Z = [θ_D · D^ρ + θ_E · E^ρ]^(1/ρ)'
    )
    
    doc.add_paragraph(
        'where Z is total production, D is domestic sales, E is exports, θ are share parameters, and ρ is '
        'related to the transformation elasticity. This specification reflects the realistic constraint that '
        'firms face adjustment costs in shifting between domestic and export markets.'
    )
    
    doc.add_paragraph(
        'World prices for imports and exports are exogenous, reflecting Italy\'s small country assumption in '
        'global markets. The exchange rate is the numeraire, fixed at unity, with domestic price flexibility '
        'ensuring equilibrium.'
    )
    
    # ===== 4.5 Energy-Environment Block =====
    doc.add_heading('4.5. Energy-Environment Block', 1)
    
    doc.add_heading('4.5.1. Energy Demand and Supply', 2)
    
    doc.add_paragraph(
        'Energy demand is explicitly tracked for three energy carriers in all sectors and household regions:'
    )
    
    energy_carriers = [
        'Renewables (RENEW): 100% clean electricity from solar, wind, hydro, geothermal, and biomass. '
        'Represents 35% of electricity demand in 2021, growing to 70-90% by 2040 depending on scenario.',
        
        'Gas (GAS): Natural gas for heating, industrial processes, and commercial applications (excluding '
        'power generation). Emission factor: 202 kg CO₂/MWh.',
        
        'Other Energy (OENERGY): Oil products, coal, and direct renewable energy (biomass, solar thermal). '
        'Weighted average emission factor: 350 kg CO₂/MWh.'
    ]
    
    for carrier in energy_carriers:
        doc.add_paragraph(carrier, style='List Bullet')
    
    doc.add_paragraph(
        'Energy efficiency improvements are represented through Autonomous Energy Efficiency Improvement (AEEI), '
        'calibrated at 1.8% annually based on historical trends and IEA projections. AEEI reduces energy intensity '
        'independently of price-induced substitution.'
    )
    
    doc.add_heading('4.5.2. CO₂ Emissions Accounting', 2)
    
    doc.add_paragraph(
        'CO₂ emissions from fuel combustion are calculated by applying sector- and carrier-specific emission '
        'factors to energy consumption:'
    )
    
    doc.add_paragraph(
        'EM_j = Σ_e (E_ej × EF_e)'
    )
    
    doc.add_paragraph(
        'where EM_j is emissions from sector j, E_ej is energy consumption of carrier e by sector j, and '
        'EF_e is the emission factor for carrier e. Emission factors are calibrated to Italian 2021 data:'
    )
    
    ef_table = doc.add_table(rows=4, cols=3)
    ef_table.style = 'Light Grid Accent 1'
    
    ef_header = ef_table.rows[0].cells
    ef_header[0].text = 'Energy Carrier'
    ef_header[1].text = 'Emission Factor (kg CO₂/MWh)'
    ef_header[2].text = '2021 Emissions (MtCO₂)'
    
    for cell in ef_header:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    ef_data = [
        ['Renewables', '0', '0.0'],
        ['Gas', '202', '145.4'],
        ['Other Energy', '350', '224.0']
    ]
    
    for i, ef_row in enumerate(ef_data):
        row_cells = ef_table.rows[i + 1].cells
        for j, value in enumerate(ef_row):
            row_cells[j].text = value
    
    doc.add_paragraph()
    
    doc.add_paragraph(
        'Transport sector emissions are calculated separately for each transport mode (road, rail, air, water, '
        'other) using mode-specific emission factors calibrated to ISPRA (2022) data. Total 2021 transport '
        'emissions: 115.2 MtCO₂.'
    )
    
    doc.add_heading('4.5.3. Climate Policy Instruments', 2)
    
    doc.add_paragraph(
        'The model incorporates detailed representation of the EU Emissions Trading System:'
    )
    
    p = doc.add_paragraph()
    p.add_run('ETS1 (EU ETS Phase 4): ').bold = True
    p.add_run(
        'Covers industry, gas, other energy, aviation, and maritime transport sectors. Carbon price starts at '
        '€53.90/tCO₂ in 2021 (actual EU ETS price), growing at 4% annually with Market Stability Reserve (MSR) '
        'managing supply. No formal price ceiling but practical upper bound of €300/tCO₂. Free allocation to '
        'industry starts at 80%, declining 2% annually.'
    )
    
    p = doc.add_paragraph()
    p.add_run('ETS2 (Buildings & Transport Extension): ').bold = True
    p.add_run(
        'Extends coverage to road transport, other transport, and services (representing buildings) starting in '
        '2027. Carbon price €45.0/tCO₂ with Price Stability Mechanism (PSM) maintaining ceiling at €45/tCO₂ and '
        'floor at €22/tCO₂. Free allocation starts at 60%, declining 3% annually.'
    )
    
    doc.add_paragraph(
        'Carbon costs are incorporated into sectoral production costs, affecting competitiveness and output. '
        'Carbon revenues are recycled through:'
    )
    
    revenue_recycling = [
        'Lump-sum transfers to households (proportional to regional population)',
        'Subsidies for renewable energy investment (higher rates in South and Islands)',
        'Support for energy efficiency improvements',
        'Labor tax reductions (exploring double dividend potential)'
    ]
    
    for mechanism in revenue_recycling:
        doc.add_paragraph(mechanism, style='List Bullet')
    
    # ===== 4.6 Market Clearing and Closure =====
    doc.add_heading('4.6. Market Clearing and Closure Rules', 1)
    
    doc.add_heading('4.6.1. Market Clearing Conditions', 2)
    
    doc.add_paragraph(
        'Equilibrium requires that supply equals demand in all markets:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Commodity Markets: ').bold = True
    p.add_run('Domestic production plus imports equals intermediate demand plus final demand (household, '
              'government, investment) plus exports.')
    
    p = doc.add_paragraph()
    p.add_run('Factor Markets: ').bold = True
    p.add_run('Total factor demand across all sectors equals factor supply. Labor supply is exogenous with '
              'endogenous wage adjustment. Capital supply is sector-specific in short run, mobile through '
              'investment in long run.')
    
    p = doc.add_paragraph()
    p.add_run('Current Account: ').bold = True
    p.add_run('The value of exports plus foreign transfers equals the value of imports plus net foreign savings. '
              'The current account balance follows an exogenous path in projections.')
    
    doc.add_heading('4.6.2. Closure Rules', 2)
    
    doc.add_paragraph(
        'CGE models require closure rules to determine which variables are exogenous and which are endogenous. '
        'The CGE-I5 model employs different closures depending on the simulation period:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Base Year (2021) - Balanced Closure: ').bold = True
    p.add_run(
        'Investment is endogenous, savings-driven. Government balance is fixed to historical value. Exchange '
        'rate is numeraire. This closure ensures calibration to observed data.'
    )
    
    p = doc.add_paragraph()
    p.add_run('Projection Years - Recursive Dynamic Closure: ').bold = True
    p.add_run(
        'Investment is determined by savings and capital inflows. Government transfers adjust to maintain fiscal '
        'balance. Labor supply grows exogenously. Capital stock updates through investment and depreciation. '
        'This closure reflects forward-looking projections with myopic expectations.'
    )
    
    # ===== 4.7 Recursive Dynamics =====
    doc.add_heading('4.7. Recursive Dynamic Framework', 1)
    
    doc.add_heading('4.7.1. Capital Accumulation', 2)
    
    doc.add_paragraph(
        'Capital stock in each sector evolves according to:'
    )
    
    doc.add_paragraph(
        'K_j,t+1 = (1 - δ) × K_j,t + I_j,t'
    )
    
    doc.add_paragraph(
        'where K is capital stock, δ is depreciation rate (5% annually), and I is investment. Investment '
        'allocation across sectors is determined by relative rates of return, subject to adjustment costs.'
    )
    
    doc.add_heading('4.7.2. Labor Force Evolution', 2)
    
    doc.add_paragraph(
        'Labor supply in each region follows demographic projections:'
    )
    
    doc.add_paragraph(
        'LS_r,t+1 = LS_r,t × (1 + g_L,r)'
    )
    
    doc.add_paragraph(
        'where LS is labor supply, g_L is the labor force growth rate (region-specific, generally negative '
        'for Italy reflecting demographic trends). Labor force participation rates are calibrated to ISTAT data '
        'and held constant in projections.'
    )
    
    doc.add_heading('4.7.3. Productivity Growth', 2)
    
    doc.add_paragraph(
        'Total Factor Productivity (TFP) grows exogenously by sector:'
    )
    
    doc.add_paragraph(
        'TFP_j,t+1 = TFP_j,t × (1 + g_TFP,j)'
    )
    
    doc.add_paragraph(
        'TFP growth rates are calibrated to historical trends (0.5-1.0% annually depending on sector), '
        'reflecting technological progress and efficiency improvements independent of factor accumulation.'
    )
    
    doc.add_heading('4.7.4. Energy Efficiency and Renewable Capacity', 2)
    
    doc.add_paragraph(
        'Energy efficiency improves autonomously through AEEI:'
    )
    
    doc.add_paragraph(
        'EI_j,t+1 = EI_j,t × (1 - AEEI)'
    )
    
    doc.add_paragraph(
        'where EI is energy intensity and AEEI = 0.018 (1.8% annual improvement).'
    )
    
    doc.add_paragraph(
        'Renewable electricity capacity expands through investment, accelerated under carbon pricing scenarios:'
    )
    
    doc.add_paragraph(
        'CAP_RENEW,t+1 = CAP_RENEW,t + INV_RENEW,t / CAPEX_RENEW'
    )
    
    doc.add_paragraph(
        'where CAP_RENEW is renewable capacity (GW), INV_RENEW is investment (€), and CAPEX_RENEW is capital '
        'cost per unit capacity. Investment acceleration factors: 35% for ETS1, 60-80% for ETS2 (higher in '
        'South and Islands).'
    )
    
    # ===== 4.8 Solution Algorithm =====
    doc.add_heading('4.8. Solution Algorithm and Numerical Implementation', 1)
    
    doc.add_heading('4.8.1. Optimization Framework', 2)
    
    doc.add_paragraph(
        'The CGE-I5 model is implemented in Pyomo (Python Optimization Modeling Objects), a flexible algebraic '
        'modeling language for optimization. The model is formulated as a Mixed Complementarity Problem (MCP) '
        'but solved using nonlinear programming techniques.'
    )
    
    doc.add_heading('4.8.2. Solver Configuration', 2)
    
    doc.add_paragraph(
        'The model employs IPOPT (Interior Point Optimizer) as the primary solver. IPOPT is well-suited for '
        'large-scale nonlinear optimization problems with the following key advantages:'
    )
    
    ipopt_features = [
        'Robust interior-point algorithm with line-search and trust-region methods',
        'Efficient handling of sparse Jacobian and Hessian matrices',
        'Automatic differentiation for derivative calculations',
        'Sophisticated convergence diagnostics and error reporting'
    ]
    
    for feature in ipopt_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_paragraph(
        'Solver tolerances are set appropriately for economic modeling: overall convergence tolerance 1e-4, '
        'constraint violation tolerance 1e-3. These values balance solution accuracy with computational efficiency.'
    )
    
    doc.add_heading('4.8.3. Calibration and Initialization', 2)
    
    doc.add_paragraph(
        'The base year (2021) calibration proceeds in several steps:'
    )
    
    calibration_steps = [
        'SAM balancing: Ensure row and column sums are consistent',
        'Parameter calculation: Derive share and efficiency parameters from SAM flows',
        'Consistency checks: Verify that parameters reproduce observed quantities and prices',
        'Sensitivity testing: Confirm reasonable response to small perturbations'
    ]
    
    for step in calibration_steps:
        p = doc.add_paragraph(style='List Number')
        p.add_run(step)
    
    doc.add_paragraph(
        'For projection years, the model is initialized using the previous year\'s solution, with dynamic '
        'parameters updated according to exogenous trajectories (labor supply, TFP, world prices, policy variables).'
    )
    
    doc.add_heading('4.8.4. Convergence and Validation', 2)
    
    doc.add_paragraph(
        'Model convergence is monitored through:'
    )
    
    convergence_checks = [
        'Objective function value (minimized deviation from equilibrium)',
        'Maximum constraint violation (all market clearing conditions)',
        'Walras\' Law verification (ensuring one market clearing is redundant)',
        'Economic plausibility checks (positive quantities, reasonable price levels)'
    ]
    
    for check in convergence_checks:
        doc.add_paragraph(check, style='List Bullet')
    
    doc.add_paragraph(
        'Failed convergence triggers diagnostic routines to identify problematic constraints or parameter values. '
        'The model incorporates variable bounds and scaling to improve numerical stability.'
    )
    
    # ===== 4.9 Model Limitations =====
    doc.add_heading('4.9. Model Limitations and Scope', 1)
    
    doc.add_paragraph(
        'As with all models, the CGE-I5 framework involves simplifications and abstractions. Key limitations include:'
    )
    
    limitations = [
        'Static expectations: Agents are myopic, not forming rational expectations about future prices or policies',
        
        'Representative agents: Households aggregated by region; within-region heterogeneity not captured',
        
        'Perfect competition: All markets assumed competitive; market power and strategic behavior excluded',
        
        'Technology representation: Production functions are smooth and continuous; discrete technology choices '
        'not modeled',
        
        'International spillovers: World prices exogenous; feedback effects through international trade limited',
        
        'Non-CO₂ emissions: Focus on CO₂ from fuel combustion; other greenhouse gases and air pollutants excluded',
        
        'Behavioral factors: Standard rational choice assumptions; behavioral biases and social norms not modeled',
        
        'Short-run rigidities: Some adjustment costs included but full range of frictions (e.g., wage stickiness) '
        'not comprehensively modeled'
    ]
    
    for limitation in limitations:
        doc.add_paragraph(limitation, style='List Bullet')
    
    doc.add_paragraph(
        'These limitations are acknowledged in interpreting results. Where possible, sensitivity analysis explores '
        'the implications of alternative assumptions. The model is best viewed as a tool for systematic scenario '
        'comparison rather than precise point prediction.'
    )
    
    # Save document
    filename = 'CGE-I5_Model_Report_Part3.docx'
    doc.save(filename)
    print(f"✓ Part 3 of CGE-I5 Model Report created: {filename}")
    print(f"  Sections included:")
    print(f"    - Model Structure and Methodology")
    print(f"      • Overall Model Architecture")
    print(f"      • Production Block (sectoral structure, technology, factors)")
    print(f"      • Income-Expenditure Block (households, government)")
    print(f"      • Trade Block (Armington imports, CET exports)")
    print(f"      • Energy-Environment Block (energy demand, emissions, climate policy)")
    print(f"      • Market Clearing and Closure Rules")
    print(f"      • Recursive Dynamic Framework")
    print(f"      • Solution Algorithm (Pyomo, IPOPT)")
    print(f"      • Model Limitations")
    return filename

if __name__ == "__main__":
    create_part3_report()
