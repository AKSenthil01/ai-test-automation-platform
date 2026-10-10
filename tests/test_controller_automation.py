import pytest

from simulators.controller_simulator import RefrigerationController


@pytest.fixture
def controller():
    return RefrigerationController()


def test_a2l_leak_shuts_down_compressor(controller):
    controller.compressor_on = True

    controller.set_leak_condition()

    assert controller.compressor_on is False
    assert controller.alarm_active is True


def test_a2l_leak_activates_ventilation_fan(controller):
    controller.set_leak_condition()

    assert controller.evaporator_fan_on is True


def test_a2l_leak_is_logged(controller):
    controller.set_leak_condition()

    assert "refrigerant leak detected" in controller.event_log


def test_manual_reset_clears_alarm_after_safe_condition(controller):
    controller.set_leak_condition()
    controller.clear_leak_condition()

    controller.manual_reset()

    assert controller.alarm_active is False


def test_high_discharge_temperature_shuts_down_compressor(controller):
    controller.compressor_on = True

    controller.set_high_discharge_temperature()

    assert controller.compressor_on is False


def test_low_suction_pressure_shuts_down_compressor(controller):
    controller.compressor_on = True

    controller.set_low_suction_pressure()

    assert controller.compressor_on is False


def test_invalid_sensor_input_enters_safe_mode(controller):
    controller.invalidate_sensor()

    assert controller.safe_mode is True


def test_alarm_mode_activates_alarm(controller):
    controller.activate_alarm_mode()

    assert controller.alarm_mode is True
    assert controller.alarm_active is True


@pytest.mark.parametrize(
    "register, expected",
    [
        (30004, 0),
        (30006, 0),
        (30007, 0),
        (30008, 0),
    ],
)
def test_modbus_status_registers(controller, register, expected):
    assert controller.modbus_registers()[register] == expected


def test_modbus_leak_status_register(controller):
    controller.set_leak_condition()

    assert controller.modbus_registers()[30007] == 1
