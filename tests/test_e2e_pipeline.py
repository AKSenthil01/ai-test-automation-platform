from pathlib import Path

from core.e2e_runner import (
    EXECUTION_LOG,
    GENERATED_TEST,
    run_excel_to_pytest_pipeline,
)


def test_excel_to_pytest_end_to_end():
    result = run_excel_to_pytest_pipeline()

    assert result["generation"]["success"] is True
    assert result["generation"]["generated_test"] is True

    assert GENERATED_TEST.exists()

    assert result["execution"] is not None
    assert result["execution"]["success"] is True

    assert Path(EXECUTION_LOG).exists()

    log_text = EXECUTION_LOG.read_text(
        encoding="utf-8"
    )

    assert "passed" in log_text.lower()