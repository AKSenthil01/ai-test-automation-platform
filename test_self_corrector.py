from ai_engine.self_corrector import SelfCorrector

requirement = "Verify A2L leak alarm during compressor startup."

code = """
def test_demo():

    configure_controller()

    fake_function()

    start_compressor()

    assert True
"""

corrected = SelfCorrector().improve(
    requirement,
    code
)

print(corrected)