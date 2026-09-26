"""Generated pytest tests from the validated Excel workbook.

DO NOT EDIT MANUALLY.
Regenerate with:
python test_generation/generate_tests_from_docs.py generated_tests.xlsx
"""

from simulators.controller_simulator import RefrigerationController

def test_generated_tc_ai_002():
    """Generated from Excel test case TC_AI_002."""
    controller = RefrigerationController()
    controller.set_leak_condition()
    assert controller.alarm_active is True

def test_generated_tc_ai_003():
    """Generated from Excel test case TC_AI_003."""
    controller = RefrigerationController()
    controller.set_leak_condition()
    assert controller.compressor_on is False

def test_generated_tc_ai_004():
    """Generated from Excel test case TC_AI_004."""
    controller = RefrigerationController()
    controller.set_leak_condition()
    assert controller.evaporator_fan_on is True

def test_generated_tc_ai_005():
    """Generated from Excel test case TC_AI_005."""
    controller = RefrigerationController()
    controller.set_leak_condition()
    assert controller.alarm_active is True

def test_generated_tc_ai_006():
    """Generated from Excel test case TC_AI_006."""
    controller = RefrigerationController()
    controller.set_leak_condition()
    assert 'refrigerant leak detected' in controller.event_log

def test_generated_tc_ai_018():
    """Generated from Excel test case TC_AI_018."""
    controller = RefrigerationController()
    controller.set_low_suction_pressure()
    assert controller.compressor_on is False

def test_generated_tc_ai_019():
    """Generated from Excel test case TC_AI_019."""
    controller = RefrigerationController()
    controller.invalidate_sensor()
    assert controller.safe_mode is True

def test_generated_tc_ai_020():
    """Generated from Excel test case TC_AI_020."""
    controller = RefrigerationController()
    controller.invalidate_sensor()
    assert controller.safe_mode is True

def test_generated_tc_ai_027():
    """Generated from Excel test case TC_AI_027."""
    controller = RefrigerationController()
    controller.set_high_discharge_temperature()
    assert controller.compressor_on is False

def test_generated_tc_ai_028():
    """Generated from Excel test case TC_AI_028."""
    controller = RefrigerationController()
    registers = controller.modbus_registers()
    assert registers[30001] == 'evaporator temperature'

def test_generated_tc_ai_029():
    """Generated from Excel test case TC_AI_029."""
    controller = RefrigerationController()
    registers = controller.modbus_registers()
    assert registers[30002] == 'suction pressure'

def test_generated_tc_ai_030():
    """Generated from Excel test case TC_AI_030."""
    controller = RefrigerationController()
    registers = controller.modbus_registers()
    assert registers[30003] == 'discharge temperature'

def test_generated_tc_ai_031():
    """Generated from Excel test case TC_AI_031."""
    controller = RefrigerationController()
    controller.compressor_on = True
    registers = controller.modbus_registers()
    assert registers[30004] == 1

def test_generated_tc_ai_032():
    """Generated from Excel test case TC_AI_032."""
    controller = RefrigerationController()
    registers = controller.modbus_registers()
    assert registers[30004] == 0

def test_generated_tc_ai_033():
    """Generated from Excel test case TC_AI_033."""
    controller = RefrigerationController()
    controller.compressor_on = True
    registers = controller.modbus_registers()
    assert registers[30004] == 1

def test_generated_tc_ai_034():
    """Generated from Excel test case TC_AI_034."""
    controller = RefrigerationController()
    controller.activate_alarm_mode()
    registers = controller.modbus_registers()
    assert registers[30006] == 1

def test_generated_tc_ai_035():
    """Generated from Excel test case TC_AI_035."""
    controller = RefrigerationController()
    registers = controller.modbus_registers()
    assert registers[30006] == 0

def test_generated_tc_ai_036():
    """Generated from Excel test case TC_AI_036."""
    controller = RefrigerationController()
    controller.activate_alarm_mode()
    registers = controller.modbus_registers()
    assert registers[30006] == 1

def test_generated_tc_ai_037():
    """Generated from Excel test case TC_AI_037."""
    controller = RefrigerationController()
    controller.set_leak_condition()
    registers = controller.modbus_registers()
    assert registers[30007] == 1

def test_generated_tc_ai_038():
    """Generated from Excel test case TC_AI_038."""
    controller = RefrigerationController()
    registers = controller.modbus_registers()
    assert registers[30007] == 0

def test_generated_tc_ai_039():
    """Generated from Excel test case TC_AI_039."""
    controller = RefrigerationController()
    controller.set_leak_condition()
    registers = controller.modbus_registers()
    assert registers[30007] == 1

def test_generated_tc_ai_041():
    """Generated from Excel test case TC_AI_041."""
    controller = RefrigerationController()
    controller.set_high_discharge_temperature()
    assert controller.compressor_on is False

def test_generated_tc_ai_042():
    """Generated from Excel test case TC_AI_042."""
    controller = RefrigerationController()
    controller.set_low_suction_pressure()
    assert controller.compressor_on is False

def test_generated_tc_ai_044():
    """Generated from Excel test case TC_AI_044."""
    controller = RefrigerationController()
    controller.set_leak_condition()
    assert controller.evaporator_fan_on is True
