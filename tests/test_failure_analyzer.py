from ai_engine.failure_analyzer import FailureAnalyzer


def test_failure_analyzer():
    log = """
    BACnet communication timeout.

    Temperature sensor failed.

    Compressor restarted unexpectedly.

    Controller generated alarm.
    """

    analyzer = FailureAnalyzer()

    result = analyzer.analyze(log)

    assert result is not None
