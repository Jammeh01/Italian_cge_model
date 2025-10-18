"""
Energy Calibration Coefficients for Italian CGE Model
Recalibrated to match official 2021 energy statistics (GSE, Eurostat, IEA)

Option B: Grid Mix Approach
- Electricity: Total grid electricity (310 TWh) with dynamic renewable share
- Gas: Natural gas for end-use only (720 TWh, excludes power generation)
- Other Energy: Oil products, coal, direct renewables (790 TWh)
- Total: 1,820 TWh (matches official TFEC)

Author: CGE Model Recalibration
Date: October 2025
"""

import numpy as np
from italy_2021_data import ENERGY_CALIBRATION_TARGETS_2021

# =============================================================================
# CALIBRATION TARGETS FROM OFFICIAL STATISTICS
# =============================================================================

# Official Italy 2021 Total Final Energy Consumption (TFEC)
# Source: GSE (Gestore Servizi Energetici), Eurostat, IEA
OFFICIAL_ENERGY_2021 = {
    # Total grid electricity (renewable + fossil mix)
    'electricity_twh': 310.0,
    # Natural gas end-use (heating, industry, commercial)
    'gas_twh': 720.0,
    # Oil products (580) + Coal (60) + Direct renewables (150)
    'other_energy_twh': 790.0,
    'total_tfec_twh': 1820.0    # Total final energy consumption
}

# Current model output (before recalibration)
CURRENT_MODEL_OUTPUT_2021 = {
    'electricity_twh': 148.78,
    'gas_twh': 290.59,
    'other_energy_twh': 69.50,
    'total_twh': 508.87
}

# =============================================================================
# ENERGY COEFFICIENT SCALING FACTORS
# =============================================================================

# Calculate scaling factors needed to match official statistics
ENERGY_SCALING_FACTORS = {
    'electricity': OFFICIAL_ENERGY_2021['electricity_twh'] / CURRENT_MODEL_OUTPUT_2021['electricity_twh'],
    'gas': OFFICIAL_ENERGY_2021['gas_twh'] / CURRENT_MODEL_OUTPUT_2021['gas_twh'],
    'other_energy': OFFICIAL_ENERGY_2021['other_energy_twh'] / CURRENT_MODEL_OUTPUT_2021['other_energy_twh'],
    'total': OFFICIAL_ENERGY_2021['total_tfec_twh'] / CURRENT_MODEL_OUTPUT_2021['total_twh']
}

print("=" * 80)
print("ENERGY CALIBRATION SCALING FACTORS")
print("=" * 80)
print(
    f"Electricity scaling factor: {ENERGY_SCALING_FACTORS['electricity']:.4f} (×{ENERGY_SCALING_FACTORS['electricity']:.2f})")
print(
    f"Gas scaling factor: {ENERGY_SCALING_FACTORS['gas']:.4f} (×{ENERGY_SCALING_FACTORS['gas']:.2f})")
print(
    f"Other Energy scaling factor: {ENERGY_SCALING_FACTORS['other_energy']:.4f} (×{ENERGY_SCALING_FACTORS['other_energy']:.2f})")
print(
    f"Overall scaling factor: {ENERGY_SCALING_FACTORS['total']:.4f} (×{ENERGY_SCALING_FACTORS['total']:.2f})")
print("=" * 80)

# =============================================================================
# ENERGY COEFFICIENT ADJUSTMENTS BY SECTOR AND HOUSEHOLD
# =============================================================================


def get_calibrated_energy_coefficient(energy_sector, user_sector, base_coefficient=1.0):
    """
    Get calibrated energy coefficient to match official statistics

    Parameters:
    -----------
    energy_sector : str
        Energy carrier ('Electricity', 'Gas', 'Other Energy')
    user_sector : str
        Consuming sector or household region
    base_coefficient : float
        Base coefficient from SAM calibration (default 1.0)

    Returns:
    --------
    float
        Calibrated energy coefficient
    """

    # Map energy sector names to scaling factors
    scaling_map = {
        'Electricity': ENERGY_SCALING_FACTORS['electricity'],
        'Gas': ENERGY_SCALING_FACTORS['gas'],
        'Other Energy': ENERGY_SCALING_FACTORS['other_energy']
    }

    # Get appropriate scaling factor
    scaling_factor = scaling_map.get(energy_sector, 1.0)

    # Apply scaling to base coefficient
    calibrated_coefficient = base_coefficient * scaling_factor

    return calibrated_coefficient


def get_all_energy_coefficients(sectors, household_regions, energy_sectors):
    """
    Generate complete energy coefficient matrix for CGE model

    Parameters:
    -----------
    sectors : list
        List of production sectors
    household_regions : list
        List of household regions
    energy_sectors : list
        List of energy sectors

    Returns:
    --------
    dict
        Dictionary of energy coefficients by (energy_sector, user)
    """

    energy_coefficients = {}

    # Combine all users (sectors + households)
    all_users = sectors + household_regions

    for es in energy_sectors:
        for user in all_users:
            # Base coefficient (can be refined based on SAM data)
            base_coeff = 1.0

            # Get calibrated coefficient
            calibrated_coeff = get_calibrated_energy_coefficient(
                es, user, base_coeff)

            # Store in dictionary
            energy_coefficients[(es, user)] = calibrated_coeff

    return energy_coefficients


# =============================================================================
# REGIONAL ENERGY COEFFICIENT ADJUSTMENTS
# =============================================================================

# Regional energy consumption patterns (from italy_2021_data.py)
REGIONAL_ENERGY_PATTERNS = {
    'NW': {  # Northwest (high industrial, high gas)
        'electricity_multiplier': 1.15,  # 15% above average
        # 32% above average (high heating + industry)
        'gas_multiplier': 1.32,
        'other_energy_multiplier': 0.90  # 10% below average
    },
    'NE': {  # Northeast (high industrial, high gas)
        'electricity_multiplier': 1.09,  # 9% above average
        'gas_multiplier': 1.24,          # 24% above average
        'other_energy_multiplier': 0.95  # 5% below average
    },
    'CENTER': {  # Center (Rome, moderate)
        'electricity_multiplier': 1.00,  # Average
        'gas_multiplier': 1.00,          # Average
        'other_energy_multiplier': 1.05  # 5% above average
    },
    'SOUTH': {  # South (lower consumption)
        'electricity_multiplier': 0.83,  # 17% below average
        'gas_multiplier': 0.67,          # 33% below average (warmer climate)
        'other_energy_multiplier': 1.10  # 10% above average (more oil)
    },
    'ISLANDS': {  # Islands (Sicily, Sardinia - limited gas)
        'electricity_multiplier': 0.89,  # 11% below average
        # 55% below average (limited infrastructure)
        'gas_multiplier': 0.45,
        'other_energy_multiplier': 1.20  # 20% above average (oil-dependent)
    }
}


def get_regional_energy_coefficient(energy_sector, household_region, base_coefficient=1.0):
    """
    Get regionally-adjusted energy coefficient

    Parameters:
    -----------
    energy_sector : str
        Energy carrier ('Electricity', 'Gas', 'Other Energy')
    household_region : str
        Household region ('NW', 'NE', 'CENTER', 'SOUTH', 'ISLANDS')
    base_coefficient : float
        Base calibrated coefficient

    Returns:
    --------
    float
        Regionally-adjusted energy coefficient
    """

    # Get regional pattern
    region_pattern = REGIONAL_ENERGY_PATTERNS.get(household_region, {})

    # Map energy sector to multiplier
    multiplier_map = {
        'Electricity': region_pattern.get('electricity_multiplier', 1.0),
        'Gas': region_pattern.get('gas_multiplier', 1.0),
        'Other Energy': region_pattern.get('other_energy_multiplier', 1.0)
    }

    # Get appropriate multiplier
    regional_multiplier = multiplier_map.get(energy_sector, 1.0)

    # Apply regional adjustment
    regional_coefficient = base_coefficient * regional_multiplier

    return regional_coefficient


# =============================================================================
# VALIDATION
# =============================================================================

def validate_energy_calibration(model_results):
    """
    Validate that recalibrated model matches official statistics

    Parameters:
    -----------
    model_results : dict
        Dictionary with model output by energy sector (in TWh)

    Returns:
    --------
    dict
        Validation results with errors
    """

    validation = {}

    for energy_type in ['electricity', 'gas', 'other_energy']:
        official = OFFICIAL_ENERGY_2021[f'{energy_type}_twh']
        model = model_results.get(energy_type, 0)
        error = abs(model - official) / official * 100

        validation[energy_type] = {
            'official_twh': official,
            'model_twh': model,
            'error_percent': error,
            'status': 'PASS' if error < 5.0 else 'FAIL'
        }

    # Total validation
    official_total = OFFICIAL_ENERGY_2021['total_tfec_twh']
    model_total = sum(model_results.values())
    total_error = abs(model_total - official_total) / official_total * 100

    validation['total'] = {
        'official_twh': official_total,
        'model_twh': model_total,
        'error_percent': total_error,
        'status': 'PASS' if total_error < 3.0 else 'FAIL'
    }

    return validation


# =============================================================================
# SUMMARY
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("ENERGY CALIBRATION SUMMARY")
    print("=" * 80)
    print("\nOFFICIAL 2021 ENERGY STATISTICS (GSE, Eurostat, IEA):")
    print(f"  Electricity: {OFFICIAL_ENERGY_2021['electricity_twh']:.1f} TWh")
    print(f"  Gas: {OFFICIAL_ENERGY_2021['gas_twh']:.1f} TWh")
    print(
        f"  Other Energy: {OFFICIAL_ENERGY_2021['other_energy_twh']:.1f} TWh")
    print(f"  TOTAL: {OFFICIAL_ENERGY_2021['total_tfec_twh']:.1f} TWh")

    print("\nCURRENT MODEL OUTPUT (Before Recalibration):")
    print(
        f"  Electricity: {CURRENT_MODEL_OUTPUT_2021['electricity_twh']:.1f} TWh")
    print(f"  Gas: {CURRENT_MODEL_OUTPUT_2021['gas_twh']:.1f} TWh")
    print(
        f"  Other Energy: {CURRENT_MODEL_OUTPUT_2021['other_energy_twh']:.1f} TWh")
    print(f"  TOTAL: {CURRENT_MODEL_OUTPUT_2021['total_twh']:.1f} TWh")

    print("\nREQUIRED ADJUSTMENTS:")
    print(
        f"  Electricity: ×{ENERGY_SCALING_FACTORS['electricity']:.2f} ({OFFICIAL_ENERGY_2021['electricity_twh'] - CURRENT_MODEL_OUTPUT_2021['electricity_twh']:+.1f} TWh)")
    print(
        f"  Gas: ×{ENERGY_SCALING_FACTORS['gas']:.2f} ({OFFICIAL_ENERGY_2021['gas_twh'] - CURRENT_MODEL_OUTPUT_2021['gas_twh']:+.1f} TWh)")
    print(
        f"  Other Energy: ×{ENERGY_SCALING_FACTORS['other_energy']:.2f} ({OFFICIAL_ENERGY_2021['other_energy_twh'] - CURRENT_MODEL_OUTPUT_2021['other_energy_twh']:+.1f} TWh)")
    print(
        f"  Overall: ×{ENERGY_SCALING_FACTORS['total']:.2f} ({OFFICIAL_ENERGY_2021['total_tfec_twh'] - CURRENT_MODEL_OUTPUT_2021['total_twh']:+.1f} TWh)")
    print("=" * 80)
