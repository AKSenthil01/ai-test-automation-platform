from pathlib import Path

import pandas as pd

from validation.validator import (
    CANONICAL_FEATURES,
    validate_workbook,
)


def make_workbook(tmp_path, rows):
    path = tmp_path / "tests.xlsx"
    df = pd.DataFrame(rows)
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Test Cases", index=False)
    return path


def base_case():
    return {
        "Test Case ID": "TC_AI_001",
        "Requirement": "Leak alarm triggers when concentration exceeds 25% of LFL.",
        "Feature": "A2L Refrigerant Leak Detection",
        "Scenario": "Leak alarm above documented threshold",
        "Steps": "1. Increase refrigerant concentration above 25% of LFL.",
        "Expected Results": "Leak alarm is activated.",
        "Test Data": "25% of LFL",
        "Automation Candidate": "YES",
        "Tool": "Pytest",
    }


def test_valid_case_passes(tmp_path):
    path = make_workbook(tmp_path, [base_case()])
    assert validate_workbook(path) == []


def test_defrost_case_is_rejected(tmp_path):
    case = base_case()
    case["Scenario"] = "Defrost operation"
    path = make_workbook(tmp_path, [case])

    issues = validate_workbook(path)

    assert any(issue["Rule"] == "Forbidden scope" for issue in issues)


def test_unsupported_number_is_rejected(tmp_path):
    case = base_case()
    case["Test Data"] = "10 bar"
    path = make_workbook(tmp_path, [case])

    issues = validate_workbook(path)

    assert any(issue["Rule"] == "Numeric grounding" for issue in issues)


def test_unknown_feature_is_rejected(tmp_path):
    case = base_case()
    case["Feature"] = "Unsupported Feature"
    path = make_workbook(tmp_path, [case])

    issues = validate_workbook(path)

    assert any(issue["Rule"] == "Canonical feature" for issue in issues)


def test_duplicate_behavior_is_warning(tmp_path):
    first = base_case()
    second = dict(first)
    second["Test Case ID"] = "TC_AI_002"

    path = make_workbook(tmp_path, [first, second])

    issues = validate_workbook(path)

    assert any(issue["Rule"] == "Duplicate behavior" for issue in issues)


def test_canonical_features_are_defined():
    assert len(CANONICAL_FEATURES) == 5
