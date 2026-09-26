Here is the executable pytest code for the given test cases:


import pytest
from hvac_controller import A2LLeakDetection, ModbusCommunication

@pytest.fixture
def controller():
    return A2LLeakDetection()

@pytest.mark.parametrize("test_case", [
    "TC_AI_039",
    "TC_AI_057",
    "TC_AI_033",
    "TC_AI_045",
    "TC_AI_068",
    "TC_AI_044",
    "TC_AI_129",
    "TC_AI_051"
])
def test_a2l_leak_detection(controller, test_case):
    # Configure controller
    controller.configure()

    # Trigger A2L leak detection
    if test_case in ["TC_AI_039", "TC_AI_057"]:
        controller.trigger_leak_detection()
    elif test_case == "TC_AI_033":
        controller.trigger_defrost_logic()
    elif test_case in ["TC_AI_045", "TC_AI_068", "TC_AI_044"]:
        controller.trigger_controller_operations()
    elif test_case == "TC_AI_129":
        controller.trigger_alarm_generation()
    elif test_case == "TC_AI_051":
        controller.trigger_modbus_communication()

    # Validate A2L leak detection
    if test_case in ["TC_AI_039", "TC_AI_057"]:
        assert controller.is_leak_detected()
    elif test_case == "TC_AI_033":
        assert controller.is_defrost_completed()
    elif test_case in ["TC_AI_045", "TC_AI_068", "TC_AI_044"]:
        assert controller.is_controller_operational()
    elif test_case == "TC_AI_129":
        assert controller.is_alarm_generated()
    elif test_case == "TC_AI_051":
        assert ModbusCommunication().is_communication_successful()

    # Apply compressor restart after defrost completion and cooling resumes properly
    if test_case in ["TC_AI_039", "TC_AI_057"]:
        controller.apply_compressor_restart()
    elif test_case == "TC_AI_033":
        controller.apply_defrost_completion()
    elif test_case in ["TC_AI_045", "TC_AI_068", "TC_AI_044"]:
        controller.apply_controller_operations()
    elif test_case == "TC_AI_129":
        controller.apply_alarm_generation()
    elif test_case == "TC_AI_051":
        ModbusCommunication().apply_modbus_communication()

@pytest.mark.parametrize("test_case", [
    "TC_AI_039",
    "TC_AI_057",
    "TC_AI_033",
    "TC_AI_045",
    "TC_AI_068",
    "TC_AI_044",
    "TC_AI_129",
    "TC_AI_051"
])
def test_modbus_communication(controller, test_case):
    # Configure controller
    controller.configure()

    # Trigger Modbus communication
    if test_case == "TC_AI_051":
        ModbusCommunication().trigger_modbus_communication()

    # Validate Modbus communication
    assert ModbusCommunication().is_communication_successful()


Note that this code assumes the existence of an `A2LLeakDetection` class and a `ModbusCommunication` class, which are not provided in the original knowledge. You will need to implement these classes based on the APIs present in the retrieved knowledge.