import pandas as pd

from core.e2e_runner import run_excel_to_pytest_pipeline


def test_excel_to_pytest_end_to_end(tmp_path):
    workbook = tmp_path / "generated_tests.xlsx"
    generated_test = tmp_path / "test_generated_from_excel.py"
    report_file = tmp_path / "generation_report.txt"
    execution_log = tmp_path / "execution.log"

    rows = [
        {
            "Test Case ID": "TC_E2E_001",
            "Requirement": "High discharge temperature causes compressor shutdown.",
            "Feature": "Compressor, Sensors, Fans and Alarm Handling",
            "Scenario": "Compressor shuts down on high discharge temperature",
            "Steps": "Set high discharge temperature on the controller.",
            "Expected Results": "Compressor is turned off.",
            "Test Data": "High discharge temperature",
            "Automation Candidate": "YES",
            "Tool": "Pytest",
        }
    ]

    with pd.ExcelWriter(workbook, engine="openpyxl") as writer:
        pd.DataFrame(rows).to_excel(
            writer,
            sheet_name="Test Cases",
            index=False,
        )

    result = run_excel_to_pytest_pipeline(
        workbook=workbook,
        generated_test=generated_test,
        report_file=report_file,
        execution_log=execution_log,
    )

    assert result["generation"]["success"] is True, (
        result["generation"].get("stderr", "")
    )
    assert result["generation"]["generated_test"] is True
    assert generated_test.exists()
    assert report_file.exists()

    assert result["execution"] is not None
    assert result["execution"]["success"] is True, (
        result["execution"].get("output", "")
    )
    assert execution_log.exists()

    log_text = execution_log.read_text(encoding="utf-8")
    assert "passed" in log_text.lower()
