from ai_engine.api_validator import APIValidator

code = """
configure_controller()

enable_a2l_detection()

simulate_refrigerant_leak()

verify_a2l_alarm()

clear_alarm()

capture_logs()

fake_function()
"""

invalid = APIValidator.validate(code)

print("Invalid APIs")
print("=" * 40)
print(invalid)