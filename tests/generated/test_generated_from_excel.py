"""Generated pytest tests from the validated Excel workbook.

DO NOT EDIT MANUALLY.
Regenerate with:
python test_generation/generate_tests_from_docs.py generated_tests.xlsx
"""

from simulators.controller_simulator import RefrigerationController

def test_generated_tc_ai_002():
    """Generated from Excel test case TC_AI_002."""
    controller = RefrigerationController()
    controller.set_high_discharge_temperature()
    assert controller.compressor_on is False

def test_generated_tc_ai_003():
    """Generated from Excel test case TC_AI_003."""
    controller = RefrigerationController()
    controller.set_high_discharge_temperature()
    assert controller.compressor_on is False

def test_generated_tc_ai_004():
    """Generated from Excel test case TC_AI_004."""
    controller = RefrigerationController()
    controller.set_low_suction_pressure()
    assert controller.compressor_on is False
