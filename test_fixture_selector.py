from ai_engine.fixture_selector import FixtureSelector

fixtures = FixtureSelector().select(
    "Verify A2L leak alarm during compressor startup"
)

for fixture in fixtures:
    print("=" * 80)
    print(fixture)