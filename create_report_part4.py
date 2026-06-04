"""
CGE-I5 Model Report Generator - Part 4
Mathematical Formulation with Key Equations
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
import docx.oxml.ns as ns
from docx.oxml import OxmlElement

def create_part4_report():
    """Create Part 4 of the CGE-I5 Model Report - Mathematical Formulation"""
    
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # ==================== MATHEMATICAL FORMULATION ====================
    doc.add_heading('5. Mathematical Formulation', 0)
    
    doc.add_paragraph(
        'This section presents the mathematical structure of the CGE-I5 model, including the key equations '
        'that define production, consumption, trade, energy demand, emissions, and market equilibrium conditions. '
        'The model consists of behavioral equations (optimizing decisions by economic agents) and equilibrium '
        'conditions (market clearing).'
    )
    
    # ===== 5.1 Notation and Sets =====
    doc.add_heading('5.1. Notation and Sets', 1)
    
    doc.add_heading('5.1.1. Sets', 2)
    
    # Create notation table
    sets_table = doc.add_table(rows=6, cols=2)
    sets_table.style = 'Light Grid Accent 1'
    
    sets_header = sets_table.rows[0].cells
    sets_header[0].text = 'Set'
    sets_header[1].text = 'Description'
    
    for cell in sets_header:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    sets_data = [
        ['j, i ∈ J', 'Production sectors (j=1,...,11)'],
        ['f ∈ F', 'Factors of production: labor (LAB), capital (CAP)'],
        ['r ∈ R', 'Household regions: NW, NE, Centre, South, Islands'],
        ['e ∈ E', 'Energy carriers: renewables (RENEW), gas (GAS), other energy (OENERGY)'],
        ['t ∈ T', 'Time periods: 2021, 2022, ..., 2040']
    ]
    
    for i, sets_row in enumerate(sets_data):
        row_cells = sets_table.rows[i + 1].cells
        for j, value in enumerate(sets_row):
            row_cells[j].text = value
    
    doc.add_paragraph()
    
    doc.add_heading('5.1.2. Variables', 2)
    
    doc.add_paragraph(
        'Endogenous variables (determined by the model):'
    )
    
    # Variables table
    vars_table = doc.add_table(rows=21, cols=2)
    vars_table.style = 'Light Grid Accent 1'
    
    vars_header = vars_table.rows[0].cells
    vars_header[0].text = 'Variable'
    vars_header[1].text = 'Description'
    
    for cell in vars_header:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    vars_data = [
        ['Z_j,t', 'Gross output of sector j at time t'],
        ['VA_j,t', 'Value-added aggregate of sector j'],
        ['KL_j,t', 'Capital-labor composite'],
        ['EN_j,t', 'Energy composite'],
        ['F_f,j,t', 'Demand for factor f by sector j'],
        ['X_i,j,t', 'Intermediate input of good i used by sector j'],
        ['E_e,j,t', 'Energy carrier e consumed by sector j'],
        ['C_r,j,t', 'Consumption of good j by household region r'],
        ['I_j,t', 'Investment demand for good j'],
        ['G_j,t', 'Government consumption of good j'],
        ['EX_j,t', 'Exports of good j'],
        ['IM_j,t', 'Imports of good j'],
        ['Q_j,t', 'Composite supply of good j (domestic + imports)'],
        ['EM_j,t', 'CO₂ emissions from sector j'],
        ['p_z,j,t', 'Producer price of good j'],
        ['p_q,j,t', 'Composite price of good j'],
        ['p_va,j,t', 'Value-added price'],
        ['w_f,t', 'Factor price (wage or capital rental rate)'],
        ['τ_c,t', 'Carbon price (€/tCO₂)'],
        ['Y_r,t', 'Household income in region r']
    ]
    
    for i, vars_row in enumerate(vars_data):
        row_cells = vars_table.rows[i + 1].cells
        for j, value in enumerate(vars_row):
            row_cells[j].text = value
    
    doc.add_paragraph()
    
    doc.add_heading('5.1.3. Parameters', 2)
    
    doc.add_paragraph(
        'Exogenous parameters (calibrated or specified):'
    )
    
    params_list = [
        'α, β, δ, θ: Share and distribution parameters in production and utility functions',
        'σ, ρ: Elasticity parameters (substitution, transformation)',
        'io_i,j: Input-output coefficients',
        'EF_e: Emission factors by energy carrier (kg CO₂/MWh)',
        'AEEI: Autonomous energy efficiency improvement rate',
        'g_L,r, g_K,j, g_TFP,j: Growth rates for labor, capital, and productivity',
        'τ_prod,j, τ_cons,j: Production and consumption tax rates'
    ]
    
    for param in params_list:
        doc.add_paragraph(param, style='List Bullet')
    
    doc.add_paragraph()
    
    # ===== 5.2 Production Block Equations =====
    doc.add_heading('5.2. Production Block Equations', 1)
    
    doc.add_heading('5.2.1. Gross Output Production Function', 2)
    
    doc.add_paragraph(
        'Gross output is produced using value-added and intermediate inputs in fixed proportions (Leontief):'
    )
    
    p = doc.add_paragraph()
    p.add_run('Z_j,t = min[VA_j,t / α_va,j , X_i,j,t / io_i,j]     ∀j,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'This implies:'
    )
    
    p = doc.add_paragraph()
    p.add_run('VA_j,t = α_va,j × Z_j,t     (Value-added requirement)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p = doc.add_paragraph()
    p.add_run('X_i,j,t = io_i,j × Z_j,t     (Intermediate input requirement)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    doc.add_heading('5.2.2. Value-Added Nested CES Production', 2)
    
    doc.add_paragraph(
        'Value-added is produced using a Capital-Labor-Energy nested structure. At the top level, value-added '
        'combines an Energy-Capital-Labor (EKL) composite:'
    )
    
    p = doc.add_paragraph()
    p.add_run('VA_j,t = A_va,j × [α_ekl × EKL_j,t^ρ_va + (1-α_ekl) × KL_j,t^ρ_va]^(1/ρ_va)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where ρ_va = (σ_va - 1)/σ_va and σ_va = 0.7 is the elasticity of substitution between energy and '
        'the capital-labor composite.'
    )
    
    doc.add_paragraph(
        'The Capital-Labor composite is:'
    )
    
    p = doc.add_paragraph()
    p.add_run('KL_j,t = [α_k × K_j,t^ρ_kl + α_l × L_j,t^ρ_kl]^(1/ρ_kl)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where ρ_kl = (σ_kl - 1)/σ_kl and σ_kl = 0.4 is the elasticity of substitution between capital and labor.'
    )
    
    doc.add_heading('5.2.3. Factor Demand Functions', 2)
    
    doc.add_paragraph(
        'Optimal factor demands are derived from cost minimization subject to the production technology. '
        'For capital and labor:'
    )
    
    p = doc.add_paragraph()
    p.add_run('K_j,t = KL_j,t × [α_k × (p_kl,j,t / w_CAP,t)^σ_kl]').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    p = doc.add_paragraph()
    p.add_run('L_j,t = KL_j,t × [α_l × (p_kl,j,t / w_LAB,t)^σ_kl]').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where p_kl,j,t is the price of the capital-labor composite and w_f,t are factor prices.'
    )
    
    doc.add_heading('5.2.4. Energy Demand', 2)
    
    doc.add_paragraph(
        'Energy demand by sector is disaggregated into three carriers with CES substitution:'
    )
    
    p = doc.add_paragraph()
    p.add_run('EN_j,t = [Σ_e δ_e,j × E_e,j,t^ρ_en]^(1/ρ_en)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where ρ_en = (σ_en - 1)/σ_en and σ_en = 1.2 is the elasticity of substitution between energy carriers. '
        'Demand for each energy carrier:'
    )
    
    p = doc.add_paragraph()
    p.add_run('E_e,j,t = EN_j,t × [δ_e,j × (p_en,j,t / p_e,t)^σ_en]').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'Energy efficiency improvements reduce energy intensity:'
    )
    
    p = doc.add_paragraph()
    p.add_run('EN_j,t = (EI_j,0 × (1 - AEEI)^t) × Z_j,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where AEEI = 0.018 (1.8% annual improvement).'
    )
    
    doc.add_paragraph()
    
    # ===== 5.3 Household Behavior =====
    doc.add_heading('5.3. Household Income and Consumption', 1)
    
    doc.add_heading('5.3.1. Household Income', 2)
    
    doc.add_paragraph(
        'Income of household region r consists of factor payments, government transfers, and other income:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Y_r,t = Σ_f (sh_f,r × w_f,t × FS_f,t) + TR_r,t + OY_r,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where sh_f,r is the share of factor f owned by region r, FS_f,t is total factor supply, TR_r,t are '
        'transfers (including carbon revenue recycling), and OY_r,t is other income.'
    )
    
    doc.add_heading('5.3.2. Household Consumption - Linear Expenditure System', 2)
    
    doc.add_paragraph(
        'Household consumption follows a Linear Expenditure System (LES), which allows for subsistence consumption:'
    )
    
    p = doc.add_paragraph()
    p.add_run('C_r,j,t = C_min,r,j + (β_r,j / p_q,j,t) × [Y_r,t^disp - Σ_i p_q,i,t × C_min,r,i]').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where C_min,r,j is subsistence consumption, β_r,j is the marginal budget share, and Y_r,t^disp is '
        'disposable income after taxes. The LES ensures that households first meet subsistence needs before '
        'allocating remaining income according to marginal propensities.'
    )
    
    doc.add_heading('5.3.3. Household Savings', 2)
    
    p = doc.add_paragraph()
    p.add_run('S_r,t = Y_r,t^disp - Σ_j p_q,j,t × C_r,j,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # ===== 5.4 Trade Equations =====
    doc.add_heading('5.4. International Trade', 1)
    
    doc.add_heading('5.4.1. Armington Aggregation (Imports)', 2)
    
    doc.add_paragraph(
        'Composite supply combines domestic production and imports with imperfect substitution:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Q_j,t = A_q,j × [δ_d,j × D_j,t^(-ρ_m,j) + δ_m,j × IM_j,t^(-ρ_m,j)]^(-1/ρ_m,j)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where ρ_m,j = (σ_m,j - 1)/σ_m,j and σ_m,j is the Armington elasticity (sector-specific, typically 2.0).'
    )
    
    doc.add_paragraph(
        'Import demand is derived from cost minimization:'
    )
    
    p = doc.add_paragraph()
    p.add_run('IM_j,t = Q_j,t × [δ_m,j × (p_q,j,t / p_m,j,t)^σ_m,j]').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where p_m,j,t = pwm_j,t × ER_t × (1 + τ_m,j) is the domestic price of imports (world price × exchange '
        'rate × tariff markup).'
    )
    
    doc.add_heading('5.4.2. CET Transformation (Exports)', 2)
    
    doc.add_paragraph(
        'Producers allocate output between domestic sales and exports according to a Constant Elasticity of '
        'Transformation function:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Z_j,t = A_t,j × [θ_d,j × D_j,t^ρ_x,j + θ_e,j × EX_j,t^ρ_x,j]^(1/ρ_x,j)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where ρ_x,j = (σ_x,j + 1)/σ_x,j and σ_x,j is the transformation elasticity (typically 2.0).'
    )
    
    doc.add_paragraph(
        'Export supply is derived from revenue maximization:'
    )
    
    p = doc.add_paragraph()
    p.add_run('EX_j,t = Z_j,t × [θ_e,j × (p_z,j,t / p_e,j,t)^σ_x,j]').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where p_e,j,t = pwe_j,t × ER_t is the domestic price received for exports (world price × exchange rate).'
    )
    
    doc.add_paragraph()
    
    # ===== 5.5 Energy and Emissions =====
    doc.add_heading('5.5. Energy Demand and CO₂ Emissions', 1)
    
    doc.add_heading('5.5.1. Total Energy Demand', 2)
    
    doc.add_paragraph(
        'Total demand for each energy carrier aggregates across sectors and household regions:'
    )
    
    p = doc.add_paragraph()
    p.add_run('E_e,t^total = Σ_j E_e,j,t + Σ_r E_e,r,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'Household energy demand follows similar CES structure with income and price elasticities calibrated to '
        'empirical estimates.'
    )
    
    doc.add_heading('5.5.2. CO₂ Emissions Calculation', 2)
    
    doc.add_paragraph(
        'Emissions from sector j are calculated by applying carrier-specific emission factors:'
    )
    
    p = doc.add_paragraph()
    p.add_run('EM_j,t = Σ_e (E_e,j,t × EF_e)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where emission factors (EF_e) are calibrated to Italian 2021 data:'
    )
    
    ef_list = [
        'EF_RENEW = 0 kg CO₂/MWh (clean renewable electricity)',
        'EF_GAS = 202 kg CO₂/MWh (natural gas combustion)',
        'EF_OENERGY = 350 kg CO₂/MWh (weighted average of oil and coal)'
    ]
    
    for ef in ef_list:
        doc.add_paragraph(ef, style='List Bullet')
    
    doc.add_paragraph(
        'Total CO₂ emissions:'
    )
    
    p = doc.add_paragraph()
    p.add_run('EM_t^total = Σ_j EM_j,t + Σ_r EM_r,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_heading('5.5.3. Carbon Pricing and Policy Costs', 2)
    
    doc.add_paragraph(
        'Carbon cost imposed on sector j depends on policy scenario and sector coverage:'
    )
    
    p = doc.add_paragraph()
    p.add_run('CC_j,t = τ_c,t × EM_j,t × (1 - FA_j,t)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where τ_c,t is the carbon price and FA_j,t is the free allocation rate (declining over time). '
        'For ETS1 sectors:'
    )
    
    p = doc.add_paragraph()
    p.add_run('τ_c,t^ETS1 = 53.90 × (1.04)^(t-2021)     capped at €300/tCO₂').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'For ETS2 sectors (starting 2027):'
    )
    
    p = doc.add_paragraph()
    p.add_run('τ_c,t^ETS2 = max[22, min[45, 45.0 × (1.025)^(t-2027)]]     Price Stability Mechanism').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'Total carbon revenue:'
    )
    
    p = doc.add_paragraph()
    p.add_run('CR_t = Σ_j CC_j,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph()
    
    # ===== 5.6 Market Clearing =====
    doc.add_heading('5.6. Market Clearing Conditions', 1)
    
    doc.add_heading('5.6.1. Commodity Market Equilibrium', 2)
    
    doc.add_paragraph(
        'For each commodity, composite supply equals total demand:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Q_j,t = Σ_i X_j,i,t + Σ_r C_r,j,t + G_j,t + I_j,t     ∀j,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'This ensures that the sum of intermediate demand, household consumption, government consumption, and '
        'investment equals the available composite supply (domestic production plus imports).'
    )
    
    doc.add_heading('5.6.2. Factor Market Equilibrium', 2)
    
    doc.add_paragraph(
        'Total demand for each factor equals its supply:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Σ_j F_f,j,t = FS_f,t     ∀f,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'For labor, supply is exogenous (FS_LAB,t given by demographics), and the wage rate adjusts to clear '
        'the market. Unemployment can occur if wage rigidities are imposed.'
    )
    
    doc.add_paragraph(
        'For capital, the aggregate capital stock is endogenous, evolving through investment and depreciation. '
        'The rental rate adjusts to equalize returns across sectors.'
    )
    
    doc.add_heading('5.6.3. Current Account Balance', 2)
    
    p = doc.add_paragraph()
    p.add_run('Σ_j (pwe_j,t × EX_j,t) + FTRANS_t = Σ_j (pwm_j,t × IM_j,t) + CAB_t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where FTRANS_t are foreign transfers and CAB_t is the current account balance (exogenous in projections).'
    )
    
    doc.add_heading('5.6.4. Walras\' Law', 2)
    
    doc.add_paragraph(
        'By Walras\' Law, if n-1 markets are in equilibrium, the nth market automatically clears. The model '
        'typically drops one market clearing condition (numeraire market) to avoid redundancy. The exchange '
        'rate is chosen as numeraire (ER = 1), with domestic prices adjusting to ensure equilibrium.'
    )
    
    doc.add_paragraph()
    
    # ===== 5.7 Recursive Dynamics =====
    doc.add_heading('5.7. Recursive Dynamic Equations', 1)
    
    doc.add_heading('5.7.1. Capital Accumulation', 2)
    
    p = doc.add_paragraph()
    p.add_run('K_j,t+1 = (1 - δ_K) × K_j,t + I_j,t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where δ_K = 0.05 is the depreciation rate. Investment is allocated across sectors based on relative '
        'returns and adjustment costs.'
    )
    
    doc.add_heading('5.7.2. Labor Supply Evolution', 2)
    
    p = doc.add_paragraph()
    p.add_run('FS_LAB,r,t+1 = FS_LAB,r,t × (1 + g_L,r)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where g_L,r is the region-specific labor force growth rate (negative for most Italian regions due to '
        'demographic decline).'
    )
    
    doc.add_heading('5.7.3. Total Factor Productivity', 2)
    
    p = doc.add_paragraph()
    p.add_run('TFP_j,t+1 = TFP_j,t × (1 + g_TFP,j)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where g_TFP,j is the sector-specific productivity growth rate (0.5-1.0% annually).'
    )
    
    doc.add_heading('5.7.4. Renewable Energy Capacity', 2)
    
    p = doc.add_paragraph()
    p.add_run('CAP_RENEW,t+1 = CAP_RENEW,t + (INV_RENEW,t / CAPEX_RENEW)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'Renewable investment is accelerated under carbon pricing scenarios through subsidies and policy incentives:'
    )
    
    p = doc.add_paragraph()
    p.add_run('INV_RENEW,t = INV_RENEW,t^base × (1 + ACC_FACTOR × Policy_t)').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where ACC_FACTOR = 0.35 for ETS1 and 0.60 for ETS2 (0.80 in South and Islands).'
    )
    
    doc.add_paragraph()
    
    # ===== 5.8 Macro Indicators =====
    doc.add_heading('5.8. Macroeconomic Indicators', 1)
    
    doc.add_heading('5.8.1. Real GDP', 2)
    
    doc.add_paragraph(
        'GDP is calculated using the production approach (sum of value-added):'
    )
    
    p = doc.add_paragraph()
    p.add_run('GDP_t = Σ_j (p_va,j,t × VA_j,t) + Indirect_Taxes_t - Subsidies_t').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'Real GDP is obtained by deflating nominal GDP using the base year price index.'
    )
    
    doc.add_heading('5.8.2. Consumer Price Index', 2)
    
    p = doc.add_paragraph()
    p.add_run('CPI_t = [Σ_j (w_j × p_q,j,t)] / [Σ_j (w_j × p_q,j,0)]').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where w_j are consumption weights from the base year.'
    )
    
    doc.add_heading('5.8.3. Producer Price Index', 2)
    
    p = doc.add_paragraph()
    p.add_run('PPI_t = [Σ_j (v_j × p_z,j,t)] / [Σ_j (v_j × p_z,j,0)]').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where v_j are production weights from the base year.'
    )
    
    doc.add_paragraph()
    
    # ===== 5.9 Solution Method =====
    doc.add_heading('5.9. Solution Method', 1)
    
    doc.add_paragraph(
        'The system of equations forms a square system (equal number of equations and endogenous variables) that '
        'is solved simultaneously for each time period. The model can be formulated as:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Find x* such that F(x*, θ) = 0').font.italic = True
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph(
        'where x* is the vector of endogenous variables, θ is the vector of parameters, and F is the system '
        'of equations (behavioral + equilibrium conditions).'
    )
    
    doc.add_paragraph(
        'The model is implemented in Pyomo and solved using IPOPT with the following algorithm:'
    )
    
    algorithm_steps = [
        'Initialize variables using previous period solution (or calibrated values for base year)',
        'Construct Jacobian matrix of first derivatives',
        'Compute search direction using interior-point method',
        'Perform line search to ensure sufficient decrease in objective',
        'Update variables and check convergence criteria',
        'If not converged and iterations < max, return to step 2',
        'Validate solution: check market clearing, Walras\' Law, positivity constraints'
    ]
    
    for i, step in enumerate(algorithm_steps, 1):
        doc.add_paragraph(f'{i}. {step}', style='List Number')
    
    doc.add_paragraph(
        'Convergence is achieved when the maximum constraint violation falls below tolerance (10⁻⁴) and '
        'complementarity conditions are satisfied.'
    )
    
    # Save document
    filename = 'CGE-I5_Model_Report_Part4.docx'
    doc.save(filename)
    print(f"✓ Part 4 of CGE-I5 Model Report created: {filename}")
    print(f"  Sections included:")
    print(f"    - Mathematical Formulation")
    print(f"      • Notation and Sets (variables, parameters)")
    print(f"      • Production Block Equations (nested CES, factor demands, energy)")
    print(f"      • Household Income and Consumption (LES)")
    print(f"      • International Trade (Armington, CET)")
    print(f"      • Energy Demand and CO₂ Emissions")
    print(f"      • Market Clearing Conditions")
    print(f"      • Recursive Dynamic Equations")
    print(f"      • Macroeconomic Indicators")
    print(f"      • Solution Method")
    return filename

if __name__ == "__main__":
    create_part4_report()
