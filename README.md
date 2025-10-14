# CGE-I5 Model

A Computable General Equilibrium (CGE) model for Italy disaggregated into the five macro-regions (Northwest, Northeast, Centre, South, Islands) - designed to assess the macro-distributional and energy impacts of decarbonisation (economic, energy and environmental policies. 


## Overview
- Multi-sector economic modeling
- Dynamic simulation from 2021-2050
- Environmental policy scenarios (ETS implementation)
- Energy demand and CO2 emissions tracking
- Regional analysis capabilities

## Project Structure

```
italian_cge_model/
├── src/                         # Core model source code
│   ├── main_model.py            # Main CGE model implementation
│   ├── dynamic_simulation_2021_2050.py  # Dynamic simulation engine
│   ├── data_processor.py        # Data processing utilities
│   ├── calibration_analyzer.py  # Model calibration tools
│   └── results/                 # Generated results and outputs
├── data/                       # Input data and SAM
   └── SAM.xlsx                # Social Accounting Matrix

```

## Features

- **Dynamic CGE Model**: Multi-period optimization with forward-looking expectations
- **Environmental Module**: CO2 emissions tracking and carbon pricing mechanisms
- **Energy Sectors**: Detailed modeling of electricity (renewable), gas, and other energy
- **Policy Analysis**: Support for ETS and other environmental policies
- **Results Visualization**: Comprehensive output generation and analysis tools

## Requirements

- Python 3.10+
- Pyomo optimization framework
- IPOPT solver (recommended)
- Pandas, NumPy for data processing
- Plotly for visualization

## Model Components

### Core Blocks

- **Production Block**: Multi-sector production with CES/Cobb-Douglas functions
- **Income-Expenditure Block**: Household and government behavior
- **Trade Block**: Import/export with Armington specification
- **Energy-Environment Block**: Energy demand and emissions
- **Market Clearing**: Supply-demand equilibrium conditions

### Scenarios

- **BAU**: Business as Usual projection
- **ETS1**: EU Emissions Trading System implementation
- **ETS2**: Enhanced ETS with additional sectors

## Results

The model generates comprehensive outputs including:

- GDP evolution by scenario
- Sectoral energy demand (MWh annual)
- CO2 emissions trajectories (MtCo2)
- Regional economic indicators
- Policy impact assessments
