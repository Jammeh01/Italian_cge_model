"""
CGE-I5 Model Report Generator - Part 2
Literature Review
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_part2_report():
    """Create Part 2 of the CGE-I5 Model Report - Literature Review"""
    
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # ==================== LITERATURE REVIEW ====================
    doc.add_heading('3. Literature Review', 0)
    
    doc.add_paragraph(
        'The CGE-I5 model builds upon a rich literature spanning computable general equilibrium modeling, '
        'energy-economy-environment interactions, and climate policy analysis. This section reviews the '
        'key theoretical and empirical contributions that inform the model\'s design and implementation.'
    )
    
    # ===== 3.1 CGE Modeling Framework =====
    doc.add_heading('3.1. Computable General Equilibrium Modeling Framework', 1)
    
    doc.add_paragraph(
        'Computable General Equilibrium (CGE) models have become the standard tool for economy-wide policy '
        'analysis, providing a coherent framework for capturing complex interactions between markets, sectors, '
        'and economic agents. The theoretical foundations of CGE modeling trace back to Walras (1874) and the '
        'Arrow-Debreu general equilibrium theory (Arrow & Debreu, 1954), which demonstrates the existence of '
        'competitive equilibrium under specific conditions.'
    )
    
    doc.add_paragraph(
        'Modern applied CGE modeling was pioneered by Johansen (1960) and further developed by Scarf (1967), '
        'who introduced computational algorithms for solving large-scale general equilibrium systems. The '
        'application of CGE models to developing countries and policy analysis was advanced significantly by '
        'Dervis, de Melo, and Robinson (1982), establishing best practices for model structure and calibration.'
    )
    
    doc.add_paragraph(
        'Lofgren, Harris, and Robinson (2002) provide a comprehensive standard CGE model framework that has '
        'influenced numerous applications, including the present work. Their formulation emphasizes the '
        'importance of Social Accounting Matrices (SAMs) for calibration and the use of flexible functional '
        'forms, particularly Constant Elasticity of Substitution (CES) functions, to represent production and '
        'consumption behavior.'
    )
    
    doc.add_paragraph(
        'For regional and multi-regional CGE models, Dixon and Parmenter (1996) and Partridge and Rickman (2010) '
        'demonstrate the importance of capturing spatial heterogeneity in economic structure and factor markets. '
        'Their work highlights how regional models can identify distributional impacts that are obscured in '
        'national aggregate models.'
    )
    
    # ===== 3.2 Energy-Economy-Environment Models =====
    doc.add_heading('3.2. Energy-Economy-Environment CGE Models', 1)
    
    doc.add_paragraph(
        'The integration of energy and environmental modules into CGE frameworks represents a major strand of '
        'literature relevant to climate policy analysis. Burniaux and Truong (2002) developed the GTAP-E model, '
        'which extends the Global Trade Analysis Project (GTAP) model with detailed energy sectors and CO₂ '
        'emissions tracking. Their nested production structure, with explicit representation of energy-capital '
        'complementarity, has become a standard approach in energy-CGE models.'
    )
    
    doc.add_paragraph(
        'The Multi-sector Multi-region Macro-econometric Model (ThreeME), developed by Callonnec et al. (2013) '
        'and refined by Reynès et al. (2019), provides a particularly relevant reference for the CGE-I5 model. '
        'ThreeME combines CGE modeling with dynamic econometric estimation and detailed energy sector '
        'disaggregation. Key features adopted in CGE-I5 include:'
    )
    
    threemme_features = [
        'Nested CES production functions with Capital-Labor-Energy-Materials (KLEM) structure',
        'Autonomous Energy Efficiency Improvements (AEEI) to capture technological progress',
        'Detailed representation of electricity generation by technology (renewables, fossil fuels)',
        'Recursive dynamic framework with forward-looking investment decisions',
        'Energy demand disaggregated by sector and energy carrier'
    ]
    
    for feature in threemme_features:
        doc.add_paragraph(feature, style='List Bullet')
    
    doc.add_paragraph(
        'Böhringer and Rutherford (2008) provide important insights on representing environmental policy '
        'constraints in CGE models, particularly the treatment of emissions permits and carbon pricing mechanisms. '
        'Their analysis of the EU ETS demonstrates the importance of modeling allowance allocation methods and '
        'banking/borrowing provisions.'
    )
    
    doc.add_paragraph(
        'The PRIMES model (Capros et al., 2013), widely used for EU energy policy analysis, offers a detailed '
        'bottom-up representation of energy technologies that complements top-down CGE approaches. The CGE-I5 '
        'model adopts a hybrid approach, using PRIMES-derived energy technology parameters while maintaining '
        'the general equilibrium framework.'
    )
    
    # ===== 3.3 Climate Policy and Carbon Pricing =====
    doc.add_heading('3.3. Climate Policy and Carbon Pricing Literature', 1)
    
    doc.add_paragraph(
        'The economic analysis of carbon pricing mechanisms has evolved considerably since Pigou\'s (1920) '
        'foundational work on externalities and corrective taxation. Nordhaus (1991, 2008, 2017) has been '
        'instrumental in developing integrated assessment models (IAMs) that link economic growth, emissions, '
        'climate change, and damages, providing a framework for determining optimal carbon prices. His DICE '
        '(Dynamic Integrated Climate-Economy) model demonstrates the importance of intertemporal optimization '
        'in climate policy design.'
    )
    
    doc.add_paragraph(
        'The EU ETS, as the world\'s largest carbon market, has generated substantial research on market-based '
        'climate policy. Ellerman, Convery, and de Perthuis (2010) provide a comprehensive assessment of the '
        'first phase of the EU ETS, highlighting lessons on allowance allocation, price volatility, and market '
        'efficiency. Subsequent work by Perino and Willner (2016) and Bruninx et al. (2020) analyzes the Market '
        'Stability Reserve (MSR) introduced in Phase 4, which is explicitly modeled in the CGE-I5 framework.'
    )
    
    doc.add_paragraph(
        'The proposed extension of the EU ETS to buildings and transport (ETS2) has been analyzed by Flachsland '
        'et al. (2020) and Edenhofer et al. (2021), who examine the implications for distributional impacts and '
        'social acceptability. Their findings emphasize the need for complementary policies, including social '
        'measures and targeted support for vulnerable households—considerations incorporated into the CGE-I5 '
        'policy scenarios.'
    )
    
    doc.add_paragraph(
        'Goulder (1995) and Parry and Williams (1999) establish the theoretical foundation for revenue recycling '
        'in carbon taxation, demonstrating how returning carbon revenues through reduced distortionary taxes can '
        'achieve a "double dividend" of environmental improvement and economic efficiency gains. The CGE-I5 model '
        'implements several revenue recycling mechanisms informed by this literature.'
    )
    
    # ===== 3.4 Energy Transition and Renewable Energy =====
    doc.add_heading('3.4. Energy Transition and Renewable Energy Integration', 1)
    
    doc.add_paragraph(
        'The literature on energy transitions provides crucial insights for modeling the shift toward renewable '
        'energy systems. Grubb, Hourcade, and Neuhoff (2014) analyze the "energy transitions paradox," where '
        'long-term decarbonization goals require near-term investments despite policy uncertainty. Their work '
        'informs the CGE-I5 model\'s treatment of renewable energy investment under alternative policy scenarios.'
    )
    
    doc.add_paragraph(
        'Creutzig et al. (2017) and IRENA (2019) document the dramatic cost reductions in solar and wind '
        'technologies, which have fundamentally altered the economics of decarbonization. These cost trajectories '
        'are incorporated into the CGE-I5 model\'s renewable energy investment functions and technology choice '
        'mechanisms.'
    )
    
    doc.add_paragraph(
        'The integration of variable renewable energy (VRE) into power systems presents technical and economic '
        'challenges analyzed by Hirth, Ueckerdt, and Edenhofer (2015) and Joskow (2011). While the CGE-I5 model '
        'does not explicitly model electricity dispatch and system operations, it incorporates effective capacity '
        'values and system integration costs based on this literature.'
    )
    
    doc.add_paragraph(
        'Jacobson et al. (2017) and Brown et al. (2018) explore pathways to 100% renewable energy systems, '
        'demonstrating technical feasibility while acknowledging economic and institutional challenges. The '
        'CGE-I5 model\'s high renewable penetration scenarios (>90% by 2040 under ETS2) are informed by these '
        'technical assessments.'
    )
    
    # ===== 3.5 Regional and Distributional Impacts =====
    doc.add_heading('3.5. Regional and Distributional Impacts of Climate Policy', 1)
    
    doc.add_paragraph(
        'The distributional impacts of climate policy have received increasing attention in recent years, '
        'particularly concerns about "just transitions" and regional equity. Bauer et al. (2020) and Hirth '
        'and Steckel (2016) demonstrate how carbon pricing can disproportionately affect lower-income households '
        'and regions dependent on carbon-intensive industries.'
    )
    
    doc.add_paragraph(
        'For Italy specifically, Antonioli and Mazzanti (2017) analyze regional disparities in environmental '
        'performance and the implications for climate policy design. Their work highlights the structural '
        'differences between Northern and Southern Italy, including industrial composition, energy efficiency, '
        'and adaptive capacity—factors explicitly represented in the CGE-I5 regional disaggregation.'
    )
    
    doc.add_paragraph(
        'Maestre-Andrés, Drews, and van den Bergh (2019) review public acceptability of carbon taxes and identify '
        'revenue recycling through social transfers as crucial for political feasibility. The CGE-I5 model\'s '
        'policy scenarios incorporate region-specific support mechanisms, particularly for Southern Italy and the '
        'Islands, informed by these insights.'
    )
    
    doc.add_paragraph(
        'The concept of "just transition," emphasized by the International Labour Organization (ILO, 2015) and '
        'incorporated into EU policy frameworks, requires attention to employment effects and regional development '
        'impacts. Hafstead and Williams (2020) provide analytical frameworks for assessing labor market transitions, '
        'which inform the CGE-I5 model\'s labor market module.'
    )
    
    # ===== 3.6 Italian Energy and Climate Policy Context =====
    doc.add_heading('3.6. Italian Energy and Climate Policy Context', 1)
    
    doc.add_paragraph(
        'Italy\'s National Energy and Climate Plan (NECP) sets forth ambitious targets for 2030, including 30% '
        'reduction in greenhouse gas emissions (compared to 2005) and 30% renewable energy share in final energy '
        'consumption (MISE, 2019). The CGE-I5 model scenarios are designed to assess pathways consistent with '
        'these targets and their extension to 2040.'
    )
    
    doc.add_paragraph(
        'Gazzetta Ufficiale (2020) outlines Italy\'s transposition of EU climate and energy directives, including '
        'specific provisions for the industrial and power sectors under the EU ETS. The CGE-I5 model\'s ETS1 '
        'scenario explicitly represents these sectoral coverages and compliance obligations.'
    )
    
    doc.add_paragraph(
        'Recent studies on Italy\'s decarbonization pathways include Sgobbi et al. (2016), who analyze deep '
        'decarbonization scenarios using the TIMES-Italy model, and Giarola et al. (2013), who examine the role '
        'of natural gas in Italy\'s energy transition. These studies provide important cross-validation for the '
        'CGE-I5 model\'s energy system trajectories.'
    )
    
    doc.add_paragraph(
        'The COVID-19 pandemic and associated economic disruptions have added complexity to energy and climate '
        'policy analysis. Studies by Forster et al. (2020) and Le Quéré et al. (2020) document the temporary '
        'emissions reductions during lockdowns and the subsequent recovery patterns. While the CGE-I5 base year '
        '(2021) represents a partial recovery phase, the model structure is designed to capture longer-term '
        'structural transitions rather than short-term shocks.'
    )
    
    # ===== 3.7 Recursive Dynamic Modeling =====
    doc.add_heading('3.7. Recursive Dynamic CGE Modeling', 1)
    
    doc.add_paragraph(
        'The recursive dynamic approach adopted in the CGE-I5 model follows the tradition established by Lau, '
        'Pahlke, and Rutherford (2002) and Robinson and Meijl (2006). Unlike fully dynamic models with '
        'intertemporal optimization, recursive dynamic models solve a sequence of static equilibria linked by '
        'dynamic updating rules for capital, labor, productivity, and other state variables.'
    )
    
    doc.add_paragraph(
        'Van der Mensbrugghe (2005) provides a comprehensive treatment of recursive dynamic CGE models in the '
        'context of long-run projections, emphasizing the importance of consistent calibration and plausible '
        'dynamic parameters. The CGE-I5 model follows his recommendations for capital accumulation (investment-driven '
        'with depreciation), labor force evolution (demographic projections), and productivity growth (sector-specific '
        'total factor productivity).'
    )
    
    doc.add_paragraph(
        'Wing (2004) discusses the treatment of energy-economy dynamics in recursive CGE models, particularly '
        'the representation of energy efficiency improvements (AEEI) and technological change in the energy sector. '
        'The CGE-I5 model adopts an AEEI rate of 1.8% annually, consistent with empirical estimates for advanced '
        'economies (IEA, 2020).'
    )
    
    doc.add_paragraph(
        'Faehn et al. (2020) demonstrate the importance of modeling expectations and policy credibility in recursive '
        'dynamic frameworks, particularly for climate policy analysis. While the CGE-I5 model employs myopic '
        'expectations (agents base decisions on current and past information), sensitivity analysis explores the '
        'implications of alternative expectation formations.'
    )
    
    # ===== 3.8 Model Validation and Comparison =====
    doc.add_heading('3.8. Model Validation and Comparison with Existing Studies', 1)
    
    doc.add_paragraph(
        'The validation of CGE models against historical data and comparison with alternative modeling approaches '
        'is essential for establishing credibility. Scrieciu (2007) and Wing (2004) discuss various validation '
        'strategies, including historical validation (backcasting), cross-model comparison, and expert elicitation '
        'for key parameters.'
    )
    
    doc.add_paragraph(
        'For Italian applications, the CGE-I5 model results can be compared with findings from:'
    )
    
    comparison_models = [
        'TIMES-Italy model (Sgobbi et al., 2016): Bottom-up energy system optimization model providing '
        'detailed technology pathways',
        
        'GTAP-based studies (e.g., Peters & Hertel, 2017): Multi-region global CGE with Italy as a region, '
        'offering international trade perspectives',
        
        'PRIMES-Italy (E3MLab, 2020): Partial equilibrium energy system model used for EU policy analysis',
        
        'ThreeME-France (Reynès et al., 2019): Similar model structure applied to France, providing methodological '
        'insights'
    ]
    
    for model in comparison_models:
        doc.add_paragraph(model, style='List Bullet')
    
    doc.add_paragraph(
        'Systematic comparison with these models, where comparable scenarios exist, provides confidence bounds '
        'for the CGE-I5 projections and highlights areas of model uncertainty or divergence.'
    )
    
    # ===== 3.9 Summary and Research Gap =====
    doc.add_heading('3.9. Synthesis and Research Gap Addressed by CGE-I5', 1)
    
    doc.add_paragraph(
        'The literature review reveals a mature body of research on CGE modeling, energy-economy interactions, '
        'and climate policy analysis. However, several gaps remain that the CGE-I5 model aims to address:'
    )
    
    gaps = [
        'Limited regional disaggregation in existing Italian CGE models: While national-level models exist, '
        'few provide the five-region disaggregation needed to assess distributional impacts across Italy\'s '
        'diverse economic geography.',
        
        'Incomplete representation of EU ETS Phase 4 and ETS2: Many existing models predate the Market Stability '
        'Reserve and proposed buildings/transport extension, limiting their relevance for current policy debates.',
        
        'Need for integrated assessment of just transition: Combining economic, energy, and regional equity '
        'dimensions in a single framework remains challenging, yet essential for comprehensive policy analysis.',
        
        'Calibration to post-COVID data: Using 2021 as the base year provides a more recent and relevant starting '
        'point than models calibrated to 2015 or earlier.',
        
        'Open-source and transparent modeling: The CGE-I5 model is developed with open documentation and aims '
        'for reproducibility, addressing calls for greater transparency in climate policy modeling (Pindyck, 2017).'
    ]
    
    for gap in gaps:
        doc.add_paragraph(gap, style='List Bullet')
    
    doc.add_paragraph(
        'By building on established methodologies while addressing these gaps, the CGE-I5 model contributes to '
        'the literature on Italian climate policy analysis and provides a tool for evidence-based policymaking '
        'in the crucial decade ahead.'
    )
    
    # Save document
    filename = 'CGE-I5_Model_Report_Part2.docx'
    doc.save(filename)
    print(f"✓ Part 2 of CGE-I5 Model Report created: {filename}")
    print(f"  Sections included:")
    print(f"    - Literature Review")
    print(f"      • CGE Modeling Framework")
    print(f"      • Energy-Economy-Environment Models")
    print(f"      • Climate Policy and Carbon Pricing")
    print(f"      • Energy Transition and Renewables")
    print(f"      • Regional and Distributional Impacts")
    print(f"      • Italian Energy and Climate Policy Context")
    print(f"      • Recursive Dynamic Modeling")
    print(f"      • Model Validation")
    print(f"      • Research Gap Addressed")
    return filename

if __name__ == "__main__":
    create_part2_report()
