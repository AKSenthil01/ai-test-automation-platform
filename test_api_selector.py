from ai_engine.api_selector import APISelector

selector = APISelector()

apis = selector.select(
    "Verify A2L leak alarm during compressor startup"
)

print()

for api in apis:
    print(api)