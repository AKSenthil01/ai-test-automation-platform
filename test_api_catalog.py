from ai_engine.api_catalog import APICatalog

apis = APICatalog.load()

print(type(apis))
print(len(apis))
print(apis)