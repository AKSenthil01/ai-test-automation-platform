from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from test_generation.generate_tests_from_docs import generate


BASE_DIR = Path(__file__).resolve().parent.parent

WORKBOOK = BASE_DIR / "generated_tests_interview_ready_50.xlsx"

GENERATED_TEST = (
    BASE_DIR
    / "tests"
    / "generated"
    / "test_generated_from_excel.py"
)

REPORT_DIR = BASE_DIR / "reports"

EXECUTION_LOG = (
    REPORT_DIR
    / "excel_pytest_execution.log"
)


def generate_tests_from_excel() -> dict:
    """
    Generate pytest tests from the validated Excel workbook.

    Uses the current capability-based Excel -> pytest generator.
    """

    try:
        if not WORKBOOK.exists():
            return {
                "return_code": 1,
                "stdout": "",
                "stderr": (
                    f"Workbook not found: {WORKBOOK}"
                ),
                "success": False,
                "generated_test": False,
            }

        generated_tests, skipped_tests = generate(
            WORKBOOK
        )

        generated_exists = GENERATED_TEST.exists()

        return {
            "return_code": 0 if generated_exists else 1,
            "stdout": (
                "Excel -> pytest generation completed successfully."
            ),
            "stderr": "",
            "success": generated_exists,
            "generated_test": generated_exists,
            "generated_count": len(generated_tests),
            "skipped_count": len(skipped_tests),
        }

    except Exception as exc:
        return {
            "return_code": 1,
            "stdout": "",
            "stderr": str(exc),
            "success": False,
            "generated_test": GENERATED_TEST.exists(),
            "generated_count": 0,
            "skipped_count": 0,
        }


def execute_generated_tests() -> dict:
    """
    Execute the pytest suite generated from Excel.
    """

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    command = [
        sys.executable,
        "-m",
        "pytest",
        str(GENERATED_TEST),
        "-v",
    ]

    result = subprocess.run(
        command,
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
    )

    output = (
        result.stdout
        + "\n"
        + result.stderr
    )

    EXECUTION_LOG.write_text(
        output,
        encoding="utf-8",
    )

    return {
        "return_code": result.returncode,
        "output": output,
        "success": result.returncode == 0,
        "log_file": EXECUTION_LOG,
    }


def run_excel_to_pytest_pipeline() -> dict:
    """
    Execute:

        Excel
          ↓
        Current capability-based pytest generator
          ↓
        Generated pytest tests
          ↓
        pytest execution

    This pipeline intentionally does not invoke the AI failure analyzer.
    """

    generation = generate_tests_from_excel()

    if not generation["success"]:
        return {
            "success": False,
            "stage": "generation",
            "generation": generation,
            "execution": None,
        }

    execution = execute_generated_tests()

    return {
        "success": execution["success"],
        "stage": "execution",
        "generation": generation,
        "execution": execution,
    }


if __name__ == "__main__":
    result = run_excel_to_pytest_pipeline()

    print("=" * 70)
    print("EXCEL → PYTEST PIPELINE")
    print("=" * 70)

    print(
        f"Generation : "
        f"{'PASSED' if result['generation']['success'] else 'FAILED'}"
    )

    if result["execution"]:
        print(
            f"Execution  : "
            f"{'PASSED' if result['execution']['success'] else 'FAILED'}"
        )

        print(
            f"Log        : "
            f"{result['execution']['log_file']}"
        )

    raise SystemExit(
        0 if result["success"] else 1
    )