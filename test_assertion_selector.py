from ai_engine.assertion_selector import AssertionSelector

for item in AssertionSelector().select(
    "Verify A2L leak alarm"
):
    print("=" * 80)
    print(item)