# CGE-I5 Model

A Computable General Equilibrium (CGE) model for Italy disaggregated into five macro-regions (Northwest, Northeast, Centre, South, Islands) designed to assess the macro-distributional and energy impacts of decarbonisation through economic, energy and environmental policy analysis.

## Overview

This recursive dynamic CGE model provides comprehensive analysis of:

- **Multi-sector economic modeling** with detailed production structure
- **Dynamic simulation** from 2021 to 2040
- **Environmental policy scenarios** including EU ETS implementation
- **Energy demand tracking** (renewables, gas, other energy)
- **CO2 emissions analysis** with carbon pricing mechanisms
- **Regional disaggregation** across Italy's five macro-regions

## Features

### Core Capabilities

- **Recursive Dynamic CGE Framework**: Multi-period optimization with calibrated base year (2021)
- **Environmental Module**: Detailed CO2 emissions tracking and carbon pricing mechanisms
- **Energy Disaggregation**: Electricity [(renewable/non-renewable), gas, and other energy carriers]
- **Regional Analysis**: Full disaggregation by Italy's five macro-regions
- **Policy Simulation**: EU ETS (Phase 1: Industry, Phase 2: Buildings & Transport)
- **Comprehensive Output**: 15+ indicator categories with detailed sectoral breakdowns

### Technical Features

- Pyomo-based optimization framework
- IPOPT solver integration for equilibrium computation
- Automated calibration to base year SAM
- Excel-based results generation
- Professional visualization outputs (PDF/PNG)

## Requirements

### Software Dependencies

- **Python**: 3.10 or higher
- **Optimization**: Pyomo 6.9.4, IPOPT solver (included in `ipopt_solver/`)
- **Data Processing**: pandas, numpy, openpyxl
- **Visualization**: matplotlib, seaborn, plotly
- **Geospatial**: geopandas, fiona

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Jammeh01/Italian_cge_model.git
   cd Italian_cge_model
   ```

2. **Create virtual environment** (recommended):

   ```bash
   python -m venv italian_cge_env
   # Windows
   italian_cge_env\Scripts\activate
   # Linux/Mac
   source italian_cge_env/bin/activate
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Verify IPOPT solver**:
   - The IPOPT solver is included in `ipopt_solver/Ipopt-3.14.16-win64-msvs2019-md/bin/`
   - Ensure the path is accessible or add to system PATH

## Model Components

### Core Model Blocks

1. **Production Block** (`production_block.py`)
   - CES and Cobb-Douglas production functions
   - Multi-sector disaggregation with intermediate inputs
   - Capital-labor-energy-materials (KLEM) structure

2. **Income-Expenditure Block** (`income_expenditure_block.py`)
   - Household consumption behavior (Linear Expenditure System)
   - Government revenue and expenditure
   - Regional income distribution

3. **Trade Block** (`trade_block.py`)
   - Armington specification for imports
   - CET transformation for exports
   - Trade balance equations

4. **Energy-Environment Block** (`energy_environment_block.py`)
   - Energy demand (renewables, gas, other energy)
   - Endogenous renewable capacity tracking with investment-driven growth
   - CO2 emission calculations with specific emission factors calibrated to Italian 2021 data:
     - Renewables (100% clean electricity): 0 kg CO2/MWh
     - Gas (heating, industry): 202 kg CO2/MWh  
     - Other Energy (oil, coal): 350 kg CO2/MWh
   - EU ETS implementation with Market Stability Reserve (ETS1) and Price Stability Mechanism (ETS2)
   - Autonomous Energy Efficiency Improvement (AEEI) at 1.8% annually

5. **Macro Indicators Block** (`macro_indicators_block.py`)
   - Real GDP calculation
   - Consumer Price Index (CPI)
   - Producer Price Index (PPI)

6. **Market Clearing & Closure** (`market_clearing_closure_block.py`)
   - Supply-demand equilibrium conditions
   - Walras' Law implementation
   - Recursive dynamic closure rules

### Policy Scenarios

- **BAU (Business as Usual)**
  - Baseline projection without additional carbon pricing beyond existing policies
  - Autonomous energy efficiency improvements (1.8% annual AEEI)
  - Natural renewable capacity growth reaching ~70% electricity share by 2040
  - Italy 2021 baseline: 60 GW renewable capacity, 35% renewable electricity share

- **ETS1 (Phase 1 - Industry)**
  - EU Emissions Trading System Phase 4 for industrial sectors
  - Carbon pricing starting at €53.90/tCO2 in 2021 (actual EU ETS price)
  - Market Stability Reserve (MSR) mechanism manages supply, declining growth rate
  - Price reaches €150/tCO2 by 2040 (practical upper bound)
  - Covered sectors: Industry, Gas, Other Energy, Air Transport, Water Transport
  - 35% renewable investment acceleration factor
  - Renewable electricity share exceeds 80% by 2040

- **ETS2 (Phase 2 - Buildings & Transport)**
  - Extended ETS coverage to buildings and transport starting 2027
  - ETS2 carbon pricing: €45.0/tCO2 in 2027 with Price Stability Mechanism (PSM)
  - PSM ceiling maintains price at €45/tCO2 (policy design feature)
  - Additional covered sectors: Road Transport, Other Transport, Services
  - 60% renewable investment acceleration factor (80% in South/Islands)
  - Renewable electricity share exceeds 90% by 2040
  - Strongest decarbonization with comprehensive just transition support

## Model Hierarchy

```
recursive_dynamic_simulation.py          ← Top-level simulation engine
    ↓ (imports)
calibration.py                           ← Base year calibration
    ↓ (imports)
main_model.py                            ← Core CGE model
    ↓ (imports & assembles)
├── production_block.py
├── income_expenditure_block.py
├── trade_block.py
├── energy_environment_block.py
├── macro_indicators_block.py
└── market_clearing_closure_block.py
```

## Usage

### Running the Model

1. **Base Year Calibration**:

   ```bash
   python src/calibration.py
   ```

   This calibrates the model to 2021 base year data from `data/SAM.xlsx`

2. **Dynamic Simulation (2021-2040)**:

   ```bash
   python src/recursive_dynamic_simulation.py
   ```

   Generates results for all three scenarios (BAU, ETS1, ETS2)

3. **Visualize Results**:

   ```bash
   python visualize_gdp_results.py
   ```

   Creates GDP evolution charts comparing scenarios

### Output Files

The model generates comprehensive Excel files in `src/results/`:

- **Italian_CGE_Enhanced_Dynamic_Results_[timestamp].xlsx**: Full simulation results
  - Macroeconomy (GDP, CPI, PPI)
  - Production by sector
  - Household income/expenditure by region
  - Energy demand by sector and carrier
  - CO2 emissions and carbon pricing
  - Trade flows
  - Labor market indicators
  - Renewable energy investments

- **Italian_CGE_BaseYear_Calibration_[timestamp].xlsx**: Base year calibration

Visualization outputs are saved in `results/` and `figures/` directories.

## Results & Indicators

The model produces 15+ categories of indicators:

### Economic Indicators

- Real GDP (total and by region)
- Consumer Price Index (CPI)
- Producer Price Index (PPI)
- Sectoral value added

### Energy Indicators

- Annual energy demand by sector (MWh)
- Energy demand by carrier type
- Household energy consumption by region
- Renewable energy capacity and investment

### Environmental Indicators

- Total CO2 emissions (MtCO2)
- Emissions by sector
- Carbon price levels (ETS1/ETS2)
- Carbon tax/ETS revenues

### Regional Indicators

- GDP by macro-region
- Household income and expenditure
- Employment and unemployment
- Population dynamics

### Trade Indicators

- Exports by sector
- Imports by sector
- Trade balance

## Technical Notes

- **Solver**: The model uses Pyomo (Python Optimization Modeling Objects) as the modeling framework, interfacing with IPOPT to find equilibrium solutions
- **Calibration**: Base year 2021 is calibrated to match the Social Accounting Matrix
- **Alignment**: All model blocks are synchronized for consistent CO2 emission factors, renewable shares, and closure rules
- **Time Horizon**: 2021-2040 (20 years) with annual time steps

## Data Sources

- **SAM**: Social Accounting Matrix for Italy (2021)
- **Geographic Data**: ISTAT administrative boundaries
- **NUTS Regions**: Eurostat NUTS 2021 classification
- **Energy Data**: Italian energy statistics and projections

## Contributing

This model is part of ongoing research on Italian economic and environmental policy analysis. For questions or collaboration opportunities, please contact the repository maintainer.

## Contact

- **Author**: Bakary Jammeh
- **Repository**: <https://github.com/Jammeh01/Italian_cge_model>
