from ai_engine.failure_analyzer import FailureAnalyzer

log = """
BACnet communication timeout.

Temperature sensor failed.

Compressor restarted unexpectedly.

Controller generated alarm.

"""

analyzer = FailureAnalyzer()

result = analyzer.analyze(log)

print("\n")

print("=" * 80)

print(result)

print("=" * 80)