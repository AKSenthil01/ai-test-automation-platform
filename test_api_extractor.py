from ai_engine.api_extractor import APIExtractor

apis = APIExtractor.extract()

print()

for api in apis:
    print(api)