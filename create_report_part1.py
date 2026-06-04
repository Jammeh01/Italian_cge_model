"""
CGE-I5 Model Report Generator - Part 1
Title Page, Executive Summary, and Introduction
"""

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from datetime import datetime

def create_part1_report():
    """Create Part 1 of the CGE-I5 Model Report"""
    
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # ==================== TITLE PAGE ====================
    # Add title
    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title.add_run('CGE-I5 MODEL\n\n')
    title_run.font.size = Pt(24)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(0, 0, 128)
    
    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_run = subtitle.add_run('A Computable General Equilibrium Model\nfor Italy with Five Macro-Regions\n\n')
    subtitle_run.font.size = Pt(18)
    subtitle_run.font.bold = True
    
    subtitle2 = doc.add_paragraph()
    subtitle2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle2_run = subtitle2.add_run('Assessing Economic and Environmental Impacts\nof Decarbonization Policies (2021-2040)\n\n\n')
    subtitle2_run.font.size = Pt(14)
    
    # Add spacing
    doc.add_paragraph('\n' * 3)
    
    # Project information
    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.CENTER
    info_run = info.add_run(f'Annual Project Report\n{datetime.now().year}\n\n')
    info_run.font.size = Pt(14)
    
    # Institution
    institution = doc.add_paragraph()
    institution.alignment = WD_ALIGN_PARAGRAPH.CENTER
    institution_run = institution.add_run('Università degli Studi di Milano-Bicocca\n')
    institution_run.font.size = Pt(12)
    
    # Add page break
    doc.add_page_break()
    
    # ==================== TABLE OF CONTENTS ====================
    toc_heading = doc.add_heading('Table of Contents', 0)
    toc_heading.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph('1. Executive Summary', style='List Number')
    doc.add_paragraph('2. Introduction', style='List Number')
    p = doc.add_paragraph('2.1. Background and Motivation', style='List Number 2')
    p = doc.add_paragraph('2.2. Model Overview', style='List Number 2')
    p = doc.add_paragraph('2.3. Objectives and Scope', style='List Number 2')
    p = doc.add_paragraph('2.4. Regional Disaggregation', style='List Number 2')
    doc.add_paragraph('3. Literature Review', style='List Number')
    doc.add_paragraph('4. Model Structure and Methodology', style='List Number')
    doc.add_paragraph('5. Mathematical Formulation', style='List Number')
    doc.add_paragraph('6. Data and Calibration', style='List Number')
    doc.add_paragraph('7. Policy Scenarios', style='List Number')
    doc.add_paragraph('8. Results and Key Findings', style='List Number')
    doc.add_paragraph('9. Conclusions and Policy Implications', style='List Number')
    doc.add_paragraph('References', style='List Number')
    
    doc.add_page_break()
    
    # ==================== EXECUTIVE SUMMARY ====================
    doc.add_heading('1. Executive Summary', 0)
    
    doc.add_paragraph(
        'This report presents the CGE-I5 (Computable General Equilibrium for Italy with 5 regions) '
        'model, a comprehensive recursive dynamic economic model designed to assess the macro-distributional '
        'and environmental impacts of decarbonization policies in Italy. The model provides detailed analysis '
        'of economic, energy, and environmental interactions across Italy\'s five macro-regions from 2021 to 2040.'
    )
    
    doc.add_heading('Key Features', 2)
    
    features = [
        'Multi-regional structure: Disaggregation into five Italian macro-regions (Northwest, Northeast, '
        'Centre, South, and Islands)',
        'Recursive dynamic framework: Annual time steps from 2021 (base year) to 2040',
        'Comprehensive sectoral detail: 11 production sectors including disaggregated energy (renewables, '
        'gas, other energy) and transport sectors',
        'Environmental module: Detailed CO₂ emissions tracking with sector-specific emission factors calibrated '
        'to Italian 2021 data (466.1 MtCO₂)',
        'Climate policy scenarios: Three scenarios including Business-as-Usual (BAU), EU ETS Phase 4 for '
        'industry (ETS1), and extended coverage including buildings and transport (ETS2)',
        'Carbon pricing mechanisms: Market Stability Reserve (MSR) for ETS1 and Price Stability Mechanism '
        '(PSM) for ETS2',
        'Energy transition analysis: Endogenous renewable capacity growth and energy efficiency improvements '
        '(AEEI at 1.8% annually)'
    ]
    
    for feature in features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_heading('Model Calibration', 2)
    
    doc.add_paragraph(
        'The model is calibrated to a 2021 Social Accounting Matrix (SAM) for Italy with the following '
        'key economic aggregates:'
    )
    
    calibration_data = [
        'Base year GDP: €1,782 billion (2021, current prices)',
        'Population: 59.13 million inhabitants',
        'Total CO₂ emissions from fuel combustion: 466.1 MtCO₂',
        'Renewable electricity share: 35% (60 GW installed capacity)',
        'Regional income distribution reflecting actual Italian economic geography'
    ]
    
    for item in calibration_data:
        doc.add_paragraph(item, style='List Bullet')
    
    doc.add_heading('Policy Scenarios', 2)
    
    doc.add_paragraph(
        'The model analyzes three distinct policy scenarios:'
    )
    
    p = doc.add_paragraph()
    p.add_run('Business-as-Usual (BAU): ').bold = True
    p.add_run(
        'Baseline projection without additional carbon pricing beyond existing policies. '
        'Includes autonomous energy efficiency improvements (1.8% annual AEEI) and natural renewable '
        'capacity growth reaching approximately 70% electricity share by 2040.'
    )
    
    p = doc.add_paragraph()
    p.add_run('ETS1 - EU ETS Phase 4 (Industry): ').bold = True
    p.add_run(
        'Implementation of the EU Emissions Trading System Phase 4 for industrial sectors, gas, '
        'other energy, and aviation/maritime transport. Carbon pricing starts at €53.90/tCO₂ in 2021 '
        '(actual EU ETS price) with Market Stability Reserve (MSR) mechanism managing supply. '
        'Price reaches approximately €150/tCO₂ by 2040. Renewable electricity share exceeds 80% by 2040 '
        'with 35% investment acceleration.'
    )
    
    p = doc.add_paragraph()
    p.add_run('ETS2 - Extended Coverage (Buildings & Transport): ').bold = True
    p.add_run(
        'Extended ETS coverage to buildings and road/other transport starting in 2027. ETS2 carbon pricing '
        'begins at €45.0/tCO₂ with Price Stability Mechanism (PSM) maintaining ceiling at €45/tCO₂. '
        'Combined with ETS1, provides comprehensive decarbonization with 60% renewable investment acceleration '
        '(80% in South/Islands). Renewable electricity share exceeds 90% by 2040 with strongest just '
        'transition support.'
    )
    
    doc.add_heading('Key Findings', 2)
    
    doc.add_paragraph(
        'The model simulations reveal important insights into the economic and environmental trade-offs '
        'of decarbonization policies in Italy:'
    )
    
    findings = [
        'Progressive carbon pricing under ETS1 and ETS2 drives significant emissions reductions while '
        'maintaining economic growth through revenue recycling and targeted regional support',
        'Regional impacts vary substantially, with southern regions and islands requiring enhanced support '
        'mechanisms to ensure a just transition',
        'Renewable energy investment accelerates dramatically under carbon pricing scenarios, with '
        'electricity sector reaching 80-90% renewable share by 2040',
        'Energy efficiency improvements (AEEI) play a crucial role in reducing energy demand and '
        'mitigating carbon costs across all scenarios',
        'The Price Stability Mechanism in ETS2 provides price predictability for households and '
        'transport sectors while maintaining decarbonization incentives'
    ]
    
    for finding in findings:
        doc.add_paragraph(finding, style='List Bullet')
    
    doc.add_page_break()
    
    # ==================== INTRODUCTION ====================
    doc.add_heading('2. Introduction', 0)
    
    doc.add_heading('2.1. Background and Motivation', 1)
    
    doc.add_paragraph(
        'Italy faces significant challenges in meeting its climate commitments under the European Green Deal '
        'and the Paris Agreement. As one of the largest economies in the European Union, Italy must achieve '
        'climate neutrality by 2050 while managing the economic and social implications of the energy transition. '
        'The country\'s diverse regional economies, ranging from the industrialized North to the less developed '
        'South and Islands, present unique challenges for policy design and implementation.'
    )
    
    doc.add_paragraph(
        'The European Union\'s climate policy framework, particularly the EU Emissions Trading System (EU ETS), '
        'provides the primary market-based mechanism for emissions reduction. Phase 4 of the EU ETS (2021-2030) '
        'introduced more stringent reduction targets and the Market Stability Reserve to manage allowance supply. '
        'Furthermore, the proposed extension to buildings and transport sectors (ETS2) from 2027 represents a '
        'major expansion of carbon pricing coverage, with potential implications for households and regional equity.'
    )
    
    doc.add_paragraph(
        'Against this backdrop, integrated assessment models capable of analyzing the complex interactions between '
        'economic activity, energy systems, and environmental outcomes are essential tools for policy analysis. '
        'Computable General Equilibrium (CGE) models, in particular, provide a rigorous framework for assessing '
        'economy-wide impacts of climate policies while accounting for market interactions, sectoral linkages, '
        'and distributional effects.'
    )
    
    doc.add_heading('2.2. Model Overview', 1)
    
    doc.add_paragraph(
        'The CGE-I5 model is a recursive dynamic computable general equilibrium model specifically designed for '
        'Italy with explicit regional disaggregation. The model builds on the tradition of multi-sectoral '
        'CGE models (Lofgren et al., 2002) while incorporating key features from energy-economy-environment '
        'models such as ThreeME (Callonnec et al., 2013) and the GTAP-E framework (Burniaux & Truong, 2002).'
    )
    
    doc.add_paragraph(
        'The model\'s distinguishing features include:'
    )
    
    overview_features = [
        'Regional disaggregation: Five macro-regions representing Italy\'s diverse economic geography '
        '(Northwest, Northeast, Centre, South, Islands)',
        
        'Sectoral structure: 11 production sectors with detailed disaggregation of energy (renewables, gas, '
        'other energy) and transport (road, rail, air, water, other)',
        
        'Production technology: Nested Constant Elasticity of Substitution (CES) production functions with '
        'Capital-Labor-Energy-Materials (KLEM) structure, allowing for substitution between factors in response '
        'to price changes',
        
        'Energy-environment module: Explicit tracking of CO₂ emissions by sector and energy carrier, with '
        'emission factors calibrated to Italian 2021 data (ISPRA, 2022)',
        
        'Climate policy instruments: Detailed representation of EU ETS Phase 4 and proposed ETS2, including '
        'Market Stability Reserve and Price Stability Mechanism',
        
        'Recursive dynamics: Forward-looking simulation from 2021 to 2040 with capital accumulation, '
        'labor force changes, and productivity growth',
        
        'Trade specification: Armington assumption for imports and Constant Elasticity of Transformation '
        '(CET) for exports, allowing for imperfect substitution in international trade'
    ]
    
    for feature in overview_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_heading('2.3. Objectives and Scope', 1)
    
    doc.add_paragraph(
        'The primary objectives of the CGE-I5 model are to:'
    )
    
    objectives = [
        'Assess the macroeconomic impacts of carbon pricing policies under EU ETS Phase 4 and its extension '
        'to buildings and transport',
        
        'Quantify sectoral and regional distributional effects of decarbonization policies across Italy\'s '
        'diverse economic landscape',
        
        'Analyze energy system transitions, including renewable energy deployment, energy efficiency '
        'improvements, and fuel switching',
        
        'Evaluate CO₂ emission reduction pathways under different policy scenarios and their consistency '
        'with Italian and EU climate targets',
        
        'Identify regional disparities in climate policy impacts and inform the design of just transition '
        'mechanisms',
        
        'Provide evidence-based insights for policymakers on the economic and environmental trade-offs '
        'of alternative decarbonization strategies'
    ]
    
    for objective in objectives:
        doc.add_paragraph(objective, style='List Bullet')
    
    doc.add_paragraph(
        'The temporal scope of the model extends from 2021 (base year) to 2040, covering the crucial period '
        'for implementing EU climate policies and achieving interim 2030 targets. The model operates with '
        'annual time steps, allowing for detailed tracking of economic and environmental indicators over time.'
    )
    
    doc.add_heading('2.4. Regional Disaggregation', 1)
    
    doc.add_paragraph(
        'A key innovation of the CGE-I5 model is its explicit representation of Italy\'s five macro-regions, '
        'which capture the country\'s significant regional economic heterogeneity:'
    )
    
    # Create a table for regional characteristics
    table = doc.add_table(rows=6, cols=4)
    table.style = 'Light Grid Accent 1'
    
    # Header row
    header_cells = table.rows[0].cells
    header_cells[0].text = 'Region'
    header_cells[1].text = 'Regions Included'
    header_cells[2].text = 'Population Share'
    header_cells[3].text = 'Key Characteristics'
    
    # Make header bold
    for cell in header_cells:
        for paragraph in cell.paragraphs:
            for run in paragraph.runs:
                run.font.bold = True
    
    # Data rows
    regions_data = [
        ['Northwest (NW)', 'Lombardy, Piedmont, Valle d\'Aosta, Liguria', '26.9%',
         'Industrial heartland, high GDP per capita'],
        ['Northeast (NE)', 'Veneto, Trentino-Alto Adige, Friuli-Venezia Giulia, Emilia-Romagna', '19.1%',
         'Manufacturing, services, high income'],
        ['Centre', 'Tuscany, Umbria, Marche, Lazio', '19.9%',
         'Services, public administration, tourism'],
        ['South', 'Abruzzo, Molise, Campania, Puglia, Basilicata, Calabria', '23.3%',
         'Agriculture, lower income, development challenges'],
        ['Islands', 'Sicily, Sardinia', '10.8%',
         'Tourism, agriculture, insularity challenges']
    ]
    
    for i, region_data in enumerate(regions_data):
        row_cells = table.rows[i + 1].cells
        for j, value in enumerate(region_data):
            row_cells[j].text = value
    
    doc.add_paragraph()  # Spacing
    
    doc.add_paragraph(
        'This regional disaggregation is essential for capturing the heterogeneous impacts of climate policies '
        'across Italy. Northern regions, with their higher industrial base and income levels, may have greater '
        'capacity to absorb carbon costs and invest in clean technologies. Southern regions and islands, '
        'characterized by lower GDP per capita and higher unemployment, face distinct challenges and require '
        'targeted support mechanisms to ensure a just transition.'
    )
    
    doc.add_paragraph(
        'The model represents household income and expenditure, labor markets, and regional income transfers, '
        'enabling analysis of distributional impacts and the design of region-specific policy measures. '
        'Regional renewable energy potentials and investment patterns are also explicitly modeled, reflecting '
        'Italy\'s diverse geographical and climatic conditions.'
    )
    
    # Save document
    filename = 'CGE-I5_Model_Report_Part1.docx'
    doc.save(filename)
    print(f"✓ Part 1 of CGE-I5 Model Report created: {filename}")
    print(f"  Sections included:")
    print(f"    - Title Page")
    print(f"    - Table of Contents")
    print(f"    - Executive Summary")
    print(f"    - Introduction (Background, Overview, Objectives, Regional Disaggregation)")
    return filename

if __name__ == "__main__":
    create_part1_report()
