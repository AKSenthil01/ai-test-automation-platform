"""
AUTO-GENERATED FILE.

Generated from:
    generated_tests_interview_ready_50.xlsx

Do not manually edit this file.

The source of truth is the validated Excel workbook.
"""

from simulators.controller_simulator import (
    RefrigerationController,
)


def test_tc_ai_003_a2l_leak_shuts_down_compressor():
    controller = RefrigerationController(
        compressor_on=True
    )

    controller.set_leak_condition()

    assert controller.compressor_on is False


def test_tc_ai_004_a2l_leak_activates_ventilation_fan():
    controller = RefrigerationController()

    controller.set_leak_condition()

    assert controller.evaporator_fan_on is True


def test_tc_ai_006_a2l_leak_is_logged():
    controller = RefrigerationController()

    controller.set_leak_condition()

    assert "refrigerant leak detected" in controller.event_log


def test_tc_ai_008_manual_reset_clears_alarm_after_safe_condition():
    controller = RefrigerationController()

    controller.set_leak_condition()

    assert controller.alarm_active is True

    controller.clear_leak_condition()
    controller.manual_reset()

    assert controller.alarm_active is False


def test_tc_ai_017_alarm_mode_activates_alarm():
    controller = RefrigerationController()

    controller.activate_alarm_mode()

    assert controller.alarm_mode is True
    assert controller.alarm_active is True


def test_tc_ai_018_low_suction_pressure_shuts_down_compressor():
    controller = RefrigerationController(
        compressor_on=True
    )

    controller.set_low_suction_pressure()

    assert controller.suction_pressure == "low"
    assert controller.compressor_on is False


def test_tc_ai_020_invalid_sensor_input_enters_safe_mode():
    controller = RefrigerationController()

    controller.invalidate_sensor()

    assert controller.sensor_input_valid is False
    assert controller.safe_mode is True


def test_tc_ai_027_high_discharge_temperature_shuts_down_compressor():
    controller = RefrigerationController(
        compressor_on=True
    )

    controller.set_high_discharge_temperature()

    assert controller.discharge_temperature == "above limit"
    assert controller.compressor_on is False


def test_tc_ai_032_modbus_register_30004():
    controller = RefrigerationController()

    registers = controller.modbus_registers()

    assert registers[30004] == 0


def test_tc_ai_035_modbus_register_30006():
    controller = RefrigerationController()

    registers = controller.modbus_registers()

    assert registers[30006] == 0


def test_tc_ai_038_modbus_register_30007():
    controller = RefrigerationController()

    registers = controller.modbus_registers()

    assert registers[30007] == 0


def test_tc_ai_039_modbus_leak_status_register():
    controller = RefrigerationController()

    controller.set_leak_condition()

    registers = controller.modbus_registers()

    assert registers[30007] == 1
