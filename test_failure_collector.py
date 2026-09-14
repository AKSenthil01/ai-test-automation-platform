from ai_engine.failure_collector import FailureCollector

collector = FailureCollector()

sample = """
FAILED test_alarm.py::test_alarm

AssertionError:
Expected alarm
"""

print(
    collector.collect(sample, "")
)