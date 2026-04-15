def test_no_critical_failures():

    with open("logs/system.log") as f:
        logs = f.read()

    assert "CRC error" not in logs
    assert "timeout" not in logs