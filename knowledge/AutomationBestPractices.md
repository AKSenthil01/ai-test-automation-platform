# QA Automation Best Practices

This document defines the coding standards and best practices that must be followed while generating pytest automation scripts.

------------------------------------------------------------

# Test Design

- One test should verify one business scenario.
- Test names should clearly describe the expected behavior.
- Tests should be independent.
- Avoid dependencies between tests.
- Avoid shared mutable state.

------------------------------------------------------------

# Pytest

- Prefer pytest fixtures instead of setup code inside test methods.
- Keep test functions small.
- Avoid duplicate code.
- Use descriptive fixture names.
- Reuse fixtures whenever possible.

Example

@pytest.fixture
def controller():

    configure_controller()

    yield

    reset_controller()

------------------------------------------------------------

# Assertions

- Every test must contain meaningful assertions.
- Never use:

assert True

assert False

- Assertions should verify business behavior.

Good

assert get_compressor_status()=="RUNNING"

Good

assert verify_a2l_alarm()

Bad

assert True

------------------------------------------------------------

# Cleanup

Always restore the controller.

Typical cleanup

clear_alarm()

stop_compressor()

disconnect_modbus()

disconnect_bacnet()

reset_controller()

------------------------------------------------------------

# API Usage

Only use APIs defined in:

Controller_API.md

Never invent APIs.

Never create placeholder functions.

Bad

wait_for_alarm()

fake_function()

controller.configure()

Good

verify_a2l_alarm()

read_alarm()

start_compressor()

------------------------------------------------------------

# Fixtures

Use fixtures for:

- Controller setup
- Modbus connection
- BACnet connection
- Compressor lifecycle
- Sensor initialization

Avoid repeating setup inside every test.

------------------------------------------------------------

# Logging

Every important action should be logged.

Example

log_step("Starting compressor")

log_step("Reading alarm")

capture_logs()

------------------------------------------------------------

# Reports

Generate reports after execution.

Example

generate_report()

take_snapshot()

------------------------------------------------------------

# Naming Convention

Test function

test_verify_a2l_alarm()

Fixture

controller()

Helper

restart_controller()

------------------------------------------------------------

# Test Flow

Typical HVAC Test Flow

configure_controller()

↓

enable_a2l_detection()

↓

start_compressor()

↓

simulate_refrigerant_leak()

↓

verify_a2l_alarm()

↓

clear_alarm()

↓

stop_compressor()

↓

reset_controller()

------------------------------------------------------------

# Error Handling

Always validate:

- controller status
- alarm status
- communication status

Never ignore failures.

------------------------------------------------------------

# AI Rules

When generating pytest scripts

✔ Use only APIs from Controller_API.md

✔ Use reusable fixtures

✔ Add cleanup

✔ Add meaningful assertions

✔ Keep tests independent

✔ Keep tests executable

✔ Do not invent APIs

✔ Do not create wrapper classes

✔ Do not generate placeholder methods

✔ Return executable pytest code only