"""
CGE-I5 Model Report Generator - Part 8
References and Conclusions
"""

from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def create_part8_report():
    """Create Part 8 of the CGE-I5 Model Report - References and Conclusions"""
    
    doc = Document()
    
    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    
    # ==================== CONCLUSIONS ====================
    doc.add_heading('9. Conclusions and Policy Implications', 0)
    
    doc.add_heading('9.1. Main Conclusions', 1)
    
    doc.add_paragraph(
        'This report has presented the CGE-I5 model, a comprehensive computable general equilibrium framework for '
        'analyzing climate policy impacts on the Italian economy. The model integrates production, consumption, trade, '
        'energy, and environmental dimensions across 11 sectors and 5 macro-regions, providing a holistic assessment '
        'of decarbonization pathways through 2040.'
    )
    
    p = doc.add_paragraph()
    p.add_run('The key conclusions from this modeling exercise are:').bold = True
    
    doc.add_heading('9.1.1. Feasibility of Deep Decarbonization', 2)
    
    doc.add_paragraph(
        'Italy can achieve deep emission reductions (53-62% by 2040) through ambitious carbon pricing combined with '
        'renewable energy support. The ETS1 and ETS2 scenarios demonstrate that reaching climate targets is technically '
        'and economically feasible, requiring GDP costs of 1.5-2.2% relative to baseline—moderate given the magnitude '
        'of transformation. These costs are likely upper bounds, as the model conservatively omits induced innovation, '
        'health co-benefits, and avoided climate damages.'
    )
    
    doc.add_heading('9.1.2. Central Role of Carbon Pricing', 2)
    
    doc.add_paragraph(
        'Explicit carbon pricing is essential to achieve climate targets. The BAU scenario shows that autonomous '
        'efficiency improvements alone deliver only 18% emission reduction by 2040, far short of requirements. Carbon '
        'prices reaching €90-120/tCO₂ by 2040 provide the economic signal needed to drive investment in renewables, '
        'improve energy efficiency, and shift consumption patterns. The price trajectory must be credible and '
        'predictable to mobilize the €400+ billion investment required.'
    )
    
    doc.add_heading('9.1.3. Renewable Energy as Core Solution', 2)
    
    doc.add_paragraph(
        'Decarbonization of electricity through renewable energy (solar, wind, hydro) is the foundation of Italy\'s '
        'low-carbon transition. Renewable electricity share must rise from 35% (2021) to 85-92% (2040) to meet targets. '
        'This requires sustained investment of €15-20 billion annually, creating over 100,000 jobs in construction, '
        'manufacturing, and maintenance. Italy\'s abundant solar and wind resources make this transition technically '
        'achievable, though grid flexibility and storage will be critical enablers.'
    )
    
    doc.add_heading('9.1.4. Importance of Regional Equity', 2)
    
    doc.add_paragraph(
        'The 80% investment subsidy for renewable projects in Southern Italy and the Islands is highly effective in '
        'promoting regional convergence. Southern regions experience smaller GDP losses, larger employment gains, and '
        'faster renewable capacity growth under policy scenarios, narrowing historical disparities. This demonstrates '
        'that climate policy can be designed to address regional inequality, provided sufficient financial support and '
        'complementary policies (skills training, grid infrastructure) are implemented.'
    )
    
    doc.add_heading('9.1.5. Revenue Recycling Protects Households', 2)
    
    doc.add_paragraph(
        'Recycling carbon revenues through per capita rebates largely protects household welfare, particularly for '
        'low-income groups. The policy is mildly progressive, with the bottom income quintile experiencing slight '
        'welfare gains while the top quintile bears most adjustment costs. This finding contradicts fears that carbon '
        'pricing is inherently regressive and highlights the importance of revenue use design. Lump-sum rebates '
        'combined with targeted support for vulnerable households can achieve both environmental and social objectives.'
    )
    
    doc.add_heading('9.1.6. Sectoral Winners and Losers', 2)
    
    doc.add_paragraph(
        'The energy transition creates clear winners (renewable energy, rail transport, energy-efficient manufacturing) '
        'and losers (fossil energy, energy-intensive industry, road transport). The renewable energy sector expands '
        '185% under ETS2, while gas and oil sectors contract 50-60%. These structural shifts necessitate just transition '
        'policies—worker retraining, early retirement support, regional economic diversification—to manage social impacts. '
        'Net employment effects are positive (+45,000 jobs), but geographic and sectoral mismatches require active labor '
        'market policies.'
    )
    
    # ===== 9.2 Policy Implications =====
    doc.add_heading('9.2. Policy Implications', 1)
    
    doc.add_heading('9.2.1. For Italian Climate Policy', 2)
    
    policy_implications_italy = [
        'Establish credible carbon price trajectory: Announce clear price path through 2040 to provide investment '
        'certainty. Consider hybrid mechanisms combining ETS-like trading with price stability mechanisms.',
        
        'Prioritize renewable energy deployment: Accelerate permitting for wind and solar projects, particularly in '
        'high-resource Southern regions. Invest in grid modernization to integrate variable renewables.',
        
        'Design progressive revenue recycling: Implement per capita carbon dividends to maintain public support. Consider '
        'higher rebates for low-income households and rural areas with limited transport alternatives.',
        
        'Support just transition: Create regional transition funds for communities dependent on fossil industries. '
        'Invest in retraining programs for displaced workers, with focus on renewable energy skills.',
        
        'Address regional disparities: Maintain 80% subsidy for Southern Italy renewable investments. Complement with '
        'infrastructure, skills, and innovation support to build lasting local capacity.',
        
        'Plan for electricity sector transformation: Develop flexibility solutions (storage, demand response, '
        'interconnections) to manage 90%+ renewable grid. Reform electricity market design to properly value flexibility.'
    ]
    
    for implication in policy_implications_italy:
        doc.add_paragraph(implication, style='List Bullet')
    
    doc.add_heading('9.2.2. For EU Climate Policy', 2)
    
    policy_implications_eu = [
        'ETS2 design lessons: Italy results support EU ETS2 proposal for buildings and transport. Price Stability '
        'Mechanism (€45-120/tCO₂) provides investment certainty while limiting political backlash risk from price spikes.',
        
        'Regional support mechanisms: EU-level support for renewable deployment in less-developed regions (e.g., '
        'Cohesion Funds, Just Transition Mechanism) is cost-effective in promoting convergence while advancing climate goals.',
        
        'Carbon border adjustment: Armington elasticity sensitivity analysis highlights carbon leakage risks if EU acts '
        'alone. CBAM implementation critical to protect European industry and incentivize global climate action.',
        
        'Revenue recycling coordination: Consider EU-wide guidance on carbon revenue use to ensure social acceptance. '
        'Share best practices on household rebates and just transition support.',
        
        'Grid integration: Italy\'s high renewable penetration requires stronger European grid interconnections. EU '
        'investment in transmission infrastructure enables Italian renewable exports and enhances energy security.'
    ]
    
    for implication in policy_implications_eu:
        doc.add_paragraph(implication, style='List Bullet')
    
    doc.add_heading('9.2.3. For CGE Modeling Practice', 2)
    
    modeling_implications = [
        'Regional disaggregation matters: Regional heterogeneity in resources, income, and institutions significantly '
        'affects policy outcomes. National-level models may miss important distributional impacts.',
        
        'Energy-environment integration: Explicit modeling of energy carriers and emission factors is essential for '
        'climate policy analysis. Simplified energy representation can misestimate abatement costs and technological '
        'feasibility.',
        
        'Dynamic modeling requirements: Recursive dynamics capturing capital accumulation and technology change are '
        'necessary for long-run policy assessment. Static models underestimate adjustment capacity.',
        
        'Sensitivity analysis: Results depend critically on energy substitution elasticity and AEEI parameters. '
        'Continued empirical research on these parameters should be a priority.',
        
        'Model limitations: Omitted factors (induced innovation, health co-benefits, behavioral change) likely mean CGE '
        'models overestimate policy costs. Complementary analysis methods (IAMs, sector models) strengthen overall assessment.'
    ]
    
    for implication in modeling_implications:
        doc.add_paragraph(implication, style='List Bullet')
    
    # ===== 9.3 Future Research =====
    doc.add_heading('9.3. Future Research Directions', 1)
    
    doc.add_paragraph(
        'Several extensions would strengthen the CGE-I5 model and address current limitations:'
    )
    
    doc.add_heading('9.3.1. Model Enhancements', 2)
    
    model_enhancements = [
        'Endogenous technological change: Incorporate induced innovation and learning-by-doing in renewable energy to '
        'capture policy-driven cost reductions and feedback effects on adoption.',
        
        'Explicit technology choice: Disaggregate renewable energy into solar, wind, biomass with distinct costs, '
        'capacity factors, and resource constraints. Include energy storage as explicit technology option.',
        
        'Air quality co-benefits: Model health impacts of reduced air pollution from fossil fuel phase-out. Quantify '
        'mortality and morbidity benefits to provide fuller cost-benefit assessment.',
        
        'Behavioral parameters: Incorporate bounded rationality, inertia, and heterogeneous discounting in household and '
        'firm decisions to better capture real-world adjustment dynamics.',
        
        'Financial sector: Add banking and capital markets to model financing constraints, risk premia, and role of '
        'green finance in enabling transition investment.',
        
        'Land use: Include agriculture-forestry-land use to assess bioenergy potential, carbon sequestration, and '
        'competition for land between food, energy, and conservation.'
    ]
    
    for enhancement in model_enhancements:
        doc.add_paragraph(enhancement, style='List Bullet')
    
    doc.add_heading('9.3.2. Policy Analysis Extensions', 2)
    
    policy_extensions = [
        'Additional policy instruments: Analyze complementary policies such as renewable portfolio standards, energy '
        'efficiency mandates, vehicle electrification requirements, and building codes.',
        
        'EU-wide coordination: Link CGE-I5 to models of other EU countries to assess impacts of coordinated EU climate '
        'policy and cross-border effects (trade, electricity flows, carbon leakage).',
        
        'Uncertainty analysis: Stochastic simulations incorporating uncertainty in parameters (elasticities, AEEI), '
        'exogenous variables (world prices, demographics), and policies (future stringency).',
        
        'Net-zero pathways: Extend time horizon to 2050 and model pathways to net-zero emissions, including negative '
        'emissions technologies (BECCS, DAC) and residual emissions sectors (agriculture).',
        
        'Circular economy: Incorporate material efficiency, recycling, and circular business models to assess their role '
        'in reducing emissions and resource consumption.',
        
        'Climate impacts: Introduce climate change impacts (heat stress, agricultural productivity, coastal damages) to '
        'model adaptation needs and benefits of avoided damages.'
    ]
    
    for extension in policy_extensions:
        doc.add_paragraph(extension, style='List Bullet')
    
    doc.add_heading('9.3.3. Empirical Priorities', 2)
    
    empirical_priorities = [
        'Energy substitution elasticity: Econometric estimation using Italian firm-level data to improve calibration of '
        'this critical parameter, with attention to heterogeneity across industries.',
        
        'AEEI trends: Analysis of historical energy efficiency improvements in Italy by sector to project future trends '
        'and identify policy drivers vs. autonomous change.',
        
        'Household energy behavior: Surveys and experiments to understand household response to carbon pricing, rebates, '
        'and information provision, informing behavioral parameter calibration.',
        
        'Regional characteristics: Detailed data collection on regional differences in industrial structure, energy '
        'systems, renewable resources, and institutional capacity to refine regional modules.',
        
        'Renewable deployment barriers: Qualitative research on non-price barriers (permitting, grid access, social '
        'acceptance, financing) to inform complementary policy design beyond carbon pricing.'
    ]
    
    for priority in empirical_priorities:
        doc.add_paragraph(priority, style='List Bullet')
    
    # ===== 9.4 Final Remarks =====
    doc.add_heading('9.4. Final Remarks', 1)
    
    doc.add_paragraph(
        'The CGE-I5 model demonstrates that Italy can achieve ambitious climate targets through well-designed carbon '
        'pricing and renewable energy support, with manageable economic costs and significant co-benefits. The transition '
        'to a low-carbon economy represents not only an environmental necessity but also an economic opportunity—creating '
        'jobs, reducing energy import dependence, improving air quality, and fostering regional development.'
    )
    
    doc.add_paragraph(
        'Success requires sustained political commitment, careful policy design, and proactive management of distributional '
        'impacts. Carbon pricing must be combined with complementary policies: renewable energy support, grid modernization, '
        'regional development programs, and just transition measures for affected workers and communities. Revenue recycling '
        'through household rebates is essential for maintaining public support.'
    )
    
    doc.add_paragraph(
        'The model provides a rigorous analytical foundation for policy design but should not be interpreted as providing '
        'precise forecasts. Scenario results illustrate plausible outcomes under different policy choices, highlighting '
        'trade-offs and design considerations. Policy decisions must integrate CGE model insights with broader considerations: '
        'technological uncertainties, political feasibility, international coordination, and ethical dimensions of climate action.'
    )
    
    doc.add_paragraph(
        'As Italy and Europe embark on this historic transformation, models like CGE-I5 serve as valuable tools for '
        'exploring pathways, anticipating challenges, and designing effective policies. Continued model development, '
        'empirical research, and policy evaluation will refine our understanding and improve decision-making. The path '
        'to climate neutrality is challenging but achievable, and the costs of inaction far exceed the costs of transition.'
    )
    
    doc.add_page_break()
    
    # ==================== REFERENCES ====================
    doc.add_heading('References', 0)
    
    doc.add_paragraph(
        'The following references were cited throughout this report. References are organized alphabetically by author.'
    )
    
    doc.add_paragraph()
    
    # CGE Modeling Foundations
    p = doc.add_paragraph()
    p.add_run('Computable General Equilibrium Modeling Foundations').bold = True
    doc.add_paragraph()
    
    references_cge = [
        'Arrow, K. J., & Debreu, G. (1954). Existence of an equilibrium for a competitive economy. '
        'Econometrica, 22(3), 265-290. https://doi.org/10.2307/1907353',
        
        'Lofgren, H., Harris, R. L., & Robinson, S. (2002). A standard computable general equilibrium (CGE) model '
        'in GAMS. Microcomputers in Policy Research, 5, 1-75. Washington, DC: International Food Policy Research Institute.',
        
        'Scarf, H. E. (1967). On the computation of equilibrium prices. In W. J. Fellner (Ed.), Ten Economic Studies '
        'in the Tradition of Irving Fisher (pp. 207-230). New York: Wiley.',
        
        'Shoven, J. B., & Whalley, J. (1984). Applied general-equilibrium models of taxation and international trade: '
        'An introduction and survey. Journal of Economic Literature, 22(3), 1007-1051.',
        
        'Wing, I. S. (2004). Computable general equilibrium models and their use in economy-wide policy analysis. '
        'MIT Joint Program on the Science and Policy of Global Change, Technical Note No. 6.'
    ]
    
    for ref in references_cge:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # Energy-Economy Models
    p = doc.add_paragraph()
    p.add_run('Energy-Economy CGE Models').bold = True
    doc.add_paragraph()
    
    references_energy = [
        'Babiker, M. H., Metcalf, G. E., & Reilly, J. (2003). Tax distortions and global climate policy. '
        'Journal of Environmental Economics and Management, 46(2), 269-287. https://doi.org/10.1016/S0095-0696(02)00039-6',
        
        'Böhringer, C., & Rutherford, T. F. (2008). Combining bottom-up and top-down. Energy Economics, 30(2), 574-596. '
        'https://doi.org/10.1016/j.eneco.2007.03.004',
        
        'Burniaux, J. M., & Truong, T. P. (2002). GTAP-E: An energy-environmental version of the GTAP model. '
        'GTAP Technical Paper No. 16, Center for Global Trade Analysis, Purdue University.',
        
        'Capros, P., Van Regemorter, D., Paroussos, L., & Karkatsoulis, P. (2013). GEM-E3 model documentation. '
        'JRC Scientific and Policy Reports, Publications Office of the European Union.',
        
        'Paltsev, S., Reilly, J. M., Jacoby, H. D., Eckaus, R. S., McFarland, J., Sarofim, M., ... & Babiker, M. (2005). '
        'The MIT emissions prediction and policy analysis (EPPA) model: version 4. MIT Joint Program Report Series, Report 125.',
        
        'Sue Wing, I. (2008). The synthesis of bottom-up and top-down approaches to climate policy modeling: '
        'Electric power technology detail in a social accounting framework. Energy Economics, 30(2), 547-573. '
        'https://doi.org/10.1016/j.eneco.2006.06.004'
    ]
    
    for ref in references_energy:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # Climate Policy and Carbon Pricing
    p = doc.add_paragraph()
    p.add_run('Climate Policy and Carbon Pricing').bold = True
    doc.add_paragraph()
    
    references_climate = [
        'Gerlagh, R., & van der Zwaan, B. (2004). A sensitivity analysis on timing and costs of greenhouse gas abatement, '
        'calculations with DEMETER. Climatic Change, 65(1-2), 39-71. https://doi.org/10.1023/B:CLIM.0000037226.48550.b3',
        
        'Nordhaus, W. D. (2017). Revisiting the social cost of carbon. Proceedings of the National Academy of Sciences, '
        '114(7), 1518-1523. https://doi.org/10.1073/pnas.1609244114',
        
        'Nordhaus, W. D., & Boyer, J. (2000). Warming the world: Economic models of global warming. Cambridge, MA: MIT Press.',
        
        'Perino, G., Ritz, R. A., & van Benthem, A. (2022). Understanding overlapping policies: Internal carbon leakage '
        'and the effect of demand-side policies. Journal of the Association of Environmental and Resource Economists, 9(5), 881-923. '
        'https://doi.org/10.1086/718879',
        
        'Stern, N. (2007). The economics of climate change: The Stern review. Cambridge University Press.',
        
        'Tol, R. S. (2009). The economic effects of climate change. Journal of Economic Perspectives, 23(2), 29-51. '
        'https://doi.org/10.1257/jep.23.2.29',
        
        'World Bank. (2023). State and trends of carbon pricing 2023. Washington, DC: World Bank. '
        'https://openknowledge.worldbank.org/handle/10986/39796'
    ]
    
    for ref in references_climate:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # EU ETS and Market Stability Reserve
    p = doc.add_paragraph()
    p.add_run('EU Emissions Trading System').bold = True
    doc.add_paragraph()
    
    references_ets = [
        'Convery, F. J. (2009). Origins and development of the EU ETS. Environmental and Resource Economics, 43(3), 391-412. '
        'https://doi.org/10.1007/s10640-009-9275-7',
        
        'Ellerman, A. D., Marcantonini, C., & Zaklan, A. (2016). The European Union emissions trading system: '
        'Ten years and counting. Review of Environmental Economics and Policy, 10(1), 89-107. https://doi.org/10.1093/reep/rev014',
        
        'Perino, G. (2018). New EU ETS phase 4 rules temporarily puncture waterbed. Nature Climate Change, 8(4), 262-264. '
        'https://doi.org/10.1038/s41558-018-0120-2',
        
        'Perino, G., & Willner, M. (2016). Procrastinating reform: The impact of the market stability reserve on the EU ETS. '
        'Journal of Environmental Economics and Management, 80, 37-52. https://doi.org/10.1016/j.jeem.2016.09.006',
        
        'Tvinnereim, E., & Mehling, M. (2018). Carbon pricing and deep decarbonisation. Energy Policy, 121, 185-189. '
        'https://doi.org/10.1016/j.enpol.2018.06.020'
    ]
    
    for ref in references_ets:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # Renewable Energy and Energy Transition
    p = doc.add_paragraph()
    p.add_run('Renewable Energy and Energy Transition').bold = True
    doc.add_paragraph()
    
    references_renewable = [
        'IEA (International Energy Agency). (2021). Net Zero by 2050: A Roadmap for the Global Energy Sector. Paris: IEA.',
        
        'IEA (International Energy Agency). (2023). World Energy Outlook 2023. Paris: IEA.',
        
        'IRENA (International Renewable Energy Agency). (2022). Renewable Power Generation Costs in 2021. Abu Dhabi: IRENA.',
        
        'Jäger-Waldau, A. (2020). Snapshot of photovoltaics—February 2020. Energies, 13(4), 930. '
        'https://doi.org/10.3390/en13040930',
        
        'Lund, H., Østergaard, P. A., Connolly, D., & Mathiesen, B. V. (2017). Smart energy and smart energy systems. '
        'Energy, 137, 556-565. https://doi.org/10.1016/j.energy.2017.05.123'
    ]
    
    for ref in references_renewable:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # Italian Context
    p = doc.add_paragraph()
    p.add_run('Italian Energy and Climate Policy').bold = True
    doc.add_paragraph()
    
    references_italy = [
        'Antonioli, D., Borghesi, S., & Mazzanti, M. (2016). Are regional systems greening the economy? Local spillovers, '
        'green innovations and firms\' economic performances. Economics of Innovation and New Technology, 25(7), 692-713. '
        'https://doi.org/10.1080/10438599.2015.1127557',
        
        'Costantini, V., Crespi, F., Martini, C., & Pennacchio, L. (2015). Demand-pull and technology-push public support '
        'for eco-innovation: The case of the biofuels sector. Research Policy, 44(3), 577-595. '
        'https://doi.org/10.1016/j.respol.2014.12.011',
        
        'GSE (Gestore dei Servizi Energetici). (2023). Rapporto statistico 2022: Energia da fonti rinnovabili in Italia. Rome: GSE.',
        
        'ISPRA (Istituto Superiore per la Protezione e la Ricerca Ambientale). (2023). Italian Greenhouse Gas Inventory '
        '1990-2021: National Inventory Report 2023. Rome: ISPRA.',
        
        'ISTAT (Istituto Nazionale di Statistica). (2023). Conti economici nazionali. Rome: ISTAT.',
        
        'Mazzanti, M., & Zoboli, R. (2009). Municipal waste Kuznets curves: Evidence on socio-economic drivers and policy '
        'effectiveness from the EU. Environmental and Resource Economics, 44(2), 203-230. '
        'https://doi.org/10.1007/s10640-009-9280-x'
    ]
    
    for ref in references_italy:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # Econometric Methods and Parameters
    p = doc.add_paragraph()
    p.add_run('Econometric Methods and Parameter Estimation').bold = True
    doc.add_paragraph()
    
    references_econometric = [
        'Antràs, P. (2004). Is the U.S. aggregate production function Cobb-Douglas? New estimates of the elasticity of '
        'substitution. Contributions in Macroeconomics, 4(1), Article 4. https://doi.org/10.2202/1534-6005.1161',
        
        'Chirinko, R. S. (2008). σ: The long and short of it. Journal of Macroeconomics, 30(2), 671-686. '
        'https://doi.org/10.1016/j.jmacro.2007.10.010',
        
        'Hertel, T., Hummels, D., Ivanic, M., & Keeney, R. (2007). How confident can we be of CGE-based assessments of '
        'Free Trade Agreements? Economic Modelling, 24(4), 611-635. https://doi.org/10.1016/j.econmod.2006.12.002',
        
        'Koetse, M. J., de Groot, H. L., & Florax, R. J. (2008). Capital-energy substitution and shifts in factor demand: '
        'A meta-analysis. Energy Economics, 30(5), 2236-2251. https://doi.org/10.1016/j.eneco.2007.06.006',
        
        'Lluch, C., Powell, A. A., & Williams, R. A. (1977). Patterns in household demand and saving. '
        'Oxford University Press for the World Bank.',
        
        'Robinson, S., Cattaneo, A., & El-Said, M. (2001). Updating and estimating a social accounting matrix using '
        'cross entropy methods. Economic Systems Research, 13(1), 47-64. https://doi.org/10.1080/09535310120026247'
    ]
    
    for ref in references_econometric:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # Optimization and Solution Methods
    p = doc.add_paragraph()
    p.add_run('Optimization and Numerical Methods').bold = True
    doc.add_paragraph()
    
    references_optimization = [
        'Byrd, R. H., Nocedal, J., & Waltz, R. A. (2006). KNITRO: An integrated package for nonlinear optimization. '
        'In G. di Pillo & M. Roma (Eds.), Large-Scale Nonlinear Optimization (pp. 35-59). Boston, MA: Springer. '
        'https://doi.org/10.1007/0-387-30065-1_4',
        
        'Hart, W. E., Laird, C. D., Watson, J. P., Woodruff, D. L., Hackebeil, G. A., Nicholson, B. L., & Siirola, J. D. (2017). '
        'Pyomo–optimization modeling in python (Vol. 67, second edition). Springer Science & Business Media.',
        
        'Hart, W. E., Watson, J. P., & Woodruff, D. L. (2011). Pyomo: Modeling and solving mathematical programs in Python. '
        'Mathematical Programming Computation, 3(3), 219-260. https://doi.org/10.1007/s12532-011-0026-8',
        
        'Wächter, A., & Biegler, L. T. (2006). On the implementation of an interior-point filter line-search algorithm '
        'for large-scale nonlinear programming. Mathematical Programming, 106(1), 25-57. '
        'https://doi.org/10.1007/s10107-004-0559-y'
    ]
    
    for ref in references_optimization:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # Distributional and Regional Analysis
    p = doc.add_paragraph()
    p.add_run('Distributional and Regional Analysis').bold = True
    doc.add_paragraph()
    
    references_distributional = [
        'Carattini, S., Carvalho, M., & Fankhauser, S. (2018). Overcoming public resistance to carbon taxes. '
        'Wiley Interdisciplinary Reviews: Climate Change, 9(5), e531. https://doi.org/10.1002/wcc.531',
        
        'Goulder, L. H., Hafstead, M. A., Kim, G., & Long, X. (2019). Impacts of a carbon tax across US household income groups: '
        'What are the equity-efficiency trade-offs? Journal of Public Economics, 175, 44-64. '
        'https://doi.org/10.1016/j.jpubeco.2019.04.002',
        
        'Markkanen, S., & Anger-Kraavi, A. (2019). Social impacts of climate change mitigation policies and their '
        'implications for inequality. Climate Policy, 19(7), 827-844. https://doi.org/10.1080/14693062.2019.1596873',
        
        'Rausch, S., Metcalf, G. E., & Reilly, J. M. (2011). Distributional impacts of carbon pricing: A general equilibrium '
        'approach with micro-data for households. Energy Economics, 33, S20-S33. https://doi.org/10.1016/j.eneco.2011.07.023'
    ]
    
    for ref in references_distributional:
        doc.add_paragraph(ref, style='List Bullet')
    
    doc.add_paragraph()
    
    # Add note about data sources
    doc.add_paragraph()
    p = doc.add_paragraph()
    p.add_run('Data Sources').bold = True
    doc.add_paragraph()
    
    data_sources = [
        'EUROSTAT: European statistical database for trade, energy, and emissions data.',
        
        'IEA (International Energy Agency): World Energy Balances and energy price statistics.',
        
        'IPCC (Intergovernmental Panel on Climate Change): 2006 IPCC Guidelines for National Greenhouse Gas Inventories.',
        
        'ISPRA (Istituto Superiore per la Protezione e la Ricerca Ambientale): Italian emissions inventory and environmental statistics.',
        
        'ISTAT (Istituto Nazionale di Statistica): Italian national accounts, supply-use tables, regional accounts, '
        'household budget surveys, and demographic projections.',
        
        'World Bank: Commodity price forecasts and development indicators.'
    ]
    
    for source in data_sources:
        doc.add_paragraph(source, style='List Bullet')
    
    # Save document
    filename = 'CGE-I5_Model_Report_Part8.docx'
    doc.save(filename)
    print(f"✓ Part 8 of CGE-I5 Model Report created: {filename}")
    print(f"  Sections included:")
    print(f"    - Conclusions and Policy Implications")
    print(f"      • Main Conclusions")
    print(f"      • Policy Implications (Italian, EU, modeling practice)")
    print(f"      • Future Research Directions")
    print(f"      • Final Remarks")
    print(f"    - References")
    print(f"      • Complete bibliography with all cited sources")
    print(f"      • Organized by topic area")
    return filename

if __name__ == "__main__":
    create_part8_report()
