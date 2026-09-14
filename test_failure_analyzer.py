from ai_engine.failure_analyzer import FailureAnalyzer

log = """
Controller restarted.

BACnet communication timeout.

Temperature sensor disconnected.

Compressor stopped unexpectedly.
"""

analysis = FailureAnalyzer().analyze(log)

print("\nRESULT\n")

print(analysis)