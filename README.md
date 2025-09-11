# Italian CGE Model

A Computable General Equilibrium (CGE) model for Italy with dynamic simulation capabilities for economic and environmental policy analysis.

## Overview

This project implements a comprehensive CGE model for the Italian economy, featuring:

- Multi-sector economic modeling
- Dynamic simulation from 2021-2050
- Environmental policy scenarios (ETS implementation)
- Energy demand and CO2 emissions tracking
- Regional analysis capabilities

## Project Structure

```
italian_cge_model/
├── src/                          # Core model source code
│   ├── main_model.py            # Main CGE model implementation
│   ├── dynamic_simulation_2021_2050.py  # Dynamic simulation engine
│   ├── data_processor.py        # Data processing utilities
│   ├── calibration_analyzer.py  # Model calibration tools
│   └── results/                 # Generated results and outputs
├── scenarios/                   # Policy scenario definitions
│   ├── BAU_scenario.py         # Business as Usual scenario
│   ├── ETS1_scenario.py        # ETS implementation scenario 1
│   └── ETS2_scenario.py        # ETS implementation scenario 2
├── data/                       # Input data and SAM
│   └── SAM.xlsx               # Social Accounting Matrix
└── tests/                     # Test suite

```

## Features

- **Dynamic CGE Model**: Multi-period optimization with forward-looking expectations
- **Environmental Module**: CO2 emissions tracking and carbon pricing mechanisms
- **Energy Sectors**: Detailed modeling of electricity, gas, and renewable energy
- **Policy Analysis**: Support for ETS and other environmental policies
- **Results Visualization**: Comprehensive output generation and analysis tools

## Requirements

- Python 3.8+
- Pyomo optimization framework
- IPOPT solver (recommended)
- Pandas, NumPy for data processing
- Plotly for visualization

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/italian_cge_model.git
cd italian_cge_model
```

2. Create and activate virtual environment:

```bash
python -m venv italian_cge_env
# On Windows:
italian_cge_env\Scripts\activate
```

3. Install dependencies:

```bash
pip install pyomo pandas numpy openpyxl plotly dash
```

## Usage

### Running the Base Model

```bash
cd src
python main_model.py
```

### Dynamic Simulation

```bash
cd src
python dynamic_simulation_2021_2050.py
```

### Policy Scenario Analysis

```bash
cd scenarios
python BAU_scenario.py
python ETS1_scenario.py
```

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
- Sectoral energy demand (MW)
- CO2 emissions trajectories (MtCo2)
- Regional economic indicators
- Policy impact assessments
