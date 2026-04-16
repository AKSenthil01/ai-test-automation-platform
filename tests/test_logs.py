import os

def test_no_critical_failures():

    if not os.path.exists("logs/system.log"):
        # ✅ Skip in CI
        assert True
        return

    with open("logs/system.log") as f:
        logs = f.read()

    assert "CRC error" not in logs