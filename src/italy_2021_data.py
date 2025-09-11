"""
2021 Italian Economic Data for CGE Model Calibration
Based on actual statistical data from ISTAT, Eurostat, IEA, and other official sources
All monetary values in millions of euros (current prices)
"""

# =============================================================================
# MACRO ECONOMIC INDICATORS (2021 ACTUAL DATA)
# =============================================================================

# GDP and Population (Official ISTAT Data)
GDP_2021 = 1782000  # €1,782 billion in millions (current prices, ISTAT)
POPULATION_2021 = 59.13  # 59.13 million people (ISTAT, 1 January 2021)
GDP_PER_CAPITA_2021 = 30137  # €30,137 per person (GDP/population)

# Employment Data (ISTAT Labour Force Survey 2021)
TOTAL_EMPLOYMENT = 22.9  # 22.9 million employed persons
UNEMPLOYMENT_RATE = 0.095  # 9.5% unemployment rate (national average)
EMPLOYMENT_RATE = 0.581  # 58.1% employment rate (15-64 age group)

# Regional Employment and Unemployment Rates (2021)
REGIONAL_UNEMPLOYMENT = {
    # 6.2% Northwest (Lombardy, Piedmont, Valle d'Aosta, Liguria)
    'NW': 0.062,
    # 6.8% Northeast (Veneto, Trentino-AA, Friuli-VG, Emilia-Romagna)
    'NE': 0.068,
    'CENTER': 0.087,  # 8.7% Center (Tuscany, Umbria, Marche, Lazio)
    # 15.8% South (Abruzzo, Molise, Campania, Puglia, Basilicata, Calabria)
    'SOUTH': 0.158,
    'ISLANDS': 0.175  # 17.5% Islands (Sicily, Sardinia)
}

# =============================================================================
# SECTORAL OUTPUT AND VALUE ADDED (2021 NACE DATA)
# =============================================================================

# Agriculture, Forestry and Fishing (NACE A)
AGRICULTURE_OUTPUT = 67700      # €67.7 billion gross output
AGRICULTURE_VALUE_ADDED = 42800  # €42.8 billion value added (2.4% of GDP)
AGRICULTURE_EMPLOYMENT = 897000  # 897k employed persons (3.9% of total)

# Industry including Energy and Construction (NACE B-F)
INDUSTRY_OUTPUT = 820000        # €820 billion gross output
INDUSTRY_VALUE_ADDED = 431600   # €431.6 billion value added (24.2% of GDP)
# 5.67 million employed persons (24.7% of total)
INDUSTRY_EMPLOYMENT = 5670000

# Services (NACE G-U)
SERVICES_OUTPUT = 920000        # €920 billion gross output
SERVICES_VALUE_ADDED = 1308000  # €1,308 billion value added (73.4% of GDP)
# 16.38 million employed persons (71.4% of total)
SERVICES_EMPLOYMENT = 16380000

# =============================================================================
# ENERGY SECTOR DATA (2021 ACTUAL DATA)
# =============================================================================

# Electricity Sector (IEA Energy Statistics 2021)
ELECTRICITY_GENERATION = 289.7  # TWh total electricity generation
ELECTRICITY_CONSUMPTION = 310.0  # TWh total electricity consumption
ELECTRICITY_RENEWABLE_SHARE = 0.413  # 41.3% renewable electricity
ELECTRICITY_CO2_INTENSITY = 0.312    # 0.312 tCO2/MWh (grid average)

# Electricity Generation Mix (2021)
ELECTRICITY_MIX = {
    'gas': 0.468,        # 46.8% natural gas
    # 41.3% renewables (hydro, wind, solar, geothermal, biomass)
    'renewables': 0.413,
    'coal': 0.071,       # 7.1% coal
    'oil': 0.015,        # 1.5% oil
    'other': 0.033       # 3.3% other sources
}

# Natural Gas Sector (SNAM, IEA Data 2021)
GAS_CONSUMPTION = 76.1    # bcm total natural gas consumption
GAS_IMPORTS = 72.3        # bcm natural gas imports (95% import dependency)
GAS_DOMESTIC_PRODUCTION = 3.3  # bcm domestic production

# Gas Consumption by Sector (2021)
GAS_CONSUMPTION_SECTORS = {
    'electricity': 29.5,  # bcm (38.8% - power generation)
    'industry': 15.8,     # bcm (20.8% - industrial processes)
    'residential': 20.1,  # bcm (26.4% - heating and cooking)
    'commercial': 7.2,    # bcm (9.5% - commercial buildings)
    'other': 3.5          # bcm (4.6% - other uses)
}

# Oil and Other Energy (Ministry of Economic Development 2021)
OIL_CONSUMPTION = 58.8    # Mt oil consumption
RENEWABLE_CAPACITY = 60.1  # GW renewable energy capacity
REFINING_CAPACITY = 1.9   # Million barrels/day refining capacity

# =============================================================================
# REGIONAL ENERGY CONSUMPTION (2021 DATA)
# =============================================================================

# Electricity Consumption by Macro Region (Terna, kWh per capita)
REGIONAL_ELECTRICITY_CONSUMPTION = {
    'NW': 1350,    # kWh per capita (high industrial consumption)
    'NE': 1280,    # kWh per capita
    'CENTER': 1180,  # kWh per capita
    'SOUTH': 980,   # kWh per capita (lower industrial activity)
    'ISLANDS': 1050  # kWh per capita (higher cooling needs)
}

# Gas Consumption by Macro Region (SNAM, m³ per capita)
REGIONAL_GAS_CONSUMPTION = {
    'NW': 950,     # m³ per capita (high heating + industrial needs)
    'NE': 890,     # m³ per capita
    'CENTER': 720,  # m³ per capita
    'SOUTH': 480,  # m³ per capita (warmer climate)
    'ISLANDS': 320  # m³ per capita (limited gas infrastructure)
}

# =============================================================================
# CO2 EMISSIONS DATA (2021 ACTUAL DATA)
# =============================================================================

# Total CO2 Emissions (ISPRA, EEA Data 2021)
TOTAL_CO2_EMISSIONS = 381.2  # Mt CO2 equivalent

# CO2 Emissions by Sector (2021)
CO2_EMISSIONS_SECTORS = {
    'electricity': 119.5,  # Mt CO2 (31.4% of total)
    'industry': 76.2,      # Mt CO2 (20.0% of total)
    'transport': 95.8,     # Mt CO2 (25.1% of total)
    'buildings': 64.5,     # Mt CO2 (16.9% of total)
    'agriculture': 17.1,   # Mt CO2 (4.5% of total)
    'other': 8.1           # Mt CO2 (2.1% of total)
}

# CO2 Emission Factors by Fuel (2021)
CO2_EMISSION_FACTORS = {
    'natural_gas': 2.03,   # tCO2/MWh
    'coal': 3.47,          # tCO2/MWh
    'oil': 2.78,           # tCO2/MWh
    'electricity': 0.312   # tCO2/MWh (grid average)
}

# =============================================================================
# TRADE DATA (2021 ACTUAL DATA)
# =============================================================================

# Total Trade (ISTAT, Balance of Payments 2021)
TOTAL_EXPORTS = 559700   # €559.7 billion (31.4% of GDP)
TOTAL_IMPORTS = 513200   # €513.2 billion (28.8% of GDP)
TRADE_BALANCE = 46500    # €46.5 billion trade surplus

# Trade by Sector Groups (2021)
TRADE_BY_SECTOR = {
    'agriculture': {
        'exports': 12200,    # €12.2 billion
        'imports': 14900     # €14.9 billion
    },
    'industry': {
        'exports': 344000,   # €344 billion
        'imports': 287000    # €287 billion
    },
    'services': {
        'exports': 129000,   # €129 billion
        'imports': 110000    # €110 billion
    },
    'energy': {
        'exports': 4100,     # €4.1 billion
        'imports': 55600     # €55.6 billion (large energy deficit)
    }
}

# =============================================================================
# GOVERNMENT FINANCES (2021 ACTUAL DATA)
# =============================================================================

# General Government (Bank of Italy, ISTAT 2021)
GOVERNMENT_REVENUE = 838900     # €838.9 billion (47.1% of GDP)
GOVERNMENT_EXPENDITURE = 958800  # €958.8 billion (53.8% of GDP)
GOVERNMENT_DEFICIT = 119900     # €119.9 billion deficit (6.7% of GDP)
GOVERNMENT_DEBT = 2683000       # €2,683 billion debt (150.6% of GDP)

# Government Revenue Sources (2021)
GOVERNMENT_REVENUE_SOURCES = {
    'income_tax': 231200,       # €231.2 billion personal income tax
    'corporate_tax': 71300,     # €71.3 billion corporate income tax
    'vat': 123300,              # €123.3 billion VAT
    'excise_taxes': 49500,      # €49.5 billion excise taxes
    'social_contributions': 277800,  # €277.8 billion social security
    'other': 85800              # €85.8 billion other revenues
}

# Government Expenditure (2021)
GOVERNMENT_CONSUMPTION = 329700  # €329.7 billion government consumption
GOVERNMENT_INVESTMENT = 57000    # €57.0 billion government investment
SOCIAL_TRANSFERS = 425600        # €425.6 billion social transfers
DEBT_SERVICE = 58400             # €58.4 billion debt service

# =============================================================================
# INVESTMENT DATA (2021 ACTUAL DATA)
# =============================================================================

# Gross Fixed Capital Formation (ISTAT 2021)
TOTAL_INVESTMENT = 331400  # €331.4 billion (18.6% of GDP)

# Investment by Asset Type (2021)
INVESTMENT_BY_ASSET = {
    'construction': 165700,    # €165.7 billion (50% of total)
    'machinery': 99400,       # €99.4 billion (30% of total)
    'transport_equipment': 33100,  # €33.1 billion (10% of total)
    'ict_equipment': 23200,   # €23.2 billion (7% of total)
    'other': 9900             # €9.9 billion (3% of total)
}

# Investment by Sector of Destination (2021)
INVESTMENT_BY_SECTOR = {
    'industry': 92800,         # €92.8 billion
    'services': 116000,        # €116.0 billion
    'electricity': 39800,      # €39.8 billion
    'gas': 26500,              # €26.5 billion
    'other_energy': 33100,     # €33.1 billion
    'transport': 13300,        # €13.3 billion
    'agriculture': 9900        # €9.9 billion
}

# =============================================================================
# REGIONAL ECONOMIC DATA (2021 ACTUAL DATA)
# =============================================================================

# Regional GDP (ISTAT, current prices 2021)
REGIONAL_GDP = {
    'NW': 656000,    # €656 billion (36.8% of total, includes Lombardy €400B)
    'NE': 404000,    # €404 billion (22.7% of total)
    'CENTER': 402000,  # €402 billion (22.6% of total, includes Lazio €207B)
    'SOUTH': 252000,  # €252 billion (14.1% of total)
    'ISLANDS': 68000  # €68 billion (3.8% of total)
}

# Regional Per Capita GDP (2021)
REGIONAL_GDP_PER_CAPITA = {
    'NW': 37200,     # €37,200 per person (highest)
    'NE': 35100,     # €35,100 per person
    'CENTER': 32400,  # €32,400 per person
    'SOUTH': 21800,  # €21,800 per person
    'ISLANDS': 22600  # €22,600 per person
}

# Regional Industrial Specialization (2021 value added shares)
REGIONAL_SPECIALIZATION = {
    'NW': {
        'industry': 0.282,     # 28.2% industry (manufacturing hub)
        'services': 0.698,     # 69.8% services
        'agriculture': 0.020   # 2.0% agriculture
    },
    'NE': {
        # 31.5% industry (manufacturing + agriculture processing)
        'industry': 0.315,
        'services': 0.645,     # 64.5% services
        'agriculture': 0.040   # 4.0% agriculture
    },
    'CENTER': {
        'industry': 0.195,     # 19.5% industry
        'services': 0.782,     # 78.2% services (Rome public sector)
        'agriculture': 0.023   # 2.3% agriculture
    },
    'SOUTH': {
        'industry': 0.168,     # 16.8% industry (lower industrialization)
        'services': 0.785,     # 78.5% services
        'agriculture': 0.047   # 4.7% agriculture
    },
    'ISLANDS': {
        'industry': 0.148,     # 14.8% industry
        'services': 0.804,     # 80.4% services
        'agriculture': 0.048   # 4.8% agriculture
    }
}

# =============================================================================
# TRANSPORT DATA (2021 ACTUAL DATA)
# =============================================================================

# Modal Share of Freight Transport (2021)
FREIGHT_MODAL_SHARE = {
    'road': 0.865,      # 86.5% road transport
    'rail': 0.089,      # 8.9% rail transport
    'water': 0.046      # 4.6% inland waterways + short sea shipping
}

# Passenger Transport (2021)
PASSENGER_TRANSPORT = {
    'road': 783.5,      # billion passenger-km (cars + buses)
    'rail': 44.2,       # billion passenger-km
    'air': 165.8,       # million passengers (COVID affected)
    'metro_tram': 4.8   # billion passenger-km (urban transport)
}

# Transport Infrastructure (2021)
TRANSPORT_INFRASTRUCTURE = {
    'road_network': 487700,    # km total road network
    'rail_network': 16800,     # km rail network
    'metro_network': 240,      # km metro lines
    'airports': 130,           # number of airports
    'ports': 230               # number of commercial ports
}

# Vehicle Stock (2021)
VEHICLE_STOCK = {
    # 39.7 million cars (663 cars/1000 inhabitants)
    'passenger_cars': 39700000,
    'commercial_vehicles': 4200000,  # 4.2 million commercial vehicles
    'motorcycles': 7000000,        # 7.0 million motorcycles
    'buses': 100000,               # 100k buses
    'trucks': 3800000              # 3.8 million trucks
}

# =============================================================================
# PRICE INDICES (2021 DATA)
# =============================================================================

# Consumer Price Index (ISTAT, 2015=100)
CPI_2021 = 102.5  # 2.5% inflation since 2015

# Producer Price Index (ISTAT, 2015=100)
PPI_2021 = 108.7  # 8.7% producer price inflation since 2015

# Energy Price Indices (2021)
ENERGY_PRICES_2021 = {
    'electricity_households': 0.2226,  # €/kWh (including taxes)
    'electricity_industry': 0.1582,    # €/kWh (excluding VAT)
    'gas_households': 0.7344,          # €/m³ (including taxes)
    'gas_industry': 0.3156,            # €/m³ (excluding VAT)
    'gasoline': 1.563,                 # €/liter (including taxes)
    'diesel': 1.425                    # €/liter (including taxes)
}

# =============================================================================
# LABOR MARKET DATA (2021 ACTUAL DATA)
# =============================================================================

# Average Wages by Sector (2021, gross annual wages)
SECTORAL_WAGES = {
    'agriculture': 18500,      # €18,500 per year
    'industry': 31200,         # €31,200 per year
    'construction': 28900,     # €28,900 per year
    'services': 28700,         # €28,700 per year
    'finance': 45600,          # €45,600 per year
    'public_admin': 34500,     # €34,500 per year
    'education': 29800,        # €29,800 per year
    'health': 32100            # €32,100 per year
}

# Labor Productivity (2021, value added per employee)
LABOR_PRODUCTIVITY = {
    'agriculture': 47700,      # €47,700 per employee
    'industry': 76100,         # €76,100 per employee
    'services': 79900          # €79,900 per employee
}

# Employment by Sector (2021, thousands of persons)
SECTORAL_EMPLOYMENT = {
    'agriculture': 897,        # 897k persons (3.9%)
    'industry': 5670,          # 5,670k persons (24.7%)
    'services': 16380          # 16,380k persons (71.4%)
}

# =============================================================================
# SOCIAL INDICATORS (2021 DATA)
# =============================================================================

# Household Income Distribution (2021)
HOUSEHOLD_DISPOSABLE_INCOME = 1053000  # €1,053 billion total disposable income
GINI_COEFFICIENT = 0.330               # Income inequality (Gini coefficient)

# Savings Rate by Region (2021)
REGIONAL_SAVINGS_RATES = {
    'NW': 0.22,        # 22% savings rate (wealthy regions save more)
    'NE': 0.20,        # 20% savings rate
    'CENTER': 0.18,    # 18% savings rate
    # 8% savings rate (lower income, higher consumption rate)
    'SOUTH': 0.08,
    'ISLANDS': 0.10    # 10% savings rate
}

# =============================================================================
# CALIBRATION TARGETS AND VALIDATION
# =============================================================================


def validate_data_consistency():
    """Validate that the data is internally consistent"""

    # Check that GDP equals sum of value added
    total_value_added = AGRICULTURE_VALUE_ADDED + \
        INDUSTRY_VALUE_ADDED + SERVICES_VALUE_ADDED
    gdp_error = abs(total_value_added - GDP_2021) / GDP_2021

    # Check that employment sums correctly
    total_employment_sectors = SECTORAL_EMPLOYMENT['agriculture'] + \
        SECTORAL_EMPLOYMENT['industry'] + SECTORAL_EMPLOYMENT['services']
    employment_error = abs(total_employment_sectors -
                           (TOTAL_EMPLOYMENT * 1000)) / (TOTAL_EMPLOYMENT * 1000)

    # Check trade balance
    calculated_trade_balance = TOTAL_EXPORTS - TOTAL_IMPORTS
    trade_error = abs(calculated_trade_balance -
                      TRADE_BALANCE) / abs(TRADE_BALANCE)

    print(f"Data Validation Results:")
    print(f"  GDP Value Added Error: {gdp_error:.1%}")
    print(f"  Employment Sum Error: {employment_error:.1%}")
    print(f"  Trade Balance Error: {trade_error:.1%}")

    return gdp_error < 0.05 and employment_error < 0.05 and trade_error < 0.05


if __name__ == "__main__":
    # Run validation when module is executed directly
    print("2021 Italian Economic Data Summary:")
    print(
        f"  GDP: €{GDP_2021:,} million (€{GDP_PER_CAPITA_2021:,} per capita)")
    print(f"  Population: {POPULATION_2021:.2f} million")
    print(
        f"  Employment: {TOTAL_EMPLOYMENT:.1f} million ({EMPLOYMENT_RATE:.1%} employment rate)")
    print(
        f"  Exports: €{TOTAL_EXPORTS:,} million ({TOTAL_EXPORTS/GDP_2021:.1%} of GDP)")
    print(
        f"  Imports: €{TOTAL_IMPORTS:,} million ({TOTAL_IMPORTS/GDP_2021:.1%} of GDP)")
    print(
        f"  Government Debt: €{GOVERNMENT_DEBT:,} million ({GOVERNMENT_DEBT/GDP_2021:.1%} of GDP)")
    print()

    # Validate data consistency
    is_consistent = validate_data_consistency()
    print(f"Data Consistency Check: {'PASSED' if is_consistent else 'FAILED'}")
