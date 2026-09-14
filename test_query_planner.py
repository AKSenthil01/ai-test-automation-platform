from ai_engine.query_planner import QueryPlanner

log = """
BACnet communication timeout.
Controller restarted.
Temperature sensor disconnected.
Compressor stopped.
Alarm generated.
"""

print("Modules:")
print(QueryPlanner.extract_modules(log))

print("\nSearch Query:")
print(QueryPlanner.build_search_query(log))