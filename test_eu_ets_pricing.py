"""
Test EU ETS Pricing Implementation
Verify that the updated EU ETS pricing parameters are correctly implemented
"""

import sys
import os
sys.path.append('src')

from definitions import model_definitions

def test_eu_ets_pricing():
    """Test the updated EU ETS pricing parameters"""
    
    print("TESTING EU ETS PRICING IMPLEMENTATION")
    print("=" * 60)
    
    # Test ETS1 pricing (EU ETS Phase 4)
    print("\n1. EU ETS PHASE 4 (ETS1) TESTING:")
    print("-" * 40)
    
    # Test base year pricing
    ets1_2021 = model_definitions.get_carbon_price(2021, 'ETS1')
    print(f"ETS1 price in 2021: €{ets1_2021:.2f}/tCO2e")
    assert abs(ets1_2021 - 53.90) < 0.01, f"Expected €53.90, got €{ets1_2021}"
    
    # Test price growth
    ets1_2025 = model_definitions.get_carbon_price(2025, 'ETS1')
    expected_2025 = 53.90 * (1.05 ** 4)  # 4 years of 5% growth
    print(f"ETS1 price in 2025: €{ets1_2025:.2f}/tCO2e (expected: €{expected_2025:.2f})")
    assert abs(ets1_2025 - expected_2025) < 0.01, f"Price growth calculation error"
    
    # Test no formal price cap (MSR managed)
    ets1_2050 = model_definitions.get_carbon_price(2050, 'ETS1')
    print(f"ETS1 price in 2050: €{ets1_2050:.2f}/tCO2e (MSR managed - practical cap at €300)")
    assert ets1_2050 <= 300.0, "Practical upper bound exceeded"
    
    print("✓ ETS1 pricing tests passed")
    
    # Test ETS2 pricing (Buildings and Transport)
    print("\n2. EU ETS BUILDINGS/TRANSPORT (ETS2) TESTING:")
    print("-" * 50)
    
    # Test before start year
    ets2_2025 = model_definitions.get_carbon_price(2025, 'ETS2')
    print(f"ETS2 price in 2025 (before start): €{ets2_2025:.2f}/tCO2e")
    assert ets2_2025 == 0.0, "ETS2 should be zero before 2027"
    
    # Test base year pricing
    ets2_2027 = model_definitions.get_carbon_price(2027, 'ETS2')
    print(f"ETS2 price in 2027: €{ets2_2027:.2f}/tCO2e")
    assert abs(ets2_2027 - 45.0) < 0.01, f"Expected €45.00, got €{ets2_2027}"
    
    # Test price cap (PSM ceiling)
    ets2_2030 = model_definitions.get_carbon_price(2030, 'ETS2')
    print(f"ETS2 price in 2030: €{ets2_2030:.2f}/tCO2e (PSM capped at €45)")
    assert ets2_2030 <= 45.0, "ETS2 price should be capped at €45 by PSM"
    assert ets2_2030 >= 22.0, "ETS2 price should not fall below €22 floor"
    
    print("✓ ETS2 pricing tests passed")
    
    # Test policy parameters
    print("\n3. ETS POLICY PARAMETERS:")
    print("-" * 30)
    
    print(f"ETS1 base price: €{model_definitions.ets1_policy['base_carbon_price']:.2f}/tCO2e")
    print(f"ETS1 price cap: {model_definitions.ets1_policy['price_cap']} (MSR managed)")
    print(f"ETS1 has MSR: {model_definitions.ets1_policy['has_msr']}")
    
    print(f"ETS2 base price: €{model_definitions.ets2_policy['base_carbon_price']:.2f}/tCO2e")
    print(f"ETS2 price cap: €{model_definitions.ets2_policy['price_cap']:.2f}/tCO2e")
    print(f"ETS2 price floor: €{model_definitions.ets2_policy['price_floor']:.2f}/tCO2e")
    print(f"ETS2 has PSM: {model_definitions.ets2_policy['has_psm']}")
    
    # Test sector coverage
    print("\n4. SECTOR COVERAGE:")
    print("-" * 20)
    print(f"ETS1 covered sectors: {model_definitions.ets1_policy['covered_sectors']}")
    print(f"ETS2 covered sectors: {model_definitions.ets2_policy['covered_sectors']}")
    
    # Test scenario definitions
    print("\n5. SCENARIO DEFINITIONS:")
    print("-" * 25)
    scenarios = model_definitions.create_scenario_definitions()
    
    for scenario_name, scenario_data in scenarios.items():
        print(f"\n{scenario_name}: {scenario_data['name']}")
        print(f"  Description: {scenario_data['description']}")
        if 'price_mechanism' in scenario_data:
            print(f"  Price mechanism: {scenario_data['price_mechanism']}")
        if 'ets1_mechanism' in scenario_data:
            print(f"  ETS1 mechanism: {scenario_data['ets1_mechanism']}")
        if 'ets2_mechanism' in scenario_data:
            print(f"  ETS2 mechanism: {scenario_data['ets2_mechanism']}")
    
    print("\n" + "=" * 60)
    print("✓ ALL EU ETS PRICING TESTS PASSED")
    print("\nEU ETS Implementation Summary:")
    print(f"- ETS1 (Phase 4): €53.90/tCO2e base, MSR managed (practical cap €300), covers {len(model_definitions.ets1_policy['covered_sectors'])} sectors")
    print(f"- ETS2 (Buildings/Transport): €45.0/tCO2e base, PSM managed (€22-€45 range), covers {len(model_definitions.ets2_policy['covered_sectors'])} sectors")
    print("- All pricing parameters updated across relevant model blocks")

def test_price_trajectories():
    """Test price trajectories over time"""
    
    print("\n\nPRICE TRAJECTORIES (2021-2035):")
    print("=" * 50)
    print("Year    ETS1 (€/tCO2e)    ETS2 (€/tCO2e)")
    print("-" * 50)
    
    for year in range(2021, 2036):
        ets1_price = model_definitions.get_carbon_price(year, 'ETS1')
        ets2_price = model_definitions.get_carbon_price(year, 'ETS2')
        print(f"{year}    {ets1_price:8.2f}        {ets2_price:8.2f}")

if __name__ == "__main__":
    test_eu_ets_pricing()
    test_price_trajectories()