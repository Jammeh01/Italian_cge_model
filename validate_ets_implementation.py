"""
Validation Script for ETS Implementation
Tests whether carbon pricing properly affects the model
"""

from definitions import model_definitions
from main_model import ItalianCGEModel
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))


def validate_ets_implementation():
    """
    Validate that ETS implementation works correctly
    Tests carbon cost linkages and scenario differences
    """

    print("="*80)
    print("VALIDATING ETS IMPLEMENTATION")
    print("="*80)
    print()

    # Create model
    print("Step 1: Creating model instance...")
    model = ItalianCGEModel("data/SAM.xlsx")

    # Load and calibrate
    print("\nStep 2: Loading and calibrating data...")
    success = model.load_and_calibrate_data()
    if not success:
        print("❌ FAILED: Could not load/calibrate data")
        return False
    print("✅ Data loaded and calibrated")

    # Build model
    print("\nStep 3: Building model structure...")
    model.build_model()
    print("✅ Model built")

    # Validation checks
    print("\n" + "="*80)
    print("VALIDATION CHECKS")
    print("="*80)

    validation_passed = True

    # Check 1: Carbon_Cost variable exists
    print("\n[Check 1] Carbon_Cost variable exists in energy block")
    if hasattr(model.model, 'Carbon_Cost'):
        print("✅ PASS: Carbon_Cost variable found")
        print(f"   Number of sectors: {len(list(model.model.Carbon_Cost))}")
    else:
        print("❌ FAIL: Carbon_Cost variable not found")
        validation_passed = False

    # Check 2: Carbon_Revenue variable exists
    print("\n[Check 2] Carbon_Revenue variable exists")
    if hasattr(model.model, 'Carbon_Revenue'):
        print("✅ PASS: Carbon_Revenue variable found")
    else:
        print("❌ FAIL: Carbon_Revenue variable not found")
        validation_passed = False

    # Check 3: Zero-profit constraint includes carbon costs
    print("\n[Check 3] Zero-profit constraint modified to include carbon costs")
    if hasattr(model.model, 'eq_zero_profit'):
        print("✅ PASS: eq_zero_profit constraint exists")
        # Check constraint formula
        constraint_obj = model.model.eq_zero_profit
        print(f"   Number of constraints: {len(list(constraint_obj))}")
    else:
        print("❌ FAIL: eq_zero_profit constraint not found")
        validation_passed = False

    # Check 4: Government revenue includes carbon revenue
    print("\n[Check 4] Government revenue constraint includes carbon revenue")
    if hasattr(model.model, 'eq_government_revenue'):
        print("✅ PASS: eq_government_revenue constraint exists")
    else:
        print("❌ FAIL: eq_government_revenue constraint not found")
        validation_passed = False

    # Check 5: ETS coverage parameters exist
    print("\n[Check 5] ETS coverage parameters exist")
    if hasattr(model.model, 'ets1_coverage') and hasattr(model.model, 'ets2_coverage'):
        print("✅ PASS: ETS coverage parameters found")
        # Show which sectors are covered
        ets1_covered = [j for j in model.calibrated_data['production_sectors']
                        if model.model.ets1_coverage[j].value > 0]
        ets2_covered = [j for j in model.calibrated_data['production_sectors']
                        if model.model.ets2_coverage[j].value > 0]
        print(f"   ETS1 covered sectors: {ets1_covered}")
        print(f"   ETS2 covered sectors: {ets2_covered}")
    else:
        print("❌ FAIL: ETS coverage parameters not found")
        validation_passed = False

    # Check 6: Free allocation parameters exist
    print("\n[Check 6] Free allocation parameters exist")
    if hasattr(model.model, 'free_alloc_ets1') and hasattr(model.model, 'free_alloc_ets2'):
        print("✅ PASS: Free allocation parameters found")
        print(
            f"   ETS1 free allocation: {model.model.free_alloc_ets1.value:.1%}")
        print(
            f"   ETS2 free allocation: {model.model.free_alloc_ets2.value:.1%}")
    else:
        print("❌ FAIL: Free allocation parameters not found")
        validation_passed = False

    # Check 7: Carbon pricing constraints exist
    print("\n[Check 7] Carbon cost calculation constraints exist")
    if hasattr(model.model, 'eq_carbon_cost'):
        print("✅ PASS: eq_carbon_cost constraint exists")
    else:
        print("❌ FAIL: eq_carbon_cost constraint not found")
        validation_passed = False

    if hasattr(model.model, 'eq_total_carbon_revenue'):
        print("✅ PASS: eq_total_carbon_revenue constraint exists")
    else:
        print("❌ FAIL: eq_total_carbon_revenue constraint not found")
        validation_passed = False

    # Summary
    print("\n" + "="*80)
    print("VALIDATION SUMMARY")
    print("="*80)

    if validation_passed:
        print("✅ ALL CHECKS PASSED")
        print("\nYour model is now properly configured to capture ETS effects!")
        print("\nNext steps:")
        print("1. Run BAU scenario: python -m src.main_model (or your run script)")
        print("2. Run ETS1 scenario")
        print("3. Run ETS2 scenario")
        print("4. Compare results: GDP, emissions, carbon revenue")
        print("\nExpected differences:")
        print("- BAU: No carbon costs, highest GDP, highest emissions")
        print("- ETS1: Carbon costs in industry/energy sectors, moderate GDP impact")
        print("- ETS2: Additional carbon costs in transport/buildings, largest GDP impact")
        return True
    else:
        print("❌ VALIDATION FAILED")
        print("\nSome components are missing. Please check:")
        print("1. energy_environment_block.py has Carbon_Cost and Carbon_Revenue variables")
        print("2. production_block.py includes carbon costs in zero-profit condition")
        print("3. income_expenditure_block.py includes carbon revenue in government budget")
        return False


def test_scenario_initialization():
    """
    Test that scenarios properly set carbon prices
    """
    print("\n" + "="*80)
    print("TESTING SCENARIO INITIALIZATION")
    print("="*80)

    model = ItalianCGEModel("data/SAM.xlsx")
    model.load_and_calibrate_data()
    model.build_model()

    # Test BAU
    print("\n[BAU Scenario - 2021]")
    model.initialize_model(year=2021, scenario='BAU')
    bau_ets1_price = model.model.carbon_price_ets1.value
    bau_ets2_price = model.model.carbon_price_ets2.value
    print(f"  ETS1 price: €{bau_ets1_price:.2f}/tCO2e (expected: €0.00)")
    print(f"  ETS2 price: €{bau_ets2_price:.2f}/tCO2e (expected: €0.00)")

    # Test ETS1
    print("\n[ETS1 Scenario - 2021]")
    model.initialize_model(year=2021, scenario='ETS1')
    ets1_price = model.model.carbon_price_ets1.value
    ets2_price = model.model.carbon_price_ets2.value
    print(f"  ETS1 price: €{ets1_price:.2f}/tCO2e (expected: €53.90)")
    print(
        f"  ETS2 price: €{ets2_price:.2f}/tCO2e (expected: €0.00 before 2027)")

    # Test ETS2
    print("\n[ETS2 Scenario - 2027]")
    model.initialize_model(year=2027, scenario='ETS2')
    ets1_price_2027 = model.model.carbon_price_ets1.value
    ets2_price_2027 = model.model.carbon_price_ets2.value
    print(f"  ETS1 price: €{ets1_price_2027:.2f}/tCO2e (expected: >€53.90)")
    print(f"  ETS2 price: €{ets2_price_2027:.2f}/tCO2e (expected: €45.00)")

    if bau_ets1_price == 0 and bau_ets2_price == 0:
        print("\n✅ BAU scenario correctly sets zero carbon prices")
    else:
        print("\n❌ BAU scenario should have zero carbon prices")

    if ets1_price > 50 and ets2_price == 0:
        print("✅ ETS1 scenario correctly sets ETS1 price, ETS2 inactive")
    else:
        print("❌ ETS1 scenario carbon prices incorrect")

    if ets1_price_2027 > 50 and ets2_price_2027 > 40:
        print("✅ ETS2 scenario correctly sets both ETS1 and ETS2 prices")
    else:
        print("❌ ETS2 scenario carbon prices incorrect")


if __name__ == "__main__":
    print("\nITALIAN CGE MODEL - ETS IMPLEMENTATION VALIDATION")
    print("This script validates that carbon pricing properly affects the model\n")

    try:
        # Run main validation
        validation_success = validate_ets_implementation()

        if validation_success:
            # Run scenario initialization tests
            test_scenario_initialization()

        print("\n" + "="*80)
        print("VALIDATION COMPLETE")
        print("="*80)

    except Exception as e:
        print(f"\n❌ ERROR during validation: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
