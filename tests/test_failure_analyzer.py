from unittest.mock import patch

from ai_engine.failure_analyzer import FailureAnalyzer


def test_failure_analyzer():
    log = """
    BACnet communication timeout.

    Temperature sensor failed.

    Compressor restarted unexpectedly.

    Controller generated alarm.
    """

    mock_response = """
    {
        "root_cause": "BACnet communication timeout caused the temperature sensor failure.",
        "component": "Temperature sensor / BACnet communication",
        "category": "Communication",
        "related_tests": [],
        "recommendation": "Check BACnet network connectivity and sensor communication.",
        "failure_type": "communication issue"
    }
    """

    with patch(
        "ai_engine.failure_analyzer.LLMClient.ask",
        return_value=mock_response
    ):
        analyzer = FailureAnalyzer()
        result = analyzer.analyze(log)

    assert result is not None
    assert isinstance(result, dict)
    assert "root_cause" in result
    assert "component" in result
    assert "category" in result
    assert "recommendation" in result
    assert "failure_type" in result
