from core.failure_demo import create_simulated_failure


def test_simulated_failure_is_deterministic():
    log_text = create_simulated_failure()

    assert "High discharge temperature protection" in log_text
    assert "Expected:" in log_text
    assert "Compressor remains ON" in log_text
    assert "Actual:" in log_text
    assert "Compressor is OFF" in log_text
    assert "high discharge temperature protection" in log_text
