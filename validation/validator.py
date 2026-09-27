import re
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CANONICAL_FEATURES = {
    "A2L Refrigerant Leak Detection",
    "Controller Operating Modes and Safety Protections",
    "Modbus RTU Monitoring and Controller Registers",
    "Compressor, Sensors, Fans and Alarm Handling",
    "BACnet MS/TP and Controller Communication",
}

ALLOWED_NUMBERS = {
    "0", "1", "2", "3", "4", "25",
    "30001", "30002", "30003", "30004",
    "30005", "30006", "30007", "30008",
}

FORBIDDEN_TERMS = {
    "defrost",
}

REQUIRED_COLUMNS = {
    "Test Case ID",
    "Requirement",
    "Feature",
    "Scenario",
    "Steps",
    "Expected Results",
    "Test Data",
    "Automation Candidate",
    "Tool",
}


def extract_numbers(value):
    return re.findall(r"(?<![A-Za-z])\d+(?:\.\d+)?", str(value))


def validate_numbers(row):
    # Test Case IDs (e.g. TC_AI_001) are generated identifiers, not source data.
    grounded_columns = [
        "Requirement", "Feature", "Scenario", "Steps",
        "Expected Results", "Test Data"
    ]
    text = " ".join(str(row.get(column, "")) for column in grounded_columns)
    return [
        number
        for number in extract_numbers(text)
        if number not in ALLOWED_NUMBERS
    ]


def validate_forbidden_terms(row):
    text = " ".join(
        str(row.get(column, ""))
        for column in ["Requirement", "Feature", "Scenario", "Steps",
                       "Expected Results", "Test Data"]
    ).lower()
    return [term for term in FORBIDDEN_TERMS if term in text]


def normalize(value):
    return re.sub(r"\s+", " ", str(value).strip().lower())


def validate_workbook(path):
    path = Path(path)
    df = pd.read_excel(path, sheet_name="Test Cases")

    issues = []

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        issues.append({
            "Test Case ID": "",
            "Severity": "ERROR",
            "Rule": "Required columns",
            "Details": f"Missing columns: {sorted(missing)}",
        })
        return issues

    for index, row in df.iterrows():
        tc_id = str(row["Test Case ID"]).strip()
        row_number = index + 2

        # Test Data is intentionally optional: the generation rules allow an empty
        # value when the source documentation provides no concrete input value.
        required_value_columns = REQUIRED_COLUMNS - {"Test Data"}
        for column in required_value_columns:
            if pd.isna(row[column]) or not str(row[column]).strip():
                issues.append({
                    "Test Case ID": tc_id,
                    "Severity": "ERROR",
                    "Rule": "Required field",
                    "Details": f"Row {row_number}: empty '{column}'",
                })

        feature = str(row["Feature"]).strip()
        if feature not in CANONICAL_FEATURES:
            issues.append({
                "Test Case ID": tc_id,
                "Severity": "ERROR",
                "Rule": "Canonical feature",
                "Details": f"Unsupported Feature: {feature}",
            })

        forbidden = validate_forbidden_terms(row)
        for term in forbidden:
            issues.append({
                "Test Case ID": tc_id,
                "Severity": "ERROR",
                "Rule": "Forbidden scope",
                "Details": f"Forbidden term detected: {term}",
            })

        unsupported = validate_numbers(row)
        if unsupported:
            issues.append({
                "Test Case ID": tc_id,
                "Severity": "ERROR",
                "Rule": "Numeric grounding",
                "Details": f"Unsupported numeric value(s): {sorted(set(unsupported))}",
            })

    duplicate_columns = ["Requirement", "Feature", "Scenario"]
    normalized_keys = df[duplicate_columns].fillna("").map(normalize).agg("|".join, axis=1)
    duplicate_mask = normalized_keys.duplicated(keep=False)

    for index in df.index[duplicate_mask]:
        issues.append({
            "Test Case ID": str(df.loc[index, "Test Case ID"]),
            "Severity": "WARNING",
            "Rule": "Duplicate behavior",
            "Details": "Requirement + Feature + Scenario matches another test case.",
        })

    return issues


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Deterministic validator for AI-generated HVAC test cases."
    )
    parser.add_argument("workbook", help="Path to generated Excel workbook.")
    args = parser.parse_args()

    issues = validate_workbook(args.workbook)

    if not issues:
        print("VALIDATION PASSED: no issues found.")
        return 0

    for issue in issues:
        print(
            f"[{issue['Severity']}] "
            f"{issue['Test Case ID']} | "
            f"{issue['Rule']} | "
            f"{issue['Details']}"
        )

    errors = sum(issue["Severity"] == "ERROR" for issue in issues)
    warnings = sum(issue["Severity"] == "WARNING" for issue in issues)

    print(f"\nValidation summary: {errors} error(s), {warnings} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
