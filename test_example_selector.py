from ai_engine.example_selector import ExampleSelector

examples = ExampleSelector().select(
    "Verify A2L leak alarm during compressor startup"
)

for e in examples:

    print("="*80)

    print(e)