from pathlib import Path

from openpyxl import Workbook

from test_generation.generate_pytest_from_excel import (
    generate_controller_test,
    generate_modbus_leak_test,
    generate_modbus_test,
    is_automation_candidate,
    read_test_cases,
    safe_test_name,
)


def test_safe_test_name():
    result = safe_test_name(
        "TC_AI_001",
        "A2L Leak Detection - Compressor Shutdown",
    )

    assert result.startswith("test_")
    assert "tc_ai_001" in result
    assert "compressor_shutdown" in result


def test_is_automation_candidate_yes():
    row = {
        "Automation Candidate": "YES"
    }

    assert is_automation_candidate(row) is True


def test_is_automation_candidate_no():
    row = {
        "Automation Candidate": "NO"
    }

    assert is_automation_candidate(row) is False


def test_read_test_cases(tmp_path):
    workbook_path = (
        tmp_path / "test_cases.xlsx"
    )

    workbook = Workbook()

    sheet = workbook.active
    sheet.title = "Test Cases"

    sheet.append(
        [
            "Test Case ID",
            "Requirement",
            "Feature",
            "Scenario",
            "Steps",
            "Expected Results",
            "Test Data",
            "Automation Candidate",
            "Tool",
        ]
    )

    sheet.append(
        [
            "TC_TEST_001",
            "Verify compressor shutdown",
            "Compressor",
            "Compressor shuts down",
            "Trigger condition",
            "Compressor OFF",
            "",
            "YES",
            "Pytest",
        ]
    )

    workbook.save(
        workbook_path
    )

    rows = read_test_cases(
        workbook_path
    )

    assert len(rows) == 1

    assert rows[0]["Test Case ID"] == (
        "TC_TEST_001"
    )

    assert rows[0]["Automation Candidate"] == (
        "YES"
    )


def test_generate_a2l_compressor_shutdown():
    code = generate_controller_test(
        "TC_AI_003",
        "A2L leak shuts down compressor",
    )

    assert (
        "RefrigerationController" in code
    )

    assert (
        "set_leak_condition()" in code
    )

    assert (
        "compressor_on is False" in code
    )


def test_generate_a2l_ventilation():
    code = generate_controller_test(
        "TC_AI_004",
        "A2L leak activates ventilation fan",
    )

    assert (
        "set_leak_condition()" in code
    )

    assert (
        "evaporator_fan_on is True" in code
    )


def test_generate_a2l_logging():
    code = generate_controller_test(
        "TC_AI_006",
        "A2L leak is logged",
    )

    assert (
        "set_leak_condition()" in code
    )

    assert (
        "refrigerant leak detected" in code
    )


def test_generate_manual_reset():
    code = generate_controller_test(
        "TC_AI_008",
        "Manual reset clears alarm",
    )

    assert (
        "clear_leak_condition()" in code
    )

    assert (
        "manual_reset()" in code
    )

    assert (
        "alarm_active is False" in code
    )


def test_generate_alarm_mode():
    code = generate_controller_test(
        "TC_AI_017",
        "Alarm mode activates alarm",
    )

    assert (
        "activate_alarm_mode()" in code
    )

    assert (
        "alarm_mode is True" in code
    )

    assert (
        "alarm_active is True" in code
    )


def test_generate_low_suction_pressure():
    code = generate_controller_test(
        "TC_AI_018",
        "Low suction pressure protection",
    )

    assert (
        "set_low_suction_pressure()" in code
    )

    assert (
        "compressor_on is False" in code
    )


def test_generate_invalid_sensor():
    code = generate_controller_test(
        "TC_AI_020",
        "Invalid sensor input",
    )

    assert (
        "invalidate_sensor()" in code
    )

    assert (
        "sensor_input_valid is False" in code
    )

    assert (
        "safe_mode is True" in code
    )


def test_generate_high_discharge_temperature():
    code = generate_controller_test(
        "TC_AI_027",
        "High discharge temperature protection",
    )

    assert (
        "set_high_discharge_temperature()" in code
    )

    assert (
        "compressor_on is False" in code
    )


def test_generate_modbus_register():
    code = generate_modbus_test(
        "TC_AI_032",
        30004,
        0,
    )

    assert (
        "modbus_registers()" in code
    )

    assert (
        "registers[30004]" in code
    )

    assert (
        "== 0" in code
    )


def test_generate_modbus_leak_status():
    code = generate_modbus_leak_test(
        "TC_AI_039"
    )

    assert (
        "set_leak_condition()" in code
    )

    assert (
        "registers[30007]" in code
    )

    assert (
        "== 1" in code
    )


def test_generated_code_does_not_import_reference_tests():
    code_blocks = [
        generate_controller_test(
            "TC_AI_003",
            "A2L leak",
        ),
        generate_modbus_test(
            "TC_AI_032",
            30004,
            0,
        ),
        generate_modbus_leak_test(
            "TC_AI_039",
        ),
    ]

    combined = "\n".join(
        code_blocks
    )

    assert (
        "tests.test_controller_automation"
        not in combined
    )

    assert (
        "test_controller_automation"
        not in combined
    )